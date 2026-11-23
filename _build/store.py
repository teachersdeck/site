"""The Store (myteachersdeck.com/store/, owner 24 Nov 2026) for _build/pages.py: it takes Pricing's place in the dock.

Two shelves and one checkout:
  - Apps and plans: the asset deck (assets/store/deck.js, a copy of the suite's facepicker.js) with one card per app;
    the card in the middle shows its plans under the deck. TeachersDeck Pro and ParentDeck Pro are bought here; the
    rest go to UniStudentDeck, the order form or a quote.
  - Premium assets: a grid of TeachersDeck's Shop items, read live from the backend (getTeacherStore: names, prices,
    previews), with a basket.
  - Checkout: the suite backend's VietQR orders (createOrder with channel 'web', backend v2.36.0). The owner marks the
    order paid in HQ as for every order; the page then shows the key (Pro) or the store key (Shop items), with a link
    that opens the web app and switches it on (#redeem=KEY, TeachersDeck 0.50.0 / ParentDeck 0.34.0). The same key
    and link arrive by email.

Prices here must equal the quote engine (teachersdeck-suite admindeck-key-manager/quote-engine.js) and the backend's
payments.js; Shop prices come from the backend itself. When a price changes, change it here, in pricing.py and on its
own page."""
import json

S = "https://myteachersdeck.com"
QUOTE = S + "/quote/"
ORDER = S + "/order/"
DEMO = S + "/demo/"
ZALO = "https://zalo.me/0705247680"
STORE_V = "1"   # bump with every assets/store/* change

