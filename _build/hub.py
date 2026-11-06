"""Get the apps (/apps/ and /vi/apps/): every app of the suite and every way to get it, built from _build/apps.json.

Each app is one row with one main button chosen for the visitor's device, and every other way in folded under
"Other ways". The choice is made here, per device group, and the page only says which group it is on
(an inline script sets <html data-dev="mobile|chrome|other"> from navigator.userAgentData and the user agent):
  mobile  phones and tablets            -> the web app, else the live demo
  chrome  Chrome or Edge on a computer  -> the Chrome Web Store, else the web app, else the live demo
  other   Safari, Firefox on a computer -> the web app, else the live demo
LMS editions go to their set-up page on every device. Without JavaScript the "other" choice shows.

Also writes the short addresses (/get/ -> /apps/, /teacher/ /student/ /parent/ /admin/ /lecture/ /uni/ -> the web apps) and a
public copy of the list at /apps/apps.json (with the latest .zip of each app) for AgentDeck and HQ.

Run from the repository root:  python _build/hub.py          (pages.py runs it too, after the inner pages)
                               python _build/hub.py --check  (also asks every web app address whether it answers)
"""
import json, pathlib, re, sys, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import ROOT, SITE, UI, esc, fix_header, head, shell, url  # noqa: E402

SLUG = "apps"
DATA = ROOT / "_build" / "apps.json"
DL = ROOT / "downloads"
ZIP_URL = f"{SITE}/downloads/"  # where the zips in DL are served (_build/downloads.py fills DL)
CONTACT = {"email": "mailto:jerry@myteachersdeck.com", "zalo": "https://zalo.me/0705247680", "demo": f"{SITE}/demo/"}
# Tile colour per app, in the order of each group; the four school apps keep the colours they have everywhere else.
TINTS = ["amber", "matcha", "indigo", "coral"]
DEVICES = ("mobile", "chrome", "other")

