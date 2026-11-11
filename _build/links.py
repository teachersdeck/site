"""The links page (/links/, /vi/links/): one page for social media bios that allow a single link (TikTok, Instagram,
YouTube, Zalo). Big buttons to the apps, the demos, the blog, YouTube, Patreon and support, then the same social icons as
the footer (copied from it, so a changed social link changes here too on the next build).

Use it in each bio with that channel's tag, so GA4 shows which channel sent the visit, for example:
  https://myteachersdeck.com/links/?utm_source=tiktok&utm_medium=social&utm_campaign=bio
Each button click is counted as the GA4 event "links_click" with the button's kind (apps, demo, blog…), nothing else.
The page is noindex: it only repeats links that are on the site already.

Run from the repository root:  python _build/links.py
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import SITE, CSS_V, UI, esc, url, shell, fix_header  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
YOUTUBE = "https://www.youtube.com/@TeachersDeckSuite"
PATREON = "https://www.patreon.com/c/TeachersDeck"
ZALO = "https://zalo.me/0705247680"

ICON = {  # 24x24 line icons, drawn in the button's text colour
    "apps": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "demo": '<path d="M5 3l14 9-14 9z"/>',
    "blog": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "youtube": '<path d="M2 8a4 4 0 0 1 4 -4h12a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-12a4 4 0 0 1 -4 -4v-8z"/><path d="M10 9l5 3l-5 3z"/>',
    "pricing": '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r="1.2"/>',
    "patreon": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
    "zalo": '<path d="M3 20l1.3 -3.9a9 8 0 1 1 3.4 2.9l-4.7 1"/><path d="M9.5 9.5h5l-5 5h5"/>',
    "support": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.9 4.9 4.3 4.3M14.8 9.2l4.3-4.3M14.8 14.8l4.3 4.3M9.2 14.8l-4.3 4.3"/>',
}

T = {
    "en": {"title": "Links: TeachersDeck Suite", "crumb": "Links",
           "description": "TeachersDeck Suite in one place: get the classroom apps, try the live demos, read the blog, watch the videos and get help.",
           "h1": "TeachersDeck Suite", "lede": "Free classroom apps for teachers, students and families. Made by a teacher in Ho Chi Minh City.",
           "follow": "Follow TeachersDeck",
           "links": [("apps", "Get the apps", "Free, in your browser or as your Chrome new tab", "apps/"),
                     ("demo", "Try the live demos", "Every app with sample data, no sign-up", "try/"),
                     ("blog", "Read the blog", "How TeachersDeck is made, and teaching ideas", "blog/"),
                     ("youtube", "Watch on YouTube", "Tips, tutorials and Deckie", YOUTUBE),
                     ("pricing", "Pricing", "Free plan, Pro and plans for schools", "pricing/"),
                     ("patreon", "Support TeachersDeck on Patreon", "Help pay for the servers, voices and AI, from $2 a month", PATREON),
                     ("zalo", "Chat on Zalo", "A quick question? Message us", ZALO),
                     ("support", "Help and support", "Ask AgentDeck, email or report a problem", "support/")]},
    "vi": {"title": "Liên kết: TeachersDeck Suite", "crumb": "Liên kết",
           "description": "TeachersDeck Suite ở một nơi: tải ứng dụng lớp học, dùng thử bản demo, đọc blog, xem video và nhận hỗ trợ.",
           "h1": "TeachersDeck Suite", "lede": "Ứng dụng lớp học miễn phí cho giáo viên, học sinh và phụ huynh. Do một giáo viên ở TP. Hồ Chí Minh làm ra.",
           "follow": "Theo dõi TeachersDeck",
           "links": [("apps", "Tải ứng dụng", "Miễn phí, trên trình duyệt hoặc làm trang tab mới của Chrome", "vi/apps/"),
                     ("demo", "Dùng thử bản demo", "Mọi ứng dụng với dữ liệu mẫu, không cần đăng ký", "try/"),
                     ("blog", "Đọc blog", "TeachersDeck được làm ra như thế nào, và ý tưởng giảng dạy", "vi/blog/"),
                     ("youtube", "Xem trên YouTube", "Mẹo, hướng dẫn và Deckie", YOUTUBE),
                     ("pricing", "Bảng giá", "Gói miễn phí, Pro và gói cho nhà trường", "vi/pricing/"),
                     ("patreon", "Ủng hộ TeachersDeck trên Patreon", "Góp phần trả chi phí máy chủ, giọng đọc và AI, từ 2 USD mỗi tháng", PATREON),
                     ("zalo", "Nhắn Zalo", "Có câu hỏi nhanh? Nhắn cho chúng tôi", ZALO),
                     ("support", "Hỗ trợ", "Hỏi AgentDeck, gửi email hoặc báo lỗi", "vi/support/")]},
}

STYLE = """<style>
.lnk{max-width:560px;margin:0 auto;padding:40px 20px 64px;text-align:center}
.lnk>img{width:96px;height:96px;border-radius:24px;display:block;margin:0 auto 14px}
.lnk h1{font-size:clamp(28px,6vw,36px);margin:0 0 8px}
.lnk .lede{margin:0 auto 26px;font-size:16px}
.lnk-list{display:flex;flex-direction:column;gap:12px;margin:0;padding:0;list-style:none;text-align:left}
.lnk-list a{display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:20px;background:var(--surface);border:1px solid var(--line);
 text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.lnk-list a:hover{transform:translateY(-1px);box-shadow:var(--tile-hover);border-color:var(--accent-text)}
.lnk-list a.primary{background:var(--accent);color:var(--on-accent);border-color:transparent}
.lnk-list svg{flex:0 0 auto;width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.lnk-list b{display:block;font:700 17px/1.3 'Quicksand',sans-serif}
.lnk-list span{display:block;font-size:14px;line-height:1.4;opacity:.8}
.lnk h2{font-size:15px;margin:34px 0 12px;color:var(--muted);font-family:'Inter',sans-serif;font-weight:600}
.lnk .social{justify-content:center;flex-wrap:wrap;margin:0}
</style>"""


def build(lang):
    t, ui = T[lang], UI[lang]
    header, footer, theme_init, fonts, tail = shell(lang)
    header = fix_header(header, lang, "links")
    here = url(lang, "links")
    social = re.search(r'<nav class="social"[^>]*>.*?</nav>', footer, re.S)
    social = social.group(0) if social else ""
    items = []
    for i, (kind, label, sub, href) in enumerate(t["links"]):
        full = href if href.startswith("http") else f"{SITE}/{href}"
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        items.append(f'<li><a{" class=\"primary\"" if i == 0 else ""} href="{esc(full)}" data-link="{kind}"{ext}>'
                     f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[kind]}</svg><div><b>{esc(label)}</b><span>{esc(sub)}</span></div></a></li>')
    ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": here + "#page", "url": here, "name": t["title"],
          "description": t["description"], "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#site"}, "about": {"@id": f"{SITE}/#org"}}
    alt = {"en": url("en", "links"), "vi": url("vi", "links")}
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t["title"])}</title>
<meta name="description" content="{esc(t["description"])}">
<meta name="robots" content="noindex,follow">
<meta name="theme-color" content="#F3F5FC">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="en" href="{alt["en"]}">
<link rel="alternate" hreflang="vi" href="{alt["vi"]}">
<link rel="alternate" hreflang="x-default" href="{alt["en"]}">
<link rel="icon" type="image/png" sizes="96x96" href="{SITE}/favicon-96.png">
<link rel="icon" href="{SITE}/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="TeachersDeck Suite">
<meta property="og:title" content="{esc(t["title"])}"><meta property="og:description" content="{esc(t["description"])}">
<meta property="og:url" content="{here}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{ui["locale"]}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/og.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{fonts}
{theme_init}
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{STYLE}
</head>
<body>
{header}
<main id="top">
<div class="lnk">
<img src="{SITE}/apple-touch-icon.png" alt="TeachersDeck logo" width="96" height="96">
<h1>{esc(t["h1"])}</h1>
<p class="lede">{esc(t["lede"])}</p>
<ul class="lnk-list">
{chr(10).join(items)}
</ul>
<h2>{esc(t["follow"])}</h2>
{social}
</div>
</main>
{footer}
<script>document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a[data-link]');if(a&&window.tdEvent)window.tdEvent('links_click',{{link_kind:a.getAttribute('data-link')}})}});</script>
{tail}
</html>
"""


def main():
    for lang in ("en", "vi"):
        out = ROOT / ("vi/links" if lang == "vi" else "links") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = build(lang)
        if not out.exists() or out.read_text(encoding="utf-8") != doc:
            out.write_text(doc, encoding="utf-8", newline="\n")
            print("wrote", out.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