# One card per app in the deck. buy: plans sold here (product = the backend's product); link: where the button goes.
APPS = {
    "en": [
        {"key": "teachersdeck", "name": "TeachersDeck Pro", "group": "For teachers", "badge": "From 120,000₫",
         "art": ["Pro", "TeachersDeck", "indigo"], "product": "teachersdeck",
         "sub": "22 Pro widgets: Lesson Planner, Games, Poll, Noise Meter, media, DrawDeck and more, plus premium clock faces and the Premium Whiteboard.",
         "plans": [{"cycle": "monthly", "label": "Monthly", "price": 120000, "per": "a month"},
                   {"cycle": "annual", "label": "Yearly", "price": 1050000, "per": "a year", "note": "Two months free"},
                   {"cycle": "annual", "founding": True, "label": "Founding Teacher", "price": 650000, "per": "a year",
                    "note": "First 100 teachers, kept every year you renew"}],
         "how": "One key, one device. Open the link we give you on the computer you teach with."},
        {"key": "parentdeck", "name": "ParentDeck Pro", "group": "For families", "badge": "From 30,000₫",
         "art": ["Pro", "ParentDeck", "matcha"], "product": "parentdeck",
         "sub": "Badge case, homework insights, wishlist, conversation starters and the weekly digest, and StudentDeck Pro for every child you link. One price per family.",
         "plans": [{"cycle": "monthly", "label": "Monthly", "price": 30000, "per": "a month"},
                   {"cycle": "annual", "label": "Yearly", "price": 300000, "per": "a year", "note": "Two months free"},
                   {"cycle": "annual", "founding": True, "label": "Founding Family", "price": 210000, "per": "the first year",
                    "note": "30% off the first year, first 50 families"}],
         "how": "Open the link we give you and sign in to ParentDeck: Pro goes on your account and every child you link."},
        {"key": "studentdeck", "name": "StudentDeck Pro", "group": "For families", "badge": "With ParentDeck Pro",
         "art": ["Pro", "StudentDeck", "amber"],
         "sub": "Children never buy anything: StudentDeck Pro comes free with the family's ParentDeck Pro or the school's plan.",
         "link": {"text": "See ParentDeck Pro", "goto": "parentdeck"}},
        {"key": "unistudent", "name": "UniStudentDeck Pro", "group": "For families", "badge": "From 50,000₫",
         "art": ["Pro", "UniStudentDeck", "coral"],
         "sub": "University students buy their own Pro inside UniStudentDeck (Settings): 50,000₫ a month or 500,000₫ a year.",
         "link": {"text": "Open UniStudentDeck", "href": "https://uni.myteachersdeck.com/"}},
        {"key": "lms", "name": "TeachersDeck for ClassIn, Canvas or Moodle", "group": "For schools", "badge": "1,250,000₫ / teacher",
         "art": ["LMS", "ClassIn · Canvas · Moodle", "indigo"],
         "sub": "TeachersDeck Pro inside your school's teaching platform, 1,250,000₫ per teacher a year. Ten teachers or more: a written quote.",
         "link": {"text": "Order for your school", "href": ORDER}},
        {"key": "school", "name": "Suite plan for schools and centers", "group": "For schools", "badge": "Quote",
         "art": ["Suite", "Schools & centers", "matcha"],
         "sub": "Pro for every teacher and family, AdminDeck Pro for the office, one flat price per campus.",
         "link": {"text": "See school plans", "href": S + "/pricing/"}},
        {"key": "kinder", "name": "KinderDeck for preschools", "group": "For schools", "badge": "Quote",
         "art": ["Kinder", "Preschools", "amber"],
         "sub": "TinyTeachersDeck, TinyParentDeck and KinderDeck: the school's licence unlocks everything.",
         "link": {"text": "Request a quote", "href": QUOTE}},
    ],
    "vi": [
        {"key": "teachersdeck", "name": "TeachersDeck Pro", "group": "Cho giáo viên", "badge": "Từ 120.000₫",
         "art": ["Pro", "TeachersDeck", "indigo"], "product": "teachersdeck",
         "sub": "22 tiện ích Pro: Soạn giáo án, Trò chơi, Bình chọn, Đo tiếng ồn, đa phương tiện, DrawDeck và hơn nữa, cùng mặt đồng hồ cao cấp và Bảng trắng cao cấp.",
         "plans": [{"cycle": "monthly", "label": "Theo tháng", "price": 120000, "per": "mỗi tháng"},
                   {"cycle": "annual", "label": "Theo năm", "price": 1050000, "per": "mỗi năm", "note": "Tặng hai tháng"},
                   {"cycle": "annual", "founding": True, "label": "Giáo viên sáng lập", "price": 650000, "per": "mỗi năm",
                    "note": "100 giáo viên đầu tiên, giữ giá mỗi năm gia hạn"}],
         "how": "Mỗi mã dùng cho một thiết bị. Mở đường liên kết chúng tôi gửi trên máy tính bạn dạy."},
        {"key": "parentdeck", "name": "ParentDeck Pro", "group": "Cho gia đình", "badge": "Từ 30.000₫",
         "art": ["Pro", "ParentDeck", "matcha"], "product": "parentdeck",
         "sub": "Tủ huy hiệu, phân tích bài tập, danh sách mong muốn, gợi ý trò chuyện và bản tin hằng tuần, cùng StudentDeck Pro cho mọi con bạn liên kết. Một giá cho cả gia đình.",
         "plans": [{"cycle": "monthly", "label": "Theo tháng", "price": 30000, "per": "mỗi tháng"},
                   {"cycle": "annual", "label": "Theo năm", "price": 300000, "per": "mỗi năm", "note": "Tặng hai tháng"},
                   {"cycle": "annual", "founding": True, "label": "Gia đình sáng lập", "price": 210000, "per": "năm đầu",
                    "note": "Giảm 30% năm đầu, 50 gia đình đầu tiên"}],
         "how": "Mở đường liên kết chúng tôi gửi và đăng nhập ParentDeck: Pro vào tài khoản của bạn và mọi con bạn liên kết."},
        {"key": "studentdeck", "name": "StudentDeck Pro", "group": "Cho gia đình", "badge": "Kèm ParentDeck Pro",
         "art": ["Pro", "StudentDeck", "amber"],
         "sub": "Trẻ em không bao giờ phải mua gì: StudentDeck Pro đi kèm miễn phí với ParentDeck Pro của gia đình hoặc gói của trường.",
         "link": {"text": "Xem ParentDeck Pro", "goto": "parentdeck"}},
        {"key": "unistudent", "name": "UniStudentDeck Pro", "group": "Cho gia đình", "badge": "Từ 50.000₫",
         "art": ["Pro", "UniStudentDeck", "coral"],
         "sub": "Sinh viên đại học tự mua Pro trong UniStudentDeck (Cài đặt): 50.000₫ mỗi tháng hoặc 500.000₫ mỗi năm.",
         "link": {"text": "Mở UniStudentDeck", "href": "https://uni.myteachersdeck.com/"}},
        {"key": "lms", "name": "TeachersDeck cho ClassIn, Canvas hoặc Moodle", "group": "Cho trường học", "badge": "1.250.000₫ / giáo viên",
         "art": ["LMS", "ClassIn · Canvas · Moodle", "indigo"],
         "sub": "TeachersDeck Pro ngay trong nền tảng dạy học của trường, 1.250.000₫ mỗi giáo viên mỗi năm. Từ mười giáo viên: báo giá bằng văn bản.",
         "link": {"text": "Đặt mua cho trường", "href": ORDER}},
        {"key": "school", "name": "Gói Suite cho trường và trung tâm", "group": "Cho trường học", "badge": "Báo giá",
         "art": ["Suite", "Trường & trung tâm", "matcha"],
         "sub": "Pro cho mọi giáo viên và gia đình, AdminDeck Pro cho văn phòng, một giá cố định cho mỗi cơ sở.",
         "link": {"text": "Xem gói cho trường", "href": S + "/vi/pricing/"}},
        {"key": "kinder", "name": "KinderDeck cho trường mầm non", "group": "Cho trường học", "badge": "Báo giá",
         "art": ["Kinder", "Mầm non", "amber"],
         "sub": "TinyTeachersDeck, TinyParentDeck và KinderDeck: giấy phép của trường mở khóa tất cả.",
         "link": {"text": "Yêu cầu báo giá", "href": QUOTE}},
    ],
}


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _vnd(v, lang):
    return f"{v:,}".replace(",", "." if lang == "vi" else ",") + "₫"


