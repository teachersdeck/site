"""App pages for _build/pages.py. Features are limited to what shipped in the released
versions (TeachersDeck 0.25.0, StudentDeck 0.13.0, ParentDeck 0.21.6, AdminDeck 0.12.0);
newer work in the monorepo is left out until it is released."""

QUOTE = "https://myteachersdeck.com/quote/"
DEMO = "https://myteachersdeck.com/demo/"
ORDER = "https://myteachersdeck.com/order/"

TEACHERSDECK = {
    "slug": "teachersdeck",
    "demo": "teachersdeck/",
    "app": {"name": "TeachersDeck", "version": "0.25.0", "os": "Chrome (new tab extension)"},
    "en": {
        "title": "TeachersDeck: Classroom Widgets and Reward Points for Teachers",
        "description": "40+ classroom widgets on Chrome's new tab: timers, name picker, group maker, attendance, reward points and a whiteboard. Free plan; Pro from 2,100,000 VND/year.",
        "crumb": "TeachersDeck",
        "kicker": "For teachers",
        "h1": "TeachersDeck: your classroom on one screen",
        "lede": "A wall of draggable classroom widgets that opens every time you open a new tab in Chrome: timers, name picker, group maker, attendance, reward points, polls, a full whiteboard and a lesson planner.",
        "cta": [("Order TeachersDeck Pro", ORDER), ("Book a demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "Everything a lesson needs", "blocks": [
                ("tiles", [
                    {"h": "Run the room", "p": "Clock, timer, stopwatch, traffic light, noise meter, dice and a name picker, ready at the front of the class."},
                    {"h": "Know your class", "p": "Class Builder with Vietnamese and English names, attendance, student stats and progress reports."},
                    {"h": "Motivate with points", "p": "Badges and reward points, a scoreboard and a rewards catalog that students see in StudentDeck."},
                    {"h": "Teach on a whiteboard", "p": "DrawDeck: pens, shapes, text, mind maps, flowcharts, math tools and templates, exported to PNG or PDF."},
                    {"h": "Plan and assign", "p": "Lesson planner, assignments, calendar, agenda board, checklists and exit tickets."},
                    {"h": "Talk to families", "p": "Notes home with sent-and-read tracking, and progress reports that parents see in ParentDeck."},
                ]),
            ]},
            {"id": "widgets", "h2": "Free and Pro widgets", "p": "The free plan is a complete classroom toolkit. Pro adds media, games and extra teaching tools.", "blocks": [
                ("h3", "Free"),
                ("chips", ["Class Builder", "Cloud Class", "Badges & Rewards", "Notes Home", "Student Stats", "Progress Reports", "Assignments",
                           "Calendar", "Attendance", "Name Picker", "Stats & XP", "Badge Display Case", "Files", "Clock", "Timer", "Stopwatch",
                           "Countdown", "Traffic Light", "Dice", "Checklist", "Agenda Board"]),
                ("h3", "Pro"),
                ("chips", ["DrawDeck whiteboard", "Lesson Planner", "Games", "Scoreboard", "Poll", "Exit Ticket", "Group Maker", "Noise Meter",
                           "Music Player", "Video Player", "Soundboard", "Google Meet", "QR Code Generator", "Hall Pass Tracker", "Reading Timer & Log",
                           "Text-to-Speech Reader", "Unit Converter", "Announcements", "Instructions Display", "Conversation Cards",
                           "Idiom of the Day", "Grammar Reference"]),
                ("table", {"head": ["Plan", "Billing", "Price", "Works out to"],
                           "rows": [["Free", "No billing", "0 VND", "Free forever"],
                                    ["Pro", "Monthly", "240,000 VND", "240,000 VND / month"],
                                    ["Pro", "Yearly", "2,100,000 VND", "175,000 VND / month"],
                                    ["Founding Teacher", "Yearly, first 100 teachers", "1,300,000 VND", "About 108,000 VND / month"]],
                           "note": "Teaching at a center or school on a campus plan? TeachersDeck Pro is already included for every teacher seat. Prices in VND, excluding VAT."}),
            ]},
            {"id": "vietnam", "h2": "Made for Vietnamese classrooms", "blocks": [
                ("tiles", [
                    {"h": "Vietnamese names, done right", "p": "Separate Họ, Tên đệm and Tên columns with an optional English name, and sorting by given name the Vietnamese way."},
                    {"h": "Lunar calendar", "p": "Show Gregorian dates, Âm lịch or both, in the Calendar and on the clock."},
                    {"h": "English and Tiếng Việt", "p": "Switch the whole interface between English and Vietnamese in one click."},
                ]),
            ]},
            {"id": "connect", "h2": "Works alone, connects when you want", "blocks": [
                ("tiles", [
                    {"h": "Your data stays on your device", "p": "Classes, files and boards are stored in your browser. Nothing goes online unless you turn on Cloud Class."},
                    {"h": "Cloud Class", "p": "Sign in with Google to give students a class code and families their own codes. Points, homework and notes then sync."},
                    {"h": "Careful with children", "p": "Class rankings are anonymised by default, and attendance is only shared with families if you turn it on."},
                ]),
            ]},
            {"id": "faq", "h2": "TeachersDeck questions", "blocks": [
                ("faq", [
                    ("Is TeachersDeck free?", "Yes. The free plan covers the everyday classroom tools. Pro costs 240,000 VND a month or 2,100,000 VND a year, and the first 100 teachers can lock in 1,300,000 VND a year."),
                    ("What do I need to run it?", "Chrome on Windows, Mac or a Chromebook. TeachersDeck opens as your new tab page."),
                    ("Do my students need accounts?", "No. If you use Cloud Class, students join with a class code and a PIN, with no email address."),
                    ("Does my school pay instead?", "On a school or center campus plan, TeachersDeck Pro is included for every teacher seat."),
                ]),
            ]},
        ],
        "band": {"h2": "Bring TeachersDeck to your classroom", "p": "Start free, or order Pro and we'll confirm by email and Zalo within one working day.",
                 "links": [("Order Pro", ORDER), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "TeachersDeck: Tiện ích lớp học và điểm thưởng cho giáo viên",
        "description": "Hơn 40 tiện ích lớp học trên tab mới Chrome: hẹn giờ, chọn tên, chia nhóm, điểm danh, điểm thưởng và bảng trắng. Có gói miễn phí; Pro từ 2.100.000 VND/năm.",
        "crumb": "TeachersDeck",
        "kicker": "Dành cho giáo viên",
        "h1": "TeachersDeck: cả lớp học trên một màn hình",
        "lede": "Một bức tường tiện ích lớp học kéo thả được, mở ra mỗi khi bạn mở tab mới trên Chrome: đồng hồ, chọn tên, chia nhóm, điểm danh, điểm thưởng, bình chọn, bảng trắng đầy đủ và công cụ soạn giáo án.",
        "cta": [("Đặt mua TeachersDeck Pro", ORDER), ("Đặt lịch demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "Mọi thứ một tiết học cần", "blocks": [
                ("tiles", [
                    {"h": "Điều hành lớp học", "p": "Đồng hồ, hẹn giờ, bấm giờ, đèn giao thông, đo tiếng ồn, xúc xắc và chọn tên, sẵn sàng trên bảng."},
                    {"h": "Hiểu lớp của bạn", "p": "Class Builder với tên tiếng Việt và tiếng Anh, điểm danh, thống kê học sinh và báo cáo tiến độ."},
                    {"h": "Khích lệ bằng điểm thưởng", "p": "Huy hiệu và điểm thưởng, bảng điểm và danh mục phần thưởng mà học sinh thấy trong StudentDeck."},
                    {"h": "Dạy trên bảng trắng", "p": "DrawDeck: bút, hình, chữ, sơ đồ tư duy, lưu đồ, công cụ toán và mẫu có sẵn, xuất ra PNG hoặc PDF."},
                    {"h": "Soạn bài và giao bài", "p": "Soạn giáo án, giao bài tập, lịch, bảng lịch trình, danh sách việc và phiếu cuối giờ."},
                    {"h": "Trao đổi với gia đình", "p": "Ghi chú gửi về nhà có theo dõi đã gửi, đã đọc, và báo cáo tiến độ phụ huynh xem trong ParentDeck."},
                ]),
            ]},
            {"id": "widgets", "h2": "Tiện ích miễn phí và Pro", "p": "Gói miễn phí là một bộ công cụ lớp học đầy đủ. Pro bổ sung đa phương tiện, trò chơi và công cụ giảng dạy.", "blocks": [
                ("h3", "Miễn phí"),
                ("chips", ["Class Builder", "Cloud Class", "Huy hiệu & phần thưởng", "Ghi chú về nhà", "Thống kê học sinh", "Báo cáo tiến độ", "Bài tập",
                           "Lịch", "Điểm danh", "Chọn tên", "Thống kê & XP", "Tủ huy hiệu", "Tệp", "Đồng hồ", "Hẹn giờ", "Bấm giờ",
                           "Đếm ngược", "Đèn giao thông", "Xúc xắc", "Danh sách việc", "Bảng lịch trình"]),
                ("h3", "Pro"),
                ("chips", ["Bảng trắng DrawDeck", "Soạn giáo án", "Trò chơi", "Bảng điểm", "Bình chọn", "Phiếu cuối giờ", "Chia nhóm", "Đo tiếng ồn",
                           "Nghe nhạc", "Xem video", "Bảng âm thanh", "Google Meet", "Tạo mã QR", "Theo dõi ra khỏi lớp", "Hẹn giờ & nhật ký đọc",
                           "Đọc văn bản thành tiếng", "Đổi đơn vị", "Bảng thông báo", "Hiển thị hướng dẫn", "Thẻ hội thoại",
                           "Thành ngữ mỗi ngày", "Tra cứu ngữ pháp"]),
                ("table", {"head": ["Gói", "Thanh toán", "Giá", "Quy ra"],
                           "rows": [["Miễn phí", "Không thanh toán", "0 VND", "Miễn phí mãi mãi"],
                                    ["Pro", "Theo tháng", "240.000 VND", "240.000 VND / tháng"],
                                    ["Pro", "Theo năm", "2.100.000 VND", "175.000 VND / tháng"],
                                    ["Giáo viên sáng lập", "Theo năm, 100 giáo viên đầu tiên", "1.300.000 VND", "Khoảng 108.000 VND / tháng"]],
                           "note": "Dạy tại trung tâm hoặc trường có gói cơ sở? TeachersDeck Pro đã được tính cho mỗi tài khoản giáo viên. Giá tính bằng VND, chưa gồm VAT."}),
            ]},
            {"id": "vietnam", "h2": "Dành cho lớp học Việt Nam", "blocks": [
                ("tiles", [
                    {"h": "Tên tiếng Việt, đúng cách", "p": "Các cột Họ, Tên đệm và Tên riêng, kèm tên tiếng Anh tùy chọn, và sắp xếp theo tên như cách người Việt vẫn làm."},
                    {"h": "Lịch âm", "p": "Hiển thị ngày dương lịch, âm lịch hoặc cả hai, trong Lịch và trên đồng hồ."},
                    {"h": "Tiếng Anh và tiếng Việt", "p": "Chuyển toàn bộ giao diện giữa tiếng Anh và tiếng Việt chỉ với một lần bấm."},
                ]),
            ]},
            {"id": "connect", "h2": "Dùng độc lập, kết nối khi bạn muốn", "blocks": [
                ("tiles", [
                    {"h": "Dữ liệu nằm trên máy của bạn", "p": "Lớp học, tệp và bảng vẽ được lưu trong trình duyệt. Không có gì lên mạng trừ khi bạn bật Cloud Class."},
                    {"h": "Cloud Class", "p": "Đăng nhập bằng Google để cấp mã lớp cho học sinh và mã riêng cho từng gia đình. Điểm, bài tập và ghi chú sẽ được đồng bộ."},
                    {"h": "Cẩn trọng với trẻ em", "p": "Bảng xếp hạng mặc định ẩn danh, và điểm danh chỉ chia sẻ với gia đình khi bạn bật."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi về TeachersDeck", "blocks": [
                ("faq", [
                    ("TeachersDeck có miễn phí không?", "Có. Gói miễn phí gồm các công cụ lớp học hằng ngày. Pro có giá 240.000 VND mỗi tháng hoặc 2.100.000 VND mỗi năm, và 100 giáo viên đầu tiên được giữ giá 1.300.000 VND mỗi năm."),
                    ("Tôi cần gì để sử dụng?", "Chrome trên Windows, Mac hoặc Chromebook. TeachersDeck mở ra như trang tab mới của bạn."),
                    ("Học sinh có cần tài khoản không?", "Không. Nếu dùng Cloud Class, học sinh vào lớp bằng mã lớp và mã PIN, không cần email."),
                    ("Nhà trường có thể chi trả thay không?", "Với gói cơ sở của trường hoặc trung tâm, TeachersDeck Pro đã được tính cho mỗi tài khoản giáo viên."),
                ]),
            ]},
        ],
        "band": {"h2": "Đưa TeachersDeck vào lớp học của bạn", "p": "Bắt đầu miễn phí, hoặc đặt mua Pro và chúng tôi sẽ xác nhận qua email và Zalo trong một ngày làm việc.",
                 "links": [("Đặt mua Pro", ORDER), ("Đặt lịch demo", DEMO)]},
    },
}

STUDENTDECK = {
    "slug": "studentdeck",
    "demo": "studentdeck/",
    "app": {"name": "StudentDeck", "version": "0.13.0", "os": "Chrome (new tab extension)"},
    "en": {
        "title": "StudentDeck: A Study Dashboard Linked to the Class",
        "description": "Focus timer, homework list, reading log, notes and badges on Chrome's new tab. Students join a class with a code and PIN, with no email or account.",
        "crumb": "StudentDeck",
        "kicker": "For students",
        "h1": "StudentDeck: a calm place to study",
        "lede": "A study dashboard that opens on every new tab: a focus timer, homework list, reading log and notes. Join a class with a code to see points, rewards and badges from the teacher.",
        "cta": [("Book a demo", DEMO), ("For parents: ParentDeck", "https://myteachersdeck.com/parentdeck/")],
        "sections": [
            {"id": "features", "h2": "Built for studying", "blocks": [
                ("tiles", [
                    {"h": "Focus timer", "p": "Work in focused blocks, with a clock always in view."},
                    {"h": "Homework and reading", "p": "A homework list to tick off and a reading log that tracks pages and minutes."},
                    {"h": "Notes and files", "p": "A notepad and a file viewer for PDFs and Google Docs, Slides and Sheets links."},
                    {"h": "XP, levels and badges", "p": "Earn XP for steady practice, with daily limits and streaks, and collect badges as you level up."},
                    {"h": "Journey", "p": "A private mood and journal space. The journal stays on the device; only the day's mood word is shared."},
                    {"h": "Class link", "p": "Join your teacher's class to see class points, redeem rewards and get calendar events."},
                ]),
            ]},
            {"id": "pro", "h2": "Extra tools with Pro", "p": "Pro is unlocked by a family's ParentDeck Pro or by the school's plan. Students are never shown prices.", "blocks": [
                ("chips", ["Games Hub", "Translate (14 languages)", "Dictionary", "Flashcards", "Idiom of the Day", "Scrapdeck scrapbook"]),
            ]},
            {"id": "privacy", "h2": "Safe for children by design", "blocks": [
                ("tiles", [
                    {"h": "No email, no account", "p": "Students join with a class code, their name and a 4-digit PIN. There is no student email or Google account."},
                    {"h": "Nothing for sale", "p": "StudentDeck never shows a price or a purchase link. Locked tools simply say to ask a grown-up at home."},
                    {"h": "Private by default", "p": "Journal text never leaves the device, and photos are cleaned of location data when added."},
                ]),
            ]},
            {"id": "faq", "h2": "StudentDeck questions", "blocks": [
                ("faq", [
                    ("Does StudentDeck work without a class?", "Yes. It is a complete study dashboard on its own. Joining a class adds points, rewards and the teacher's calendar."),
                    ("How does a student join a class?", "With the class code from the teacher, their name and a 4-digit PIN. No email address is needed."),
                    ("How do students get Pro?", "Through a family's ParentDeck Pro plan or the school's Suite plan. Students never pay or see prices."),
                    ("Which languages does it support?", "The interface is in English, and the Translate tool covers 14 languages including Vietnamese."),
                ]),
            ]},
        ],
        "band": {"h2": "See StudentDeck with your class", "p": "Book a demo and we'll show how StudentDeck, TeachersDeck and ParentDeck work together.",
                 "links": [("Book a demo", DEMO), ("Request a quote", QUOTE)]},
    },
    "vi": {
        "title": "StudentDeck: Bảng học tập kết nối với lớp học",
        "description": "Hẹn giờ tập trung, bài tập, nhật ký đọc, ghi chú và huy hiệu trên tab mới Chrome. Học sinh vào lớp bằng mã và PIN, không cần email hay tài khoản.",
        "crumb": "StudentDeck",
        "kicker": "Dành cho học sinh",
        "h1": "StudentDeck: một góc học tập yên tĩnh",
        "lede": "Bảng học tập mở ra trên mỗi tab mới: hẹn giờ tập trung, danh sách bài tập, nhật ký đọc và ghi chú. Vào lớp bằng mã để xem điểm, phần thưởng và huy hiệu từ giáo viên.",
        "cta": [("Đặt lịch demo", DEMO), ("Dành cho phụ huynh: ParentDeck", "https://myteachersdeck.com/vi/parentdeck/")],
        "sections": [
            {"id": "features", "h2": "Được làm để học", "blocks": [
                ("tiles", [
                    {"h": "Hẹn giờ tập trung", "p": "Học theo từng khoảng tập trung, với đồng hồ luôn hiển thị."},
                    {"h": "Bài tập và đọc sách", "p": "Danh sách bài tập để đánh dấu và nhật ký đọc theo dõi số trang và số phút."},
                    {"h": "Ghi chú và tệp", "p": "Sổ ghi chú và trình xem tệp cho PDF và liên kết Google Docs, Slides, Sheets."},
                    {"h": "XP, cấp độ và huy hiệu", "p": "Nhận XP khi luyện tập đều đặn, có giới hạn mỗi ngày và chuỗi ngày, và sưu tập huy hiệu khi lên cấp."},
                    {"h": "Hành trình", "p": "Không gian riêng ghi tâm trạng và nhật ký. Nhật ký ở lại trên máy; chỉ từ chỉ tâm trạng trong ngày được chia sẻ."},
                    {"h": "Kết nối lớp học", "p": "Vào lớp của giáo viên để xem điểm lớp, đổi phần thưởng và nhận sự kiện trên lịch."},
                ]),
            ]},
            {"id": "pro", "h2": "Thêm công cụ với Pro", "p": "Pro được mở khi gia đình dùng ParentDeck Pro hoặc nhà trường có gói Suite. Học sinh không bao giờ thấy giá tiền.", "blocks": [
                ("chips", ["Trò chơi", "Dịch (14 ngôn ngữ)", "Từ điển", "Thẻ ghi nhớ", "Thành ngữ mỗi ngày", "Sổ lưu niệm Scrapdeck"]),
            ]},
            {"id": "privacy", "h2": "An toàn cho trẻ em ngay từ thiết kế", "blocks": [
                ("tiles", [
                    {"h": "Không email, không tài khoản", "p": "Học sinh vào lớp bằng mã lớp, tên và mã PIN 4 số. Không có email hay tài khoản Google của học sinh."},
                    {"h": "Không bán hàng", "p": "StudentDeck không bao giờ hiện giá hay liên kết mua hàng. Công cụ bị khóa chỉ nhắc hỏi người lớn ở nhà."},
                    {"h": "Riêng tư mặc định", "p": "Nội dung nhật ký không rời khỏi máy, và ảnh được xóa thông tin vị trí khi thêm vào."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi về StudentDeck", "blocks": [
                ("faq", [
                    ("StudentDeck có dùng được khi không vào lớp không?", "Có. Đây là một bảng học tập đầy đủ. Vào lớp sẽ có thêm điểm, phần thưởng và lịch của giáo viên."),
                    ("Học sinh vào lớp thế nào?", "Bằng mã lớp giáo viên cung cấp, tên và mã PIN 4 số. Không cần email."),
                    ("Học sinh có Pro bằng cách nào?", "Qua gói ParentDeck Pro của gia đình hoặc gói Suite của nhà trường. Học sinh không trả tiền và không thấy giá."),
                    ("StudentDeck hỗ trợ ngôn ngữ nào?", "Giao diện bằng tiếng Anh, và công cụ Dịch hỗ trợ 14 ngôn ngữ, gồm cả tiếng Việt."),
                ]),
            ]},
        ],
        "band": {"h2": "Xem StudentDeck cùng lớp của bạn", "p": "Đặt lịch demo để xem StudentDeck, TeachersDeck và ParentDeck làm việc cùng nhau.",
                 "links": [("Đặt lịch demo", DEMO), ("Yêu cầu báo giá", QUOTE)]},
    },
}

PARENTDECK = {
    "slug": "parentdeck",
    "demo": "parentdeck/",
    "app": {"name": "ParentDeck", "version": "0.21.6", "os": "Chrome (new tab extension)"},
    "en": {
        "title": "ParentDeck: Your Child's Points, Homework and Teacher Notes",
        "description": "A read-only family dashboard: points, homework, attendance, progress reports and teacher notes in real time. Free for one child; Pro from 300,000 VND/year.",
        "crumb": "ParentDeck",
        "kicker": "For families",
        "h1": "ParentDeck: know how school is going",
        "lede": "A read-only dashboard for families, updated in real time from the teacher and your child's StudentDeck: points, homework, attendance, progress reports and notes from the teacher.",
        "cta": [("Order ParentDeck Pro", ORDER), ("Book a demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "Everything in one glance", "blocks": [
                ("tiles", [
                    {"h": "Student summary", "p": "Points, stats, goals and streaks, with a simple status: on track, needs monitoring or off track, and why."},
                    {"h": "Notes from the teacher", "p": "Read the teacher's notes home; the teacher sees when you've read them."},
                    {"h": "Homework and attendance", "p": "What's due, what's done, and attendance when the teacher shares it."},
                    {"h": "Progress reports and calendar", "p": "Reports from the teacher and the class calendar, with Gregorian and lunar dates."},
                    {"h": "Family overview", "p": "Several children? See them side by side."},
                    {"h": "A guide, not a grade", "p": "Practice figures come from your child's device and are shown as activity, never as marks."},
                ]),
            ]},
            {"id": "plans", "h2": "Free and Pro", "p": "ParentDeck Pro also unlocks your child's StudentDeck Pro.", "blocks": [
                ("h3", "Pro adds"),
                ("chips", ["Badge Display Case", "Homework insights", "Rewards Wishlist", "Conversation Starters", "Weekly Digest", "Class Pulse"]),
                ("table", {"head": ["Children", "Per year", "Per month, billed yearly", "Rule"],
                           "rows": [["1 child", "300,000 VND", "25,000 VND", "Full price"],
                                    ["2 children", "510,000 VND", "42,500 VND", "2nd child 30% off"],
                                    ["3 children", "660,000 VND", "55,000 VND", "3rd child and more 50% off"],
                                    ["4 children", "810,000 VND", "67,500 VND", "Same rule applies"]],
                           "note": "Monthly: 30,000 VND per child. ParentDeck Free covers one child, read-only. Founding Family: the first 200 children get 30% off their first year. If the school's plan already pays for your child's StudentDeck licence, you don't pay for it again."}),
            ]},
            {"id": "privacy", "h2": "Private for every family", "blocks": [
                ("tiles", [
                    {"h": "Your child's own code", "p": "You link with a family code for your child only, so families can't see each other's children."},
                    {"h": "Read-only", "p": "ParentDeck never writes anything back to the class."},
                    {"h": "Anonymous rankings", "p": "Class rankings stay anonymous unless the teacher chooses otherwise."},
                ]),
            ]},
            {"id": "faq", "h2": "ParentDeck questions", "blocks": [
                ("faq", [
                    ("How do I link to my child?", "Sign in with Google and enter your child's family code, which the teacher or your child's StudentDeck gives you."),
                    ("How much does ParentDeck cost?", "ParentDeck Free covers one child. Pro is 30,000 VND per child per month or 300,000 VND per child per year, with discounts for brothers and sisters."),
                    ("Can I change anything in the class?", "No. ParentDeck is read-only, so it never changes your child's work, points or the teacher's records."),
                    ("Does it work in Vietnamese?", "Yes. ParentDeck works in English and Vietnamese, and its calendar shows lunar dates."),
                ]),
            ]},
        ],
        "band": {"h2": "Follow your child's progress", "p": "Order ParentDeck Pro and we'll confirm by email and Zalo within one working day.",
                 "links": [("Order ParentDeck Pro", ORDER), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "ParentDeck: Điểm, bài tập và ghi chú giáo viên của con",
        "description": "Bảng thông tin chỉ để xem cho gia đình: điểm, bài tập, điểm danh, báo cáo và ghi chú của giáo viên theo thời gian thực. Pro từ 300.000 VND/năm.",
        "crumb": "ParentDeck",
        "kicker": "Dành cho gia đình",
        "h1": "ParentDeck: biết con học thế nào",
        "lede": "Bảng thông tin chỉ để xem dành cho gia đình, cập nhật theo thời gian thực từ giáo viên và StudentDeck của con: điểm, bài tập, điểm danh, báo cáo tiến độ và ghi chú của giáo viên.",
        "cta": [("Đặt mua ParentDeck Pro", ORDER), ("Đặt lịch demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "Mọi thứ trong một cái nhìn", "blocks": [
                ("tiles", [
                    {"h": "Tóm tắt về con", "p": "Điểm, thống kê, mục tiêu và chuỗi ngày, cùng tình trạng đơn giản: đang tốt, cần theo dõi hoặc chưa đạt, kèm lý do."},
                    {"h": "Ghi chú của giáo viên", "p": "Đọc ghi chú giáo viên gửi về; giáo viên biết khi bạn đã đọc."},
                    {"h": "Bài tập và điểm danh", "p": "Bài nào cần nộp, bài nào đã xong, và điểm danh khi giáo viên chia sẻ."},
                    {"h": "Báo cáo tiến độ và lịch", "p": "Báo cáo của giáo viên và lịch của lớp, có ngày dương lịch và âm lịch."},
                    {"h": "Tổng quan gia đình", "p": "Có nhiều con? Xem các con cạnh nhau."},
                    {"h": "Gợi ý, không phải điểm số", "p": "Số liệu luyện tập đến từ máy của con và được hiển thị như mức hoạt động, không bao giờ là điểm."},
                ]),
            ]},
            {"id": "plans", "h2": "Miễn phí và Pro", "p": "ParentDeck Pro cũng mở khóa StudentDeck Pro cho con.", "blocks": [
                ("h3", "Pro bổ sung"),
                ("chips", ["Tủ huy hiệu", "Phân tích bài tập", "Danh sách phần thưởng mong muốn", "Gợi ý trò chuyện", "Bản tin hằng tuần", "Nhịp lớp học"]),
                ("table", {"head": ["Số con", "Mỗi năm", "Mỗi tháng, trả theo năm", "Quy tắc"],
                           "rows": [["1 con", "300.000 VND", "25.000 VND", "Giá đầy đủ"],
                                    ["2 con", "510.000 VND", "42.500 VND", "Con thứ 2 giảm 30%"],
                                    ["3 con", "660.000 VND", "55.000 VND", "Từ con thứ 3 giảm 50%"],
                                    ["4 con", "810.000 VND", "67.500 VND", "Áp dụng cùng quy tắc"]],
                           "note": "Theo tháng: 30.000 VND mỗi con. ParentDeck Miễn phí dành cho một con, chỉ xem. Gia đình sáng lập: 200 học sinh đầu tiên được giảm 30% năm đầu. Nếu gói của trường đã chi trả bản quyền StudentDeck cho con, bạn không phải trả lại."}),
            ]},
            {"id": "privacy", "h2": "Riêng tư cho từng gia đình", "blocks": [
                ("tiles", [
                    {"h": "Mã riêng của con", "p": "Bạn liên kết bằng mã gia đình chỉ dành cho con mình, nên các gia đình không thể xem con của nhau."},
                    {"h": "Chỉ để xem", "p": "ParentDeck không bao giờ ghi ngược dữ liệu vào lớp học."},
                    {"h": "Xếp hạng ẩn danh", "p": "Bảng xếp hạng lớp được giữ ẩn danh trừ khi giáo viên chọn khác."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi về ParentDeck", "blocks": [
                ("faq", [
                    ("Làm sao để liên kết với con?", "Đăng nhập bằng Google và nhập mã gia đình của con, do giáo viên hoặc StudentDeck của con cung cấp."),
                    ("ParentDeck có giá bao nhiêu?", "ParentDeck Miễn phí dành cho một con. Pro có giá 30.000 VND mỗi con mỗi tháng hoặc 300.000 VND mỗi con mỗi năm, có giảm giá cho anh chị em."),
                    ("Tôi có thể thay đổi gì trong lớp không?", "Không. ParentDeck chỉ để xem, nên không bao giờ thay đổi bài làm, điểm của con hay hồ sơ của giáo viên."),
                    ("ParentDeck có tiếng Việt không?", "Có. ParentDeck có tiếng Anh và tiếng Việt, và lịch hiển thị ngày âm lịch."),
                ]),
            ]},
        ],
        "band": {"h2": "Theo dõi tiến độ của con", "p": "Đặt mua ParentDeck Pro và chúng tôi sẽ xác nhận qua email và Zalo trong một ngày làm việc.",
                 "links": [("Đặt mua ParentDeck Pro", ORDER), ("Đặt lịch demo", DEMO)]},
    },
}

ADMINDECK = {
    "slug": "admindeck",
    "demo": "admindeck/",
    "app": {"name": "AdminDeck", "version": "0.12.0", "os": "Chrome (new tab extension)"},
    "en": {
        "title": "AdminDeck: School Dashboard for Principals and Managers",
        "description": "Every class in one place: school stats, directories, join codes, roster checks, notes to teachers and safety switches. Included in Suite campus plans.",
        "crumb": "AdminDeck",
        "kicker": "For school leaders",
        "h1": "AdminDeck: every class, one dashboard",
        "lede": "A school oversight dashboard for principals, academic directors and center managers: activity, homework completion, join codes, rosters and people, across every class.",
        "cta": [("Request a quote", QUOTE), ("Book a demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "See the whole school", "blocks": [
                ("tiles", [
                    {"h": "School stats", "p": "Tiles, trends and a class-by-class table, with CSV export."},
                    {"h": "Teachers and people", "p": "A teacher directory and a people directory filtered by teachers, students, parents and staff."},
                    {"h": "Notes to teachers", "p": "Send notes to teachers and see when they've been read."},
                    {"h": "Calendar master view", "p": "Every class calendar in one place."},
                    {"h": "Join codes and rosters", "p": "Manage class join codes and catch roster problems before they cause trouble."},
                    {"h": "Student safety switches", "p": "Turn photos, sharing and the rewards shop on or off for the whole school."},
                ]),
            ]},
            {"id": "pro", "h2": "More with Pro", "p": "Pro widgets help leaders track engagement and run the school's setup.", "blocks": [
                ("chips", ["Points & Rewards", "Assignments", "Student Activity Pulse", "Class Onboarding Funnel", "Family Link Coverage",
                           "Teacher Engagement", "SchoolDeck (staff, classes, timetable)", "School themes sent to TeachersDeck"]),
                ("table", {"head": ["Suite plan", "Teachers", "Students", "Admins", "Per month", "Per year"],
                           "rows": [["Suite Starter", "up to 8", "up to 150", "2", "1,500,000 VND", "15,000,000 VND"],
                                    ["Suite Standard", "up to 20", "up to 400", "5", "3,000,000 VND", "30,000,000 VND"],
                                    ["Suite Growth", "up to 40", "up to 900", "Unlimited", "5,200,000 VND", "52,000,000 VND"]],
                           "note": "AdminDeck comes with every Suite campus plan, together with StudentDeck and ParentDeck. Prices in VND, excluding VAT. Chains of 4 or more campuses get 10% to 20% off."}),
            ]},
            {"id": "privacy", "h2": "Oversight without exposing children", "blocks": [
                ("tiles", [
                    {"h": "No student names in stats", "p": "School Stats shows totals and trends, not individual students."},
                    {"h": "Small classes protected", "p": "Classes with fewer than 3 students show no day-by-day trend."},
                    {"h": "Each school sees only itself", "p": "Access is limited on the server, so no school can see another school's data."},
                ]),
            ]},
            {"id": "faq", "h2": "AdminDeck questions", "blocks": [
                ("faq", [
                    ("How do we get AdminDeck?", "AdminDeck is included in every TeachersDeck Suite campus plan, from 1,500,000 VND a month."),
                    ("Can leaders see individual students?", "School Stats shows totals and trends without student names. Directories list people so leaders can manage rosters."),
                    ("Does it work for chains?", "Yes. Groups of 4 or more campuses get one contract, one invoice and a group overview, with 10% to 20% off list price."),
                    ("Which languages does it support?", "AdminDeck works in English and Vietnamese."),
                ]),
            ]},
        ],
        "band": {"h2": "Get AdminDeck for your school", "p": "Tell us about your school and we'll send a written quote within one working day.",
                 "links": [("Request a quote", QUOTE), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "AdminDeck: Bảng điều hành toàn trường cho ban giám hiệu",
        "description": "Mọi lớp ở một nơi: thống kê trường, danh bạ, mã tham gia, kiểm tra danh sách lớp, ghi chú cho giáo viên và công tắc an toàn. Có trong gói Suite.",
        "crumb": "AdminDeck",
        "kicker": "Dành cho ban giám hiệu",
        "h1": "AdminDeck: mọi lớp học, một bảng điều hành",
        "lede": "Bảng điều hành toàn trường cho hiệu trưởng, quản lý học thuật và quản lý trung tâm: mức hoạt động, tỷ lệ hoàn thành bài, mã tham gia, danh sách lớp và con người, trên mọi lớp.",
        "cta": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)],
        "sections": [
            {"id": "features", "h2": "Nhìn thấy toàn trường", "blocks": [
                ("tiles", [
                    {"h": "Thống kê trường", "p": "Ô số liệu, xu hướng và bảng theo từng lớp, có xuất CSV."},
                    {"h": "Giáo viên và mọi người", "p": "Danh bạ giáo viên và danh bạ mọi người, lọc theo giáo viên, học sinh, phụ huynh và nhân viên."},
                    {"h": "Ghi chú cho giáo viên", "p": "Gửi ghi chú cho giáo viên và biết khi họ đã đọc."},
                    {"h": "Lịch tổng", "p": "Lịch của mọi lớp ở cùng một nơi."},
                    {"h": "Mã tham gia và danh sách lớp", "p": "Quản lý mã vào lớp và phát hiện sớm vấn đề trong danh sách lớp."},
                    {"h": "Công tắc an toàn cho học sinh", "p": "Bật hoặc tắt ảnh, chia sẻ và cửa hàng phần thưởng cho toàn trường."},
                ]),
            ]},
            {"id": "pro", "h2": "Thêm với Pro", "p": "Các tiện ích Pro giúp ban giám hiệu theo dõi mức tham gia và quản lý thiết lập của trường.", "blocks": [
                ("chips", ["Điểm & phần thưởng", "Bài tập", "Nhịp hoạt động học sinh", "Tiến trình vào lớp", "Mức liên kết gia đình",
                           "Mức tham gia của giáo viên", "SchoolDeck (nhân sự, lớp, thời khóa biểu)", "Gửi giao diện trường sang TeachersDeck"]),
                ("table", {"head": ["Gói Suite", "Giáo viên", "Học sinh", "Quản trị", "Mỗi tháng", "Mỗi năm"],
                           "rows": [["Suite Starter", "tối đa 8", "tối đa 150", "2", "1.500.000 VND", "15.000.000 VND"],
                                    ["Suite Standard", "tối đa 20", "tối đa 400", "5", "3.000.000 VND", "30.000.000 VND"],
                                    ["Suite Growth", "tối đa 40", "tối đa 900", "Không giới hạn", "5.200.000 VND", "52.000.000 VND"]],
                           "note": "AdminDeck có trong mọi gói cơ sở Suite, cùng với StudentDeck và ParentDeck. Giá tính bằng VND, chưa gồm VAT. Hệ thống từ 4 cơ sở được giảm 10% đến 20%."}),
            ]},
            {"id": "privacy", "h2": "Quản lý mà không làm lộ thông tin trẻ em", "blocks": [
                ("tiles", [
                    {"h": "Không có tên học sinh trong thống kê", "p": "Thống kê trường hiển thị tổng số và xu hướng, không hiển thị từng học sinh."},
                    {"h": "Bảo vệ lớp nhỏ", "p": "Lớp có dưới 3 học sinh không hiển thị xu hướng theo ngày."},
                    {"h": "Mỗi trường chỉ thấy trường mình", "p": "Quyền truy cập được giới hạn trên máy chủ, nên không trường nào xem được dữ liệu của trường khác."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi về AdminDeck", "blocks": [
                ("faq", [
                    ("Làm sao để có AdminDeck?", "AdminDeck có trong mọi gói cơ sở TeachersDeck Suite, từ 1.500.000 VND mỗi tháng."),
                    ("Ban giám hiệu có xem được từng học sinh không?", "Thống kê trường chỉ hiển thị tổng số và xu hướng, không có tên học sinh. Danh bạ liệt kê mọi người để quản lý danh sách lớp."),
                    ("AdminDeck có dùng được cho chuỗi không?", "Có. Hệ thống từ 4 cơ sở có một hợp đồng, một hóa đơn và tổng quan toàn hệ thống, giảm 10% đến 20% trên giá niêm yết."),
                    ("AdminDeck hỗ trợ ngôn ngữ nào?", "AdminDeck có tiếng Anh và tiếng Việt."),
                ]),
            ]},
        ],
        "band": {"h2": "Đưa AdminDeck vào trường của bạn", "p": "Cho chúng tôi biết về trường của bạn, chúng tôi sẽ gửi báo giá bằng văn bản trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)]},
    },
}

APPS = [TEACHERSDECK, STUDENTDECK, PARENTDECK, ADMINDECK]
