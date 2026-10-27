"""Page content for _build/pages.py. Prices follow TeachersDeck Pricing Sheet v2."""

QUOTE = "https://myteachersdeck.com/quote/"
DEMO = "https://myteachersdeck.com/demo/"
ORDER = "https://myteachersdeck.com/order/"

INTERNATIONAL = {
    "slug": "international-schools",
    "en": {
        "title": "TeachersDeck Suite for International Schools: Seat Fees",
        "description": "Classroom tools for international schools in Vietnam: a campus plan plus a yearly seat fee per student and parent. Worked example and FAQ.",
        "crumb": "International schools",
        "kicker": "For international and private schools",
        "h1": "TeachersDeck Suite for international schools",
        "lede": "One campus plan for your teachers, plus a small yearly seat fee for every student and parent. Teachers, students, families and leaders work from one shared system, in English and Vietnamese.",
        "sections": [
            {"id": "gets", "h2": "What your school gets", "p": "Suite campus plans add StudentDeck, ParentDeck and AdminDeck to TeachersDeck.", "blocks": [
                ("tiles", [
                    {"h": "TeachersDeck Pro for every teacher", "p": "Every teacher seat on a campus plan includes TeachersDeck Pro, so teachers never need a personal subscription."},
                    {"h": "StudentDeck for every student", "p": "Students join with a class code and a PIN. No email address and no personal account."},
                    {"h": "ParentDeck for families", "p": "A read-only view of points, homework, reading and teacher notes, updated in real time."},
                    {"h": "AdminDeck for leaders", "p": "Every class in one place: activity, homework completion, join codes, rosters and people."},
                ]),
            ]},
            {"id": "fees", "h2": "Seat fees, per year", "p": "International schools pay a campus plan plus a seat fee for each student and parent.", "blocks": [
                ("table", {"head": ["Seat", "Price per year", "About in USD", "Notes"],
                           "rows": [["Student", "100,000 VND", "about $4", "Each student"],
                                    ["Parent", "500,000 VND", "about $19", "Each parent"]],
                           "note": "Seat fees are charged on top of the campus plan. Private schools and language centers pay no seat fees."}),
                ("h3", "Suite campus plans", "Yearly prices are 10 months, so two months are free."),
                ("table", {"head": ["Plan", "Teachers", "Students", "Per month", "Per year", "Founding rate*"],
                           "rows": [["Suite Starter", "up to 8", "up to 150", "1,500,000 VND", "15,000,000 VND", "1,050,000 VND / month"],
                                    ["Suite Standard", "up to 20", "up to 400", "3,000,000 VND", "30,000,000 VND", "2,100,000 VND / month"],
                                    ["Suite Growth", "up to 40", "up to 900", "5,200,000 VND", "52,000,000 VND", "3,640,000 VND / month"]],
                           "note": "*Founding rate: 30% off the campus plan for 12 months for schools that join through the 30-day free pilot. Extra teacher seat 90,000 VND / month."}),
            ]},
            {"id": "example", "h2": "Example: 10 teachers, 100 students, 100 to 150 parents", "p": "This school needs Suite Starter plus 2 extra teachers: 15,000,000 + (2 × 90,000 × 12) = 17,160,000 VND a year.", "blocks": [
                ("table", {"head": ["Per year", "International school", "Private school", "Language center"],
                           "rows": [["Campus plan", "17,160,000 VND", "17,160,000 VND", "17,160,000 VND"],
                                    ["100 student seats", "10,000,000 VND", "None", "None"],
                                    ["100 to 150 parent seats", "50,000,000 to 75,000,000 VND", "None", "None"],
                                    ["!Total per year", "77,160,000 to 102,160,000 VND", "17,160,000 VND", "17,160,000 VND"],
                                    ["!Total with founding rate", "74,760,000 to 99,760,000 VND", "14,760,000 VND", "14,760,000 VND"]],
                           "note": "In USD: about $2,934 to $3,884 a year ($2,843 to $3,793 with the founding rate). Prices in VND, excluding VAT; USD about 26,300 VND per USD."}),
            ]},
            {"id": "why", "h2": "Built for international schools", "blocks": [
                ("tiles", [
                    {"h": "English and Vietnamese", "p": "TeachersDeck, ParentDeck and AdminDeck work in English and Tiếng Việt, so teachers and families each use their own language. StudentDeck is in English."},
                    {"h": "Careful with children's data", "p": "No student email or account. Class rankings are anonymised by default, and parent screens are read-only."},
                    {"h": "Try it first", "p": "A 30-day free pilot with up to 5 classrooms, free setup and no card needed."},
                    {"h": "One invoice, VAT included", "p": "Prices exclude VAT and VAT invoices are available. Groups of 4 or more campuses get 10% to 20% off list price."},
                ]),
            ]},
            {"id": "faq", "h2": "Questions from international schools", "blocks": [
                ("faq", [
                    ("What are seat fees?", "International schools pay 100,000 VND per student and 500,000 VND per parent each year, on top of the campus plan. Private schools and language centers do not pay seat fees."),
                    ("Who pays for student licences?", "The school, through the Suite campus plan. Families never pay twice for the same child; ParentDeck Pro stays optional."),
                    ("Can we try before we pay?", "Yes. The 30-day free pilot gives up to 5 classrooms, free setup and no card needed."),
                    ("What does the founding rate mean?", "Schools that join through the pilot get 30% off the campus plan for 12 months. Suite Starter at the founding rate is 1,050,000 VND a month."),
                    ("Do prices include VAT?", "No. Prices exclude VAT, and VAT invoices are available."),
                ]),
            ]},
        ],
        "band": {"h2": "Get a written quote for your school", "p": "Tell us your number of teachers, students and parents, and we'll reply by email and Zalo within one working day.",
                 "links": [("Request a quote", QUOTE), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "TeachersDeck Suite cho trường quốc tế: Phí người dùng",
        "description": "Công cụ lớp học cho trường quốc tế tại Việt Nam: gói cơ sở cộng phí mỗi năm cho mỗi học sinh và phụ huynh. Có ví dụ tính giá và câu hỏi thường gặp.",
        "crumb": "Trường quốc tế",
        "kicker": "Dành cho trường quốc tế và trường tư thục",
        "h1": "TeachersDeck Suite cho trường quốc tế",
        "lede": "Một gói cơ sở cho giáo viên, cộng một khoản phí nhỏ mỗi năm cho mỗi học sinh và phụ huynh. Giáo viên, học sinh, gia đình và ban giám hiệu làm việc trên cùng một hệ thống, bằng tiếng Anh và tiếng Việt.",
        "sections": [
            {"id": "gets", "h2": "Nhà trường nhận được gì", "p": "Các gói cơ sở Suite bổ sung StudentDeck, ParentDeck và AdminDeck cho TeachersDeck.", "blocks": [
                ("tiles", [
                    {"h": "TeachersDeck Pro cho mọi giáo viên", "p": "Mỗi tài khoản giáo viên trong gói cơ sở đã gồm TeachersDeck Pro, nên giáo viên không cần đăng ký riêng."},
                    {"h": "StudentDeck cho mọi học sinh", "p": "Học sinh vào lớp bằng mã lớp và mã PIN. Không cần email, không cần tài khoản cá nhân."},
                    {"h": "ParentDeck cho gia đình", "p": "Xem điểm, bài tập, việc đọc và ghi chú của giáo viên, cập nhật theo thời gian thực, chỉ để xem."},
                    {"h": "AdminDeck cho ban giám hiệu", "p": "Mọi lớp ở cùng một nơi: mức hoạt động, tỷ lệ hoàn thành bài, mã tham gia, danh sách lớp và con người."},
                ]),
            ]},
            {"id": "fees", "h2": "Phí theo người dùng, mỗi năm", "p": "Trường quốc tế trả gói cơ sở cộng phí cho mỗi học sinh và phụ huynh.", "blocks": [
                ("table", {"head": ["Đối tượng", "Giá mỗi năm", "Khoảng USD", "Ghi chú"],
                           "rows": [["Học sinh", "100.000 VND", "khoảng $4", "Mỗi học sinh"],
                                    ["Phụ huynh", "500.000 VND", "khoảng $19", "Mỗi phụ huynh"]],
                           "note": "Phí theo người dùng được tính thêm vào gói cơ sở. Trường tư thục và trung tâm ngoại ngữ không trả phí này."}),
                ("h3", "Gói cơ sở Suite", "Giá theo năm tính 10 tháng, tức tặng 2 tháng."),
                ("table", {"head": ["Gói", "Giáo viên", "Học sinh", "Mỗi tháng", "Mỗi năm", "Giá sáng lập*"],
                           "rows": [["Suite Starter", "tối đa 8", "tối đa 150", "1.500.000 VND", "15.000.000 VND", "1.050.000 VND / tháng"],
                                    ["Suite Standard", "tối đa 20", "tối đa 400", "3.000.000 VND", "30.000.000 VND", "2.100.000 VND / tháng"],
                                    ["Suite Growth", "tối đa 40", "tối đa 900", "5.200.000 VND", "52.000.000 VND", "3.640.000 VND / tháng"]],
                           "note": "*Giá sáng lập: giảm 30% gói cơ sở trong 12 tháng cho trường tham gia qua chương trình dùng thử 30 ngày miễn phí. Thêm tài khoản giáo viên 90.000 VND / tháng."}),
            ]},
            {"id": "example", "h2": "Ví dụ: 10 giáo viên, 100 học sinh, 100 đến 150 phụ huynh", "p": "Trường này cần gói Suite Starter cộng 2 tài khoản giáo viên: 15.000.000 + (2 × 90.000 × 12) = 17.160.000 VND mỗi năm.", "blocks": [
                ("table", {"head": ["Mỗi năm", "Trường quốc tế", "Trường tư thục", "Trung tâm ngoại ngữ"],
                           "rows": [["Gói cơ sở", "17.160.000 VND", "17.160.000 VND", "17.160.000 VND"],
                                    ["100 học sinh", "10.000.000 VND", "Không", "Không"],
                                    ["100 đến 150 phụ huynh", "50.000.000 đến 75.000.000 VND", "Không", "Không"],
                                    ["!Tổng mỗi năm", "77.160.000 đến 102.160.000 VND", "17.160.000 VND", "17.160.000 VND"],
                                    ["!Tổng với giá sáng lập", "74.760.000 đến 99.760.000 VND", "14.760.000 VND", "14.760.000 VND"]],
                           "note": "Quy đổi USD: khoảng $2.934 đến $3.884 mỗi năm ($2.843 đến $3.793 với giá sáng lập). Giá tính bằng VND, chưa gồm VAT; khoảng 26.300 VND/USD."}),
            ]},
            {"id": "why", "h2": "Phù hợp với trường quốc tế", "blocks": [
                ("tiles", [
                    {"h": "Tiếng Anh và tiếng Việt", "p": "TeachersDeck, ParentDeck và AdminDeck có tiếng Anh và tiếng Việt, để giáo viên và gia đình dùng ngôn ngữ của mình. StudentDeck hiện bằng tiếng Anh."},
                    {"h": "Cẩn trọng với dữ liệu trẻ em", "p": "Học sinh không cần email hay tài khoản. Bảng xếp hạng mặc định ẩn danh, màn hình phụ huynh chỉ để xem."},
                    {"h": "Dùng thử trước", "p": "Chương trình dùng thử 30 ngày miễn phí, tối đa 5 lớp, miễn phí cài đặt, không cần thẻ."},
                    {"h": "Một hóa đơn, có VAT", "p": "Giá chưa gồm VAT và có xuất hóa đơn VAT. Hệ thống từ 4 cơ sở được giảm 10% đến 20% trên giá niêm yết."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi từ trường quốc tế", "blocks": [
                ("faq", [
                    ("Phí theo người dùng là gì?", "Trường quốc tế trả 100.000 VND cho mỗi học sinh và 500.000 VND cho mỗi phụ huynh mỗi năm, cộng vào gói cơ sở. Trường tư thục và trung tâm ngoại ngữ không trả phí này."),
                    ("Ai trả bản quyền cho học sinh?", "Nhà trường, qua gói cơ sở Suite. Gia đình không phải trả hai lần cho cùng một học sinh; ParentDeck Pro vẫn là tùy chọn."),
                    ("Chúng tôi có thể dùng thử trước không?", "Có. Chương trình dùng thử 30 ngày miễn phí gồm tối đa 5 lớp, miễn phí cài đặt và không cần thẻ."),
                    ("Giá sáng lập nghĩa là gì?", "Trường tham gia qua chương trình dùng thử được giảm 30% gói cơ sở trong 12 tháng. Suite Starter với giá sáng lập là 1.050.000 VND mỗi tháng."),
                    ("Giá đã gồm VAT chưa?", "Chưa. Giá chưa gồm VAT, và có xuất hóa đơn VAT."),
                ]),
            ]},
        ],
        "band": {"h2": "Nhận báo giá bằng văn bản cho trường bạn", "p": "Cho chúng tôi biết số giáo viên, học sinh và phụ huynh, chúng tôi sẽ phản hồi qua email và Zalo trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)]},
    },
}

from apps import APPS  # noqa: E402
from centers import LANGUAGE_CENTERS  # noqa: E402
from universities import UNIVERSITIES  # noqa: E402
from classin import CLASSIN  # noqa: E402
from canvas import CANVAS  # noqa: E402
from pricing import PRICING  # noqa: E402
from support import SUPPORT  # noqa: E402

from intl import apply as _intl_extras  # noqa: E402
_intl_extras(INTERNATIONAL)

PAGES = [*APPS, CLASSIN, CANVAS, PRICING, LANGUAGE_CENTERS, INTERNATIONAL, UNIVERSITIES, SUPPORT]
