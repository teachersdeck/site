"""Keeps every version number on the site in step with development.

Reads https://teachersdeck.github.io/demo/versions.json, which the suite's demo-site workflow publishes
on every push to main that touches an app (and after every release), and uses its "development"
versions: the ones on main, which the live demos run. It updates:
  - the "Current versions" line in the footer of both home pages (index.html, vi/index.html),
  - the beta note in both home heroes ("currently in beta (v…)", TeachersDeck's version),
  - the "Actively built: TeachersDeck v…" line in the home proof strip,
  - each app page's softwareVersion in _build/apps.py,
then rebuilds the inner pages with pages.py so their footers and structured data match.

Run from the repository root:  python _build/versions.py  [path-or-url of versions.json]
Prints what changed; changes nothing when the numbers are already current.
.github/workflows/versions.yml runs it every hour and commits any change; a push to the suite's main
reaches the site within about an hour.
"""
import json, pathlib, re, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = "https://teachersdeck.github.io/demo/versions.json"
APPS = [("teachersdeck", "TeachersDeck"), ("studentdeck", "StudentDeck"), ("parentdeck", "ParentDeck"), ("admindeck", "AdminDeck")]
FOOTER = re.compile(r'(<span data-i="f_note">[^<]*</span>: )[^<]*(</span>)')
STRIP = re.compile(r'(<span class="ps-ver">TeachersDeck v)\d+\.\d+\.\d+(</span>)')
BETA = re.compile(r'(<p class="beta" data-i="beta">[^<]*\(v)\d+\.\d+\.\d+(\))')


def load(src):
    if re.match(r"https?://", src):
        with urllib.request.urlopen(src, timeout=30) as r:
            return json.load(r)
    return json.loads(pathlib.Path(src).read_text(encoding="utf-8"))


def main(src):
    data = load(src)
    apps = data.get("development") or data["apps"]   # development versions; releases if an older file has none
    for slug, _ in APPS:
        if not re.fullmatch(r"\d+\.\d+\.\d+", apps.get(slug, {}).get("version", "")):
            sys.exit(f"versions: {src} has no usable version for {slug}")
    line = " · ".join(f"{name} {apps[slug]['label']}" for slug, name in APPS)
    changed = []

    for rel in ("index.html", "vi/index.html"):
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        new, n = FOOTER.subn(lambda m: m.group(1) + line + m.group(2), s)
        if n != 1:
            sys.exit(f"versions: expected one footer version line in {rel}, found {n}")
        new, n = BETA.subn(lambda m: m.group(1) + apps["teachersdeck"]["version"] + m.group(2), new)
        if n != 1:
            sys.exit(f"versions: expected one beta note with a version in {rel}, found {n}")
        new, n = STRIP.subn(lambda m: m.group(1) + apps["teachersdeck"]["version"] + m.group(2), new)
        if n != 1:
            sys.exit(f"versions: expected one proof-strip version in {rel}, found {n}")
        if new != s:
            p.write_text(new, encoding="utf-8")
            changed.append(rel)

    p = ROOT / "_build" / "apps.py"
    s = new = p.read_text(encoding="utf-8")
    for slug, name in APPS:
        new, n = re.subn(r'("app": \{"name": "' + name + r'", "version": ")[^"]*(")', lambda m: m.group(1) + apps[slug]["version"] + m.group(2), new)
        if n != 1:
            sys.exit(f"versions: expected one app entry for {name} in _build/apps.py, found {n}")
    new = re.sub(r"versions \(TeachersDeck [^)]*\)", "versions (" + ", ".join(f"{name} {apps[slug]['version']}" for slug, name in APPS) + ")", new, count=1)
    if new != s:
        p.write_text(new, encoding="utf-8")
        changed.append("_build/apps.py")

    if not changed:
        print("versions: already current (" + line + ")")
        return
    subprocess.run([sys.executable, str(ROOT / "_build" / "pages.py")], check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    print("versions: updated to " + line + " in " + ", ".join(changed) + ", inner pages rebuilt")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SOURCE)