T = {
    "en": {
        "title": "Get the apps — TeachersDeck Suite",
        "description": "Every TeachersDeck Suite app and the best way to get it on your device: web apps for phones and tablets, "
                       "the Chrome Web Store, .zip downloads, live demos, the ClassIn, Canvas and Moodle editions and the KinderDeck preschool apps.",
        "crumb": "Get the apps", "kicker": "TeachersDeck Suite", "h1": "Get the apps",
        "lede": "Find your app below. Its main button is the best way in on the device you are using; every other way is under Other ways.",
        "groups_p": {"school": "For schools and language centers: one app for each person in the class.",
                     "preschool": "KinderDeck, the preschool edition: one app for the office, one for teachers, one for families.",
                     "uni": "UniDeck, the university edition, in early preview.",
                     "lms": "TeachersDeck inside the platform your school already uses."},
        "dev": {"mobile": "On a phone or tablet the web apps work best: open one, then add it to your Home Screen.",
                "chrome": "You are on Chrome or Edge on a computer: TeachersDeck and StudentDeck can open on every new tab.",
                "other": "On this browser the web apps work best. TeachersDeck and StudentDeck can also run in Chrome as your new tab."},
        "web": "Open the web app", "store": "Add to Chrome", "demo": "Try the live demo", "setup": "Set it up", "book": "Book a demo", "contact": "Contact us",
        "status": {"preview": "Early access", "beta": "Beta", "soon": "Coming soon"},
        "hs": "Then add it to your Home Screen",
        "more": "Other ways",
        "way": {"web": "Web app, on any device", "store": "Chrome Web Store, updates itself", "zip": ".zip for Chrome",
                "zip_how": "how to install", "demo": "Live demo, pretend data, no sign-in", "setup": "Set-up guide", "page": "About"},
        "install_h": "How to install", "install_p": "Three ways to keep an app one tap away.",
        "hs_h": "Add a web app to your Home Screen",
        "hs_steps": [("iPhone and iPad", "Open the web app in Safari, tap <b>Share</b>, then <b>Add to Home Screen</b>."),
                     ("Android", "Open the web app in Chrome, tap the <b>⋮</b> menu, then <b>Add to Home screen</b> or <b>Install app</b>."),
                     ("Computer", "In Chrome or Edge, click the install icon at the end of the address bar, or open the menu and choose <b>Install</b>.")],
        "zip_h": "Install a .zip in Chrome",
        "zip_steps": ["Unzip it into a folder you will keep, such as Documents. Chrome reads that folder every time, so don't move or delete it.",
                      "In Chrome, open <code>chrome://extensions</code> and turn on <b>Developer mode</b> (top right).",
                      "Click <b>Load unpacked</b> and choose the folder that holds <code>manifest.json</code>.",
                      "Open a new tab. One app per Chrome profile: each one becomes the new-tab page."],
        "zip_note": "Everything works when installed from a .zip, including signing in and cloud classes; Chrome asks once for permission to "
                    "show the Google sign-in window. The app doesn't update itself: download the new version when there is one.",
        "faq_h": "Questions about installing",
        "faq": [("Do I need to install anything?",
                 "No. Every app with a web app opens in a browser on any phone, tablet or computer. On Chrome, TeachersDeck and StudentDeck can also be your new tab."),
                ("Which should I pick: the web app or Chrome?",
                 "On a phone or tablet, the web app. On a computer with Chrome or Edge, the Chrome Web Store version opens TeachersDeck or StudentDeck on every new tab and updates itself. Both use the same account and data."),
                ("Why are some apps only a live demo?",
                 "CampusDeck and the ParentDeck family view are in early preview. Try the live demo with pretend data, then contact us to set them up for your campus."),
                ("When can our kindergarten use KinderDeck?",
                 "KinderDeck is in early access: we set it up with each kindergarten ourselves, including moving the school's spreadsheets into the app. TinyTeachersDeck and TinyParentDeck are in beta: download them below. Book a demo and we'll show you around."),
                ("Who needs the .zip?",
                 "Schools that manage Chrome by hand, or computers that can't reach the Chrome Web Store. The .zip does everything the store version does, but doesn't update itself.")],
        "band_h": "Need help setting up?", "band_p": "Tell us about your class or school and we'll help you choose and set up the right apps.",
        "band": [("Email us", CONTACT["email"]), ("Message on Zalo", CONTACT["zalo"]), ("Book a demo", CONTACT["demo"])],
        "redirect": "Opening", "tap": "Tap here if it doesn't open",
    },
    "vi": {
        "title": "Tải ứng dụng — TeachersDeck Suite",
        "description": "Mọi ứng dụng của TeachersDeck Suite và cách tốt nhất để dùng trên thiết bị của bạn: ứng dụng web cho điện thoại và máy tính bảng, "
                       "Chrome Web Store, tệp .zip, bản demo trực tuyến, phiên bản cho ClassIn, Canvas, Moodle và các ứng dụng mầm non KinderDeck.",
        "crumb": "Tải ứng dụng", "kicker": "TeachersDeck Suite", "h1": "Tải ứng dụng",
        "lede": "Tìm ứng dụng của bạn bên dưới. Nút chính là cách tốt nhất trên thiết bị bạn đang dùng; các cách khác nằm trong mục Cách khác.",
        "groups_p": {"school": "Cho trường học và trung tâm ngoại ngữ: mỗi người trong lớp một ứng dụng.",
                     "preschool": "KinderDeck, phiên bản mầm non: một ứng dụng cho văn phòng, một cho giáo viên, một cho gia đình.",
                     "uni": "UniDeck, phiên bản đại học, đang trong giai đoạn xem trước.",
                     "lms": "TeachersDeck ngay trong nền tảng trường bạn đang dùng."},
        "dev": {"mobile": "Trên điện thoại hoặc máy tính bảng, ứng dụng web là tốt nhất: mở ứng dụng rồi thêm vào Màn hình chính.",
                "chrome": "Bạn đang dùng Chrome hoặc Edge trên máy tính: TeachersDeck và StudentDeck có thể mở mỗi khi bạn mở tab mới.",
                "other": "Trên trình duyệt này, ứng dụng web là tốt nhất. TeachersDeck và StudentDeck cũng chạy được trong Chrome dưới dạng tab mới."},
        "web": "Mở ứng dụng web", "store": "Thêm vào Chrome", "demo": "Dùng thử bản demo", "setup": "Cách cài đặt", "book": "Đặt lịch demo", "contact": "Liên hệ",
        "status": {"preview": "Truy cập sớm", "beta": "Bản beta", "soon": "Sắp ra mắt"},
        "hs": "Sau đó thêm vào Màn hình chính",
        "more": "Cách khác",
        "way": {"web": "Ứng dụng web, trên mọi thiết bị", "store": "Chrome Web Store, tự cập nhật", "zip": "Tệp .zip cho Chrome",
                "zip_how": "cách cài", "demo": "Bản demo, dữ liệu mẫu, không cần đăng nhập", "setup": "Hướng dẫn cài đặt", "page": "Giới thiệu"},
        "install_h": "Cách cài đặt", "install_p": "Ba cách để ứng dụng luôn trong tầm tay.",
        "hs_h": "Thêm ứng dụng web vào Màn hình chính",
        "hs_steps": [("iPhone và iPad", "Mở ứng dụng web trong Safari, chạm <b>Chia sẻ</b>, rồi <b>Thêm vào MH chính</b>."),
                     ("Android", "Mở ứng dụng web trong Chrome, chạm menu <b>⋮</b>, rồi <b>Thêm vào màn hình chính</b> hoặc <b>Cài đặt ứng dụng</b>."),
                     ("Máy tính", "Trong Chrome hoặc Edge, bấm biểu tượng cài đặt ở cuối thanh địa chỉ, hoặc mở menu và chọn <b>Cài đặt</b>.")],
        "zip_h": "Cài tệp .zip vào Chrome",
        "zip_steps": ["Giải nén vào một thư mục bạn sẽ giữ lại, ví dụ Documents. Chrome đọc thư mục đó mỗi lần mở, nên đừng di chuyển hay xóa nó.",
                      "Trong Chrome, mở <code>chrome://extensions</code> và bật <b>Chế độ dành cho nhà phát triển</b> (Developer mode, góc trên bên phải).",
                      "Bấm <b>Tải tiện ích đã giải nén</b> (Load unpacked) và chọn thư mục có tệp <code>manifest.json</code>.",
                      "Mở một tab mới. Mỗi hồ sơ Chrome chỉ dùng một ứng dụng, vì mỗi ứng dụng trở thành trang tab mới."],
        "zip_note": "Khi cài từ tệp .zip, mọi tính năng đều hoạt động, kể cả đăng nhập và lớp học trực tuyến; Chrome sẽ hỏi một lần để cho phép "
                    "mở cửa sổ đăng nhập Google. Ứng dụng không tự cập nhật: hãy tải phiên bản mới khi có.",
        "faq_h": "Câu hỏi về cài đặt",
        "faq": [("Tôi có cần cài đặt gì không?",
                 "Không. Mọi ứng dụng có bản web đều mở được trong trình duyệt trên điện thoại, máy tính bảng hay máy tính. Trên Chrome, TeachersDeck và StudentDeck còn có thể làm trang tab mới."),
                ("Nên chọn ứng dụng web hay Chrome?",
                 "Trên điện thoại hoặc máy tính bảng, hãy chọn ứng dụng web. Trên máy tính có Chrome hoặc Edge, bản Chrome Web Store mở TeachersDeck hoặc StudentDeck mỗi khi mở tab mới và tự cập nhật. Cả hai dùng chung tài khoản và dữ liệu."),
                ("Vì sao một số ứng dụng chỉ có bản demo?",
                 "CampusDeck và ParentDeck cho gia đình đang trong giai đoạn xem trước. Hãy dùng thử bản demo với dữ liệu mẫu, rồi liên hệ chúng tôi để thiết lập cho cơ sở của bạn."),
                ("Khi nào trường mầm non của tôi dùng được KinderDeck?",
                 "KinderDeck đang trong giai đoạn truy cập sớm: chúng tôi tự thiết lập cho từng trường, kể cả chuyển các bảng tính của trường vào ứng dụng. TinyTeachersDeck và TinyParentDeck đang ở bản beta: tải về ở bên dưới. Hãy đặt lịch demo để chúng tôi giới thiệu."),
                ("Ai cần tệp .zip?",
                 "Các trường tự quản lý Chrome, hoặc máy tính không vào được Chrome Web Store. Tệp .zip làm được mọi thứ như bản trên cửa hàng, nhưng không tự cập nhật.")],
        "band_h": "Cần hỗ trợ cài đặt?", "band_p": "Hãy cho chúng tôi biết về lớp hoặc trường của bạn, chúng tôi sẽ giúp chọn và cài đặt ứng dụng phù hợp.",
        "band": [("Gửi email", CONTACT["email"]), ("Nhắn qua Zalo", CONTACT["zalo"]), ("Đặt lịch demo", CONTACT["demo"])],
        "redirect": "Đang mở", "tap": "Chạm vào đây nếu trang không tự mở",
    },
}

