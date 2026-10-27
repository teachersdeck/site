"""StudentDeck Child Privacy & Policies: one source for the web page (/student-privacy/) and the PDF.

    python3 _build/privacy.py            # writes student-privacy/index.html and the PDF

Copy cleaned from the owner's v1.1 PDF (26 Oct 2026). The bracketed retention periods are confirmed
as written (owner, 27 Oct 2026). Change the policy here, bump VERSION/UPDATED, and rebuild both.
"""
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import ROOT, SITE, shell, fix_header  # noqa: E402

VERSION = "1.1"
EFFECTIVE = "26 October 2026"
UPDATED = "27 October 2026"
SLUG = "student-privacy"
PDF = f"StudentDeck_Child_Privacy_and_Policies_v{VERSION}.pdf"

SUMMARY = ("StudentDeck collects only what it needs to run a learning experience. We never sell student data and never "
           "show targeted ads to children. Parents and schools stay in control of a child's information, including the "
           "right to see it, correct it and have it deleted.")

# Blocks: ("p", text) · ("lead", bold lead, text) · ("ul", [items]) · ("dl", [(term, text)]) · ("table", head, rows) · ("h3", text)
SECTIONS = [
    ("Our commitment to children", [
        ("p", "StudentDeck (\"StudentDeck\", \"we\", \"us\" or \"our\") provides digital tools that help students organise "
              "their learning, study materials and schoolwork. Because many of our users are children, we hold ourselves to "
              "a higher standard of care than we would for adults. This policy explains how we collect, use, protect and "
              "delete children's personal information, and the rules that keep StudentDeck a safe place to learn."),
        ("p", "Our guiding principles:"),
        ("dl", [("Data minimisation", "we collect only what is needed to deliver the service."),
                ("Purpose limitation", "children's data is used only for education and to run the service."),
                ("Parental and school control", "the adults responsible for a child can review, correct and delete their data."),
                ("No commercial exploitation", "we do not sell children's data or advertise to them."),
                ("Safety by design", "privacy-protective defaults and age-appropriate features.")]),
    ]),
    ("Scope and who this applies to", [
        ("p", "This policy applies to all StudentDeck websites, apps and related services used by or on behalf of children. "
              "A child means anyone under 13, or under the age of digital consent in their country where that is higher "
              "(for example, 16 in some countries). We also give these protections to all students under 18."),
        ("table", ["Term", "Meaning"], [
            ["Child", "A user under 13, or under the local age of digital consent"],
            ["Minor student", "A user under 18"],
            ["Parent or guardian", "A child's parent or legal guardian"],
            ["School", "A school, district or educational organisation that provides StudentDeck to its students"],
            ["Personal information", "Any information that identifies, relates to, or could reasonably be linked to a specific person"]]),
    ]),
    ("Information we collect", [
        ("p", "We collect only what a student reasonably needs to use StudentDeck."),
        ("table", ["Category", "Examples", "Why we collect it"], [
            ["Account information", "First name or username, grade level, school or class code, parent or guardian email (for children)", "To create and manage the account and to obtain consent"],
            ["Learning content", "Notes, flashcards, decks, assignments and study schedules the student creates", "To provide the core features"],
            ["Usage information", "Features used, session length, progress, error logs", "To run, improve and secure the service"],
            ["Device information", "Device type, operating system, app version, IP address (for security)", "Compatibility, and preventing fraud and abuse"],
            ["Communications", "Support requests, messages from parents or teachers", "To answer questions"]]),
        ("p", "A child never has to give their full legal name, home address, phone number, government ID, precise location, "
              "photos or biometric data to use StudentDeck. If an optional feature ever needs this kind of information, we will "
              "explain why and get verifiable consent from a parent or the school first."),
        ("p", "We collect information about a child from the child, from a parent or guardian, or from a school acting for "
              "the parent. We use cookies and similar technologies only for essential functions, such as keeping a student "
              "signed in, and never for behavioural advertising."),
    ]),
    ("How we use children's information", [
        ("p", "We use children's personal information only to:"),
        ("ul", ["Provide, maintain and personalise StudentDeck's educational features.",
                "Save and sync a student's learning content and progress.",
                "Share progress reports with parents, guardians and teachers where permitted.",
                "Keep the service safe, detect abuse and prevent security incidents.",
                "Provide support and send essential service notices.",
                "Improve the service using de-identified or aggregated data that cannot reasonably identify a child.",
                "Meet our legal obligations."]),
    ]),
    ("What we never do", [
        ("p", "StudentDeck will never:"),
        ("ul", ["Sell or rent children's personal information.",
                "Show targeted or behavioural advertising to children.",
                "Build advertising or marketing profiles of children.",
                "Use children's content or data to train third-party AI models.",
                "Make a child's participation depend on sharing more data than necessary.",
                "Let strangers contact children through StudentDeck, or publicly display a child's personal information.",
                "Use children's data for a materially different purpose from those described here without new consent."]),
    ]),
    ("Parental and school consent", [
        ("lead", "Accounts children create directly.", "Before we collect personal information from a child under 13, we get "
                 "verifiable parental consent. We email the parent or guardian, explain what we collect and why, and ask them "
                 "to confirm in a reasonable way, such as a signed consent form, a confirmation link with a second verification "
                 "step, or another method the law allows. Until consent is given, the account stays inactive and we keep only "
                 "what we need to ask for consent."),
        ("lead", "Accounts provided by a school.", "When a school provides StudentDeck to its students, the school may consent "
                 "on parents' behalf for educational use only. The school is then responsible for telling parents and for "
                 "making sure it has the authority to consent. We follow the school's documented instructions and use student "
                 "data only for the school's educational purposes."),
        ("lead", "Withdrawing consent.", "A parent or guardian can withdraw consent at any time by contacting us. This may "
                 "limit or end the child's use of StudentDeck, and we will delete the child's data as described under "
                 "Data retention and deletion."),
    ]),
    ("Sharing and disclosure", [
        ("p", "We share children's personal information only in these limited cases."),
        ("table", ["Shared with", "Purpose", "Safeguards"], [
            ["Parents and guardians", "To see their child's data and progress", "Identity verification"],
            ["Schools and teachers", "Educational use under the school's agreement", "Data processing terms and role-based access"],
            ["Service providers (hosting, support, security)", "To run StudentDeck for us", "Written contracts, no use for their own purposes, confidentiality and security duties"],
            ["Legal and safety", "To respond to valid legal process or protect a child's safety", "Only what is required"],
            ["Business transfers", "A merger or acquisition", "The new owner must keep this policy; parents are told of material changes"]]),
        ("p", "We may share aggregated or de-identified data that cannot reasonably identify a child, for example for research "
              "on learning outcomes. We do not try to re-identify this data, and anyone who receives it must agree not to either."),
    ]),
    ("Data retention and deletion", [
        ("p", "We keep children's personal information only as long as we need it for the purposes in this policy."),
        ("table", ["Data", "How long we keep it"], [
            ["Active account and learning content", "While the account is active"],
            ["Account without parental consent", "Deleted within 7 days"],
            ["Inactive account", "Deleted after 12 months without use, after we give notice"],
            ["Closed account", "Deleted within 30 days of the request, unless the law requires us to keep it"],
            ["Backups", "Overwritten within 90 days"],
            ["Security and audit logs", "Up to 12 months"]]),
        ("p", "When a school ends its agreement with us, we delete or return its student data within 60 days, unless the "
              "school tells us otherwise or the law requires us to keep it."),
    ]),
    ("Parent and student rights", [
        ("p", "Parents, guardians and, where applicable, students have the right to:"),
        ("dl", [("Access", "see the personal information we hold about the child."),
                ("Correct", "ask us to fix information that is wrong."),
                ("Delete", "ask us to delete the child's information and account."),
                ("Restrict or object", "limit certain uses of the child's data."),
                ("Refuse further collection", "stop us collecting or using more."),
                ("Portability", "get a copy of the child's content in a common format."),
                ("Complain", "contact us or the relevant data protection authority.")]),
        ("p", "To use these rights, contact us (see Contact us below). We may need to confirm your identity and your "
              "relationship to the child first. We aim to reply within 30 days. For accounts provided by a school, we may "
              "pass your request to the school, which controls the student's records."),
    ]),
    ("Data security", [
        ("p", "We protect children's data with administrative, technical and physical safeguards suited to how sensitive it is:"),
        ("ul", ["Encryption in transit (TLS) and at rest.",
                "Role-based, least-privilege access for staff.",
                "Multi-factor authentication for administrative systems.",
                "Background checks and yearly privacy and security training for anyone with access to student data.",
                "Regular vulnerability testing, monitoring and security reviews.",
                "Checks on service providers, with security requirements in their contracts.",
                "Secure development, with a privacy review before we launch any feature children use."]),
        ("p", "No system is perfectly secure. We encourage families to use strong, unique passwords and keep login details private."),
    ]),
    ("Safe and respectful use", [
        ("p", "Everyone who uses StudentDeck must follow these rules to keep it safe for learners."),
        ("h3", "Students are expected to"),
        ("ul", ["Be kind and respectful: no bullying, harassment or hate speech.",
                "Never share passwords, a home address, a phone number or other private details.",
                "Only upload content they have the right to use and that is suitable for school.",
                "Tell a parent, a teacher or StudentDeck about anything that makes them uncomfortable."]),
        ("h3", "Not allowed"),
        ("ul", ["Sexual, violent or otherwise age-inappropriate material.",
                "Content that promotes self-harm, drugs, weapons or illegal activity.",
                "Trying to contact, groom or exploit children, or to get their personal information.",
                "Impersonation, cheating tools that break a school's academic integrity rules, or trying to hack or disrupt the service."]),
        ("h3", "Teachers and school staff"),
        ("p", "Teachers and school administrators may access student information only for legitimate educational purposes, "
              "and must follow their school's policies and the law."),
    ]),
    ("Content moderation and reporting", [
        ("p", "StudentDeck uses automated tools and human review to find content that breaks this policy. Sharing and "
              "collaboration features are off by default for children and, when turned on, are limited to approved classmates "
              "or teachers in the same school or family group."),
        ("lead", "Reporting a concern.", "Anyone can report a safety or privacy concern with the in-app Report button or by "
                 "emailing teachersdeck@gmail.com. We review reports promptly and deal with urgent safety issues first."),
        ("lead", "What we do.", "Depending on how serious it is, we may remove content, warn or suspend accounts, tell parents "
                 "or the school and, where required or appropriate, report to the police or child protection authorities. "
                 "Material showing child sexual abuse or exploitation is removed immediately and reported to the authorities "
                 "as the law requires."),
    ]),
    ("Third-party services", [
        ("p", "StudentDeck may link to or work with other services, such as single sign-on or a school's learning management "
              "system. We check the privacy and security of any integration children use, and turn it on only when it is "
              "needed for education. Other services have their own privacy practices, which we encourage parents and schools "
              "to read. We do not allow third-party advertising trackers, or analytics that profile children, in StudentDeck."),
    ]),
    ("Legal compliance", [
        ("p", "We design our practices to meet the child and student privacy laws that apply to our users, which may include:"),
        ("table", ["Law or framework", "Where", "What it covers"], [
            ["COPPA (Children's Online Privacy Protection Act)", "United States", "Parental notice and consent for children under 13"],
            ["FERPA (Family Educational Rights and Privacy Act)", "United States", "Protection of student education records; the school official role"],
            ["State student privacy laws (such as SOPIPA and California AB 1584)", "United States", "Limits on using student data and on advertising"],
            ["GDPR, UK GDPR and the Age Appropriate Design Code", "EU and UK", "Lawful basis, the age of consent for children, and data subject rights"],
            ["PDPA, Decree 13/2023/ND-CP and the Law on Children", "Vietnam", "Consent and protection of children's personal data"],
            ["PIPEDA and provincial laws", "Canada", "Meaningful consent and safeguards"]]),
        ("p", "Where a local law gives children or parents stronger protection than this policy, we follow the stronger standard."),
    ]),
    ("Data breach response", [
        ("p", "If we find a breach affecting children's personal information, we will contain it promptly, investigate, and "
              "take steps to stop it happening again. We will tell affected parents, guardians and schools without undue "
              "delay, and regulators where the law requires (for example, within 72 hours under the GDPR), explaining what "
              "happened, what information was involved, and what they can do to protect themselves."),
    ]),
    ("Changes to this policy", [
        ("p", "We may update this policy when our practices or the law change, and will post the new version with a new "
              "\"Last updated\" date. For material changes to how we collect, use or share children's information, we will "
              "tell parents and schools directly (for example, by email) and, where required, get new consent before the "
              "changes apply to existing children's accounts."),
    ]),
    ("Contact us", [
        ("p", "Send questions, requests or concerns about children's privacy to:"),
        ("table", ["", ""], [
            ["Team", "StudentDeck Privacy & Child Safety"],
            ["Email", "teachersdeck@gmail.com"],
            ["Data Protection Officer", "Jerry Lai, jerry@myteachersdeck.com"],
            ["Address", "Saigon (Ho Chi Minh City), Vietnam"],
            ["Response time", "Within 30 days"]]),
    ]),
]

