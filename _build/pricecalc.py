"""Pricing page: "Build your price", a calculator for every audience. Runs in assets/pricecalc.js, whose prices mirror
_build/pricing.py (TeachersDeck Pricing Sheet v3). Change both together."""
import html, json

e = lambda s: html.escape(s, quote=True)  # noqa: E731
T = {
    "en": {
        "h2": "Build your price", "p": "Answer a few questions and see an itemised yearly price. Prices in VND, excluding VAT.",
        "who": "Who is it for?", "whos": [("teacher", "A teacher"), ("family", "A family"), ("center", "Language center"), ("private", "Private school"), ("intl", "International school"), ("uni", "University")],
        "product": "Product", "products": [("pro", "TeachersDeck Pro"), ("platform", "ClassIn or Canvas")],
        "bill": "Billing", "bills": [("year", "Yearly (2 months free)"), ("month", "Monthly")],
        "apps": "Apps", "appss": [("suite", "Full suite: all four apps"), ("td", "TeachersDeck only")],
        "kids": "Children", "camp": "Campuses", "camp_uni": "Faculties", "t": "Teachers per campus", "s": "Students per campus", "p_par": "Parents who link, in total",
        "found_t": "Founding Teacher price (first 100 teachers)", "found_f": "Founding Family (first 200 children, 30% off the first year)",
        "found_c": "Join through the 30-day pilot (30% off the plan for 12 months, up to 3 campuses)", "two": "Two-year agreement (extra 5% off the plans)",
        "L": {"year": "a year", "month": "a month", "total": "Total per year", "permonth": "About {v} a month · about {u} a year at 26,300 VND per USD",
              "pro": "TeachersDeck Pro", "proF": "TeachersDeck Pro, Founding Teacher", "plat": "TeachersDeck for ClassIn or Canvas", "monthly": "{v} × 12 months",
              "child": "ParentDeck Pro, child {n}", "sib": "{d}% off", "foundF": "Founding Family, 30% off the first year",
              "plan": "{n} × {plan}", "extraT": "Extra teachers: {n} × 90,000 VND × 12", "foundC": "Pilot founding rate, 30% off for 12 months",
              "disc": "Volume discount, {d}% off the plans", "seatS": "Student seats: {n} × 100,000 VND", "seatP": "Parent seats: {n} × 500,000 VND",
              "custom": "More than 40 teachers or 900 students on a campus: we send a custom quote.", "noseat": "No seat fees for students or parents.",
              "cta_q": "Request a written quote", "cta_o": "Order now"},
    },
    "vi": {
        "h2": "Tự tính giá", "p": "Trả lời vài câu hỏi để xem giá mỗi năm theo từng khoản. Giá tính bằng VND, chưa gồm VAT.",
        "who": "Dành cho ai?", "whos": [("teacher", "Giáo viên"), ("family", "Gia đình"), ("center", "Trung tâm ngoại ngữ"), ("private", "Trường tư thục"), ("intl", "Trường quốc tế"), ("uni", "Trường đại học")],
        "product": "Sản phẩm", "products": [("pro", "TeachersDeck Pro"), ("platform", "ClassIn hoặc Canvas")],
        "bill": "Thanh toán", "bills": [("year", "Theo năm (tặng 2 tháng)"), ("month", "Theo tháng")],
        "apps": "Ứng dụng", "appss": [("suite", "Trọn bộ: cả bốn ứng dụng"), ("td", "Chỉ TeachersDeck")],
        "kids": "Số con", "camp": "Số cơ sở", "camp_uni": "Số khoa", "t": "Giáo viên mỗi cơ sở", "s": "Học sinh mỗi cơ sở", "p_par": "Tổng số phụ huynh liên kết",
        "found_t": "Giá Giáo viên sáng lập (100 giáo viên đầu tiên)", "found_f": "Gia đình sáng lập (200 trẻ đầu tiên, giảm 30% năm đầu)",
        "found_c": "Tham gia qua chương trình dùng thử 30 ngày (giảm 30% gói trong 12 tháng, tối đa 3 cơ sở)", "two": "Hợp đồng hai năm (giảm thêm 5% trên các gói)",
        "L": {"year": "một năm", "month": "một tháng", "total": "Tổng mỗi năm", "permonth": "Khoảng {v} mỗi tháng · khoảng {u} một năm với 26.300 VND/USD",
              "pro": "TeachersDeck Pro", "proF": "TeachersDeck Pro, Giáo viên sáng lập", "plat": "TeachersDeck cho ClassIn hoặc Canvas", "monthly": "{v} × 12 tháng",
              "child": "ParentDeck Pro, con thứ {n}", "sib": "giảm {d}%", "foundF": "Gia đình sáng lập, giảm 30% năm đầu",
              "plan": "{n} × {plan}", "extraT": "Thêm giáo viên: {n} × 90.000 VND × 12", "foundC": "Giá sáng lập qua dùng thử, giảm 30% trong 12 tháng",
              "disc": "Chiết khấu số lượng, giảm {d}% trên các gói", "seatS": "Phí học sinh: {n} × 100.000 VND", "seatP": "Phí phụ huynh: {n} × 500.000 VND",
              "custom": "Hơn 40 giáo viên hoặc 900 học sinh mỗi cơ sở: chúng tôi gửi báo giá riêng.", "noseat": "Không thu phí học sinh hay phụ huynh.",
              "cta_q": "Yêu cầu báo giá bằng văn bản", "cta_o": "Đặt mua ngay"},
    },
}


