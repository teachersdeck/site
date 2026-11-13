"""Translates new or changed English blog posts into Vietnamese, for /vi/blog/ (see _build/blog.py).

For every English post in the Blogger feed that has no Vietnamese version yet, or whose English text changed since it
was translated, this asks a language model (through OpenRouter) for a Vietnamese version and saves it as
_build/blog-vi/YYYY-MM-<slug>.html. blog.py then publishes it at /vi/blog/YYYY/MM/<slug>/.

A translation is only saved if it keeps the post's HTML exactly (same tags in the same order, same links and pictures)
and is really in Vietnamese; otherwise the post is tried again on the next run. A file marked "keep: yes" is never
replaced, so a translation corrected by hand stays as it is.

Needs OPENROUTER_API_KEY (a repository secret). Without it nothing changes and the run only warns.
BLOG_TRANSLATE_MODEL (a repository variable) picks the model; the default is OpenRouter's free router.

Run from the repository root:  python _build/blog_translate.py  [path-or-url of the feed JSON]
.github/workflows/versions.yml runs it every hour, just before blog.py.
"""
import datetime, json, os, pathlib, re, sys, time, urllib.error, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import blog  # noqa: E402

API = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.environ.get("BLOG_TRANSLATE_MODEL") or "openrouter/free"
PER_RUN = 3   # at most this many posts per run, so one run can't cost much

SYSTEM = """You translate blog posts from English into Vietnamese for TeachersDeck, a set of classroom apps made by Jerry,
an American teacher in Ho Chi Minh City. Readers are Vietnamese teachers, school leaders and parents.

Write natural, warm, everyday Vietnamese, as a Vietnamese teacher would write it, not a word-for-word translation.
Keep Jerry's first-person voice ("tôi") and address the reader as "bạn".
Keep these names exactly as they are: TeachersDeck, StudentDeck, ParentDeck, AdminDeck, LectureDeck, UniDeck,
UniStudentDeck, UniParentDeck, KinderDeck, AgentDeck, Deckie, ClassIn, Canvas, Moodle, Claude, Google, YouTube, Jerry.
Write "Saigon" as "Sài Gòn".

The post is HTML. Translate only the human-readable text. Keep every tag and every attribute exactly as it is, in the
same order: do not add, remove, merge or reorder tags, and do not change any href, src, class or other attribute.

Answer in exactly this form and nothing else (no code fences, no notes):
TITLE: <the Vietnamese title>
---
<the translated HTML>"""


def ask(title, body, key):
    req = urllib.request.Request(API, method="POST", data=json.dumps({
        "model": MODEL, "temperature": 0.2, "max_tokens": 16000, "reasoning": {"exclude": True},
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": f"TITLE: {title}\n---\n{body}"}],
    }).encode("utf-8"), headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://myteachersdeck.com", "X-Title": "TeachersDeck blog translation",
    })
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    if data.get("error"):
        raise RuntimeError(data["error"].get("message") or data["error"])
    return data["choices"][0]["message"]["content"] or "", data.get("model", MODEL)


def parse(text):
    text = re.sub(r"^\s*```[a-z]*\s*|\s*```\s*$", "", text.strip())
    m = re.match(r"\s*TITLE:\s*(.+?)\s*\n\s*-{3,}\s*\n(.*)$", text, re.S)
    if not m:
        raise ValueError("the answer is not in the TITLE / --- / HTML form")
    return m.group(1).strip(), m.group(2).strip()


def tags(h):
    return re.findall(r"<\s*(/?[a-zA-Z][a-zA-Z0-9]*)", h)


def links(h):
    return sorted(re.findall(r'\b(?:href|src)="([^"]*)"', h))


def check(src, title, out):
    if tags(src) != tags(out):
        raise ValueError("the HTML tags changed")
    if links(src) != links(out):
        raise ValueError("a link or picture address changed")
    if blog.language(title, out, []) != "vi":
        raise ValueError("the answer does not look Vietnamese")


def save(p, title, body, model):
    blog.TRANSLATIONS.mkdir(parents=True, exist_ok=True)
    f = blog.translation_file(p)
    head = [f"<!-- title: {title.replace('--', '–')} -->", f"<!-- source: {p['blogger']} -->",
            f"<!-- source-hash: {blog.source_hash(p)} -->",
            f"<!-- translated-by: {model}, {datetime.date.today().isoformat()} -->", "<!-- keep: no -->"]
    f.write_text("\n".join(head) + "\n" + body + "\n", encoding="utf-8", newline="\n")
    print("wrote", f.relative_to(blog.ROOT).as_posix())


def todo(all_posts):
    vi_paths = {p["path"] for p in all_posts if p["lang"] == "vi"}
    out = []
    for p in all_posts:
        if p["lang"] != "en" or p["path"] in vi_paths:
            continue
        f = blog.translation_file(p)
        if f.exists():
            meta, _ = blog.read_translation(f)
            if meta.get("keep", "").lower() == "yes" or meta.get("source-hash") == blog.source_hash(p):
                continue
        out.append(p)
    return out


def main(src):
    try:
        posts = todo(blog.posts(src))
    except Exception as e:  # noqa: BLE001 - a feed problem changes nothing
        sys.exit(f"blog_translate: could not read {src}: {e}")
    if not posts:
        print("blog_translate: every English post has its Vietnamese version")
        return
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        print(f"::warning::{len(posts)} blog post(s) wait for a Vietnamese translation: OPENROUTER_API_KEY is not set")
        return
    failed = 0
    for p in posts[:PER_RUN]:
        for attempt in range(3):
            try:
                answer, model = ask(p["title"], p["html"], key)
                title, body = parse(answer)
                check(p["html"], title, body)
                save(p, title, body, model)
                break
            except (urllib.error.URLError, RuntimeError, ValueError, KeyError, TimeoutError) as e:
                print(f"blog_translate: {p['path']} attempt {attempt + 1}: {e}")
                time.sleep(5 * (attempt + 1))
        else:
            failed += 1
            print(f"::warning::Could not translate {p['path']} this time; it will be tried again next run")
    if failed == len(posts[:PER_RUN]):
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else blog.SOURCE)