CONSENT = ("I am the parent or legal guardian of the child named below. I have read the StudentDeck Child Privacy & Policies "
           "and consent to the collection and use of my child's personal information as described.")
CONSENT_FIELDS = ["Child's first name or username", "Parent or guardian name", "Signature", "Date"]


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------- web page ----------
def esc(s):
    return html.escape(s, quote=True)


def link_emails(s):
    return re.sub(r"[\w.]+@[\w.]+\w", lambda m: f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>', s)


def block_html(b):
    k = b[0]
    if k == "p":
        return f"<p>{link_emails(esc(b[1]))}</p>"
    if k == "lead":
        return f"<p><strong>{esc(b[1])}</strong> {link_emails(esc(b[2]))}</p>"
    if k == "h3":
        return f"<h3>{esc(b[1])}</h3>"
    if k == "ul":
        return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in b[1]) + "</ul>"
    if k == "dl":
        return "<ul>" + "".join(f"<li><strong>{esc(t)}:</strong> {esc(d)}</li>" for t, d in b[1]) + "</ul>"
    if k == "table":
        head = "" if not any(b[1]) else "<thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in b[1]) + "</tr></thead>"
        rows = "".join("<tr>" + "".join(f"<td>{link_emails(esc(c))}</td>" for c in r) + "</tr>" for r in b[2])
        return f'<div class="table-wrap"><table class="ptable">{head}<tbody>{rows}</tbody></table></div>'
    raise ValueError(k)


