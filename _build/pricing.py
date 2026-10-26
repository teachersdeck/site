"""Pricing page for _build/pages.py: every tier in one widget (assets/pricing.js).

Three audience tabs (Teachers, Schools & centers, Families), each with at most three plan cards and a
monthly/yearly switch; everything else (founding rates, chain discounts, seat fees, teachers-only campus
plans) is a short list under the cards, each item linking to the page with the details.
Prices are the ones already on the site (price sheet v3, 25 Oct 2026); nothing new is priced here.
When a price changes, change it here AND on its own page."""
import json

ORDER = "https://myteachersdeck.com/order/"
QUOTE = "https://myteachersdeck.com/quote/"
DEMO = "https://myteachersdeck.com/demo/"
ZALO = "https://zalo.me/0705247680"
S = "https://myteachersdeck.com"
TD_DEMO = "https://teachersdeck.github.io/demo/teachersdeck/?demo=1"

DATA = {
    "en": {
        "locale": "en-US",
        "t": {"month": "month", "year": "year", "billedMonthly": "billed monthly", "billedYearly": "billed yearly",
              "yearlyOnly": "yearly plan", "free": "free forever", "popular": "Popular", "toggle": "Yearly billing",
              "save": "2 months free", "tabs": "Who is it for?"},
        "tabs": [
            {"id": "teachers", "label": "Teachers", "unit": "per teacher", "cards": [
                {"name": "Free", "tag": "Try it in class", "free": True,
                 "features": ["The everyday classroom widgets: clock, timers, traffic light, dice, checklist, calendar and more",
                              "Runs in your browser or as your Chrome new tab", "English and Tiếng Việt",
                              "Your classes stay on your own device"],
                 "button": {"text": "Try the live demo", "href": TD_DEMO, "demo": "teachersdeck"},
                 "desc": "No account needed."},
                {"name": "TeachersDeck Pro", "tag": "For one teacher", "monthly": 240000, "yearly": 2100000, "popular": True,
                 "features": ["Every widget: DrawDeck whiteboard, Lesson Planner, Games, Poll, Exit Ticket and more",
                              "Cloud Class: students and parents join with a code",
                              "Notes home and progress reports for parents",
                              "Founding Teacher: the first 100 teachers pay 1,300,000 VND a year"],
                 "button": {"text": "Order Pro", "href": ORDER},
                 "desc": "Already included for every teacher on a school or center plan.",
                 "links": [{"text": "More about TeachersDeck", "href": S + "/teachersdeck/"}]},
                {"name": "ClassIn or Canvas", "tag": "Inside your teaching platform", "yearly": 1250000,
                 "features": ["TeachersDeck on your ClassIn board, opened with one link",
                              "Or launched from any Canvas course, signed in through Canvas",
                              "Widgets that show no student data on a shared screen",
                              "Free live demo, no account needed"],
                 "button": {"text": "Order for ClassIn or Canvas", "href": ORDER},
                 "desc": "Centers and schools with 10 or more teachers get a written quote.",
                 "links": [{"text": "ClassIn", "href": S + "/classin/"}, {"text": "Canvas", "href": S + "/canvas/"}]},
            ], "notes": []},
            {"id": "schools", "label": "Schools & centers", "unit": "per campus", "cards": [
                {"name": "Suite Starter", "tag": "A small center or one department", "monthly": 1500000, "yearly": 15000000,
                 "features": ["Up to 8 teachers and 150 students", "TeachersDeck Pro for every teacher",
                              "StudentDeck, ParentDeck and AdminDeck", "2 admin accounts"],
                 "button": {"text": "Request a quote", "href": QUOTE}},
                {"name": "Suite Standard", "tag": "Most campuses", "monthly": 3000000, "yearly": 30000000, "popular": True,
                 "features": ["Up to 20 teachers and 400 students", "TeachersDeck Pro for every teacher",
                              "StudentDeck, ParentDeck and AdminDeck", "5 admin accounts"],
                 "button": {"text": "Request a quote", "href": QUOTE},
                 "desc": "Extra teacher 90,000 VND a month; extra 50 students 150,000 VND a month."},
                {"name": "Suite Growth", "tag": "Larger schools", "monthly": 5200000, "yearly": 52000000,
                 "features": ["Up to 40 teachers and 900 students", "TeachersDeck Pro for every teacher",
                              "StudentDeck, ParentDeck and AdminDeck", "Unlimited admin accounts"],
                 "button": {"text": "Request a quote", "href": QUOTE},
                 "desc": "Bigger than this? We send a custom quote."},
            ], "notes": [
                {"text": "Try it free for 30 days. Join through the pilot and your plan is 30% off for the first 12 months.",
                 "links": [{"text": "Book a demo", "href": DEMO}]},
                {"text": "Groups of 4 or more campuses or faculties get 10% to 20% off, and 5% more on a two-year agreement.",
                 "links": [{"text": "Language centers and chains", "href": S + "/language-centers/"}]},
                {"text": "International schools and universities also pay yearly seats: 100,000 VND per student and 500,000 VND per parent who links. Private schools and language centers pay no seat fees.",
                 "links": [{"text": "International and private schools", "href": S + "/international-schools/"},
                           {"text": "Universities", "href": S + "/universities/"}]},
                {"text": "Only need the teacher app? TeachersDeck campus plans start at 800,000 VND a month.",
                 "links": [{"text": "See the plans", "href": S + "/language-centers/"}]},
            ]},
            {"id": "families", "label": "Families", "unit": "per child", "cards": [
                {"name": "ParentDeck Free", "tag": "One child", "free": True,
                 "features": ["Follow one child's points, homework and notes from the teacher",
                              "Read-only: nothing to set up or manage", "Your child's own private code"],
                 "button": {"text": "See ParentDeck", "href": S + "/parentdeck/"}},
                {"name": "ParentDeck Pro", "tag": "For each child", "monthly": 30000, "yearly": 300000, "popular": True,
                 "features": ["Badge Display Case, Homework insights and Rewards Wishlist",
                              "Conversation Starters, Weekly Digest and Class Pulse",
                              "Also unlocks your child's StudentDeck Pro",
                              "Brothers and sisters: 2nd child 30% off, 3rd and more 50% off"],
                 "button": {"text": "Order ParentDeck Pro", "href": ORDER},
                 "desc": "Founding Family: the first 200 children get 30% off their first year."},
            ], "notes": [
                {"text": "If your child's school plan already pays for StudentDeck, you don't pay for it again.", "links": []},
            ]},
        ],
    },
    "vi": {
        "locale": "vi-VN",
        "t": {"month": "tháng", "year": "năm", "billedMonthly": "thanh toán hằng tháng", "billedYearly": "thanh toán hằng năm",
              "yearlyOnly": "gói theo năm", "free": "miễn phí mãi mãi", "popular": "Phổ biến", "toggle": "Thanh toán theo năm",
              "save": "tặng 2 tháng", "tabs": "Dành cho ai?"},
        "tabs": [
            {"id": "teachers", "label": "Giáo viên", "unit": "mỗi giáo viên", "cards": [
                {"name": "Miễn phí", "tag": "Dùng thử trên lớp", "free": True,
                 "features": ["Các tiện ích lớp học hằng ngày: đồng hồ, hẹn giờ, đèn giao thông, xúc xắc, danh sách việc, lịch và nhiều hơn nữa",
                              "Chạy trên trình duyệt hoặc làm trang tab mới của Chrome", "Tiếng Anh và tiếng Việt",
                              "Lớp học của bạn được lưu trên chính thiết bị của bạn"],
                 "button": {"text": "Dùng thử bản demo", "href": TD_DEMO, "demo": "teachersdeck"},
                 "desc": "Không cần tài khoản."},
                {"name": "TeachersDeck Pro", "tag": "Cho một giáo viên", "monthly": 240000, "yearly": 2100000, "popular": True,
                 "features": ["Mọi tiện ích: bảng trắng DrawDeck, Soạn giáo án, Trò chơi, Bình chọn, Phiếu cuối giờ và nhiều hơn nữa",
                              "Cloud Class: học sinh và phụ huynh tham gia bằng mã",
                              "Ghi chú về nhà và báo cáo tiến độ cho phụ huynh",
                              "Giáo viên sáng lập: 100 giáo viên đầu tiên chỉ trả 1.300.000 VND mỗi năm"],
                 "button": {"text": "Đặt mua Pro", "href": ORDER},
                 "desc": "Đã bao gồm cho mọi giáo viên trong gói của trường hoặc trung tâm.",
                 "links": [{"text": "Xem TeachersDeck", "href": S + "/vi/teachersdeck/"}]},
                {"name": "ClassIn hoặc Canvas", "tag": "Trong nền tảng bạn đang dạy", "yearly": 1250000,
                 "features": ["TeachersDeck trên bảng ClassIn, mở bằng một link",
                              "Hoặc mở từ mọi khóa học Canvas, đăng nhập qua Canvas",
                              "Tiện ích không hiển thị dữ liệu học sinh trên màn hình chung",
                              "Bản demo trực tuyến miễn phí, không cần tài khoản"],
                 "button": {"text": "Đặt mua cho ClassIn hoặc Canvas", "href": ORDER},
                 "desc": "Trung tâm và trường từ 10 giáo viên nhận báo giá bằng văn bản.",
                 "links": [{"text": "ClassIn", "href": S + "/vi/classin/"}, {"text": "Canvas", "href": S + "/vi/canvas/"}]},
            ], "notes": []},
            {"id": "schools", "label": "Trường & trung tâm", "unit": "mỗi cơ sở", "cards": [
                {"name": "Suite Starter", "tag": "Trung tâm nhỏ hoặc một khoa", "monthly": 1500000, "yearly": 15000000,
                 "features": ["Tối đa 8 giáo viên và 150 học sinh", "TeachersDeck Pro cho mọi giáo viên",
                              "StudentDeck, ParentDeck và AdminDeck", "2 tài khoản quản trị"],
                 "button": {"text": "Yêu cầu báo giá", "href": QUOTE}},
                {"name": "Suite Standard", "tag": "Phù hợp hầu hết cơ sở", "monthly": 3000000, "yearly": 30000000, "popular": True,
                 "features": ["Tối đa 20 giáo viên và 400 học sinh", "TeachersDeck Pro cho mọi giáo viên",
                              "StudentDeck, ParentDeck và AdminDeck", "5 tài khoản quản trị"],
                 "button": {"text": "Yêu cầu báo giá", "href": QUOTE},
                 "desc": "Thêm giáo viên 90.000 VND mỗi tháng; thêm 50 học sinh 150.000 VND mỗi tháng."},
                {"name": "Suite Growth", "tag": "Trường lớn hơn", "monthly": 5200000, "yearly": 52000000,
                 "features": ["Tối đa 40 giáo viên và 900 học sinh", "TeachersDeck Pro cho mọi giáo viên",
                              "StudentDeck, ParentDeck và AdminDeck", "Không giới hạn tài khoản quản trị"],
                 "button": {"text": "Yêu cầu báo giá", "href": QUOTE},
                 "desc": "Lớn hơn mức này? Chúng tôi gửi báo giá riêng."},
            ], "notes": [
                {"text": "Dùng thử miễn phí 30 ngày. Tham gia qua chương trình thí điểm, gói của bạn được giảm 30% trong 12 tháng đầu.",
                 "links": [{"text": "Đặt lịch demo", "href": DEMO}]},
                {"text": "Từ 4 cơ sở hoặc khoa trở lên được giảm 10% đến 20%, và thêm 5% khi ký hợp đồng hai năm.",
                 "links": [{"text": "Trung tâm ngoại ngữ và chuỗi", "href": S + "/vi/language-centers/"}]},
                {"text": "Trường quốc tế và đại học trả thêm phí theo người mỗi năm: 100.000 VND mỗi học sinh và 500.000 VND mỗi phụ huynh liên kết. Trường tư thục và trung tâm ngoại ngữ không tính phí này.",
                 "links": [{"text": "Trường quốc tế và tư thục", "href": S + "/vi/international-schools/"},
                           {"text": "Trường đại học", "href": S + "/vi/universities/"}]},
                {"text": "Chỉ cần ứng dụng cho giáo viên? Gói TeachersDeck cho cơ sở từ 800.000 VND mỗi tháng.",
                 "links": [{"text": "Xem các gói", "href": S + "/vi/language-centers/"}]},
            ]},
            {"id": "families", "label": "Gia đình", "unit": "mỗi con", "cards": [
                {"name": "ParentDeck Miễn phí", "tag": "Một con", "free": True,
                 "features": ["Theo dõi điểm thưởng, bài tập và ghi chú từ giáo viên của một con",
                              "Chỉ xem: không cần thiết lập hay quản lý", "Mã riêng tư của con bạn"],
                 "button": {"text": "Xem ParentDeck", "href": S + "/vi/parentdeck/"}},
                {"name": "ParentDeck Pro", "tag": "Cho mỗi con", "monthly": 30000, "yearly": 300000, "popular": True,
                 "features": ["Tủ huy hiệu, Phân tích bài tập và Danh sách phần thưởng mong muốn",
                              "Gợi ý trò chuyện, Bản tin hằng tuần và Nhịp lớp học",
                              "Mở khóa StudentDeck Pro cho con bạn",
                              "Anh chị em: con thứ 2 giảm 30%, từ con thứ 3 giảm 50%"],
                 "button": {"text": "Đặt mua ParentDeck Pro", "href": ORDER},
                 "desc": "Gia đình sáng lập: 200 học sinh đầu tiên được giảm 30% năm đầu."},
            ], "notes": [
                {"text": "Nếu gói của trường đã chi trả StudentDeck cho con, bạn không phải trả lại.", "links": []},
            ]},
        ],
    },
}


