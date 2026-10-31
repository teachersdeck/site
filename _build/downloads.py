"""The home pages' Downloads section: the latest release of each app as a .zip, served from this site.

Finds the newest release of each app in teachersdeck/teachersdeck-suite (a private repository, so it runs with the
owner's signed-in GitHub CLI, `gh`), copies its zip into downloads/, removes older zips there, and rewrites
<section id="downloads"> in index.html and vi/index.html (inserted before <section id="plans"> the first time).

Run from the repository root:  python _build/downloads.py
Prints what changed. The files are small and interest is low, so GitHub Pages serves them for now; when that
changes, point URL at another host (see the note in the commit that added this) and stop copying the zips here.
"""
import datetime, json, pathlib, re, subprocess, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "teachersdeck/teachersdeck-suite"
OUT = ROOT / "downloads"
URL = "https://myteachersdeck.com/downloads/"
# (tag prefix, name, tile colour, Chrome Web Store link or None)
APPS = [
    ("teachersdeck", "TeachersDeck", "t-amber", "https://chromewebstore.google.com/detail/teachersdeck/gemkljlgmnajlmdlcgdegpegaoiahaea"),
    ("studentdeck", "StudentDeck", "t-matcha", "https://chromewebstore.google.com/detail/studentdeck/edijnonmpllfbhoblceimhfkadonebhg"),
    ("parentdeck", "ParentDeck", "t-indigo", None),
    ("admindeck", "AdminDeck", "t-coral", None),
]
T = {
    "en": {
        "h": "Downloads", "p": "The latest version of each app as a .zip, to install in Chrome by hand. Free; Pro widgets need a licence key once the beta ends.",
        "who": {"teachersdeck": "For teachers", "studentdeck": "For students", "parentdeck": "For families", "admindeck": "For school leaders"},
        "dl": "Download", "store": "Or add it from the Chrome Web Store", "date": "%d %b %Y",
        "how": "How to install a .zip",
        "steps": ["Unzip it into a folder you will keep, such as Documents. Chrome reads that folder every time, so don't move or delete it.",
                  "In Chrome, open <code>chrome://extensions</code> and turn on <b>Developer mode</b> (top right).",
                  "Click <b>Load unpacked</b> and choose the folder that holds <code>manifest.json</code>.",
                  "Open a new tab. One app per Chrome profile: each one becomes the new-tab page."],
        "note": "Everything works when installed from a .zip, including signing in and cloud classes; Chrome asks once for permission to show the Google sign-in window. The app doesn't update itself: download the new version when there is one. Questions? <a href=\"mailto:jerry@myteachersdeck.com\">Ask us</a>.",
    },
    "vi": {
        "h": "Tải về", "p": "Phiên bản mới nhất của từng ứng dụng dưới dạng tệp .zip, để tự cài vào Chrome. Miễn phí; các widget Pro cần khóa bản quyền khi giai đoạn beta kết thúc.",
        "who": {"teachersdeck": "Cho giáo viên", "studentdeck": "Cho học sinh", "parentdeck": "Cho phụ huynh", "admindeck": "Cho ban giám hiệu"},
        "dl": "Tải về", "store": "Hoặc thêm từ Chrome Web Store", "date": "%d/%m/%Y",
        "how": "Cách cài tệp .zip",
        "steps": ["Giải nén vào một thư mục bạn sẽ giữ lại, ví dụ Documents. Chrome đọc thư mục đó mỗi lần mở, nên đừng di chuyển hay xóa nó.",
                  "Trong Chrome, mở <code>chrome://extensions</code> và bật <b>Chế độ dành cho nhà phát triển</b> (Developer mode, góc trên bên phải).",
                  "Bấm <b>Tải tiện ích đã giải nén</b> (Load unpacked) và chọn thư mục có tệp <code>manifest.json</code>.",
                  "Mở một tab mới. Mỗi hồ sơ Chrome chỉ dùng một ứng dụng, vì mỗi ứng dụng trở thành trang tab mới."],
        "note": "Khi cài từ tệp .zip, mọi tính năng đều hoạt động, kể cả đăng nhập và lớp học trực tuyến; Chrome sẽ hỏi một lần để cho phép mở cửa sổ đăng nhập Google. Ứng dụng không tự cập nhật: hãy tải phiên bản mới khi có. Cần hỗ trợ? <a href=\"mailto:jerry@myteachersdeck.com\">Liên hệ chúng tôi</a>.",
    },
}


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def latest(prefix):
    """The newest release of one app: (version, zip name, size in bytes, date)."""
    rows = json.loads(gh("release", "list", "-R", REPO, "--limit", "200", "--json", "tagName,publishedAt"))
    tags = [r for r in rows if re.fullmatch(rf"{prefix}-v\d+\.\d+\.\d+", r["tagName"])]
    tag = max(tags, key=lambda r: tuple(int(x) for x in r["tagName"].split("-v")[1].split(".")))
    assets = json.loads(gh("release", "view", tag["tagName"], "-R", REPO, "--json", "assets"))["assets"]
    z = next(a for a in assets if a["name"].endswith(".zip") and "obfuscated" not in a["name"])
    return tag["tagName"].split("-v")[1], z["name"], z["size"], tag["publishedAt"][:10]


