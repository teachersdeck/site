"""Universities page extras: a UniDeck live tour (one preview, four app tabs) and a multi-faculty cost calculator.
Both run in assets/uni.js; prices mirror the tables in universities.py (Pricing Sheet v2)."""
import html, json

e = lambda s: html.escape(s, quote=True)  # noqa: E731
D = "https://teachersdeck.github.io/demo/unideck/"
APPS = [("lecturedeck", "LectureDeck"), ("unistudentdeck", "UniStudentDeck"), ("campusdeck", "CampusDeck"), ("parentdeck", "ParentDeck")]
T = {
    "en": {"tour": "Take the live tour", "tour_p": "Pick an app to see its real demo running below, with example data.", "bar": "Live demo", "open": "Open full demo ↗", "play": "Preview the live demo",
           "roles": ["for lecturers", "for students", "for a campus or program", "family view, opt-in"],
           "calc_h": "Work out the cost for your university", "calc_p": "Set the number of faculties and their plan, then students and parents. Discounts across faculties apply automatically.",
           "f": "Faculties", "plan": "Plan for each faculty", "s": "Students in total", "p": "Parents who link", "two": "Two-year agreement (extra 5% off the plans)",
           "rows": {"plans": "{n} faculty plans", "disc": "{d}% off the plans", "list": "list price", "seat_s": "Student seats", "seat_p": "Parent seats", "total": "Total per year",
                    "per": "About {v} per student a year · about {u} at 26,300 VND per USD", "big": "25 or more faculties: 20% off or better, by custom quote."},
           "note": "An estimate in VND, excluding VAT. The volume discount applies to the faculty plans, not the seat fees.", "cta": "Request a written quote"},
    "vi": {"tour": "Xem thử trực tiếp", "tour_p": "Chọn một ứng dụng để xem bản demo thật chạy ngay bên dưới, với dữ liệu mẫu.", "bar": "Bản demo trực tuyến", "open": "Mở bản demo đầy đủ ↗", "play": "Xem trước bản demo",
           "roles": ["cho giảng viên", "cho sinh viên", "cho cơ sở hoặc chương trình", "chế độ gia đình, tùy chọn"],
           "calc_h": "Tính chi phí cho trường của bạn", "calc_p": "Chọn số khoa và gói cho mỗi khoa, rồi số sinh viên và phụ huynh. Chiết khấu theo số khoa được áp dụng tự động.",
           "f": "Số khoa", "plan": "Gói cho mỗi khoa", "s": "Tổng số sinh viên", "p": "Phụ huynh liên kết", "two": "Hợp đồng hai năm (giảm thêm 5% trên các gói)",
           "rows": {"plans": "{n} gói khoa", "disc": "giảm {d}% trên các gói", "list": "giá niêm yết", "seat_s": "Phí sinh viên", "seat_p": "Phí phụ huynh", "total": "Tổng mỗi năm",
                    "per": "Khoảng {v} mỗi sinh viên một năm · khoảng {u} với 26.300 VND/USD", "big": "Từ 25 khoa: giảm 20% hoặc hơn, theo báo giá riêng."},
           "note": "Ước tính bằng VND, chưa gồm VAT. Chiết khấu theo số lượng áp dụng cho các gói khoa, không áp dụng cho phí theo người dùng.", "cta": "Yêu cầu báo giá bằng văn bản"},
}


def tour(lang):
    t = T[lang]
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-app="{k}" data-name="{e(n)}">'
                   f'<b>{e(n)}</b><small>{e(t["roles"][i])}</small></button>' for i, (k, n) in enumerate(APPS))
    k, n = APPS[0]
    src = f"{D}{k}/?demo=1"
    box = (f'<div class="live live-lg" data-live="unideck-{k}" data-src="{src}" data-title="{e(n)}" data-autoload><div class="live-bar"><i></i><i></i><i></i>'
           f'<span>{e(t["bar"])} · <span class="ut-name">{e(n)}</span></span><a href="{src}" target="_blank" rel="noopener" data-demo-window="unideck-{k}">{e(t["open"])}</a></div>'
           f'<div class="live-view"><button type="button" class="live-play"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4L13 8z" fill="currentColor"/></svg>'
           f'<span>{e(t["play"])}</span></button></div></div>')
    return (f'<div class="utour"><h3>{e(t["tour"])}</h3><p class="note" style="font-style:normal">{e(t["tour_p"])}</p>'
            f'<div class="ut-tabs" role="tablist" aria-label="UniDeck">{tabs}</div>{box}</div>')


def calc(lang):
    t = T[lang]
    plans = [("Suite Starter", 15000000), ("Suite Standard", 30000000), ("Suite Growth", 52000000)]
    pb = "".join(f'<button type="button" role="radio" aria-checked="{"true" if n == "Suite Standard" else "false"}" data-price="{p}" data-name="{n}">{n}</button>' for n, p in plans)
    box = (f'<div class="calc ucalc" hidden data-lang="{lang}" data-l="{e(json.dumps(t["rows"], ensure_ascii=False))}"><div class="calc-in">'
           f'<label for="u-f"><span>{e(t["f"])}</span><b data-o="f"></b></label><input id="u-f" type="range" min="1" max="30" value="4">'
           f'<p class="calc-lbl">{e(t["plan"])}</p><div class="u-plans" role="radiogroup" aria-label="{e(t["plan"])}">{pb}</div>'
           f'<label for="u-s"><span>{e(t["s"])}</span><b data-o="s"></b></label><input id="u-s" type="range" min="100" max="20000" step="100" value="1600">'
           f'<label for="u-p"><span>{e(t["p"])}</span><b data-o="p"></b></label><input id="u-p" type="range" min="0" max="10000" step="50" value="400">'
           f'<label class="calc-chk"><input type="checkbox" id="u-two"> {e(t["two"])}</label></div>'
           f'<div class="calc-out" aria-live="polite"><dl data-o="rows"></dl><p class="calc-usd" data-o="per"></p><p class="calc-note">{e(t["note"])}</p>'
           f'<a class="btn primary" href="https://myteachersdeck.com/quote/">{e(t["cta"])}</a></div></div>')
    return {"id": "calc", "h2": t["calc_h"], "p": t["calc_p"], "blocks": [("html", box)]}


def apply(page):
    for lang in ("en", "vi"):
        secs = page[lang]["sections"]
        uni = secs[[s["id"] for s in secs].index("unideck")]
        kind, h = uni["blocks"][0]
        uni["blocks"][0] = (kind, tour(lang) + '<h3 class="section-gap">' + ("All four apps" if lang == "en" else "Cả bốn ứng dụng") + '</h3>' + h
                            + '<script src="/assets/uni.js?v=1" defer></script>')
        ids = [s["id"] for s in secs]
        secs.insert(ids.index("example"), calc(lang))