# Sets <html data-dev> before the rows render, so the right button shows without a flash. No storage, no tracking.
DETECT = ("<script>(function(){var n=navigator,u=n.userAgent||'',d=n.userAgentData,"
          "p=/iPhone|iPod|Android.+Mobile|Windows Phone/i.test(u)||!!(d&&d.mobile),"
          "t=!p&&(/iPad|Android|Tablet|Silk|Kindle/i.test(u)||(/Macintosh/.test(u)&&n.maxTouchPoints>1)),"
          "c=d&&d.brands?d.brands.some(function(b){return/Chromium|Google Chrome|Microsoft Edge/.test(b.brand)}):/Chrome\\/|Edg\\//.test(u)&&!/OPR\\/|SamsungBrowser/.test(u),"
          "r=document.documentElement;r.setAttribute('data-dev',p||t?'mobile':c?'chrome':'other');"
          "r.setAttribute('data-dev-group',p?'phone':t?'tablet':'computer')})()</script>")


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def latest_zip(prefix):
    """(version, file name, size in bytes) of the newest downloads/<prefix>-v<x.y.z>….zip, or None."""
    found = []
    for f in DL.glob(f"{prefix}-v*.zip"):
        m = re.match(rf"{re.escape(prefix)}-v(\d+)\.(\d+)\.(\d+)", f.name)
        if m:
            found.append((tuple(int(x) for x in m.groups()), f))
    if not found:
        return None
    v, f = max(found)
    return ".".join(map(str, v)), f.name, f.stat().st_size