def build_page():
    header, footer, theme_init, fonts, tail = shell("en")
    header = fix_header(header, "en", SLUG)
    here = f"{SITE}/{SLUG}/"
    title = "StudentDeck Child Privacy & Policies | TeachersDeck Suite"
    desc = ("How StudentDeck collects, uses, protects and deletes children's information: no selling data, no targeted ads, "
            "and parents and schools in control.")
    toc = "".join(f'<li><a href="#{slugify(t)}">{esc(t)}</a></li>' for t, _ in SECTIONS)
    body = "\n".join(
        f'<section class="pol-sec" id="{slugify(t)}"><h2><span>{i}.</span> {esc(t)}</h2>\n' + "\n".join(block_html(b) for b in blocks) + "</section>"
        for i, (t, blocks) in enumerate(SECTIONS, 1))
    consent = (f'<section class="pol-sec" id="consent-form"><h2>Parent or guardian consent form</h2><p>For accounts children create '
               f'directly, a parent or guardian can sign the consent form at the end of the <a href="/{PDF}" target="_blank" rel="noopener">PDF version</a>.</p></section>')
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#F3F5FC">
<link rel="canonical" href="{here}">
<link rel="icon" type="image/png" sizes="48x48" href="{SITE}/favicon-48.png">
<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">
<meta property="og:type" content="article"><meta property="og:site_name" content="TeachersDeck Suite">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{here}"><meta property="og:image" content="{SITE}/og.png">
{fonts}
{theme_init}
<link rel="stylesheet" href="/assets/site.css?v=uni1">
</head>
<body>
{header}
<main id="top">
<div class="wrap hero inner">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{SITE}/">Home</a> › <a href="{SITE}/#privacy">Built carefully, because students are children</a> › <span aria-current="page">Child privacy</span></nav>
<p class="kicker">StudentDeck</p>
<h1>Child Privacy &amp; Policies</h1>
<p class="lede">{esc(SUMMARY)}</p>
<p class="pol-meta">Version {VERSION} · Effective {EFFECTIVE} · Last updated {UPDATED}</p>
<div class="cta"><a class="btn primary" href="/{PDF}" target="_blank" rel="noopener">Download the PDF</a><a class="btn" href="mailto:teachersdeck@gmail.com">Ask a privacy question</a></div>
</div>
<section id="policy"><div class="wrap pol">
<nav class="pol-toc" aria-label="Contents"><h2>Contents</h2><ol>{toc}</ol></nav>
<div class="pol-body">
{body}
{consent}
<p class="pol-meta">Copyright © 2026 TeachersDeck™</p>
</div>
</div></section>
</main>
{footer}
{tail}
</html>
"""
    out = ROOT / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out


# ---------- PDF ----------
def build_pdf():
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate,
                                    Spacer, Table, TableStyle)

    pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("Sans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold")
    ink, muted, indigo, line, soft = (colors.HexColor(c) for c in ("#161C25", "#4D5565", "#4A55B8", "#D7DBE6", "#F3F5FC"))
    body = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=14, textColor=ink, spaceAfter=6)
    cell = ParagraphStyle("c", parent=body, fontSize=8.8, leading=12, spaceAfter=0)
    cellb = ParagraphStyle("cb", parent=cell, fontName="Sans-Bold")
    h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=13.5, leading=18, textColor=indigo, spaceBefore=12, spaceAfter=6)
    h3 = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.4, leading=14, textColor=ink, spaceBefore=6, spaceAfter=4)
    e = lambda s: html.escape(s, quote=False)  # noqa: E731

    def table(head, rows, widths):
        data = ([[Paragraph(e(h), cellb) for h in head]] if any(head) else []) + \
               [[Paragraph(e(c), cellb if (not any(head) and j == 0) else cell) for j, c in enumerate(r)] for r in rows]
        t = Table(data, colWidths=widths, repeatRows=1 if any(head) else 0)
        st = [("GRID", (0, 0), (-1, -1), 0.5, line), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
        if any(head):
            st.append(("BACKGROUND", (0, 0), (-1, 0), soft))
        t.setStyle(TableStyle(st))
        return t

    W = letter[0] - 2 * 0.9 * inch
    story = [Spacer(1, 2.2 * inch),
             Paragraph("StudentDeck", ParagraphStyle("t1", fontName="Sans-Bold", fontSize=30, leading=36, alignment=TA_CENTER, textColor=indigo)),
             Paragraph("Child Privacy &amp; Policies", ParagraphStyle("t2", fontName="Sans-Bold", fontSize=20, leading=28, alignment=TA_CENTER, textColor=ink)),
             Paragraph("Protecting students, respecting families", ParagraphStyle("t3", fontName="Sans", fontSize=12, leading=18, alignment=TA_CENTER, textColor=muted, spaceAfter=40)),
             Paragraph(f"Version {VERSION} · Effective {EFFECTIVE} · Last updated {UPDATED}", ParagraphStyle("t4", parent=body, alignment=TA_CENTER, textColor=muted)),
             Paragraph(f'<a href="{SITE}/{SLUG}/" color="#4A55B8">{SITE.replace("https://", "")}/{SLUG}/</a>', ParagraphStyle("t5", parent=body, alignment=TA_CENTER)),
             PageBreak(),
             Paragraph("Contents", h2)]
    story += [Paragraph(f"{i}. {e(t)}", ParagraphStyle("toc", parent=body, spaceAfter=2)) for i, (t, _) in enumerate(SECTIONS, 1)]
    box = Table([[Paragraph("<b>In plain language.</b> " + e(SUMMARY), body)]], colWidths=[W])
    box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), soft), ("BOX", (0, 0), (-1, -1), 0.6, indigo),
                             ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                             ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [Spacer(1, 14), box, PageBreak()]

    for i, (t, blocks) in enumerate(SECTIONS, 1):
        flow = [Paragraph(f"{i}. {e(t)}", h2)]
        for b in blocks:
            k = b[0]
            if k == "p":
                flow.append(Paragraph(e(b[1]), body))
            elif k == "lead":
                flow.append(Paragraph(f"<b>{e(b[1])}</b> {e(b[2])}", body))
            elif k == "h3":
                flow.append(Paragraph(e(b[1]), h3))
            elif k in ("ul", "dl"):
                items = b[1] if k == "ul" else [f"<b>{e(x)}:</b> {e(y)}" for x, y in b[1]]
                items = [e(x) for x in items] if k == "ul" else items
                flow.append(ListFlowable([ListItem(Paragraph(x, ParagraphStyle("li", parent=body, spaceAfter=2)), leftIndent=14) for x in items],
                                         bulletType="bullet", start="•", leftIndent=14, bulletFontName="Sans"))
                flow.append(Spacer(1, 4))
            elif k == "table":
                n = len(b[1])
                widths = {2: [W * .34, W * .66], 3: [W * .26, W * .42, W * .32]}[n]
                flow.append(table(b[1], b[2], widths))
                flow.append(Spacer(1, 8))
        story.append(KeepTogether(flow[:3]))
        story += flow[3:]

    story += [Spacer(1, 16), Paragraph("Parent or guardian consent (for accounts children create directly)", h2), Paragraph(e(CONSENT), body), Spacer(1, 8)]
    form = Table([[Paragraph(e(f), cell), ""] for f in CONSENT_FIELDS], colWidths=[W * .34, W * .66], rowHeights=[30] * len(CONSENT_FIELDS))
    form.setStyle(TableStyle([("LINEBELOW", (1, 0), (1, -1), 0.6, ink), ("VALIGN", (0, 0), (-1, -1), "BOTTOM")]))
    story.append(form)

    def deco(c, d):
        if d.page == 1:
            c.saveState(); c.setFont("Sans", 8.5); c.setFillColor(muted)
            c.drawCentredString(letter[0] / 2, 0.6 * inch, "Copyright © 2026 TeachersDeck™"); c.restoreState()
            return
        c.saveState(); c.setFont("Sans", 8); c.setFillColor(muted)
        c.drawString(0.9 * inch, letter[1] - 0.55 * inch, "StudentDeck")
        c.drawRightString(letter[0] - 0.9 * inch, letter[1] - 0.55 * inch, "Child Privacy & Policies")
        c.drawString(0.9 * inch, 0.55 * inch, f"StudentDeck Child Privacy & Policies · Version {VERSION} · Copyright © 2026 TeachersDeck™")
        c.drawRightString(letter[0] - 0.9 * inch, 0.55 * inch, f"Page {d.page - 1}")
        c.restoreState()

    out = ROOT / PDF
    SimpleDocTemplate(str(out), pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                      bottomMargin=0.85 * inch, title="StudentDeck Child Privacy & Policies", author="TeachersDeck",
                      subject=f"Version {VERSION}").build(story, onFirstPage=deco, onLaterPages=deco)
    return out


if __name__ == "__main__":
    print(build_page())
    print(build_pdf())
