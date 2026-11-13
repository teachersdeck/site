"""Brings the TeachersDeck blog (written in Blogger at myteachersdeck.blogspot.com) onto myteachersdeck.com.

Posts are written in Blogger as usual. This reads the blog's public feed (no key) and builds:
  /blog/ and /vi/blog/            the list of posts (each language lists every post; posts in the other language are tagged)
  /blog/YYYY/MM/<slug>/           one page per English post, at the same path as on Blogger
  /vi/blog/YYYY/MM/<slug>/        the same for posts written in Vietnamese
and adds them to sitemap.xml.

English posts are also published in Vietnamese at /vi/blog/YYYY/MM/<slug>/ when _build/blog-vi/ holds a translation
(YYYY-MM-<slug>.html). _build/blog_translate.py writes those for new or changed posts; they can also be written or
corrected by hand (set "keep: yes" in the file so a later change to the English post doesn't replace it).
The two pages link to each other (hreflang), and each blog list shows a post once, in its own language.

The Blogger theme points each post's canonical link to its page here, so search engines
credit myteachersdeck.com. Comments stay on Blogger ("Comment on this post").

It also makes sure every page's dock has the Blog button (next to Support) and every footer links to the blog; pages
built later copy the header and footer from the home pages, so they get them too.

Run from the repository root:  python _build/blog.py  [path-or-url of the feed JSON]
.github/workflows/versions.yml runs it every hour and commits any change.
A failed or empty feed changes nothing, so a Blogger hiccup can never empty the blog.
"""
import datetime, hashlib, html, json, pathlib, re, shutil, sys, urllib.request
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import SITE, CSS_V, UI, esc, url, shell, fix_header  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOG = "https://myteachersdeck.blogspot.com"
SOURCE = f"{BLOG}/feeds/posts/default?alt=json&max-results=150"
MANIFEST = ROOT / "_build" / "blog-posts.json"   # the post folders this script made, so removed posts are removed here too
TRANSLATIONS = ROOT / "_build" / "blog-vi"       # Vietnamese versions of English posts

T = {
    "en": {"crumb": "Blog", "kicker": "Blog", "h1": "Notes from the classroom",
           "lede": "How TeachersDeck is made, ideas for your lessons, and what's new in the apps. Written by Jerry, a teacher in Ho Chi Minh City.",
           "title": "Blog: TeachersDeck Suite",
           "description": "The TeachersDeck blog: how the classroom apps are made, teaching ideas and news from TeachersDeck, StudentDeck, ParentDeck and AdminDeck.",
           "min": "{} min read", "other": "In Vietnamese", "read": "Read the post", "empty": "The first post is on its way.",
           "comment": "Comment on this post", "more": "More from the blog", "all": "All posts", "pair": "Đọc bằng tiếng Việt",
           "band_h2": "Try TeachersDeck in your classroom", "band_p": "40+ free classroom tools: timers, name picker, groups, points and more. Opens in your browser.",
           "band": [("Get the apps", "apps/"), ("Try the live demo", "try/")], "date": "%d %B %Y"},
    "vi": {"crumb": "Blog", "kicker": "Blog", "h1": "Ghi chép từ lớp học",
           "lede": "TeachersDeck được làm ra như thế nào, ý tưởng cho tiết học, và điểm mới trong các ứng dụng. Do Jerry, một giáo viên ở TP. Hồ Chí Minh, viết.",
           "title": "Blog: TeachersDeck Suite",
           "description": "Blog TeachersDeck: cách các ứng dụng lớp học được làm ra, ý tưởng giảng dạy và tin mới từ TeachersDeck, StudentDeck, ParentDeck và AdminDeck.",
           "min": "{} phút đọc", "other": "Tiếng Anh", "read": "Đọc bài", "empty": "Bài viết đầu tiên sắp ra mắt.",
           "comment": "Bình luận về bài này", "more": "Bài viết khác", "all": "Tất cả bài viết", "pair": "Bản gốc tiếng Anh",
           "band_h2": "Dùng thử TeachersDeck trong lớp của bạn", "band_p": "Hơn 40 công cụ lớp học miễn phí: hẹn giờ, gọi tên ngẫu nhiên, chia nhóm, cộng điểm và nhiều hơn nữa. Mở ngay trên trình duyệt.",
           "band": [("Tải ứng dụng", "vi/apps/"), ("Dùng thử bản demo", "try/")], "date": "%d/%m/%Y"},
}

