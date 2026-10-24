"""Helpers for the ReportLab-built price sheets: list text lines with positions,
remove chosen lines from a page, and draw replacement text in the same style."""
import io, pathlib
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

H = 841.89
W = 595.28
FONT_DIR = pathlib.Path(__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("Carlito", str(FONT_DIR / "Carlito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-Regular", str(FONT_DIR / "Carlito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-Bold", str(FONT_DIR / "Carlito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-Italic", str(FONT_DIR / "Carlito-Italic.ttf")))

# palette sampled from the sheets
INK = (0.082353, 0.105882, 0.156863)      # dark header / table head
TEXT = (0.086275, 0.109804, 0.145098)
MUTED = (0.356863, 0.384314, 0.439216)
AMBER = (0.909804, 0.639216, 0.239216)
AMBER_TEXT = (0.721569, 0.47451, 0.101961)
CREAM = (0.964706, 0.945098, 0.905882)


def text_groups(page, reader):
    """Each ReportLab text line is `q cm(1 0 0 -1 x ytop) [rg] BT ... ET Q`.
    Returns dicts with op index range, x, ytop (from top), font size, colour and decoded text."""
    ops = ContentStream(page.get_contents(), reader).operations
    fonts = {k: v.get_object()["/BaseFont"].split("+")[-1] for k, v in page["/Resources"]["/Font"].items()}
    out, stack = [], []
    for i, (args, op) in enumerate(ops):
        if op == b"q":
            stack.append(i)
        elif op == b"Q" and stack:
            s = stack.pop()
            inner = ops[s + 1:i]
            names = [o for _, o in inner]
            if b"BT" in names and b"q" not in names and inner and inner[0][1] == b"cm":
                a = [float(v) for v in inner[0][0]]
                size = next((float(g[1]) for g, o in inner if o == b"Tf"), None)
                col = next((tuple(float(v) for v in g) for g, o in inner if o == b"rg"), None)
                font = next((fonts.get(g[0], str(g[0])) for g, o in inner if o == b"Tf"), None)
                out.append(dict(start=s, end=i, x=a[4], ytop=a[5], size=size, color=col, font=font, text=""))
    # decode text by position using pypdf's own decoder
    pos = []
    def visit(t, cm, tm, fd, fs):
        if t.strip():
            pos.append((cm[4], H - cm[5] if cm[3] < 0 else cm[5], t))
    page.extract_text(visitor_text=visit)
    for g in out:
        g["text"] = "".join(t for x, y, t in pos if abs(x - g["x"]) < 0.5 and abs(y - g["ytop"]) < 0.5 or (abs(x - g["x"]) < 0.5 and abs((H - y) - g["ytop"]) < 0.5)).strip()
    return ops, out


def strip_groups(page, reader, keep):
    """Remove text groups for which keep(group) is False."""
    ops, groups = text_groups(page, reader)
    drop = set()
    for g in groups:
        if not keep(g):
            drop.update(range(g["start"], g["end"] + 1))
    cs = ContentStream(None, reader)
    cs.operations = [o for i, o in enumerate(ops) if i not in drop]
    page[NameObject("/Contents")] = cs
    return [g for g in groups if not keep(g)]


def overlay(page, draw):
    """draw(c) paints on a ReportLab canvas in top-down coordinates; merged over the page."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(W, H))
    c.translate(0, H)
    c.scale(1, -1)
    draw(c)
    c.showPage()
    c.save()
    buf.seek(0)
    page.merge_page(PdfReader(buf).pages[0])


def text(c, x, ytop, s, font="Carlito", size=9, color=TEXT, align="left"):
    """Draw one line with its baseline at ytop (top-down), like the source sheets."""
    c.saveState()
    c.translate(x, ytop)
    c.scale(1, -1)
    c.setFillColorRGB(*color)
    c.setFont(font, size)
    if align == "right":
        c.drawRightString(0, 0, s)
    elif align == "center":
        c.drawCentredString(0, 0, s)
    else:
        c.drawString(0, 0, s)
    c.restoreState()


def wrap(s, font, size, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, x, ytop, s, width, font="Carlito", size=9, leading=None, color=TEXT):
    leading = leading or size * 1.3
    lines = wrap(s, font, size, width)
    for i, ln in enumerate(lines):
        text(c, x, ytop + i * leading, ln, font, size, color)
    return ytop + (len(lines) - 1) * leading


def flat_lines(page, reader):
    """For pages written as `rg BT Tm Tf TL Tj T* ET` (no q/cm per line)."""
    ops = ContentStream(page.get_contents(), reader).operations
    fonts = {k: v.get_object()["/BaseFont"].split("+")[-1] for k, v in page["/Resources"]["/Font"].items()}
    out, col, cur = [], None, None
    for i, (a, o) in enumerate(ops):
        if o == b"rg":
            col = tuple(float(v) for v in a)
        elif o == b"BT":
            cur = dict(start=i, color=col)
        elif o == b"Tm" and cur is not None:
            cur["x"], cur["ytop"] = float(a[4]), H - float(a[5])
        elif o == b"Tf" and cur is not None:
            cur["font"], cur["size"] = fonts.get(a[0], str(a[0])), float(a[1])
        elif o == b"ET" and cur is not None:
            cur["end"] = i
            if "x" in cur:
                out.append(cur)
            cur = None
    pos = []
    page.extract_text(visitor_text=lambda t, cm, tm, fd, fs: t.strip() and pos.append((tm[4], H - tm[5], t)))
    for g in out:
        g["text"] = "".join(t for x, y, t in pos if abs(x - g["x"]) < 0.5 and abs(y - g["ytop"]) < 0.5).strip()
    return ops, out


def strip_all_text(page, reader):
    ops = ContentStream(page.get_contents(), reader).operations
    keep, inside = [], False
    for a, o in ops:
        if o == b"BT":
            inside = True
        if not inside:
            keep.append((a, o))
        if o == b"ET":
            inside = False
    cs = ContentStream(None, reader)
    cs.operations = keep
    page[NameObject("/Contents")] = cs


def _mul(a, b):
    """3x3 affine product of PDF matrices [a b c d e f]: a then b."""
    return [a[0]*b[0] + a[1]*b[2], a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2], a[2]*b[1] + a[3]*b[3],
            a[4]*b[0] + a[5]*b[2] + b[4], a[4]*b[1] + a[5]*b[3] + b[5]]


def strip_regions(page, reader, rects):
    """Delete every text block (BT..ET) whose starting point lies inside one of the
    rects, given top-down as (x0, ytop0, x1, ytop1). Works whatever the page structure,
    by following the transformation matrices. Returns how many blocks were removed."""
    ops = ContentStream(page.get_contents(), reader).operations
    ctm, stack, keep, removed = [1, 0, 0, 1, 0, 0], [], [], 0
    block, tm, start = None, None, None
    def inside(x, y):
        yt = H - y
        return any(x0 - 0.5 <= x <= x1 + 0.5 and y0 - 0.5 <= yt <= y1 + 0.5 for x0, y0, x1, y1 in rects)
    for a, o in ops:
        if block is not None:
            block.append((a, o))
            if o in (b"Tm",):
                tm = [float(v) for v in a] if start is None else tm
                if start is None:
                    m = _mul(tm, ctm); start = (m[4], m[5])
            elif o in (b"Td", b"TD") and start is None:
                tm = _mul([1, 0, 0, 1, float(a[0]), float(a[1])], tm); m = _mul(tm, ctm); start = (m[4], m[5])
            elif o in (b"Tj", b"TJ", b"'", b'"') and start is None:
                m = _mul(tm, ctm); start = (m[4], m[5])
            if o == b"ET":
                if start is not None and inside(*start):
                    removed += 1
                else:
                    keep.extend(block)
                block = None
            continue
        if o == b"q":
            stack.append(ctm[:])
        elif o == b"Q":
            ctm = stack.pop() if stack else ctm
        elif o == b"cm":
            ctm = _mul([float(v) for v in a], ctm)
        elif o == b"BT":
            block, tm, start = [(a, o)], [1, 0, 0, 1, 0, 0], None
            continue
        keep.append((a, o))
    cs = ContentStream(None, reader)
    cs.operations = keep
    page[NameObject("/Contents")] = cs
    return removed