def kb(n):
    return f"{round(n / 1024):,} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def main_way(app, dev):
    """The one main way in for an app on a device group: 'setup', 'store', 'web', 'demo', or 'book' (a demo with us) when there is nothing to open."""
    if app.get("setup"):
        return "setup"
    order = {"mobile": ["web"], "chrome": ["store", "web"], "other": ["web"]}[dev]
    return next((w for w in order if app.get(w)), "demo" if app.get("demo") else "book")


def href(lang, app, way):
    if way in ("setup", "page"):
        return url(lang, "") + app[way].lstrip("/")
    if way == "book":
        return CONTACT["demo"]
    if way == "store":
        return app["store"] + ("?hl=vi" if lang == "vi" else "")
    return app[way]


def ext(way):
    """Attributes for a link that leaves the site; the demo opens in its own window like everywhere else (site.js)."""
    return ' target="_blank" rel="noopener"' if way in ("web", "store", "demo") else ""


def row(lang, app, tint):
    t = T[lang]
    pick = {}
    for dev in DEVICES:
        pick.setdefault(main_way(app, dev), []).append(dev)
    go = []
    for way, devs in pick.items():
        demo = f' data-demo-window="{esc(app["demoWindow"])}"' if way == "demo" else ""
        arrow = " ↗" if ext(way) else ""
        go.append(f'<a class="btn primary" data-for="{" ".join(devs)}" data-way="{way}" href="{esc(href(lang, app, way))}"{ext(way)}{demo}>{esc(t[way])}{arrow}</a>')
        if way in ("demo", "book"):
            go.append(f'<a class="btn" data-for="{" ".join(devs)}" data-way="contact" href="{CONTACT["email"]}">{esc(t["contact"])}</a>')
        if way == "web" and "mobile" in devs:
            go.append(f'<a class="ga-hs" data-for="mobile" href="#home-screen">{esc(t["hs"])}</a>')

    w = t["way"]
    ways = []
    if app.get("web"):
        host = app["web"].split("//")[1].rstrip("/")
        ways.append(f'<li><a data-way="web" href="{esc(app["web"])}"{ext("web")}>{esc(w["web"])}</a> <small>{esc(host)}</small></li>')
    if app.get("store"):
        ways.append(f'<li><a data-way="store" href="{esc(href(lang, app, "store"))}"{ext("store")}>{esc(w["store"])}</a></li>')
    z = app.get("zip") and latest_zip(app["zip"])
    if z:
        ver, name, size = z
        ways.append(f'<li><a data-way="zip" href="{ZIP_URL}{esc(name)}" download>{esc(w["zip"])}</a> '
                    f'<small>v{ver}{" beta" if "-beta" in name else ""} · {kb(size)} · <a href="#zip">{esc(w["zip_how"])}</a></small></li>')
    if app.get("demo"):
        ways.append(f'<li><a data-way="demo" href="{esc(app["demo"])}"{ext("demo")} data-demo-window="{esc(app["demoWindow"])}">{esc(w["demo"])}</a></li>')
    if app.get("setup"):
        ways.append(f'<li><a data-way="setup" href="{esc(href(lang, app, "setup"))}">{esc(w["setup"])}</a></li>')
    if app.get("page"):
        ways.append(f'<li><a data-way="page" href="{esc(href(lang, app, "page"))}">{esc(w["page"])} {esc(app["name"])}</a></li>')

    tag = f' <span class="ga-tag">{esc(t["status"][app["status"]])}</span>' if app.get("status") else ""
    initial = "".join(c for c in app["name"].replace("for ", "") if c.isupper())[:2]
    return (f'<article class="ga-row" id="{app["id"]}" data-app="{app["id"]}" style="--tint:var(--{tint});--on-tint:var(--on-{tint})">'
            f'<div class="ga-id"><span class="ga-ic" aria-hidden="true">{esc(initial)}</span><div><h3>{esc(app["name"])}{tag}</h3>'
            f'<p><b>{esc(app["for"][lang])}</b> · {esc(app["line"][lang])}</p></div></div>'
            f'<div class="ga-go">{"".join(go)}</div>'
            f'<details class="ga-more"><summary>{esc(t["more"])}</summary><ul>{"".join(ways)}</ul></details></article>')


