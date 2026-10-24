"""Price sheet v3 (EN and VI): v2 plus a universities page after international schools.
Changed text is covered with the background colour and redrawn in Carlito; the new page
reuses the v2 international page's header and footer, with its body redrawn."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pdftext import *

repo, outdir = map(pathlib.Path, sys.argv[1:3])
TOTAL = 9
PAGE_BG = (0.9647, 0.9451, 0.9059)
ROW_ALT = (0.9255, 0.902, 0.8471)
RULE = (0.8667, 0.8353, 0.7608)
HEAD_GREY = (0.796078, 0.815686, 0.858824)

L = {
 "en": dict(
  src="TeachersDeck_Pricing_Sheet_EN_v2.pdf", out="TeachersDeck_Pricing_Sheet_EN_v3.pdf", title="TeachersDeck Pricing Sheet (v3)",
  page=lambda n: f"Page {n} of {TOTAL}",
  intro="Start free. Pay per teacher, per child, or one flat price per campus. International schools and universities add a small seat fee. Every price on this sheet is in VND and excludes VAT.",
  card3="One flat price per campus, not per teacher. Suite adds AdminDeck, StudentDeck and ParentDeck from 1,500,000 VND a month. International schools and universities add seat fees (pages 4 to 6).",
  card4="One contract, one invoice, a launch plan and priority support. Page 7. Support, maintenance and training fees are on page 8.",
  p4_support="Basic support on Zalo and email (page 8)",
  p4_note="International schools and universities also pay a seat fee per student and per parent on top of the campus plan. See pages 5 and 6.",
  kicker="PRICING · TEACHERSDECK", h="For universities", sub="A Suite plan for each faculty, plus a small seat fee for every student and linked parent.",
  t1="Seat fees, per year",
  seat_head=["Seat", "Price per year", "About in USD", "Notes"],
  seat_rows=[["Student", "100,000 VND", "about $4", "Each enrolled student"], ["Parent", "500,000 VND", "about $19", "Each parent linked with ParentDeck"]],
  seat_note="Seat fees are charged on top of the faculty plans. Parent seats count only the families who link with ParentDeck.",
  t2="Faculty plans and discounts across faculties",
  t2_sub="Each faculty or department takes its own Suite campus plan (page 4). Each faculty plan counts as one campus for the volume discounts, which apply to the plans, not the seat fees.",
  disc_head=["Faculty plans", "Discount on the plans", "Notes"],
  disc_rows=[["1 to 3", "List price", "Each faculty on its own plan"], ["4 to 9", "10% off", "One contract and one invoice"],
             ["10 to 24", "15% off", "Premium support included"], ["25 or more", "20% off or better", "Custom quote"],
             ["Two-year agreement", "Extra 5% off", "Added to any tier above"]],
  t3="Example: 4 faculties, 1,600 students, 400 parents",
  t3_sub="Four faculties each on Suite Standard, with 400 parents linked through ParentDeck.",
  ex_head=["Per year", "Calculation", "Price"],
  ex_rows=[["4 faculty plans", "4 × 30,000,000, minus 10%", "108,000,000 VND"], ["1,600 student seats", "1,600 × 100,000", "160,000,000 VND"],
           ["400 parent seats", "400 × 500,000", "200,000,000 VND"], ["!Total per year", "", "468,000,000 VND"]],
  ex_note="About $17,795 a year, or about 292,500 VND per student. A faculty larger than Suite Growth adds extra seats (page 4) or gets a custom quote.",
  box_h="Families far from campus",
  box_p="Students often live far from home. Parents who link with ParentDeck follow homework, attendance and lecturer notes in real time, read-only. Only linked parents count as parent seats.",
  faq=[("Who pays for student licences?", "Either the school, through a Suite campus plan, or the family, through ParentDeck Pro per child. Nobody pays twice for the same child."),
       ("What are seat fees?", "International schools and universities pay 100,000 VND per student and 500,000 VND per parent each year, on top of the campus plan (universities: only parents linked with ParentDeck). Private schools and language centers do not pay seat fees."),
       ("Can we try before we pay?", "Yes. The 30-day free pilot gives small schools and language centers up to 5 classrooms, free setup and no card needed."),
       ("What does the founding rate mean?", "Teachers: the first 100 keep their price for 12 months. Centers that join through the pilot get 30% off the campus plan for 12 months. Families: the first 200 children get 30% off their first year."),
       ("Can we change plans later?", "Yes. You can move up to a bigger plan at any time, and founding discounts carry over when a center upgrades to Suite."),
       ("Do prices include VAT?", "No. Prices exclude VAT, and VAT invoices are available. Prices in USD are approximate, using about 26,300 VND per USD."),
       ("Why pay 10 months for a year?", "Annual campus plans are priced at 10 months, so you get two months free compared with paying monthly.")],
  footer_text="TeachersDeck · Prices in VND, excluding VAT. VAT invoices available. USD about 26,300 VND per USD."),
 "vi": dict(
  src="TeachersDeck_Pricing_Sheet_VI_v2.pdf", out="TeachersDeck_Pricing_Sheet_VI_v3.pdf", title="Bảng giá TeachersDeck (v3)",
  page=lambda n: f"Trang {n} / {TOTAL}",
  intro="Bắt đầu miễn phí. Trả theo giáo viên, theo từng con, hoặc một mức giá cố định cho mỗi cơ sở. Trường quốc tế và trường đại học trả thêm một khoản phí nhỏ theo người dùng. Mọi mức giá trong bảng này tính bằng VND và chưa gồm VAT.",
  card3="Một mức giá cố định cho mỗi cơ sở, không tính theo giáo viên. Suite thêm AdminDeck, StudentDeck và ParentDeck từ 1.500.000 VND mỗi tháng. Trường quốc tế và trường đại học trả thêm phí theo người dùng (trang 4 đến 6).",
  card4="Một hợp đồng, một hóa đơn, kế hoạch triển khai và hỗ trợ ưu tiên. Trang 7. Phí hỗ trợ, bảo trì và đào tạo ở trang 8.",
  p4_support="Hỗ trợ cơ bản qua Zalo và email (trang 8)",
  p4_note="Trường quốc tế và trường đại học trả thêm phí theo người dùng cho mỗi học sinh, sinh viên và phụ huynh, cộng vào gói cơ sở. Xem trang 5 và 6.",
  kicker="BẢNG GIÁ · TEACHERSDECK", h="Dành cho trường đại học", sub="Một gói Suite cho mỗi khoa, cộng một khoản phí nhỏ cho mỗi sinh viên và phụ huynh có liên kết.",
  t1="Phí theo người dùng, mỗi năm",
  seat_head=["Đối tượng", "Giá mỗi năm", "Khoảng USD", "Ghi chú"],
  seat_rows=[["Sinh viên", "100.000 VND", "khoảng $4", "Mỗi sinh viên đang học"], ["Phụ huynh", "500.000 VND", "khoảng $19", "Mỗi phụ huynh liên kết với ParentDeck"]],
  seat_note="Phí theo người dùng được tính thêm vào các gói của khoa. Phí phụ huynh chỉ tính cho các gia đình liên kết với ParentDeck.",
  t2="Gói cho khoa và giảm giá khi có nhiều khoa",
  t2_sub="Mỗi khoa hoặc bộ môn dùng một gói cơ sở Suite riêng (trang 4). Mỗi gói khoa được tính là một cơ sở khi giảm giá theo số lượng; mức giảm áp dụng cho gói, không áp dụng cho phí theo người dùng.",
  disc_head=["Số gói khoa", "Mức giảm trên gói", "Ghi chú"],
  disc_rows=[["1 đến 3", "Giá niêm yết", "Mỗi khoa một gói riêng"], ["4 đến 9", "Giảm 10%", "Một hợp đồng và một hóa đơn"],
             ["10 đến 24", "Giảm 15%", "Đã gồm hỗ trợ cao cấp"], ["Từ 25", "Giảm từ 20% trở lên", "Báo giá riêng"],
             ["Hợp đồng hai năm", "Giảm thêm 5%", "Cộng thêm vào mọi mức ở trên"]],
  t3="Ví dụ: 4 khoa, 1.600 sinh viên, 400 phụ huynh",
  t3_sub="Bốn khoa đều dùng Suite Standard, với 400 phụ huynh liên kết qua ParentDeck.",
  ex_head=["Mỗi năm", "Cách tính", "Giá"],
  ex_rows=[["4 gói khoa", "4 × 30.000.000, trừ 10%", "108.000.000 VND"], ["1.600 sinh viên", "1.600 × 100.000", "160.000.000 VND"],
           ["400 phụ huynh", "400 × 500.000", "200.000.000 VND"], ["!Tổng mỗi năm", "", "468.000.000 VND"]],
  ex_note="Khoảng $17.795 mỗi năm, tức khoảng 292.500 VND cho mỗi sinh viên. Khoa lớn hơn gói Suite Growth thêm tài khoản (trang 4) hoặc được báo giá riêng.",
  box_h="Gia đình ở xa trường",
  box_p="Sinh viên thường sống xa nhà. Phụ huynh liên kết với ParentDeck theo dõi bài tập, điểm danh và ghi chú của giảng viên theo thời gian thực, chỉ để xem. Chỉ phụ huynh có liên kết mới được tính phí.",
  faq=[("Ai trả bản quyền cho học sinh?", "Hoặc nhà trường, qua gói cơ sở Suite, hoặc gia đình, qua ParentDeck Pro theo từng con. Không ai phải trả hai lần cho cùng một học sinh."),
       ("Phí theo người dùng là gì?", "Trường quốc tế và trường đại học trả 100.000 VND cho mỗi học sinh, sinh viên và 500.000 VND cho mỗi phụ huynh mỗi năm, cộng vào gói cơ sở (trường đại học: chỉ tính phụ huynh liên kết với ParentDeck). Trường tư thục và trung tâm ngoại ngữ không trả phí này."),
       ("Chúng tôi có thể dùng thử trước khi trả tiền không?", "Có. Chương trình dùng thử 30 ngày dành cho trường nhỏ và trung tâm ngoại ngữ gồm tối đa 5 lớp, miễn phí cài đặt và không cần thẻ."),
       ("Giá sáng lập nghĩa là gì?", "Giáo viên: 100 người đầu tiên giữ nguyên giá trong 12 tháng. Trung tâm tham gia qua chương trình dùng thử được giảm 30% gói cơ sở trong 12 tháng. Gia đình: 200 học sinh đầu tiên được giảm 30% năm đầu."),
       ("Chúng tôi có thể đổi gói sau này không?", "Có. Bạn có thể nâng lên gói lớn hơn bất cứ lúc nào, và ưu đãi sáng lập được giữ nguyên khi trung tâm nâng cấp lên Suite."),
       ("Giá đã gồm VAT chưa?", "Chưa. Giá chưa gồm VAT, và có xuất hóa đơn VAT. Giá USD chỉ mang tính tham khảo, quy đổi khoảng 26.300 VND/USD."),
       ("Vì sao trả 10 tháng cho cả năm?", "Gói cơ sở theo năm được tính 10 tháng, nên bạn được tặng hai tháng so với trả hằng tháng.")],
  footer_text="TeachersDeck · Giá tính bằng VND, chưa gồm VAT. Có xuất hóa đơn VAT. Quy đổi USD khoảng 26.300 VND/USD."),
}
problems = []
# Areas whose old words are removed from the PDF and redrawn (top-down x0, y0, x1, y1).
PAGE_NO, CARD3, CARD4 = (470, 808, 557, 822), (52, 668, 293, 732), (310, 668, 551, 732)
P4_SUPPORT, P4_NOTE, FAQ = (66, 683, 300, 697), (38, 762, 557, 788), (38, 134, 557, 482)
INTRO = (38, 370, 560, 430)


def cover(c, x0, y0, x1, y1, color=PAGE_BG):
    c.setFillColorRGB(*color); c.rect(x0, y0, x1 - x0, y1 - y0, stroke=0, fill=1)


def fit(c, x, y, s, width, font, size, leading, max_lines, color, label):
    sz, ld = size, leading
    while len(wrap(s, font, sz, width)) > max_lines and sz > 7.25:
        sz -= 0.25; ld = leading * sz / size
    if len(wrap(s, font, sz, width)) > max_lines:
        problems.append(label)
    if sz != size:
        print(f"  note: {label} at {sz}pt")
    return para(c, x, y, s, width, font, sz, ld, color)


def page_no(c, label):
    cover(c, 470, 808, 557, 822)
    text(c, 555.28, 817.89, label, "Carlito", 8, MUTED, align="right")


def table(c, top, head, rows, cols, widths):
    """Same look as the v2 tables: dark rounded header band, alternating rows, beige rules."""
    c.setFillColorRGB(*INK); c.roundRect(40, top, 515, 22, 6, stroke=0, fill=1)
    for x, h in zip(cols, head):
        text(c, x, top + 13.56, h, "Carlito-Bold", 8.5, AMBER)
    y = top + 21.5
    for i, row in enumerate(rows):
        bold = row[0].startswith("!")
        cells = [row[0].lstrip("!")] + row[1:]
        cover(c, 40, y, 555, y + 24, (1, 1, 1) if i % 2 == 0 else ROW_ALT)
        c.setStrokeColorRGB(*RULE); c.setLineWidth(0.6); c.line(40, y, 555, y); c.line(40, y + 24, 555, y + 24)
        for j, (x, w, s) in enumerate(zip(cols, widths, cells)):
            f = "Carlito-Bold" if (j == 0 or bold) else "Carlito"
            sz = 9
            while pdfmetrics.stringWidth(s, f, sz) > w and sz > 7.25: sz -= 0.25
            if pdfmetrics.stringWidth(s, f, sz) > w: problems.append(f"cell {s!r}")
            text(c, x, y + 13.54, s, f, sz, TEXT if (j == 0 or bold) else MUTED)
        y += 24
    return y


for lang, t in L.items():
    print("==", lang)
    rd = PdfReader(str(repo / t["src"]))
    w = PdfWriter()
    order = [0, 1, 2, 3, 4, "new", 5, 6, 7]
    for n, src in enumerate(order, 1):
        if src == "new":
            base = PdfReader(str(repo / t["src"]))
            p = base.pages[4]
            strip_all_text(p, base)   # keep the header band, logo and footer rule; drop every word
        else:
            p = rd.pages[src]
            rects = [PAGE_NO]
            if src == 0: rects = [CARD3, CARD4, INTRO]
            if src == 3: rects += [P4_SUPPORT, P4_NOTE]
            if src == 7: rects += [FAQ]
            gone = strip_regions(p, rd, rects)
            print(f"  p{n}: removed {gone} old text blocks")

        def draw(c, n=n, src=src):
            if src == 0:
                cover(c, 52, 668, 293, 732); cover(c, 310, 668, 551, 732); cover(c, *INTRO[:2], *INTRO[2:], INK)
                fit(c, 40, 385, t["intro"], 425, "Carlito", 13, 18, 3, HEAD_GREY, "cover intro")
                fit(c, 56, 678, t["card3"], 230, "Carlito", 9.5, 12.5, 4, MUTED, "cover card 3")
                fit(c, 314.3, 678, t["card4"], 230, "Carlito", 9.5, 12.5, 4, MUTED, "cover card 4")
                return
            page_no(c, t["page"](n))
            if src == 3:
                cover(c, 66, 683, 300, 697, (1, 1, 1))   # sits inside the white "Every campus plan includes" box
                text(c, 69, 692.5, t["p4_support"], "Carlito", 9.5, TEXT)
                cover(c, 38, 762, 557, 788)
                fit(c, 40, 771, t["p4_note"], 515, "Carlito-Italic", 9, 12, 2, MUTED, "p4 note")
            if src == 7:
                cover(c, 38, 134, 557, 482)
                y = 146.36
                for q, a in t["faq"]:
                    text(c, 40, y, q, "Carlito-Bold", 11, TEXT)
                    y = para(c, 40, y + 15.24, a, 515, "Carlito", 10, 13, MUTED) + 24
                end = y - 24
                print(f"  FAQ ends {end:.1f}pt (demo box starts ~486)")
                if end > 470: problems.append(f"FAQ too long ({end:.1f})")
            if src == "new":
                cover(c, 100, 30, 560, 110, INK)          # header text area
                cover(c, 0, 118, 595.28, 800)             # body; footer rule at 802 stays
                text(c, 108, 42.04, t["kicker"], "Carlito-Bold", 9, AMBER)
                text(c, 108, 74.2, t["h"], "Carlito-Bold", 25, (1, 1, 1))
                text(c, 108, 96.08, t["sub"], "Carlito", 10.5, HEAD_GREY)
                text(c, 40, 146.08, t["t1"], "Carlito-Bold", 13, TEXT)
                y = table(c, 160, t["seat_head"], t["seat_rows"], [47, 190, 330, 410], [138, 135, 75, 140])
                y = fit(c, 40, y + 15.8, t["seat_note"], 515, "Carlito-Italic", 9, 12, 2, MUTED, "seat note")
                text(c, 40, y + 32, t["t2"], "Carlito-Bold", 13, TEXT)
                y = fit(c, 40, y + 47.3, t["t2_sub"], 515, "Carlito", 9.5, 12.5, 2, MUTED, "t2 sub")
                y = table(c, y + 12, t["disc_head"], t["disc_rows"], [47, 217, 387], [165, 165, 165])
                text(c, 40, y + 30, t["t3"], "Carlito-Bold", 13, TEXT)
                y = fit(c, 40, y + 45.3, t["t3_sub"], 515, "Carlito", 9.5, 12.5, 1, MUTED, "t3 sub")
                y = table(c, y + 12, t["ex_head"], t["ex_rows"], [47, 217, 420], [165, 195, 130])
                y = fit(c, 40, y + 15.8, t["ex_note"], 515, "Carlito-Italic", 9, 12, 2, MUTED, "ex note")
                bt = y + 18
                c.setFillColorRGB(1, 1, 1); c.setStrokeColorRGB(*RULE); c.setLineWidth(0.7)
                c.roundRect(40, bt, 515, 74, 14, stroke=1, fill=1)
                text(c, 56, bt + 22.4, t["box_h"], "Carlito-Bold", 11, TEXT)
                last = fit(c, 56, bt + 40.2, t["box_p"], 483, "Carlito", 9.5, 12.5, 2, MUTED, "box")
                print(f"  universities page: box {bt:.1f}-{bt + 74:.1f}, footer rule at 802")
                if bt + 74 > 795: problems.append(f"universities page overflows ({bt + 74:.1f})")
                text(c, 40, 817.89, t["footer_text"], "Carlito", 8, MUTED)
        overlay(p, draw)
        w.add_page(p)
    if problems:
        sys.exit("FIT PROBLEMS: " + "; ".join(problems))
    w.add_metadata({"/Title": t["title"], "/Author": "TeachersDeck"})
    for pg in w.pages:
        pg.compress_content_streams(level=9)
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    with open(outdir / t["out"], "wb") as f:
        w.write(f)
    print("  wrote", t["out"], len(w.pages), "pages")
