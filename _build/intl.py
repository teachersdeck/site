"""International schools page extras: a seat-fee calculator and live ParentDeck / AdminDeck previews.
The calculator runs in assets/calc.js with the prices below; keep them in step with the tables in content.py."""
import html

e = lambda s: html.escape(s, quote=True)  # noqa: E731
DEMO = "https://teachersdeck.github.io/demo/"
T = {
    "en": {
        "see_h": "See what families and leaders get", "see_p": "The real ParentDeck and AdminDeck demos, running on this page with sample data. Click one to open it in its own window.",
        "bar": "Live demo", "open": "Open full demo ↗", "play": "Preview the live demo",
        "pd": "ParentDeck, for families", "ad": "AdminDeck, for school leaders",
        "calc_h": "Work out your yearly cost", "calc_p": "Move the sliders to match your school. The total updates as you go.",
        "t": "Teachers", "s": "Students", "p": "Parents who link", "found": "Joining through the 30-day pilot (founding rate)",
        "plan": "Campus plan", "extra": "extra teachers", "seat_s": "Student seats", "seat_p": "Parent seats", "total": "Total per year",
        "usd": "About {} a year at 26,300 VND per USD.", "big": "Over 900 students: we send a custom quote.",
        "note": "An estimate in VND, excluding VAT. We confirm every price in a written quote.", "cta": "Request a written quote",
    },
    "vi": {
        "see_h": "Xem gia đình và ban giám hiệu nhận được gì", "see_p": "Bản demo thật của ParentDeck và AdminDeck, chạy ngay trên trang này với dữ liệu mẫu. Bấm vào để mở trong cửa sổ riêng.",
        "bar": "Bản demo trực tuyến", "open": "Mở bản demo đầy đủ ↗", "play": "Xem trước bản demo",
        "pd": "ParentDeck, cho gia đình", "ad": "AdminDeck, cho ban giám hiệu",
        "calc_h": "Tính chi phí mỗi năm", "calc_p": "Kéo các thanh trượt cho đúng với trường bạn. Tổng tiền cập nhật ngay.",
        "t": "Giáo viên", "s": "Học sinh", "p": "Phụ huynh liên kết", "found": "Tham gia qua chương trình dùng thử 30 ngày (giá sáng lập)",
        "plan": "Gói cơ sở", "extra": "tài khoản giáo viên thêm", "seat_s": "Phí học sinh", "seat_p": "Phí phụ huynh", "total": "Tổng mỗi năm",
        "usd": "Khoảng {} mỗi năm, với 26.300 VND/USD.", "big": "Trên 900 học sinh: chúng tôi gửi báo giá riêng.",
        "note": "Ước tính bằng VND, chưa gồm VAT. Mọi mức giá được xác nhận trong báo giá bằng văn bản.", "cta": "Yêu cầu báo giá bằng văn bản",
    },
}


def live_box(lang, slug, title):
    t = T[lang]
    src = f"{DEMO}{slug}/?demo=1"
    return (f'<div class="live" data-live="{slug}" data-src="{src}" data-title="{e(title)}" data-autoload><div class="live-bar"><i></i><i></i><i></i>'
            f'<span>{e(t["bar"])} · {e(title)}</span><a href="{src}" target="_blank" rel="noopener" data-demo-window="{slug}">{e(t["open"])}</a></div>'
            f'<div class="live-view"><button type="button" class="live-play"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4L13 8z" fill="currentColor"/></svg>'
            f'<span>{e(t["play"])}</span></button></div></div>')


def see(lang):
    t = T[lang]
    return {"id": "see", "h2": t["see_h"], "p": t["see_p"], "blocks": [("html",
            f'<div class="intl-live">{live_box(lang, "parentdeck", t["pd"])}{live_box(lang, "admindeck", t["ad"])}</div>')]}


def calc(lang):
    t = T[lang]
    labels = {k: t[k] for k in ("plan", "extra", "seat_s", "seat_p", "total", "usd", "big")}
    import json
    box = (f'<div class="calc" hidden data-lang="{lang}" data-l="{e(json.dumps(labels, ensure_ascii=False))}">'
           f'<div class="calc-in">'
           f'<label for="c-t"><span>{e(t["t"])}</span><b data-o="t"></b></label><input id="c-t" type="range" min="1" max="60" value="10">'
           f'<label for="c-s"><span>{e(t["s"])}</span><b data-o="s"></b></label><input id="c-s" type="range" min="10" max="1000" step="10" value="100">'
           f'<label for="c-p"><span>{e(t["p"])}</span><b data-o="p"></b></label><input id="c-p" type="range" min="0" max="1500" step="10" value="100">'
           f'<label class="calc-chk"><input type="checkbox" id="c-f"> {e(t["found"])}</label></div>'
           f'<div class="calc-out" aria-live="polite"><dl data-o="rows"></dl><p class="calc-usd" data-o="usd"></p>'
           f'<p class="calc-note">{e(t["note"])}</p><a class="btn primary" href="https://myteachersdeck.com/quote/">{e(t["cta"])}</a></div></div>'
           '<script src="/assets/calc.js?v=1" defer></script>')
    return {"id": "calc", "h2": t["calc_h"], "p": t["calc_p"], "blocks": [("html", box)]}


def apply(page):
    for lang in ("en", "vi"):
        secs = page[lang]["sections"]
        ids = [s["id"] for s in secs]
        secs.insert(ids.index("gets") + 1, see(lang))
        ids = [s["id"] for s in secs]
        secs.insert(ids.index("example"), calc(lang))