def build(lang, data):
    t, ui = T[lang], UI[lang]
    header, footer, _, _, tail = shell(lang)
    header = fix_header(header, lang, SLUG)
    here, home = url(lang, SLUG), url(lang, "")
    graph = [
        {"@type": "WebPage", "@id": here + "#page", "url": here, "name": t["title"], "description": t["description"],
         "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#site"}, "about": {"@id": f"{SITE}/#org"}, "breadcrumb": {"@id": here + "#crumbs"}},
        {"@type": "BreadcrumbList", "@id": here + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": here}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    jump = "".join(f'<a class="btn" href="#{g["id"]}">{esc(g[lang])}</a>' for g in data["groups"])
    devnote = "".join(f'<p class="ga-dev" data-for="{d}">{esc(t["dev"][d])}</p>' for d in DEVICES)
    groups = []
    for g in data["groups"]:
        apps = [a for a in data["apps"] if a["group"] == g["id"]]
        rows = "".join(row(lang, a, TINTS[i % 4]) for i, a in enumerate(apps))
        groups.append(f'<section id="{g["id"]}"><div class="wrap"><div class="head"><h2>{esc(g[lang])}</h2>'
                      f'<p>{esc(t["groups_p"][g["id"]])}</p></div><div class="ga-list">{rows}</div></div></section>')

    hs = "".join(f"<li><b>{esc(k)}</b> {v}</li>" for k, v in t["hs_steps"])
    zs = "".join(f"<li>{s}</li>" for s in t["zip_steps"])
    install = (f'<section id="install"><div class="wrap"><div class="head"><h2>{esc(t["install_h"])}</h2><p>{esc(t["install_p"])}</p></div>'
               f'<div class="faq"><details id="home-screen"><summary>{esc(t["hs_h"])}</summary><ul class="ga-steps">{hs}</ul></details>'
               f'<details id="zip"><summary>{esc(t["zip_h"])}</summary><ol class="ga-steps">{zs}</ol><p>{t["zip_note"]}</p></details></div>'
               f'</div></section>')
    faq = (f'<section id="faq"><div class="wrap"><div class="head"><h2>{esc(t["faq_h"])}</h2></div><div class="faq">' +
           "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"]) + "</div></div></section>")
    band = (f'<section id="next"><div class="wrap"><div class="cta-band"><div><h2>{esc(t["band_h"])}</h2><p>{esc(t["band_p"])}</p></div>'
            f'<div class="cta">' + "".join(f'<a class="btn{" alt" if i else ""}" href="{h}">{esc(x)}</a>' for i, (x, h) in enumerate(t["band"])) +
            "</div></div></div></section>")
    tail = tail.replace("</body>", '<script src="/assets/hub.js?v=1" defer></script>\n</body>')

    doc = f"""{head(lang, SLUG, t["title"], t["description"], ld)}<body>
{header}
<main id="top">
{DETECT}
<div class="wrap hero inner ga-hero">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">{esc(ui["home"])}</a> › <span aria-current="page">{esc(t["crumb"])}</span></nav>
<p class="kicker">{esc(t["kicker"])}</p>
<h1>{esc(t["h1"])}</h1>
<p class="lede">{esc(t["lede"])}</p>
{devnote}
<div class="cta ga-jump">{jump}</div>
</div>
{chr(10).join(groups)}
{install}
{faq}
{band}
</main>
{footer}
{tail}
</html>
"""
    out = ROOT / (f"vi/{SLUG}" if lang == "vi" else SLUG) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8", newline="\n")
    return out


