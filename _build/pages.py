"""Builds the inner pages of myteachersdeck.com (one per app, plus international schools)
in English and Vietnamese. The header and footer are copied from the two home pages,
so inner pages always match them.

Run from the repository root:  python _build/pages.py
This folder starts with an underscore, so GitHub Pages does not publish it.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://myteachersdeck.com"
DEMO_SITE = "https://teachersdeck.github.io/demo/"
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import PAGES  # noqa: E402

UI = {
    "en": {"home": "Home", "skip": "Skip to content", "quote": "Request a quote", "demo": "Book a demo", "try": "Try the live demo",
           "more": "More from TeachersDeck Suite", "locale": "en_US", "alt_locale": "vi_VN"},
    "vi": {"home": "Trang chủ", "skip": "Bỏ qua đến nội dung", "quote": "Yêu cầu báo giá", "demo": "Đặt lịch demo", "try": "Dùng thử bản demo",
           "more": "Xem thêm về TeachersDeck Suite", "locale": "vi_VN", "alt_locale": "en_US"},
}


def esc(s):
    return html.escape(s, quote=True)


def url(lang, slug):
    return f"{SITE}/{'vi/' if lang == 'vi' else ''}{slug + '/' if slug else ''}"


def shell(lang):
    """Head extras, header and footer taken from the matching home page."""
    src = (ROOT / ("vi/index.html" if lang == "vi" else "index.html")).read_text(encoding="utf-8").replace("\r\n", "\n")
    header = re.search(r"<header>.*?</header>", src, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
    theme_init = re.search(r"<script>try\{[^\n]*?td_theme[^\n]*?</script>", src).group(0)
    fonts = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com[^"]*" rel="stylesheet">', src).group(0)
    tail = re.search(r'<script src="/assets/site.js" defer></script>\n.*?</body>', src, re.S).group(0)
    return header, footer, theme_init, fonts, tail


def fix_header(header, lang, slug):
    home = url(lang, "")
    header = header.replace('<a class="brand" href="#top">', f'<a class="brand" href="{home}">')
    header = re.sub(r'<a href="#(apps|connect|why|start)"', lambda m: f'<a href="{home}#{m.group(1)}"', header)
    header = re.sub(r'(<a href=")[^"]*(" hreflang="en")', lambda m: m.group(1) + url("en", slug) + m.group(2), header)
    header = re.sub(r'(<a href=")[^"]*(" hreflang="vi")', lambda m: m.group(1) + url("vi", slug) + m.group(2), header)
    return header


def render_section(sec):
    out = [f'<section id="{sec["id"]}"><div class="wrap">', '<div class="head">', f'<h2>{esc(sec["h2"])}</h2>']
    if sec.get("p"):
        out.append(f'<p>{esc(sec["p"])}</p>')
    out.append("</div>")
    for block in sec["blocks"]:
        kind = block[0]
        if kind == "tiles":
            out.append(f'<div class="tiles n{len(block[1])}">')
            for i, t in enumerate(block[1]):
                tint = t.get("tint") or ["amber", "matcha", "indigo", "coral"][i % 4]
                body = f'<p>{esc(t["p"])}</p>' if t.get("p") else ""
                if t.get("li"):
                    body += "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in t["li"]) + "</ul>"
                out.append(f'<div class="tile t-{tint}"><h3>{esc(t["h"])}</h3>{body}</div>')
            out.append("</div>")
        elif kind == "table":
            t = block[1]
            out.append('<div class="table-wrap"><table class="ptable"><thead><tr>' +
                       "".join(f"<th>{esc(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>")
            for row in t["rows"]:
                cls = ' class="total"' if row and row[0].startswith("!") else ""
                cells = [row[0].lstrip("!")] + list(row[1:])
                out.append(f"<tr{cls}>" + "".join(f"<td>{esc(c)}</td>" for c in cells) + "</tr>")
            out.append("</tbody></table></div>")
            if t.get("note"):
                out.append(f'<p class="note">{esc(t["note"])}</p>')
        elif kind == "h3":
            out.append(f'<h3 class="section-gap">{esc(block[1])}</h3>' + (f'<p class="note" style="font-style:normal">{esc(block[2])}</p>' if len(block) > 2 else ""))
        elif kind == "chips":
            out.append('<ul class="chips">' + "".join(f"<li>{esc(c)}</li>" for c in block[1]) + "</ul>")
        elif kind == "faq":
            out.append('<div class="faq">' + "".join(
                f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in block[1]) + "</div>")
        elif kind == "html":
            out.append(block[1])
    out.append("</div></section>")
    return "\n".join(out)


def build(page, lang):
    c = page[lang]
    slug = page["slug"]
    ui = UI[lang]
    header, footer, theme_init, fonts, tail = shell(lang)
    header = fix_header(header, lang, slug)
    here, home = url(lang, slug), url(lang, "")

    faq = [b[1] for s in c["sections"] for b in s["blocks"] if b[0] == "faq"]
    graph = [
        {"@type": "WebPage", "@id": here + "#page", "url": here, "name": c["title"], "description": c["description"],
         "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#site"}, "about": {"@id": f"{SITE}/#org"},
         "breadcrumb": {"@id": here + "#crumbs"}},
        {"@type": "BreadcrumbList", "@id": here + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home},
            {"@type": "ListItem", "position": 2, "name": c["crumb"], "item": here}]},
    ]
    if page.get("app"):
        app = page["app"]
        graph.append({"@type": "SoftwareApplication", "name": app["name"], "url": here, "applicationCategory": "EducationalApplication",
                      "operatingSystem": app["os"], "softwareVersion": app["version"], "description": c["description"],
                      "inLanguage": ["en", "vi"], "publisher": {"@id": f"{SITE}/#org"},
                      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "VND"}})
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq[0]]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    cta = c.get("cta") or [(ui["quote"], f"{SITE}/quote/"), (ui["demo"], f"{SITE}/demo/")]
    cta_html = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{h}">{esc(t)}</a>' for i, (t, h) in enumerate(cta))
    if page.get("demo"):  # the live demo opens in its own window (assets/site.js); a new tab if pop-ups are blocked
        cta_html += (f'<a class="btn try" href="{DEMO_SITE}{page["demo"]}?demo=1" target="_blank" rel="noopener" '
                     f'data-demo-window="{page["demo"].strip("/")}">{esc(ui["try"])}</a>')
    band = c["band"]
    band_html = (f'<section id="next"><div class="wrap"><div class="cta-band"><div><h2>{esc(band["h2"])}</h2><p>{esc(band["p"])}</p></div>'
                 f'<div class="cta">' + "".join(f'<a class="btn{" alt" if i else ""}" href="{h}">{esc(t)}</a>' for i, (t, h) in enumerate(band["links"])) +
                 "</div></div></div></section>")
    others = [p for p in PAGES if p["slug"] != slug]
    more_html = (f'<section id="more"><div class="wrap"><div class="head"><h2>{esc(ui["more"])}</h2></div><div class="more-apps">' +
                 "".join(f'<a class="btn" href="{url(lang, p["slug"])}">{esc(p[lang]["crumb"])}</a>' for p in others) +
                 "</div></div></section>")

    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(c["title"])}</title>
<meta name="description" content="{esc(c["description"])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#F3F5FC">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="en" href="{url("en", slug)}">
<link rel="alternate" hreflang="vi" href="{url("vi", slug)}">
<link rel="alternate" hreflang="x-default" href="{url("en", slug)}">
<link rel="icon" type="image/png" sizes="48x48" href="{SITE}/favicon-48.png">
<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="TeachersDeck Suite">
<meta property="og:title" content="{esc(c["title"])}"><meta property="og:description" content="{esc(c["description"])}">
<meta property="og:url" content="{here}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="TeachersDeck Suite logo"><meta property="og:locale" content="{ui["locale"]}"><meta property="og:locale:alternate" content="{ui["alt_locale"]}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(c["title"])}"><meta name="twitter:description" content="{esc(c["description"])}"><meta name="twitter:image" content="{SITE}/og.png">
<script type="application/ld+json">{ld}</script>
{fonts}
{theme_init}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
{header}
<main id="top">
<div class="wrap hero inner">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">{esc(ui["home"])}</a> › <span aria-current="page">{esc(c["crumb"])}</span></nav>
<p class="kicker">{esc(c["kicker"])}</p>
<h1>{esc(c["h1"])}</h1>
<p class="lede">{esc(c["lede"])}</p>
<div class="cta">{cta_html}</div>
</div>
{chr(10).join(render_section(s) for s in c["sections"])}
{band_html}
{more_html}
</main>
{footer}
{tail}
</html>
"""
    out = ROOT / (f"vi/{slug}" if lang == "vi" else slug) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out


def sitemap(date):
    entries = [("", ""), *[(p["slug"], p["slug"]) for p in PAGES]]
    rows = []
    for slug, _ in entries:
        alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{url("en", slug)}"/>'
                f'<xhtml:link rel="alternate" hreflang="vi" href="{url("vi", slug)}"/>')
        for lang in ("en", "vi"):
            rows.append(f'<url><loc>{url(lang, slug)}</loc><lastmod>{date}</lastmod>{alts}</url>')
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")


if __name__ == "__main__":
    import datetime
    for page in PAGES:
        for lang in ("en", "vi"):
            print("wrote", build(page, lang).relative_to(ROOT))
    sitemap(datetime.date.today().isoformat())
    print("wrote sitemap.xml")