def static_apps(lang):
    """Every app and plan as plain HTML: search engines, AgentDeck's knowledge builder and browsers without JavaScript.
    assets/store/store.js replaces it with the deck."""
    out = ['<div class="st-static"><ul>']
    for a in APPS[lang]:
        plans = "; ".join(f'{p["label"]} {_vnd(p["price"], lang)} {p["per"]}' for p in a.get("plans", []))
        out.append(f'<li><b>{_esc(a["name"])}</b>: {_esc(a["sub"])}{(" " + _esc(plans) + ".") if plans else ""}</li>')
    out.append("</ul></div>")
    return "".join(out)


def apps_block(lang):
    data = json.dumps(APPS[lang], ensure_ascii=False).replace("</", "<\\/")
    return ('<script>document.documentElement.classList.add("js")</script>'
            f'<div class="st-apps" data-store-apps>{static_apps(lang)}</div>'
            f'<script type="application/json" id="store-apps">{data}</script>')


def assets_block(lang):
    t = {"en": "The Shop opens here with JavaScript on. You can also buy every item inside TeachersDeck: Theme → Shop.",
         "vi": "Cửa hàng hiện ở đây khi bật JavaScript. Bạn cũng có thể mua mọi mục ngay trong TeachersDeck: Giao diện → Cửa hàng."}[lang]
    return (f'<div class="st-assets" data-store-assets><p class="note st-static">{_esc(t)}</p></div>'
            '<div id="st-orders" class="st-orders" hidden></div>'
            f'<link rel="stylesheet" href="/assets/store/deck.css?v={STORE_V}">'
            f'<link rel="stylesheet" href="/assets/store/store.css?v={STORE_V}">'
            f'<script src="/assets/store/store-core.js?v={STORE_V}" defer></script>'
            f'<script src="/assets/store/deck.js?v={STORE_V}" defer></script>'
            f'<script src="/assets/store/store.js?v={STORE_V}" defer></script>')


