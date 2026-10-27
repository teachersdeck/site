"""Language centers page extras: a live tour of the three apps a center uses most, and a chain cost calculator.
Both run in assets/centers.js; prices mirror the tables in centers.py (Pricing Sheet v2)."""
import html, json

e = lambda s: html.escape(s, quote=True)  # noqa: E731
D = "https://teachersdeck.github.io/demo/"
APPS = [("teachersdeck", "TeachersDeck"), ("parentdeck", "ParentDeck"), ("admindeck", "AdminDeck")]
PLANS = [("TeachersDeck Starter", 8000000), ("TeachersDeck Standard", 18000000), ("TeachersDeck Growth", 32000000),
         ("Suite Starter", 15000000), ("Suite Standard", 30000000), ("Suite Growth", 52000000)]
T = {
    "en": {"tour_h": "See a center's day in the live demo", "tour_p": "Pick a view: your teachers' classroom screen, what parents follow, and the group overview managers use.",
           "roles": ["for your teachers", "for parents", "for managers"], "bar": "Live demo", "open": "Open full demo ↗", "play": "Preview the live demo",
           "calc_h": "Work out the cost for your group", "calc_p": "Choose how many centers and the plan each one uses. Volume discounts start at 4 centers.",
           "n": "Centers", "plan": "Plan for each center", "two": "Two-year agreement (extra 5% off)",
           "rows": {"list": "{n} × {plan}, list price", "disc": "Volume discount, {d}% off", "total": "Total per year", "per": "About {v} per center a month · about {u} a year at 26,300 VND per USD",
                    "big": "25 or more centers: 20% off or better. We send a custom quote, so this is the most you would pay.", "none": "1 to 3 centers pay list price; discounts start at 4."},
           "note": "An estimate in VND, excluding VAT. No seat fees for students or parents, at any size.", "cta": "Request a written quote"},
    "vi": {"tour_h": "Xem một ngày của trung tâm trong bản demo", "tour_p": "Chọn một góc nhìn: màn hình lớp học của giáo viên, những gì phụ huynh theo dõi, và trang tổng quan hệ thống cho quản lý.",
           "roles": ["cho giáo viên", "cho phụ huynh", "cho quản lý"], "bar": "Bản demo trực tuyến", "open": "Mở bản demo đầy đủ ↗", "play": "Xem trước bản demo",
           "calc_h": "Tính chi phí cho hệ thống của bạn", "calc_p": "Chọn số trung tâm và gói cho mỗi trung tâm. Chiết khấu theo số lượng bắt đầu từ 4 trung tâm.",
           "n": "Số trung tâm", "plan": "Gói cho mỗi trung tâm", "two": "Hợp đồng hai năm (giảm thêm 5%)",
           "rows": {"list": "{n} × {plan}, giá niêm yết", "disc": "Chiết khấu số lượng, giảm {d}%", "total": "Tổng mỗi năm", "per": "Khoảng {v} mỗi trung tâm một tháng · khoảng {u} một năm với 26.300 VND/USD",
                    "big": "Từ 25 trung tâm: giảm 20% hoặc hơn. Chúng tôi gửi báo giá riêng, nên đây là mức tối đa bạn phải trả.", "none": "1 đến 3 trung tâm trả giá niêm yết; chiết khấu bắt đầu từ 4 trung tâm."},
           "note": "Ước tính bằng VND, chưa gồm VAT. Không thu phí học sinh hay phụ huynh, ở mọi quy mô.", "cta": "Yêu cầu báo giá bằng văn bản"},
}


def tour(lang):
    t = T[lang]
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-app="{k}" data-name="{e(n)}">'
                   f'<b>{e(n)}</b><small>{e(t["roles"][i])}</small></button>' for i, (k, n) in enumerate(APPS))
    k, n = APPS[0]
    src = f"{D}{k}/?demo=1"
    box = (f'<div class="live live-lg" data-live="{k}" data-src="{src}" data-title="{e(n)}" data-autoload><div class="live-bar"><i></i><i></i><i></i>'
           f'<span>{e(t["bar"])} · <span class="ut-name">{e(n)}</span></span><a href="{src}" target="_blank" rel="noopener" data-demo-window="{k}">{e(t["open"])}</a></div>'
           f'<div class="live-view"><button type="button" class="live-play"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4L13 8z" fill="currentColor"/></svg>'
           f'<span>{e(t["play"])}</span></button></div></div>')
    html_ = (f'<div class="utour" data-base="{D}"><div class="ut-tabs ut3" role="tablist" aria-label="Demo">{tabs}</div>{box}</div>'
             '<script src="/assets/centers.js?v=1" defer></script>')
    return {"id": "tour", "h2": t["tour_h"], "p": t["tour_p"], "blocks": [("html", html_)]}


def calc(lang):
    t = T[lang]
    opts = "".join(f'<option value="{p}"{" selected" if n == "Suite Standard" else ""}>{n}</option>' for n, p in PLANS)
    box = (f'<div class="calc ccalc" hidden data-lang="{lang}" data-l="{e(json.dumps(t["rows"], ensure_ascii=False))}"><div class="calc-in">'
           f'<label for="cc-n"><span>{e(t["n"])}</span><b data-o="n"></b></label><input id="cc-n" type="range" min="1" max="60" value="4">'
           f'<label for="cc-p" class="calc-lbl">{e(t["plan"])}</label><select id="cc-p" class="calc-sel">{opts}</select>'
           f'<label class="calc-chk"><input type="checkbox" id="cc-two"> {e(t["two"])}</label></div>'
           f'<div class="calc-out" aria-live="polite"><dl data-o="rows"></dl><p class="calc-usd" data-o="per"></p><p class="calc-note">{e(t["note"])}</p>'
           f'<a class="btn primary" href="https://myteachersdeck.com/quote/">{e(t["cta"])}</a></div></div>')
    return {"id": "calc", "h2": t["calc_h"], "p": t["calc_p"], "blocks": [("html", box)]}


def apply(page):
    for lang in ("en", "vi"):
        secs = page[lang]["sections"]
        secs.insert([s["id"] for s in secs].index("sizes") + 1, tour(lang))
        secs.insert([s["id"] for s in secs].index("chains") + 1, calc(lang))
