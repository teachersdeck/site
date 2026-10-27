"""TeachersDeck for ClassIn page for _build/pages.py.
Pricing agreed with the owner (2026-10-25): about $50 a year per teacher, set at 1,250,000 VND
(the site converts at about 25,000 VND to the dollar). Centers with 10 or more teachers get a quote.
Facts on the page come from the ClassIn port status notes (classin/PORT-STATUS.md in the suite)."""

from live import section as live_section  # noqa: E402

ORDER = "https://myteachersdeck.com/order/"
QUOTE = "https://myteachersdeck.com/quote/"
SITE = "https://teachersdeck.github.io/teachersdeck-classin/"

CLASSIN = {
    "slug": "classin",
    "demo": SITE + "?demo=1",
    "demo_name": "classin",
    "en": {
        "title": "TeachersDeck for ClassIn: Classroom Widgets on the ClassIn Board",
        "description": "Timers, a traffic light, a noise meter, scoreboards and more, opened in ClassIn's own browser during an online lesson. 1,250,000 VND per teacher per year.",
        "crumb": "TeachersDeck for ClassIn",
        "kicker": "For ClassIn teachers",
        "h1": "TeachersDeck for ClassIn",
        "lede": "Put TeachersDeck's classroom widgets on your ClassIn board. Open a link in ClassIn's Browser tool and your students see a timer, a traffic light or today's instructions, sized to fill the window. Nothing to install.",
        "try": "Try the live demo",
        "cta": [("Order for ClassIn", ORDER)],
        "sections": [
            {"id": "what", "h2": "What it is", "p": "A version of TeachersDeck built to run inside ClassIn's shared Browser tool.", "blocks": [
                ("tiles", [
                    {"h": "Opens in ClassIn's browser", "p": "No extension and no install. Paste a link into ClassIn's Browser tool and the widgets open straight away, on Windows or Mac."},
                    {"h": "One link, one widget", "p": "A link can open a single widget filling the window, already set up: a 5-minute timer, a scoreboard with your team names, or today's agenda."},
                    {"h": "Students hear the timer", "p": "When time is up, a chime plays and the whole window flashes \"Time's up! · Hết giờ!\", so remote students notice even without sound."},
                    {"h": "Safe on a shared screen", "p": "Every student sees your browser, so widgets with student names, points or progress are switched off in this edition."},
                ]),
            ]},
            {"id": "widgets", "h2": "Widgets you can open with a link", "p": "Seven widgets take ready-made settings in the link, and the full deck is there for everything else.", "blocks": [
                ("chips", ["Timer", "Stopwatch", "Traffic Light", "Noise Meter", "Scoreboard", "Instructions", "Agenda"]),
                ("tiles", [
                    {"h": "Link builder", "p": "Pick a widget, set it up, and copy the link or a QR code. Links work in English and Vietnamese."},
                    {"h": "Lesson packs", "p": "Ready-made sets of links for a whole lesson, from warm-up to exit, so a class runs from one list."},
                    {"h": "Tested inside ClassIn", "p": "Checked in ClassIn's own browser in October 2026: all 8 checks passed, including sound, the microphone and settings that stay saved."},
                ]),
            ]},
            {"id": "pricing", "h2": "Pricing", "p": "One yearly price per teacher.", "blocks": [
                ("table", {"head": ["Plan", "Price per year", "About in USD", "Includes"],
                           "rows": [["TeachersDeck for ClassIn", "1,250,000 VND", "about $50", "One teacher, every widget, link builder, lesson packs and updates"],
                                    ["Centers with 10 or more teachers", "Written quote", "", "Volume pricing and one invoice for the center"]],
                           "note": "Prices in VND, excluding VAT. Try the live demo first: it is free and needs no account."}),
            ]},
            {"id": "faq", "h2": "TeachersDeck for ClassIn questions", "blocks": [
                ("faq", [
                    ("Which ClassIn plans can use it?", "Any ClassIn account that shows the Browser tool in a lesson. If you can open a web page inside a lesson, TeachersDeck works there."),
                    ("Do my students need to do anything?", "No. They see your ClassIn board as usual. Turn on ClassIn's \"Share audio\" so they hear the timer chime."),
                    ("Can I use the Noise Meter in ClassIn?", "Yes. It works alongside ClassIn's own use of your microphone; this was checked in a real ClassIn lesson."),
                    ("Is it the same as the TeachersDeck Chrome extension?", "It is the same widgets, set up for a shared screen. Already have TeachersDeck Pro? Ask us about adding ClassIn."),
                ]),
            ]},
        ],
        "band": {"h2": "Bring TeachersDeck to your ClassIn lessons", "p": "Order for yourself, or tell us about your center and we'll reply by email and Zalo within one working day.",
                 "links": [("Order for ClassIn", ORDER), ("Request a quote", QUOTE)]},
    },
    "vi": {
        "title": "TeachersDeck cho ClassIn: tiện ích lớp học trên bảng ClassIn",
        "description": "Hẹn giờ, đèn giao thông, đo tiếng ồn, bảng điểm và nhiều hơn nữa, mở ngay trong trình duyệt của ClassIn khi dạy trực tuyến. 1.250.000 VND mỗi giáo viên mỗi năm.",
        "crumb": "TeachersDeck cho ClassIn",
        "kicker": "Dành cho giáo viên dạy trên ClassIn",
        "h1": "TeachersDeck cho ClassIn",
        "lede": "Đưa các tiện ích lớp học của TeachersDeck lên bảng ClassIn. Mở một đường link trong công cụ Trình duyệt của ClassIn, học sinh sẽ thấy đồng hồ hẹn giờ, đèn giao thông hoặc hướng dẫn hôm nay, phóng to vừa cửa sổ. Không cần cài đặt.",
        "try": "Dùng thử bản demo",
        "cta": [("Đặt mua cho ClassIn", ORDER)],
        "sections": [
            {"id": "what", "h2": "Đây là gì", "p": "Một phiên bản TeachersDeck được làm để chạy trong công cụ Trình duyệt dùng chung của ClassIn.", "blocks": [
                ("tiles", [
                    {"h": "Mở trong trình duyệt của ClassIn", "p": "Không cần tiện ích mở rộng, không cần cài đặt. Dán link vào công cụ Trình duyệt của ClassIn là dùng được ngay, trên Windows hoặc Mac."},
                    {"h": "Một link, một tiện ích", "p": "Mỗi link có thể mở một tiện ích vừa cửa sổ, đã cài sẵn: hẹn giờ 5 phút, bảng điểm với tên các đội, hoặc lịch trình buổi học."},
                    {"h": "Học sinh nghe được khi hết giờ", "p": "Khi hết giờ, chuông reo và cả cửa sổ hiện \"Time's up! · Hết giờ!\", để học sinh học từ xa vẫn nhận ra dù không có âm thanh."},
                    {"h": "An toàn trên màn hình chung", "p": "Mọi học sinh đều thấy trình duyệt của bạn, nên các tiện ích có tên, điểm hoặc tiến độ học sinh được tắt trong phiên bản này."},
                ]),
            ]},
            {"id": "widgets", "h2": "Các tiện ích mở được bằng link", "p": "Bảy tiện ích nhận cài đặt sẵn qua link, và toàn bộ bảng tiện ích vẫn có cho mọi việc khác.", "blocks": [
                ("chips", ["Hẹn giờ", "Bấm giờ", "Đèn giao thông", "Đo tiếng ồn", "Bảng điểm", "Hướng dẫn", "Lịch trình"]),
                ("tiles", [
                    {"h": "Công cụ tạo link", "p": "Chọn tiện ích, cài đặt, rồi sao chép link hoặc mã QR. Link dùng được bằng tiếng Anh và tiếng Việt."},
                    {"h": "Bộ link cho bài học", "p": "Các bộ link soạn sẵn cho cả buổi học, từ khởi động đến kết thúc, để cả lớp chạy theo một danh sách."},
                    {"h": "Đã thử trong ClassIn", "p": "Đã kiểm tra trong trình duyệt của ClassIn vào tháng 10/2026: đạt cả 8 bước, gồm âm thanh, micrô và cài đặt được lưu lại."},
                ]),
            ]},
            {"id": "pricing", "h2": "Bảng giá", "p": "Một mức giá mỗi năm cho mỗi giáo viên.", "blocks": [
                ("table", {"head": ["Gói", "Giá mỗi năm", "Khoảng USD", "Bao gồm"],
                           "rows": [["TeachersDeck cho ClassIn", "1.250.000 VND", "khoảng $50", "Một giáo viên, mọi tiện ích, công cụ tạo link, bộ link bài học và cập nhật"],
                                    ["Trung tâm từ 10 giáo viên", "Báo giá bằng văn bản", "", "Giá theo số lượng và một hóa đơn cho trung tâm"]],
                           "note": "Giá tính bằng VND, chưa gồm VAT. Hãy dùng thử bản demo trước: miễn phí và không cần tài khoản."}),
            ]},
            {"id": "faq", "h2": "Câu hỏi về TeachersDeck cho ClassIn", "blocks": [
                ("faq", [
                    ("Gói ClassIn nào dùng được?", "Mọi tài khoản ClassIn có công cụ Trình duyệt trong buổi học. Nếu bạn mở được trang web trong buổi học, TeachersDeck chạy được ở đó."),
                    ("Học sinh có cần làm gì không?", "Không. Học sinh vẫn xem bảng ClassIn như bình thường. Hãy bật \"Chia sẻ âm thanh\" của ClassIn để học sinh nghe được chuông hẹn giờ."),
                    ("Có dùng Đo tiếng ồn trong ClassIn được không?", "Được. Tiện ích này chạy song song với micrô mà ClassIn đang dùng; đã kiểm tra trong một buổi học ClassIn thật."),
                    ("Có giống tiện ích TeachersDeck trên Chrome không?", "Cùng các tiện ích, được thiết lập cho màn hình dùng chung. Đã có TeachersDeck Pro? Hãy hỏi chúng tôi về việc thêm ClassIn."),
                ]),
            ]},
        ],
        "band": {"h2": "Mang TeachersDeck vào buổi học ClassIn", "p": "Đặt mua cho bạn, hoặc cho chúng tôi biết về trung tâm của bạn, chúng tôi sẽ phản hồi qua email và Zalo trong một ngày làm việc.",
                 "links": [("Đặt mua cho ClassIn", ORDER), ("Yêu cầu báo giá", QUOTE)]},
    },
}


for _lang in ("en", "vi"):
    CLASSIN[_lang]["sections"].insert(0, live_section(_lang, CLASSIN["demo"], CLASSIN["demo_name"], "TeachersDeck for ClassIn" if _lang == "en" else "TeachersDeck cho ClassIn"))