STEPS = {
    "en": [{"h": "1. Choose", "p": "A Pro plan from the deck, or themes, faces and docks from the grid.", "tint": "indigo"},
           {"h": "2. Pay by VietQR", "p": "Scan the code in any Vietnamese banking app. Keep the order code in the transfer note.", "tint": "amber"},
           {"h": "3. Get your key", "p": "Once we confirm the transfer, your key appears on this page and in your email.", "tint": "matcha"},
           {"h": "4. Open the app", "p": "One click opens the web app with the key, and it switches on by itself.", "tint": "coral"}],
    "vi": [{"h": "1. Chọn", "p": "Một gói Pro trong bộ thẻ, hoặc giao diện, mặt đồng hồ và dock trong lưới.", "tint": "indigo"},
           {"h": "2. Thanh toán VietQR", "p": "Quét mã bằng bất kỳ ứng dụng ngân hàng Việt Nam nào. Giữ mã đơn trong nội dung chuyển khoản.", "tint": "amber"},
           {"h": "3. Nhận mã", "p": "Khi chúng tôi xác nhận chuyển khoản, mã hiện trên trang này và trong email của bạn.", "tint": "matcha"},
           {"h": "4. Mở ứng dụng", "p": "Một cú nhấp mở ứng dụng web cùng mã, và mã tự bật.", "tint": "coral"}],
}

FAQ = {
    "en": [("How do I pay?", "By VietQR bank transfer from any Vietnamese bank. The order code (like TD K7Q4M9) must stay in the transfer note so we can match your payment. Buying from abroad? Request a quote and we send an invoice."),
           ("When do I get my key?", "As soon as we confirm the transfer: we check the account every day. Keep this page open, or come back later: your order is remembered in this browser, and the key is emailed too."),
           ("How does the key reach the app?", "The page and the email give you a link such as teacher.myteachersdeck.com/#redeem=KEY. Open it and Pro (or your Shop items) switches on. You can also type the key in the app: TeachersDeck → Settings → Pro, or Theme → Shop → I have a store key."),
           ("What is a store key?", "Themes, faces and docks bought here go on a store key (SK-XXXX-XXXX-XXXX). Enter it on any computer and your items come with it. Buy more later and they are added to the same key."),
           ("Can my child buy something?", "No. StudentDeck never shows a price. Children get Pro through their family's ParentDeck Pro or their school's plan.")],
    "vi": [("Thanh toán thế nào?", "Bằng chuyển khoản VietQR từ bất kỳ ngân hàng Việt Nam nào. Mã đơn (như TD K7Q4M9) phải giữ nguyên trong nội dung chuyển khoản để chúng tôi đối chiếu. Mua từ nước ngoài? Yêu cầu báo giá và chúng tôi gửi hóa đơn."),
           ("Khi nào tôi nhận được mã?", "Ngay khi chúng tôi xác nhận chuyển khoản: chúng tôi kiểm tra tài khoản mỗi ngày. Giữ trang này mở, hoặc quay lại sau: đơn của bạn được ghi nhớ trong trình duyệt này, và mã cũng được gửi qua email."),
           ("Mã vào ứng dụng bằng cách nào?", "Trang và email cho bạn một đường liên kết như teacher.myteachersdeck.com/#redeem=MÃ. Mở nó là Pro (hoặc các mục đã mua) tự bật. Bạn cũng có thể nhập mã trong ứng dụng: TeachersDeck → Cài đặt → Pro, hoặc Giao diện → Cửa hàng → Tôi có mã cửa hàng."),
           ("Mã cửa hàng là gì?", "Giao diện, mặt đồng hồ và dock mua ở đây nằm trên một mã cửa hàng (SK-XXXX-XXXX-XXXX). Nhập mã trên máy nào thì các mục đi theo đến đó. Mua thêm sau này sẽ được thêm vào cùng mã."),
           ("Con tôi có mua được gì không?", "Không. StudentDeck không bao giờ hiện giá. Trẻ có Pro qua ParentDeck Pro của gia đình hoặc gói của trường.")],
}