def redirect(path, to, label):
    """A forwarding page like /try/ and /order/: a short address that is easy to say out loud."""
    t = T["en"]
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(label)} — TeachersDeck Suite</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{to}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}"+location.hash)</script>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#F3F5FC;color:#161C25;font:16px/1.6 system-ui,sans-serif;text-align:center;padding:16px;box-sizing:border-box}}a{{color:#4A55B8}}</style>
</head>
<body>
<p>{t["redirect"]} {esc(label)}… <a href="{to}">{t["tap"]}</a></p>
</body>
</html>
"""
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8", newline="\n")
    return out


def public_list(data):
    """/apps/apps.json: the list as AgentDeck and HQ read it, with absolute links and the latest .zip filled in."""
    apps = []
    for a in data["apps"]:
        x = {k: v for k, v in a.items() if k not in ("zip", "demoWindow")}
        for k in ("setup", "page"):
            if a.get(k):
                x[k] = f"{SITE}/{a[k]}"
        z = a.get("zip") and latest_zip(a["zip"])
        if z:
            x["zip"] = {"version": z[0], "url": f"{ZIP_URL}{z[1]}", "bytes": z[2]}
        if a.get("short"):
            x["short"] = f"{SITE}/{a['short']}/"
        x["hub"] = f"{SITE}/apps/#{a['id']}"
        apps.append(x)
    out = ROOT / SLUG / "apps.json"
    out.write_text(json.dumps({"groups": data["groups"], "apps": apps}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return out


def check(data):
    """Asks every web app address whether it answers; returns the ones that don't."""
    bad = []
    for a in data["apps"]:
        if a.get("web"):
            try:
                with urllib.request.urlopen(urllib.request.Request(a["web"], method="HEAD"), timeout=15) as r:
                    ok = r.status < 400
            except Exception:  # noqa: BLE001 - any failure means the button would lead nowhere
                ok = False
            print(("answers   " if ok else "NO ANSWER ") + a["web"])
            if not ok:
                bad.append(a["web"])
    return bad


def main(argv):
    data = load()
    written = [build(lang, data) for lang in ("en", "vi")]
    written.append(redirect("get", f"{SITE}/apps/", "Get the apps"))
    for a in data["apps"]:
        if a.get("short") and a.get("web"):
            written.append(redirect(a["short"], a["web"], a["name"]))
    written.append(public_list(data))
    for f in written:
        print("wrote", f.relative_to(ROOT).as_posix())
    if "--check" in argv and check(data):
        print("Some web app addresses don't answer: take their \"web\" out of _build/apps.json until they do.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
