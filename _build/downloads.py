"""The latest release of each app as a .zip, served from this site and listed on Get the apps (/apps/).

Finds the newest release of each app with a "zip" in _build/apps.json, in the app's "repo" (default
teachersdeck/teachersdeck-suite; the KinderDeck apps are in teachersdeck/kinderdeck-suite; both private, so it runs with
the owner's signed-in GitHub CLI, `gh`), copies a public copy of its zip into downloads/,
removes older zips there, then rebuilds the hub (_build/hub.py), which reads the version and size from the file name.

Run from the repository root:  python _build/downloads.py
Prints what changed. The files are small and interest is low, so GitHub Pages serves them for now; when that
changes, point ZIP_URL in _build/hub.py at another host (phase 3 of the Get the apps plan: a public teachersdeck/downloads repository)
and stop copying the zips here.
"""
import json, pathlib, re, subprocess, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "teachersdeck/teachersdeck-suite"
OUT = ROOT / "downloads"
# (tag prefix, repository) of the apps that have a .zip, from the one list of apps.
APPS = [(a["zip"], a.get("repo", REPO)) for a in json.loads((ROOT / "_build" / "apps.json").read_text(encoding="utf-8"))["apps"] if a.get("zip")]


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def latest(prefix, repo=REPO):
    """The newest release of one app: (version, zip name, size in bytes, date)."""
    rows = json.loads(gh("release", "list", "-R", repo, "--limit", "200", "--json", "tagName,publishedAt"))
    tags = [r for r in rows if re.fullmatch(rf"{prefix}-v\d+\.\d+\.\d+", r["tagName"])]
    tag = max(tags, key=lambda r: tuple(int(x) for x in r["tagName"].split("-v")[1].split(".")))
    assets = json.loads(gh("release", "view", tag["tagName"], "-R", repo, "--json", "assets"))["assets"]
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


def main():
    found = [(prefix, repo, latest(prefix, repo)) for prefix, repo in APPS]
    OUT.mkdir(exist_ok=True)
    keep = {r[2][1] for r in found}
    for prefix, repo, (ver, file, size, date) in found:
        if not (OUT / file).exists():
            with tempfile.TemporaryDirectory() as tmp:
                gh("release", "download", f"{prefix}-v{ver}", "-R", repo, "-p", file, "-D", tmp)
                public_copy(pathlib.Path(tmp) / file, OUT / file)
            print("downloaded", file)
    for old in OUT.glob("*.zip"):
        if old.name not in keep:
            old.unlink()
            print("removed", old.name)
    subprocess.run([sys.executable, str(ROOT / "_build" / "hub.py")], check=True, cwd=ROOT)

if __name__ == "__main__":
    sys.exit(main())