STORE = {
    "slug": "store",
    "en": {
        "title": "Store: TeachersDeck Pro, ParentDeck Pro and Premium Themes",
        "description": "Buy TeachersDeck Pro, ParentDeck Pro, premium themes, clock faces and docks by VietQR. Your key appears on the page and opens the app in one click.",
        "crumb": "Store",
        "kicker": "Store",
        "h1": "Pro plans and premium assets",
        "lede": "Pay by VietQR and get your key on this page and by email. One click opens the app with it. Prices in VND.",
        "cta": [("Pro plans", "#apps-plans"), ("Premium assets", "#assets")],
        "sections": [
            {"id": "apps-plans", "h2": "Apps and plans", "p": "Turn the deck to an app. Its plans appear underneath.", "blocks": [("html", apps_block("en"))]},
            {"id": "assets", "h2": "Premium assets", "p": "Themes, watch and clock faces, docks and the Premium Whiteboard for TeachersDeck. Bought once, yours to keep.", "blocks": [("html", assets_block("en"))]},
            {"id": "how", "h2": "How buying works", "blocks": [("tiles", STEPS["en"])]},
            {"id": "faq", "h2": "Questions", "blocks": [("faq", FAQ["en"])]},
        ],
        "band": {"h2": "Buying for a whole school?", "p": "One plan covers every teacher and family, with AdminDeck Pro for the office. We reply by email and Zalo within one working day.",
                 "links": [("Request a quote", QUOTE), ("Message on Zalo", ZALO)]},
    },
    "vi": {
        "title": "Cửa hàng: TeachersDeck Pro, ParentDeck Pro và giao diện cao cấp",
        "description": "Mua TeachersDeck Pro, ParentDeck Pro, giao diện, mặt đồng hồ và dock cao cấp bằng VietQR. Mã hiện ngay trên trang và mở ứng dụng chỉ với một cú nhấp.",
        "crumb": "Cửa hàng",
        "kicker": "Cửa hàng",
        "h1": "Gói Pro và tài nguyên cao cấp",
        "lede": "Thanh toán VietQR, nhận mã trên trang này và qua email. Một cú nhấp mở ứng dụng cùng mã. Giá tính bằng VND.",
        "cta": [("Gói Pro", "#apps-plans"), ("Tài nguyên cao cấp", "#assets")],
        "sections": [
            {"id": "apps-plans", "h2": "Ứng dụng và gói", "p": "Xoay bộ thẻ đến một ứng dụng. Các gói của nó hiện bên dưới.", "blocks": [("html", apps_block("vi"))]},
            {"id": "assets", "h2": "Tài nguyên cao cấp", "p": "Giao diện, mặt đồng hồ, dock và Bảng trắng cao cấp cho TeachersDeck. Mua một lần, dùng mãi.", "blocks": [("html", assets_block("vi"))]},
            {"id": "how", "h2": "Cách mua", "blocks": [("tiles", STEPS["vi"])]},
            {"id": "faq", "h2": "Câu hỏi", "blocks": [("faq", FAQ["vi"])]},
        ],
        "band": {"h2": "Mua cho cả trường?", "p": "Một gói cho mọi giáo viên và gia đình, kèm AdminDeck Pro cho văn phòng. Chúng tôi trả lời qua email và Zalo trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Nhắn Zalo", ZALO)]},
    },
}