def public_copy(src, dest):
    """The release zip without its developer files: Markdown notes and scopes, build tools and tests stay private.
    Everything the app loads (index.html, js, css, icons, games, AdminDeck's shared functions, LICENSE, BUILD) stays."""
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            rest = item.filename.split("/", 1)[1] if "/" in item.filename else item.filename
            if rest.lower().endswith(".md") or rest.startswith("tools/") or "/tools/" in rest:
                continue
            zout.writestr(item, zin.read(item.filename))


def kb(n):
    return f"{round(n / 1024):,} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def section(lang, rows):
    t = T[lang]
    tiles = []
    for (prefix, name, cls, store), (ver, file, size, date) in rows:
        d = datetime.date.fromisoformat(date).strftime(t["date"]).lstrip("0")
        extra = f'<a class="dl-store" href="{store}{"?hl=vi" if lang == "vi" else ""}" target="_blank" rel="noopener">{t["store"]} ↗</a>' if store else ""
        tiles.append(f'<div class="tile {cls}"><h3>{name}</h3><p class="dl-who">{t["who"][prefix]}</p>'
                     f'<p class="dl-meta">v{ver} beta · {kb(size)} · {d}</p>'
                     f'<a class="btn" href="{URL}{file}" download>{t["dl"]} .zip</a>{extra}</div>')
    steps = "".join(f"<li>{s}</li>" for s in t["steps"])
    return (f'<section id="downloads"><div class="wrap">\n<div class="head"><h2>{t["h"]}</h2><p>{t["p"]}</p></div>\n'
            f'<div class="tiles n4">{"".join(tiles)}</div>\n'
            f'<details class="dl-how"><summary>{t["how"]}</summary><ol>{steps}</ol><p>{t["note"]}</p></details>\n'
            f'</div></section>\n\n')


def main():
    found = [(app, latest(app[0])) for app in APPS]
    OUT.mkdir(exist_ok=True)
    keep = {r[1][1] for r in found}
    for (prefix, *_), (ver, file, size, date) in found:
        if not (OUT / file).exists():
            with tempfile.TemporaryDirectory() as tmp:
                gh("release", "download", f"{prefix}-v{ver}", "-R", REPO, "-p", file, "-D", tmp)
                public_copy(pathlib.Path(tmp) / file, OUT / file)
            print("downloaded", file)
    # Sizes shown on the page are the public copies'.
    rows = [(app, (ver, file, (OUT / file).stat().st_size, date)) for app, (ver, file, size, date) in found]
    for old in OUT.glob("*.zip"):
        if old.name not in keep:
            old.unlink()
            print("removed", old.name)
    for lang, f in (("en", "index.html"), ("vi", "vi/index.html")):
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        new = section(lang, rows)
        if '<section id="downloads">' in s:
            s2 = re.sub(r'<section id="downloads">.*?</section>\n\n', lambda m: new, s, flags=re.S)
        else:
            i = s.index('<section id="plans"')
            s2 = s[:i] + new + s[i:]
        if s2 != s:
            p.write_text(s2, encoding="utf-8", newline="\n")
            print("updated", f)


if __name__ == "__main__":
    sys.exit(main())