def widget(lang):
    data = json.dumps(DATA[lang], ensure_ascii=False).replace("</", "<\\/")
    return ('<div class="pricing" data-pricing><noscript><p>Prices: see the plan pages linked below.</p></noscript></div>'
            f'<script type="application/json" id="pricing-data">{data}</script>'
            '<script src="/assets/pricing.js" defer></script>')


PRICING = {
    "slug": "pricing",
    "en": {
        "title": "Pricing: TeachersDeck Suite for Teachers, Schools and Families",
        "description": "TeachersDeck Suite prices in one place: free and Pro for teachers, Suite campus plans for schools and centers, ParentDeck for families. Prices in VND.",
        "crumb": "Pricing",
        "kicker": "Pricing",
        "h1": "Simple pricing for every classroom",
        "lede": "Choose who it's for, then the plan. Prices are in VND, excluding VAT. Yearly plans are 10 months, so two months are free.",
        "cta": [("Request a quote", QUOTE), ("Book a demo", DEMO)],
        "sections": [{"id": "plans", "h2": "Plans", "blocks": [("html", widget("en"))]}],
        "band": {"h2": "Not sure which plan fits?", "p": "Tell us about your class, center or school and we'll suggest one by email and Zalo within one working day.",
                 "links": [("Request a quote", QUOTE), ("Message on Zalo", ZALO)]},
    },
    "vi": {
        "title": "Bảng giá: TeachersDeck Suite cho giáo viên, trường học và gia đình",
        "description": "Giá TeachersDeck Suite ở một nơi: miễn phí và Pro cho giáo viên, gói Suite cho trường và trung tâm, ParentDeck cho gia đình. Giá tính bằng VND.",
        "crumb": "Bảng giá",
        "kicker": "Bảng giá",
        "h1": "Bảng giá đơn giản cho mọi lớp học",
        "lede": "Chọn đối tượng, rồi chọn gói. Giá tính bằng VND, chưa gồm VAT. Gói năm tính 10 tháng, nên được tặng hai tháng.",
        "cta": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)],
        "sections": [{"id": "plans", "h2": "Các gói", "blocks": [("html", widget("vi"))]}],
        "band": {"h2": "Chưa chắc gói nào phù hợp?", "p": "Cho chúng tôi biết về lớp, trung tâm hoặc trường của bạn, chúng tôi sẽ gợi ý qua email và Zalo trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Nhắn Zalo", ZALO)]},
    },
}
