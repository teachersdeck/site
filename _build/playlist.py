"""Keeps the home page video list in step with the TeachersDeck YouTube playlist.

The "See the suite in action" player on both home pages (index.html, vi/index.html) shows a different video from
the playlist on each visit, in a shuffled order kept in the visitor's browser (the inline script after the iframe).
The list it picks from is the data-videos attribute on <div class="vid">: a JSON list of [video id, title].

This reads the playlist's public feed (no API key; the feed lists up to 15 videos, newest first in the
playlist's own order) and rewrites that attribute when the playlist changed.

Run from the repository root:  python _build/playlist.py  [path-or-url of the feed]
Prints what changed; changes nothing when the list is already current.
.github/workflows/versions.yml runs it every hour with versions.py and commits any change.
"""
import html, json, pathlib, re, sys, urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAYLIST = "PLKHFg_wJdC-k"
SOURCE = f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST}"
PAGES = ["index.html", "vi/index.html"]
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
ATTR = re.compile(r"(<div class=\"vid\" data-list=\"" + PLAYLIST + r"\" data-videos=')[^']*(')")


def load(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (site build)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    return pathlib.Path(src).read_bytes()


def videos(src):
    root = ET.fromstring(load(src))
    out = []
    for e in root.findall("a:entry", NS):
        vid = (e.findtext("yt:videoId", "", NS) or "").strip()
        title = (e.findtext("a:title", "", NS) or "").strip()
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) and vid not in (v for v, _ in out):
            out.append([vid, title])
    return out


def main(src):
    vids = videos(src)
    if len(vids) < 2:   # a failed or empty feed must never empty the player
        sys.exit(f"playlist: {src} gave {len(vids)} video(s); leaving the pages as they are")
    value = html.escape(json.dumps(vids, ensure_ascii=False, separators=(",", ":")), quote=True)
    for page in PAGES:
        path = ROOT / page
        text = path.read_text(encoding="utf-8")
        if not ATTR.search(text):
            sys.exit(f"playlist: no <div class=\"vid\" data-list=\"{PLAYLIST}\" data-videos='…'> in {page}")
        new = ATTR.sub(lambda m: m.group(1) + value + m.group(2), text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(f"{page}: {len(vids)} videos")
    print("playlist: done")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SOURCE)
