"""Which copy of TeachersDeck's server functions the apps use: Google's Cloud Functions or the lights-on server.

backend.json (served at https://myteachersdeck.com/backend.json) is read by every app (js/backend.js), HQ's web app,
the website chat (assets/agentdeck.js) and the timed jobs on both servers. Readers use "functions" and "agentChat";
"active" names the side those came from, and "sides" holds both sides' addresses so switching is one command:

    python _build/backend.py                 # show the active side and both sides' health
    python _build/backend.py google          # switch to Google  (then commit and push; live within ~10 minutes)
    python _build/backend.py render          # switch to the lights-on server on Render
    python _build/backend.py watch           # what .github/workflows/backend-watch.yml runs: switch only when the
                                             # active side is down 3 times in a row and the other side is up

Both sides run the same code against the same Firestore (HQ repo docs/LIGHTS-ON.md), so switching is safe at any time.
Health = GET <side>/healthz answers 200 with "ok": true. Only the Python standard library is used.
"""
import json, pathlib, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILE = ROOT / "backend.json"
SIDES = ("google", "render")


def load():
    return json.loads(FILE.read_text(encoding="utf-8"))


def save(cfg):
    FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def healthy(side, cfg, tries=1, wait=0):
    url = cfg["sides"][side]["functions"].rstrip("/") + "/healthz"
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Cache-Control": "no-store", "User-Agent": "backend-watch"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 200 and json.loads(r.read().decode("utf-8") or "{}").get("ok") is True:
                    return True
        except Exception as e:  # noqa: BLE001 — any failure counts as down
            print(f"  {side}: try {i + 1}: {type(e).__name__}: {str(e)[:160]}")
        if i + 1 < tries:
            time.sleep(wait)
    return False


def switch(cfg, side):
    """Point the readers at one side. Returns True when something changed."""
    if side not in SIDES:
        raise SystemExit(f"Unknown side {side!r}: use one of {SIDES}")
    want = cfg["sides"][side]
    changed = cfg.get("active") != side or cfg.get("functions") != want["functions"] or cfg.get("agentChat") != want["agentChat"]
    cfg["active"], cfg["functions"], cfg["agentChat"] = side, want["functions"], want["agentChat"]
    return changed


def main(argv):
    cfg = load()
    arg = argv[0] if argv else ""
    if arg in SIDES:
        print(("Switched to " if switch(cfg, arg) else "Already on ") + arg)
        save(cfg)
        return 0
    if arg == "watch":
        active = cfg.get("active")
        other = "render" if active == "google" else "google"
        if healthy(active, cfg, tries=3, wait=60):
            print(f"{active} (active) is up. {other}: {'up' if healthy(other, cfg) else 'DOWN'}")
            return 0
        if not healthy(other, cfg, tries=2, wait=20):
            print(f"::error::Both sides are down ({active} is active). Nothing switched.")
            return 2
        switch(cfg, other)
        save(cfg)
        print(f"SWITCHED {active} -> {other}: {active} stopped answering /healthz, {other} is up.")
        return 10   # tells the workflow to commit, push and fail loudly so the owner gets GitHub's email
    print(f"active: {cfg.get('active')}")
    for s in SIDES:
        print(f"  {s}: {cfg['sides'][s]['functions']}  {'up' if healthy(s, cfg) else 'DOWN'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