# The styles for the blog pages only, so assets/site.css (and its version on every page) stays as it is.
STYLE = """<style>
.bloglist{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:var(--gap);margin:0 0 56px}
.bcard{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;color:inherit;transition:transform .15s ease,box-shadow .15s ease}
.bcard:hover{transform:translateY(-2px);box-shadow:var(--tile-hover)}
.bcard img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:var(--line)}
.bcard div{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.bcard h2{font-size:21px}
.bcard p{margin:0;color:var(--muted);font-size:15px;line-height:1.55}
.bmeta{font-size:13px;color:var(--muted)}
.bmeta .tag{display:inline-block;margin-left:6px;padding:1px 8px;border-radius:999px;border:1px solid var(--line)}
.bcard .more{margin-top:auto;color:var(--accent-text);font-weight:600;font-size:14px}
.blogpost{max-width:760px;margin:0 auto;padding:48px 20px 24px}
.blogpost h1{font-size:clamp(30px,5vw,44px);margin:0 0 12px;letter-spacing:-.4px}
.blogpost .bmeta{margin:0 0 28px}
.post-body{font-size:18px;line-height:1.75}
.post-body h2{font-size:28px;margin:1.7em 0 .5em}
.post-body h3{font-size:22px;margin:1.5em 0 .4em}
.post-body h4,.post-body h5,.post-body h6{font-size:18px;margin:1.4em 0 .4em}
.post-body p{margin:0 0 1.1em}
.post-body a{color:var(--accent-text)}
.post-body img{max-width:100%;height:auto;border-radius:16px}
.post-body img.wide{display:block;width:100%;margin:0 auto}
.post-body .separator{margin:1.2em 0}
.post-body iframe{display:block;width:100%;height:auto;aspect-ratio:16/9;border:0;border-radius:16px;background:#000;margin:0 auto}
.post-body blockquote{margin:1.4em 0;padding:4px 20px;border-left:4px solid var(--accent);color:var(--muted)}
.post-body table{max-width:100%;border-collapse:collapse}
.post-body .tr-caption-container{margin:1.2em auto}
.post-body .tr-caption{font-size:14px;color:var(--muted);text-align:center;padding-top:6px}
.post-body .center{text-align:center}
.post-body pre{overflow:auto;padding:14px;border-radius:12px;background:var(--line)}
.post-foot{display:flex;gap:12px;flex-wrap:wrap;margin:36px 0 0;padding-top:22px;border-top:1px solid var(--line)}
@media (max-width:640px){.post-body{font-size:17px}.blogpost{padding-top:32px}}
</style>"""

DOCK_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/>'
             '<path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/></svg>')


def blog_url(lang, path=""):
    return url(lang, "blog") + path


# ---------- feed ----------

def load(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (site build)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    return pathlib.Path(src).read_bytes()


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


VI_CHARS = re.compile(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", re.I)


def language(title, body, labels):
    if {"vi", "tiếng việt", "tieng viet", "vietnamese"} & {l.lower() for l in labels}:
        return "vi"
    if {"en", "english"} & {l.lower() for l in labels}:
        return "en"
    t = title + " " + text_of(body)[:3000]
    letters = sum(c.isalpha() for c in t) or 1
    return "vi" if len(VI_CHARS.findall(t)) / letters > 0.03 else "en"


def big_image(src):
    """Blogger's full-size copy of an image (/s1600/), instead of a thumbnail size."""
    return re.sub(r"/(s|w)\d+(-[a-z0-9-]+)?/", "/s1600/", src).replace("=s72-c", "=s1600")


def posts(src):
    feed = json.loads(load(src))["feed"]
    out = []
    for e in feed.get("entry", []):
        link = next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), "")
        m = re.match(re.escape(BLOG) + r"/(\d{4})/(\d{2})/([a-z0-9-]+)\.html$", link)
        if not m:
            continue   # pages (not posts) and drafts have no dated address
        body = e.get("content", {}).get("$t", "")
        labels = [c.get("term", "") for c in e.get("category", [])]
        title = text_of(e.get("title", {}).get("$t", "")) or "Untitled"
        lang = language(title, body, labels)
        clean, first_img = Clean.run(body)
        thumb = first_img or big_image(e.get("media$thumbnail", {}).get("url", ""))
        words = len(text_of(clean).split())
        out.append({
            "title": title, "path": f"{m.group(1)}/{m.group(2)}/{m.group(3)}/", "blogger": link, "lang": lang,
            "published": e["published"]["$t"], "updated": e.get("updated", {}).get("$t", e["published"]["$t"]),
            "labels": [l for l in labels if l.lower() not in ("en", "vi", "english", "tiếng việt", "vietnamese")],
            "html": clean, "image": thumb, "minutes": max(1, round(words / 220)),
            "description": summary(clean), "author": (e.get("author") or [{}])[0].get("name", {}).get("$t", "TeachersDeck"),
        })
    out.sort(key=lambda p: p["published"], reverse=True)
    return out


