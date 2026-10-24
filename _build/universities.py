"""Universities page for _build/pages.py.
Not on price sheet v2. Agreed with the owner (2026-10-24): priced like international schools,
a Suite campus plan per faculty plus a yearly seat fee per student (100,000 VND) and per parent
who links with ParentDeck (500,000 VND); faculties count as campuses for the chain volume
discounts, which apply to the campus plans only; universities beyond Suite Growth get a quote."""

QUOTE = "https://myteachersdeck.com/quote/"
DEMO = "https://myteachersdeck.com/demo/"

UNIVERSITIES = {
    "slug": "universities",
    "demo": "unideck/unistudentdeck/",
    "en": {
        "title": "TeachersDeck Suite for Universities: Faculty Plans and Seats",
        "description": "Classroom tools for universities in Vietnam: a campus plan per faculty, a yearly seat fee per student and parent, and volume discounts across faculties.",
        "crumb": "Universities",
        "try": "Try UniDeck",
        "kicker": "For universities",
        "h1": "TeachersDeck Suite for universities",
        "lede": "A campus plan for each faculty, plus a small yearly seat fee for every student and for each parent who follows along. Lecturers, students, families and university leaders share one system, in English and Vietnamese.",
        "sections": [
            {"id": "unideck", "h2": 'UniDeck: the university edition', "p": 'A version of the suite made for higher education, now in early preview. Every app has a live demo with example data, which opens in its own window.', "blocks": [("html", '<div class="tiles n4"><div class="tile t-indigo"><span class="early">Early preview</span><h3>LectureDeck</h3><p>For lecturers: courses, assignments and grading, built on TeachersDeck.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/lecturedeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-lecturedeck">Try the live demo</a></div><div class="tile t-amber"><h3>UniStudentDeck</h3><p>For undergraduate and graduate students: a calm study dashboard with assignments, a calendar, a focus timer and notes.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/unistudentdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-unistudentdeck">Try the live demo</a></div><div class="tile t-matcha"><span class="early">Early preview</span><h3>CampusDeck</h3><p>For a campus, program or center: courses, terms and enrollment in one place.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/campusdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-campusdeck">Try the live demo</a></div><div class="tile t-coral"><span class="early">Early preview</span><h3>ParentDeck family view</h3><p>Opt-in: an adult student chooses what to share with family, and can stop sharing at any time.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/parentdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-parentdeck">Try the live demo</a></div></div><p class="note">UniDeck is in early preview, so the demos change often. The plans and prices below are for TeachersDeck Suite, available now. <a href="https://teachersdeck.github.io/demo/" target="_blank" rel="noopener">See all the live demos</a></p>')]},
            {"id": "gets", "h2": "What your university gets", "p": "Suite plans give each faculty all four apps.", "blocks": [
                ("tiles", [
                    {"h": "TeachersDeck Pro for every lecturer", "p": "Every lecturer seat on a faculty plan includes TeachersDeck Pro: attendance, assignments, polls, a whiteboard and more."},
                    {"h": "StudentDeck for every student", "p": "Students join a course with a class code and a PIN, and keep a focus timer, homework list and notes in one place."},
                    {"h": "ParentDeck for families far away", "p": "Students often live far from home. Parents follow homework, attendance and lecturer notes in real time, read-only."},
                    {"h": "AdminDeck for faculty leaders", "p": "Deans and administrators see every course: activity, homework completion, join codes, rosters and people."},
                ]),
            ]},
            {"id": "pricing", "h2": "How university pricing works", "p": "Three parts: a campus plan for each faculty, a seat fee per student and a seat fee per parent who links.", "blocks": [
                ("table", {"head": ["Part", "Price per year", "About in USD", "Notes"],
                           "rows": [["Student seat", "100,000 VND", "about $4", "Each enrolled student"],
                                    ["Parent seat", "500,000 VND", "about $19", "Each parent account linked with ParentDeck"]],
                           "note": "Seat fees are charged on top of the faculty plans. Parent seats count only the families who link."}),
                ("h3", "Faculty plans", "Each faculty or department takes its own Suite plan. Yearly prices are 10 months, so two months are free."),
                ("table", {"head": ["Plan", "Lecturers", "Students", "Per month", "Per year"],
                           "rows": [["Suite Starter", "up to 8", "up to 150", "1,500,000 VND", "15,000,000 VND"],
                                    ["Suite Standard", "up to 20", "up to 400", "3,000,000 VND", "30,000,000 VND"],
                                    ["Suite Growth", "up to 40", "up to 900", "5,200,000 VND", "52,000,000 VND"]],
                           "note": "Extra lecturer seat 90,000 VND / month; extra 50 students 150,000 VND / month. A faculty larger than Suite Growth gets a custom quote."}),
                ("h3", "Discounts across faculties", "Each faculty plan counts as one campus, so a university with several faculties gets the group discount on its faculty plans."),
                ("table", {"head": ["Faculty plans", "Discount on the plans", "Notes"],
                           "rows": [["1 to 3", "List price", "Each faculty on its own plan"],
                                    ["4 to 9", "10% off", "One contract and one invoice"],
                                    ["10 to 24", "15% off", "Premium support included"],
                                    ["25 or more", "20% off or better", "Custom quote"],
                                    ["Two-year agreement", "Extra 5% off", "Added to any tier above"]]}),
            ]},
            {"id": "example", "h2": "Example: 4 faculties, 1,600 students, 400 parents", "p": "Four faculties each on Suite Standard, with 400 parents linked through ParentDeck.", "blocks": [
                ("table", {"head": ["Per year", "Calculation", "Price"],
                           "rows": [["4 faculty plans", "4 × 30,000,000, minus 10%", "108,000,000 VND"],
                                    ["1,600 student seats", "1,600 × 100,000", "160,000,000 VND"],
                                    ["400 parent seats", "400 × 500,000", "200,000,000 VND"],
                                    ["!Total per year", "", "468,000,000 VND"]],
                           "note": "About $17,795 a year, or about 292,500 VND per student. The volume discount applies to the faculty plans, not the seat fees. Prices in VND, excluding VAT; USD about 26,300 VND per USD."}),
            ]},
            {"id": "why", "h2": "Built for universities", "blocks": [
                ("tiles", [
                    {"h": "Families stay in the loop", "p": "Parents who live far from campus see homework, attendance and lecturer notes without calling or visiting."},
                    {"h": "English and Vietnamese", "p": "TeachersDeck, ParentDeck and AdminDeck work in English and Tiếng Việt, so staff and families each use their own language."},
                    {"h": "One agreement for every faculty", "p": "From 4 faculties, one contract and one VAT invoice, with a named contact and a launch plan per faculty."},
                    {"h": "Data kept in its place", "p": "Each university sees only its own data, and parent screens are read-only."},
                ]),
            ]},
            {"id": "faq", "h2": "Questions from universities", "blocks": [
                ("faq", [
                    ("Why do universities pay seat fees?", "Like international schools, universities pay a faculty plan plus a yearly seat fee: 100,000 VND per student and 500,000 VND per parent who links with ParentDeck."),
                    ("Do we pay for every parent?", "No. Parent seats count only the families who link with ParentDeck to follow their student."),
                    ("How do discounts work across faculties?", "Each faculty plan counts as one campus: 10% off from 4 plans, 15% off with premium support from 10, and 20% off or better from 25. A two-year agreement takes another 5% off. Discounts apply to the faculty plans."),
                    ("Our faculty is bigger than Suite Growth. What then?", "Add extra lecturer seats and student blocks, or ask us for a custom quote for the faculty or the whole university."),
                    ("Do prices include VAT?", "No. Prices exclude VAT, and VAT invoices are available."),
                ]),
            ]},
        ],
        "band": {"h2": "Get a written quote for your university", "p": "Tell us your faculties and the number of lecturers, students and parents, and we'll reply by email and Zalo within one working day.",
                 "links": [("Request a quote", QUOTE), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "TeachersDeck Suite cho trường đại học: Gói theo khoa và phí",
        "description": "Công cụ lớp học cho trường đại học tại Việt Nam: gói cơ sở cho từng khoa, phí mỗi năm cho mỗi sinh viên và phụ huynh, và giảm giá khi có nhiều khoa.",
        "crumb": "Trường đại học",
        "try": "Dùng thử UniDeck",
        "kicker": "Dành cho trường đại học",
        "h1": "TeachersDeck Suite cho trường đại học",
        "lede": "Một gói cơ sở cho mỗi khoa, cộng một khoản phí nhỏ mỗi năm cho mỗi sinh viên và mỗi phụ huynh theo dõi. Giảng viên, sinh viên, gia đình và lãnh đạo nhà trường dùng chung một hệ thống, bằng tiếng Anh và tiếng Việt.",
        "sections": [
            {"id": "unideck", "h2": 'UniDeck: phiên bản dành cho đại học', "p": 'Phiên bản của bộ ứng dụng dành riêng cho giáo dục đại học, hiện đang ở giai đoạn xem trước. Mỗi ứng dụng có bản demo trực tuyến với dữ liệu mẫu, mở trong cửa sổ riêng.', "blocks": [("html", '<div class="tiles n4"><div class="tile t-indigo"><span class="early">Bản xem trước</span><h3>LectureDeck</h3><p>Dành cho giảng viên: khóa học, bài tập và chấm điểm, xây dựng trên TeachersDeck.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/lecturedeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-lecturedeck">Dùng thử bản demo</a></div><div class="tile t-amber"><h3>UniStudentDeck</h3><p>Dành cho sinh viên đại học và sau đại học: bảng học tập gọn gàng với bài tập, lịch, hẹn giờ tập trung và ghi chú.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/unistudentdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-unistudentdeck">Dùng thử bản demo</a></div><div class="tile t-matcha"><span class="early">Bản xem trước</span><h3>CampusDeck</h3><p>Dành cho cơ sở, chương trình hoặc trung tâm: khóa học, học kỳ và tuyển sinh ở một nơi.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/campusdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-campusdeck">Dùng thử bản demo</a></div><div class="tile t-coral"><span class="early">Bản xem trước</span><h3>ParentDeck (chế độ gia đình)</h3><p>Tùy chọn: sinh viên tự chọn chia sẻ gì với gia đình và có thể dừng chia sẻ bất cứ lúc nào.</p><a class="btn" href="https://teachersdeck.github.io/demo/unideck/parentdeck/?demo=1" target="_blank" rel="noopener" data-demo-window="unideck-parentdeck">Dùng thử bản demo</a></div></div><p class="note">UniDeck đang ở giai đoạn xem trước nên các bản demo thay đổi thường xuyên. Các gói và bảng giá bên dưới dành cho TeachersDeck Suite, đã sẵn sàng sử dụng. <a href="https://teachersdeck.github.io/demo/" target="_blank" rel="noopener">Xem tất cả bản demo</a></p>')]},
            {"id": "gets", "h2": "Nhà trường nhận được gì", "p": "Các gói Suite cung cấp cả bốn ứng dụng cho mỗi khoa.", "blocks": [
                ("tiles", [
                    {"h": "TeachersDeck Pro cho mọi giảng viên", "p": "Mỗi tài khoản giảng viên trong gói của khoa đã gồm TeachersDeck Pro: điểm danh, giao bài, bình chọn, bảng trắng và nhiều hơn nữa."},
                    {"h": "StudentDeck cho mọi sinh viên", "p": "Sinh viên vào lớp bằng mã lớp và mã PIN, có hẹn giờ tập trung, danh sách bài tập và ghi chú ở cùng một nơi."},
                    {"h": "ParentDeck cho gia đình ở xa", "p": "Sinh viên thường sống xa nhà. Phụ huynh theo dõi bài tập, điểm danh và ghi chú của giảng viên theo thời gian thực, chỉ để xem."},
                    {"h": "AdminDeck cho lãnh đạo khoa", "p": "Trưởng khoa và phòng đào tạo xem mọi lớp học phần: mức hoạt động, tỷ lệ hoàn thành bài, mã tham gia, danh sách lớp và con người."},
                ]),
            ]},
            {"id": "pricing", "h2": "Cách tính giá cho trường đại học", "p": "Gồm ba phần: gói cơ sở cho mỗi khoa, phí cho mỗi sinh viên và phí cho mỗi phụ huynh có liên kết.", "blocks": [
                ("table", {"head": ["Phần", "Giá mỗi năm", "Khoảng USD", "Ghi chú"],
                           "rows": [["Phí sinh viên", "100.000 VND", "khoảng $4", "Mỗi sinh viên đang học"],
                                    ["Phí phụ huynh", "500.000 VND", "khoảng $19", "Mỗi tài khoản phụ huynh liên kết với ParentDeck"]],
                           "note": "Phí theo người dùng được tính thêm vào các gói của khoa. Phí phụ huynh chỉ tính cho các gia đình có liên kết."}),
                ("h3", "Gói cho khoa", "Mỗi khoa hoặc bộ môn dùng một gói Suite riêng. Giá theo năm tính 10 tháng, tức tặng 2 tháng."),
                ("table", {"head": ["Gói", "Giảng viên", "Sinh viên", "Mỗi tháng", "Mỗi năm"],
                           "rows": [["Suite Starter", "tối đa 8", "tối đa 150", "1.500.000 VND", "15.000.000 VND"],
                                    ["Suite Standard", "tối đa 20", "tối đa 400", "3.000.000 VND", "30.000.000 VND"],
                                    ["Suite Growth", "tối đa 40", "tối đa 900", "5.200.000 VND", "52.000.000 VND"]],
                           "note": "Thêm tài khoản giảng viên 90.000 VND / tháng; thêm 50 sinh viên 150.000 VND / tháng. Khoa lớn hơn gói Suite Growth được báo giá riêng."}),
                ("h3", "Giảm giá khi có nhiều khoa", "Mỗi gói của khoa được tính là một cơ sở, nên trường có nhiều khoa được giảm giá hệ thống trên các gói của khoa."),
                ("table", {"head": ["Số gói khoa", "Mức giảm trên gói", "Ghi chú"],
                           "rows": [["1 đến 3", "Giá niêm yết", "Mỗi khoa một gói riêng"],
                                    ["4 đến 9", "Giảm 10%", "Một hợp đồng và một hóa đơn"],
                                    ["10 đến 24", "Giảm 15%", "Đã gồm hỗ trợ cao cấp"],
                                    ["Từ 25", "Giảm từ 20% trở lên", "Báo giá riêng"],
                                    ["Hợp đồng hai năm", "Giảm thêm 5%", "Cộng thêm vào mọi mức ở trên"]]}),
            ]},
            {"id": "example", "h2": "Ví dụ: 4 khoa, 1.600 sinh viên, 400 phụ huynh", "p": "Bốn khoa đều dùng Suite Standard, với 400 phụ huynh liên kết qua ParentDeck.", "blocks": [
                ("table", {"head": ["Mỗi năm", "Cách tính", "Giá"],
                           "rows": [["4 gói khoa", "4 × 30.000.000, trừ 10%", "108.000.000 VND"],
                                    ["1.600 sinh viên", "1.600 × 100.000", "160.000.000 VND"],
                                    ["400 phụ huynh", "400 × 500.000", "200.000.000 VND"],
                                    ["!Tổng mỗi năm", "", "468.000.000 VND"]],
                           "note": "Khoảng $17.795 mỗi năm, tức khoảng 292.500 VND cho mỗi sinh viên. Mức giảm theo số lượng áp dụng cho gói của khoa, không áp dụng cho phí theo người dùng. Giá tính bằng VND, chưa gồm VAT; khoảng 26.300 VND/USD."}),
            ]},
            {"id": "why", "h2": "Phù hợp với trường đại học", "blocks": [
                ("tiles", [
                    {"h": "Gia đình luôn nắm được tình hình", "p": "Phụ huynh sống xa trường vẫn xem được bài tập, điểm danh và ghi chú của giảng viên mà không cần gọi điện hay đến trường."},
                    {"h": "Tiếng Anh và tiếng Việt", "p": "TeachersDeck, ParentDeck và AdminDeck có tiếng Anh và tiếng Việt, để cán bộ và gia đình dùng ngôn ngữ của mình."},
                    {"h": "Một thỏa thuận cho mọi khoa", "p": "Từ 4 khoa, một hợp đồng và một hóa đơn VAT, có người phụ trách riêng và kế hoạch triển khai cho từng khoa."},
                    {"h": "Dữ liệu đúng chỗ", "p": "Mỗi trường chỉ thấy dữ liệu của mình, và màn hình phụ huynh chỉ để xem."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi từ trường đại học", "blocks": [
                ("faq", [
                    ("Vì sao trường đại học trả phí theo người dùng?", "Giống trường quốc tế, trường đại học trả gói cho khoa cộng phí mỗi năm: 100.000 VND cho mỗi sinh viên và 500.000 VND cho mỗi phụ huynh liên kết với ParentDeck."),
                    ("Chúng tôi có phải trả cho mọi phụ huynh không?", "Không. Phí phụ huynh chỉ tính cho các gia đình liên kết với ParentDeck để theo dõi sinh viên."),
                    ("Giảm giá khi có nhiều khoa thế nào?", "Mỗi gói khoa được tính là một cơ sở: giảm 10% từ 4 gói, giảm 15% kèm hỗ trợ cao cấp từ 10, và giảm từ 20% trở lên từ 25. Hợp đồng hai năm được giảm thêm 5%. Mức giảm áp dụng cho gói của khoa."),
                    ("Khoa của chúng tôi lớn hơn gói Suite Growth thì sao?", "Thêm tài khoản giảng viên và nhóm sinh viên, hoặc yêu cầu báo giá riêng cho khoa hoặc cả trường."),
                    ("Giá đã gồm VAT chưa?", "Chưa. Giá chưa gồm VAT, và có xuất hóa đơn VAT."),
                ]),
            ]},
        ],
        "band": {"h2": "Nhận báo giá bằng văn bản cho trường bạn", "p": "Cho chúng tôi biết các khoa và số giảng viên, sinh viên, phụ huynh, chúng tôi sẽ phản hồi qua email và Zalo trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)]},
    },
}
