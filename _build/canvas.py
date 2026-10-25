"""TeachersDeck for Canvas page for _build/pages.py.
Pricing agreed with the owner (2026-10-25): the same as ClassIn, 1,250,000 VND (about $50) per teacher
per year; institutions get a quote. Facts on the page come from the Canvas port status notes
(canvas/canvas/PORT-STATUS.md in the suite): LTI 1.3 launch, 26 widgets (canvas/js/platform.js), launch-only (no roster or
gradebook access), tested on the saLTIre LTI test platform but not yet in a real Canvas course, so the
page offers a pilot rather than claiming Canvas certification."""

ORDER = "https://myteachersdeck.com/order/"
QUOTE = "https://myteachersdeck.com/quote/"
SITE = "https://teachersdeck.github.io/teachersdeck-canvas/"

CANVAS = {
    "slug": "canvas",
    "demo": SITE + "?demo=1",
    "demo_name": "canvas",
    "en": {
        "title": "TeachersDeck for Canvas: Classroom Widgets Inside Your Canvas Courses",
        "description": "Timers, a traffic light, a noise meter, a name picker and more, launched from any Canvas course with LTI 1.3. 1,250,000 VND per teacher per year.",
        "crumb": "TeachersDeck for Canvas",
        "kicker": "For schools and universities on Canvas",
        "h1": "TeachersDeck for Canvas",
        "lede": "Open TeachersDeck's classroom widgets straight from a Canvas course. Teachers click it in the course menu and they are signed in already: no extension, no extra account, nothing to install.",
        "try": "Try the live demo",
        "cta": [("Order for Canvas", ORDER)],
        "sections": [
            {"id": "what", "h2": "What it is", "p": "A version of TeachersDeck that Canvas launches like any other course tool.", "blocks": [
                ("tiles", [
                    {"h": "Opens from the course", "p": "TeachersDeck appears in the Canvas course menu. One click opens the deck, ready to show on the classroom screen."},
                    {"h": "Signed in through Canvas", "p": "Canvas tells TeachersDeck who the teacher is, using the LTI 1.3 standard, so there is no separate login or password."},
                    {"h": "Teachers only", "p": "Teachers and teaching assistants get the deck. Students who open it see a short note to ask their teacher."},
                    {"h": "No roster or gradebook access", "p": "TeachersDeck asks Canvas for nothing beyond the launch: it never reads your class lists, grades or submissions."},
                ]),
            ]},
            {"id": "widgets", "h2": "The 26 widgets in the Canvas edition", "p": "Board tools, the DrawDeck whiteboard, polls, group maker, games, language tools and media: everything that needs no student records.", "blocks": [
                ("chips", ["Clock", "Timer", "Stopwatch", "Countdown", "Traffic Light", "Scoreboard", "Noise Meter", "Instructions Display", "Dice", "Checklist", "QR Code Generator", "Agenda Board", "Name Picker", "Hall Pass Tracker", "Calendar", "DrawDeck whiteboard", "Poll", "Group Maker", "Games", "Grammar Reference", "Idiom of the Day", "Conversation Cards", "Text-to-Speech Reader", "Music Player", "Video Player", "Files"]),
                ("tiles", [
                    {"h": "Easy for your Canvas admin", "p": "Your admin adds TeachersDeck once for the whole institution, using Canvas's own setup for LTI tools. We guide them through it."},
                    {"h": "One licence for the institution", "p": "Pro is switched on for the whole school at once, so every teacher who launches it from Canvas gets every widget."},
                    {"h": "English and Vietnamese", "p": "The deck opens in the language of the teacher's Canvas account."},
                ]),
            ]},
            {"id": "pricing", "h2": "Pricing and the pilot", "p": "The same yearly price per teacher as TeachersDeck for ClassIn. We are now running a pilot with schools and universities in Vietnam: we set it up with your Canvas admin and stay in touch through the first weeks.", "blocks": [
                ("table", {"head": ["Plan", "Price per year", "About in USD", "Includes"],
                           "rows": [["TeachersDeck for Canvas", "1,250,000 VND", "about $50", "One teacher, all 26 widgets, setup help and updates"],
                                    ["Schools and universities with 10 or more teachers", "Written quote", "", "Volume pricing and one invoice for the institution"]],
                           "note": "Prices in VND, excluding VAT. Try the live demo first: it is free and needs no account. In the demo the widgets open with example data; in Canvas they open from your course."}),
            ]},
            {"id": "faq", "h2": "TeachersDeck for Canvas questions", "blocks": [
                ("faq", [
                    ("Who has to set it up?", "Your Canvas admin, once, for the whole institution. After that every teacher finds TeachersDeck in their courses."),
                    ("What does TeachersDeck see from Canvas?", "Only what a launch needs: who the teacher is, their role and their language. It requests no access to rosters, grades or submissions."),
                    ("Do students use it?", "Not in this edition. Students see the deck on the classroom screen; StudentDeck and ParentDeck connected to Canvas are planned after the pilot."),
                    ("Is it the same as the TeachersDeck Chrome extension?", "It is the same widgets, launched from Canvas instead of the browser's new tab. Already have TeachersDeck Pro? Ask us about adding Canvas."),
                ]),
            ]},
        ],
        "band": {"h2": "Bring TeachersDeck into your Canvas courses", "p": "Order for yourself, or tell us about your school or university and we'll reply by email and Zalo within one working day.",
                 "links": [("Order for Canvas", ORDER), ("Request a quote", QUOTE)]},
    },
    "vi": {
        "title": "TeachersDeck cho Canvas: tiện ích lớp học ngay trong khóa học Canvas",
        "description": "Hẹn giờ, đèn giao thông, đo tiếng ồn, chọn tên ngẫu nhiên và nhiều hơn nữa, mở từ mọi khóa học Canvas qua LTI 1.3. 1.250.000 VND mỗi giáo viên mỗi năm.",
        "crumb": "TeachersDeck cho Canvas",
        "kicker": "Dành cho trường học và đại học dùng Canvas",
        "h1": "TeachersDeck cho Canvas",
        "lede": "Mở các tiện ích lớp học của TeachersDeck ngay từ khóa học Canvas. Giáo viên bấm vào trong menu khóa học là đã đăng nhập sẵn: không cần tiện ích mở rộng, không cần thêm tài khoản, không cần cài đặt.",
        "try": "Dùng thử bản demo",
        "cta": [("Đặt mua cho Canvas", ORDER)],
        "sections": [
            {"id": "what", "h2": "Đây là gì", "p": "Một phiên bản TeachersDeck được Canvas mở như mọi công cụ khóa học khác.", "blocks": [
                ("tiles", [
                    {"h": "Mở từ khóa học", "p": "TeachersDeck có trong menu khóa học Canvas. Một cú bấm là mở bảng tiện ích, sẵn sàng chiếu lên màn hình lớp học."},
                    {"h": "Đăng nhập qua Canvas", "p": "Canvas cho TeachersDeck biết giáo viên là ai theo chuẩn LTI 1.3, nên không cần đăng nhập hay mật khẩu riêng."},
                    {"h": "Chỉ dành cho giáo viên", "p": "Giáo viên và trợ giảng dùng được bảng tiện ích. Học sinh mở ra sẽ thấy lời nhắn hỏi giáo viên."},
                    {"h": "Không truy cập danh sách lớp hay sổ điểm", "p": "TeachersDeck không yêu cầu Canvas gì ngoài việc mở công cụ: không bao giờ đọc danh sách lớp, điểm hay bài nộp."},
                ]),
            ]},
            {"id": "widgets", "h2": "26 tiện ích trong phiên bản Canvas", "p": "Công cụ trình chiếu, bảng trắng DrawDeck, bình chọn, chia nhóm, trò chơi, công cụ ngôn ngữ và đa phương tiện: mọi thứ không cần dữ liệu học sinh.", "blocks": [
                ("chips", ["Đồng hồ", "Hẹn giờ", "Bấm giờ", "Đếm ngược", "Đèn giao thông", "Bảng điểm", "Đo tiếng ồn", "Hiển thị hướng dẫn", "Xúc xắc", "Danh sách việc", "Tạo mã QR", "Bảng lịch trình", "Chọn tên", "Theo dõi ra khỏi lớp", "Lịch", "Bảng trắng DrawDeck", "Bình chọn", "Chia nhóm", "Trò chơi", "Tra cứu ngữ pháp", "Thành ngữ mỗi ngày", "Thẻ hội thoại", "Đọc văn bản thành tiếng", "Nghe nhạc", "Xem video", "Tệp"]),
                ("tiles", [
                    {"h": "Dễ cho quản trị Canvas", "p": "Quản trị viên thêm TeachersDeck một lần cho cả trường, bằng cách thiết lập công cụ LTI có sẵn của Canvas. Chúng tôi hướng dẫn từng bước."},
                    {"h": "Một giấy phép cho cả trường", "p": "Bản Pro được bật cho cả trường cùng lúc, nên mọi giáo viên mở từ Canvas đều có đủ tiện ích."},
                    {"h": "Tiếng Anh và tiếng Việt", "p": "Bảng tiện ích mở bằng ngôn ngữ của tài khoản Canvas của giáo viên."},
                ]),
            ]},
            {"id": "pricing", "h2": "Bảng giá và chương trình thí điểm", "p": "Cùng mức giá mỗi năm cho mỗi giáo viên như TeachersDeck cho ClassIn. Chúng tôi đang thí điểm với các trường học và đại học tại Việt Nam: cùng quản trị Canvas của bạn thiết lập và đồng hành trong những tuần đầu.", "blocks": [
                ("table", {"head": ["Gói", "Giá mỗi năm", "Khoảng USD", "Bao gồm"],
                           "rows": [["TeachersDeck cho Canvas", "1.250.000 VND", "khoảng $50", "Một giáo viên, đủ 26 tiện ích, hỗ trợ thiết lập và cập nhật"],
                                    ["Trường học và đại học từ 10 giáo viên", "Báo giá bằng văn bản", "", "Giá theo số lượng và một hóa đơn cho nhà trường"]],
                           "note": "Giá tính bằng VND, chưa gồm VAT. Hãy dùng thử bản demo trước: miễn phí và không cần tài khoản. Trong bản demo các tiện ích mở với dữ liệu mẫu; trong Canvas chúng mở từ khóa học của bạn."}),
            ]},
            {"id": "faq", "h2": "Câu hỏi về TeachersDeck cho Canvas", "blocks": [
                ("faq", [
                    ("Ai cần thiết lập?", "Quản trị viên Canvas của trường, một lần cho cả trường. Sau đó mọi giáo viên đều thấy TeachersDeck trong khóa học của mình."),
                    ("TeachersDeck thấy gì từ Canvas?", "Chỉ những gì cần để mở công cụ: giáo viên là ai, vai trò và ngôn ngữ. Không yêu cầu truy cập danh sách lớp, điểm hay bài nộp."),
                    ("Học sinh có dùng không?", "Chưa có trong phiên bản này. Học sinh xem bảng tiện ích trên màn hình lớp học; StudentDeck và ParentDeck kết nối Canvas dự kiến có sau đợt thí điểm."),
                    ("Có giống tiện ích TeachersDeck trên Chrome không?", "Cùng các tiện ích, nhưng mở từ Canvas thay vì từ tab mới của trình duyệt. Đã có TeachersDeck Pro? Hãy hỏi chúng tôi về việc thêm Canvas."),
                ]),
            ]},
        ],
        "band": {"h2": "Đưa TeachersDeck vào khóa học Canvas", "p": "Đặt mua cho bạn, hoặc cho chúng tôi biết về trường của bạn, chúng tôi sẽ phản hồi qua email và Zalo trong một ngày làm việc.",
                 "links": [("Đặt mua cho Canvas", ORDER), ("Yêu cầu báo giá", QUOTE)]},
    },
}