def summary(fragment, n=155):
    paras = [text_of(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", fragment, re.S)]
    t = next((p for p in paras if len(p) > 40), "") or text_of(fragment)
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


# ---------- Vietnamese versions of English posts ----------

def translation_file(p):
    return TRANSLATIONS / (p["path"].strip("/").replace("/", "-") + ".html")


def source_hash(p):
    """Changes only when the English post's title or text really changes (not on every Blogger 'updated')."""
    return hashlib.sha256((p["title"] + "\n" + p["html"]).encode("utf-8")).hexdigest()[:16]


def read_translation(f):
    """A translation file is the post's HTML after a few header lines like <!-- title: ... -->."""
    lines, meta, i = f.read_text(encoding="utf-8").splitlines(), {}, 0
    while i < len(lines):
        m = re.match(r"^<!--\s*([a-z-]+):\s*(.*?)\s*-->$", lines[i].strip())
        if not m:
            break
        meta[m.group(1)] = m.group(2)
        i += 1
    return meta, "\n".join(lines[i:]).strip()


def add_translations(all_posts):
    """Adds a Vietnamese post for every English post with a translation (unless a Vietnamese post already has its path),
    and marks the posts that have a counterpart in the other language ("pair")."""
    have = {(p["lang"], p["path"]) for p in all_posts}
    out = list(all_posts)
    for p in all_posts:
        f = translation_file(p)
        if p["lang"] != "en" or ("vi", p["path"]) in have or not f.exists():
            continue
        meta, body = read_translation(f)
        clean, _ = Clean.run(body)   # the same cleaning as Blogger posts, so a translation can't add scripts or styles
        title = text_of(meta.get("title", ""))
        if not title or not clean:
            print(f"blog: {f.name} has no title or text; skipped")
            continue
        if meta.get("source-hash") != source_hash(p):
            print(f"blog: {f.name} was made from an older version of the English post")
        out.append({**p, "lang": "vi", "title": title, "html": clean, "description": summary(clean), "translated": True})
    paths = {(p["lang"], p["path"]) for p in out}
    for p in out:
        p["pair"] = ("vi" if p["lang"] == "en" else "en", p["path"]) in paths
    out.sort(key=lambda p: (p["published"], p["lang"] == "en"), reverse=True)
    return out


# ---------- cleaning the post HTML ----------

class Clean(HTMLParser):
    """Keeps the post's text, headings, links, pictures and videos, and drops Blogger's inline styles and scripts.
    The post's own <h1>s become <h2>s (the page title is the only <h1>), and large pictures load at full size."""
    TAGS = {"p", "br", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "b", "em", "i", "u", "s", "a", "img", "iframe", "ul", "ol",
            "li", "blockquote", "div", "span", "figure", "figcaption", "table", "thead", "tbody", "tr", "th", "td", "hr", "pre",
            "code", "sup", "sub"}
    VOID = {"br", "img", "hr"}
    DROP = {"script", "style", "noscript", "form", "input", "button", "object", "embed"}
    CLASSES = {"separator", "tr-caption-container", "tr-caption"}
    VIDEO = re.compile(r"^(https:)?//(www\.)?(youtube(-nocookie)?\.com/embed/|player\.vimeo\.com/video/|www\.blogger\.com/video\.g)")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip, self.first_img = [], [], 0, ""

    @classmethod
    def run(cls, fragment):
        c = cls()
        c.feed(fragment)
        c.close()
        while c.stack:
            c.out.append(f"</{c.stack.pop()}>")
        body = "".join(c.out)
        body = re.sub(r"(<br>\s*){3,}", "<br><br>", body)
        body = re.sub(r"^(\s*<br>)+", "", body)   # Blogger often starts a post with blank lines
        body = re.sub(r"<(p|div|span|h2|h3)( class=\"[^\"]*\")?>\s*(<br>\s*)*</\1>", "", body)   # empty blocks
        return body.strip(), c.first_img

    def handle_starttag(self, tag, attrs):
        if tag in self.DROP:
            self.skip += tag not in self.VOID and tag not in ("input", "embed")
            return
        if self.skip or tag not in self.TAGS:
            return
        a = dict(attrs)
        name = "h2" if tag == "h1" else tag
        keep = []
        classes = [c for c in (a.get("class") or "").split() if c in self.CLASSES]
        if re.search(r"text-align:\s*center", a.get("style") or "") or (a.get("align") or "").lower() == "center":
            classes.append("center")
        if tag == "a":
            href = a.get("href") or ""
            if not re.match(r"^(https?:|mailto:|#)", href):
                self._open(name, [])   # keep the text, drop an unsafe or relative link
                return
            keep.append(("href", href))
            if href.startswith("http") and "myteachersdeck.com" not in href:
                keep += [("target", "_blank"), ("rel", "noopener")]
        elif tag == "img":
            src = a.get("src") or ""
            if not src.startswith("http"):
                return
            wide = int(re.sub(r"\D", "", a.get("data-original-width") or a.get("width") or "0") or 0) >= 600
            if wide:
                src = big_image(src)
                classes.append("wide")
            if not self.first_img:
                self.first_img = big_image(src)
            keep += [("src", src), ("alt", a.get("alt") or ""), ("loading", "lazy"), ("decoding", "async")]
        elif tag == "iframe":
            src = a.get("src") or ""
            if not self.VIDEO.match(src):
                self.skip += 1
                return
            keep += [("src", "https:" + src if src.startswith("//") else src), ("title", a.get("title") or "Video"),
                     ("loading", "lazy"), ("allowfullscreen", ""), ("referrerpolicy", "strict-origin-when-cross-origin"),
                     ("allow", "accelerometer; encrypted-media; gyroscope; picture-in-picture")]
        if classes:
            keep.insert(0, ("class", " ".join(dict.fromkeys(classes))))
        self._open(name, keep)

    def _open(self, name, keep):
        attrs = "".join(f' {k}="{esc(v)}"' if v != "" or k == "alt" else f" {k}" for k, v in keep)
        self.out.append(f"<{name}{attrs}>")
        if name not in self.VOID:
            self.stack.append(name)

    def handle_endtag(self, tag):
        if tag in self.DROP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "iframe" and self.skip:
            self.skip -= 1
            return
        if self.skip or tag not in self.TAGS or tag in self.VOID:
            return
        name = "h2" if tag == "h1" else tag
        if name in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f"</{t}>")
                if t == name:
                    break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID and tag in self.TAGS and not self.skip:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.skip:
            self.out.append(esc(data).replace("&#x27;", "'"))


# ---------- pages ----------

def date(p, lang):
    d = datetime.date.fromisoformat(p["published"][:10])
    if lang == "en":
        return f"{d.day} {d.strftime('%B %Y')}"
    return d.strftime(T["vi"]["date"])


def head(lang, title, description, here, alternates, og_type="website", image=None, ld=None):
    ui = UI[lang]
    _, _, theme_init, fonts, _ = shell(lang)
    image = image or f"{SITE}/og.png"
    alts = "".join(f'<link rel="alternate" hreflang="{h}" href="{u}">\n' for h, u in alternates)
    size = '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if image.endswith("/og.png") else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#F3F5FC">
<link rel="canonical" href="{here}">
{alts}<link rel="alternate" type="application/atom+xml" title="TeachersDeck blog" href="{BLOG}/feeds/posts/default">
<link rel="icon" type="image/png" sizes="48x48" href="{SITE}/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="{SITE}/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="{SITE}/favicon-192.png">
<link rel="icon" href="{SITE}/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="TeachersDeck Suite">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{here}"><meta property="og:image" content="{esc(image)}">{size}
<meta property="og:locale" content="{ui["locale"]}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{esc(image)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{fonts}
{theme_init}
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{STYLE}
</head>
"""


def band(lang):
    t = T[lang]
    links = "".join(f'<a class="btn{" alt" if i else ""}" href="{SITE}/{h}">{esc(n)}</a>' for i, (n, h) in enumerate(t["band"]))
    return (f'<section id="next"><div class="wrap"><div class="cta-band"><div><h2>{esc(t["band_h2"])}</h2><p>{esc(t["band_p"])}</p></div>'
            f'<div class="cta">{links}</div></div></div></section>')


def card(p, lang):
    t = T[lang]
    tag = f'<span class="tag">{esc(t["other"])}</span>' if p["lang"] != lang else ""
    img = f'<img src="{esc(p["image"])}" alt="" loading="lazy" decoding="async">' if p["image"] else ""
    return (f'<a class="bcard" href="{blog_url(p["lang"], p["path"])}">{img}<div>'
            f'<span class="bmeta">{date(p, lang)} · {t["min"].format(p["minutes"])}{tag}</span>'
            f'<h2>{esc(p["title"])}</h2><p>{esc(p["description"])}</p><span class="more">{esc(t["read"])} →</span></div></a>')


def page(lang, title, description, here, alternates, body, ld, og_type="website", image=None):
    header, footer, _, _, tail = shell(lang)
    header = fix_header(header, lang, "blog")
    return f"""{head(lang, title, description, here, alternates, og_type, image, ld)}<body>
{header}
<main id="top">
{body}
</main>
{footer}
{tail}
</html>
"""


def build_index(lang, all_posts):
    t, ui = T[lang], UI[lang]
    here, home = blog_url(lang), url(lang, "")
    mine = [p for p in all_posts if p["lang"] == lang] + [p for p in all_posts if p["lang"] != lang and not p.get("pair")]
    cards = "".join(card(p, lang) for p in mine) or f'<p class="lede">{esc(t["empty"])}</p>'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": here + "#blog", "url": here, "name": t["title"], "description": t["description"], "inLanguage": lang,
         "isPartOf": {"@id": f"{SITE}/#site"}, "publisher": {"@id": f"{SITE}/#org"},
         "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": blog_url(p["lang"], p["path"]),
                       "datePublished": p["published"], "image": p["image"] or None} for p in all_posts[:20]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": here}]}]}
    body = f"""<div class="wrap hero inner">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">{esc(ui["home"])}</a> › <span aria-current="page">{esc(t["crumb"])}</span></nav>
<p class="kicker">{esc(t["kicker"])}</p>
<h1>{esc(t["h1"])}</h1>
<p class="lede">{esc(t["lede"])}</p>
</div>
<div class="wrap"><div class="bloglist">{cards}</div></div>
{band(lang)}"""
    alts = [("en", blog_url("en")), ("vi", blog_url("vi")), ("x-default", blog_url("en"))]
    return page(lang, t["title"], t["description"], here, alts, body, ld)


def build_post(p, all_posts):
    lang = p["lang"]
    t, ui = T[lang], UI[lang]
    here, home, index = blog_url(lang, p["path"]), url(lang, ""), blog_url(lang)
    other_lang = "vi" if lang == "en" else "en"
    pair_url = blog_url(other_lang, p["path"]) if p.get("pair") else ""
    others = [o for o in all_posts if o["path"] != p["path"] and o["lang"] == lang]
    others = (others + [o for o in all_posts if o["path"] != p["path"] and o["lang"] != lang and not o.get("pair")])[:3]
    more = (f'<section id="more"><div class="wrap"><div class="head"><h2>{esc(t["more"])}</h2></div>'
            f'<div class="bloglist">{"".join(card(o, lang) for o in others)}</div></div></section>') if others else ""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": here + "#post", "mainEntityOfPage": here, "url": here, "headline": p["title"][:110],
         "description": p["description"], "datePublished": p["published"], "dateModified": p["updated"], "inLanguage": lang,
         "image": [p["image"]] if p["image"] else [f"{SITE}/og.png"], "keywords": p["labels"] or None,
         "author": {"@type": "Person", "name": "Jerry" if p["author"] in ("TeachersDeck", "") else p["author"], "url": SITE + "/"},
         "publisher": {"@id": f"{SITE}/#org"}, "isPartOf": {"@id": blog_url("en") + "#blog"},
         **({"translationOfWork": {"@id": pair_url + "#post"}} if p.get("translated") else {})},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": index},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": here}]}]}
    pair_link = (f' · <a href="{pair_url}" hreflang="{other_lang}" lang="vi">{esc(t["pair"])}</a>'
                 if pair_url else "")
    body = f"""<article class="blogpost">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">{esc(ui["home"])}</a> › <a href="{index}">{esc(t["crumb"])}</a> › <span aria-current="page">{esc(p["title"])}</span></nav>
<h1>{esc(p["title"])}</h1>
<p class="bmeta"><time datetime="{p["published"]}">{date(p, lang)}</time> · {t["min"].format(p["minutes"])}{pair_link}</p>
<div class="post-body">
{p["html"]}
</div>
<div class="post-foot"><a class="btn" href="{esc(p["blogger"])}#comments" rel="noopener">{esc(t["comment"])}</a><a class="btn" href="{index}">{esc(t["all"])}</a></div>
</article>
{band(lang)}
{more}"""
    alts = ([("en", blog_url("en", p["path"])), ("vi", blog_url("vi", p["path"])), ("x-default", blog_url("en", p["path"]))]
            if pair_url else [(lang, here), ("x-default", here)])
    return page(lang, f'{p["title"]} · TeachersDeck blog', p["description"], here, alts, body, ld,
                "article", p["image"] or None)


# ---------- dock, footer, sitemap ----------

DOCK_ITEM = '<a href="{href}" class="dk-i" data-i="nav_blog" aria-label="Blog">' + DOCK_ICON + '<span class="dk-tip" aria-hidden="true">Blog</span></a>'


def ensure_nav():
    """Adds the Blog button to the dock (just before Support) and a Blog link to the footer of every page that lacks them."""
    changed = []
    for f in sorted(ROOT.rglob("*.html")):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(("_", ".", "demo/")) or "/node_modules/" in rel:
            continue
        text = f.read_text(encoding="utf-8")
        new = text
        vi = 'lang="vi"' in text[:300]
        href = blog_url("vi" if vi else "en")
        if 'data-i="nav_blog"' not in new:
            new = re.sub(r'(<a href="[^"]*/support/" class="dk-i")', DOCK_ITEM.format(href=href).replace("\\", "\\\\") + r"\1", new, count=1)
        if '<div class="wrap sitelinks">' in new and f'sitelinks"><nav' in new and '>Blog</a></nav>' not in new:
            new = re.sub(r'(<div class="wrap sitelinks"><nav[^>]*>.*?)(</nav>)', lambda m: m.group(1) + f' · <a href="{href}">Blog</a>' + m.group(2), new, count=1, flags=re.S)
        if new != text:
            f.write_text(new, encoding="utf-8", newline="\n")
            changed.append(rel)
    return changed


def sitemap(all_posts):
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if "/blog/" not in l]
    today = datetime.date.today().isoformat()
    newest = max((p["updated"][:10] for p in all_posts), default=today)
    alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{blog_url("en")}"/>'
            f'<xhtml:link rel="alternate" hreflang="vi" href="{blog_url("vi")}"/>')
    rows = [f'<url><loc>{blog_url(l)}</loc><lastmod>{newest}</lastmod>{alts}</url>' for l in ("en", "vi")]
    rows += [f'<url><loc>{blog_url(p["lang"], p["path"])}</loc><lastmod>{p["updated"][:10]}</lastmod></url>' for p in all_posts]
    end = lines.index("</urlset>")
    new = "\n".join(lines[:end] + rows + lines[end:]) + "\n"
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
        return True
    return False


def write(rel, doc, written):
    f = ROOT / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    if not f.exists() or f.read_text(encoding="utf-8") != doc:
        f.write_text(doc, encoding="utf-8", newline="\n")
        print("wrote", rel)
    written.add(rel)


def main(src):
    try:
        all_posts = add_translations(posts(src))
    except Exception as e:  # noqa: BLE001 - any feed problem leaves the site as it is
        sys.exit(f"blog: could not read {src}: {e}; leaving the blog as it is")
    if not all_posts:
        sys.exit(f"blog: {src} gave no posts; leaving the blog as it is")
    for rel in ensure_nav():
        print("dock/footer:", rel)
    written = set()
    for lang in ("en", "vi"):
        write(f"{'vi/' if lang == 'vi' else ''}blog/index.html", build_index(lang, all_posts), written)
    for p in all_posts:
        write(f"{'vi/' if p['lang'] == 'vi' else ''}blog/{p['path']}index.html", build_post(p, all_posts), written)
    old = set(json.loads(MANIFEST.read_text(encoding="utf-8"))) if MANIFEST.exists() else set()
    for rel in sorted(old - written):   # a post deleted or moved in Blogger
        d = (ROOT / rel).parent
        if d.is_dir() and d.relative_to(ROOT).as_posix().count("/") >= 3:
            shutil.rmtree(d)
            print("removed", d.relative_to(ROOT).as_posix())
    MANIFEST.write_text(json.dumps(sorted(written), indent=1) + "\n", encoding="utf-8", newline="\n")
    if sitemap(all_posts):
        print("wrote sitemap.xml")
    print(f"blog: {len(all_posts)} post(s)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SOURCE)