def chips(name, items, default):
    return (f'<div class="bp-chips" role="radiogroup" data-k="{name}">' +
            "".join(f'<button type="button" role="radio" aria-checked="{"true" if k == default else "false"}" data-v="{k}">{e(n)}</button>' for k, n in items) + "</div>")


def rng(id_, label, lo, hi, step, val, show):
    return (f'<div class="bp-f" data-show="{show}"><label for="{id_}"><span>{e(label)}</span><b data-o="{id_}"></b></label>'
            f'<input id="{id_}" type="range" min="{lo}" max="{hi}" step="{step}" value="{val}"></div>')


def chk(id_, label, show):
    return f'<label class="calc-chk bp-f" data-show="{show}"><input type="checkbox" id="{id_}"> {e(label)}</label>'


def section(lang):
    t = T[lang]
    form = (f'<div class="bp-f"><p class="calc-lbl">{e(t["who"])}</p>{chips("who", t["whos"], "center")}</div>'
            f'<div class="bp-f" data-show="teacher"><p class="calc-lbl">{e(t["product"])}</p>{chips("product", t["products"], "pro")}</div>'
            f'<div class="bp-f" data-show="teacher family"><p class="calc-lbl">{e(t["bill"])}</p>{chips("bill", t["bills"], "year")}</div>'
            f'<div class="bp-f" data-show="center private intl uni"><p class="calc-lbl">{e(t["apps"])}</p>{chips("apps", t["appss"], "suite")}</div>'
            + rng("bp-k", t["kids"], 1, 6, 1, 1, "family")
            + f'<div class="bp-f" data-show="center private intl uni"><label for="bp-c"><span class="bp-camp" data-a="{e(t["camp"])}" data-b="{e(t["camp_uni"])}">{e(t["camp"])}</span><b data-o="bp-c"></b></label><input id="bp-c" type="range" min="1" max="60" step="1" value="1"></div>'
            + rng("bp-t", t["t"], 1, 60, 1, 10, "center private intl uni")
            + rng("bp-s", t["s"], 10, 1000, 10, 150, "center private intl uni")
            + rng("bp-p", t["p_par"], 0, 5000, 10, 100, "intl uni")
            + chk("bp-ft", t["found_t"], "teacher-pro") + chk("bp-ff", t["found_f"], "family")
            + chk("bp-fc", t["found_c"], "center private intl uni") + chk("bp-two", t["two"], "center private intl uni"))
    box = (f'<div class="calc bp" hidden data-lang="{lang}" data-l="{e(json.dumps(t["L"], ensure_ascii=False))}"><div class="calc-in">{form}</div>'
           f'<div class="calc-out" aria-live="polite"><dl data-o="rows"></dl><p class="calc-usd" data-o="per"></p><p class="calc-note" data-o="note"></p>'
           f'<a class="btn primary" data-o="cta" href="https://myteachersdeck.com/quote/"></a></div></div><script src="/assets/pricecalc.js?v=1" defer></script>')
    return {"id": "build", "h2": t["h2"], "p": t["p"], "blocks": [("html", box)]}


def apply(page):
    for lang in ("en", "vi"):
        page[lang]["sections"].append(section(lang))
