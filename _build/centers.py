"""Language centers page for _build/pages.py: single site, multi-site and large chains.
Prices, discounts and inclusions follow TeachersDeck Pricing Sheet v2 (pages 4, 6 and 7).
The sheet's top tier is "25 or more campuses: 20% off or better, custom quote", so chains
of 50+ are shown as a custom quote, with the list price and the 20% figure as a ceiling."""

QUOTE = "https://myteachersdeck.com/quote/"
DEMO = "https://myteachersdeck.com/demo/"

LANGUAGE_CENTERS = {
    "slug": "language-centers",
    "en": {
        "title": "TeachersDeck Suite for Language Centers, from 1 to 50+ Sites",
        "description": "Classroom tools for language centers: one flat price per campus, no seat fees, and 10% to 20%+ off for chains of 4, 10, 25 or 50+ sites. Free 30-day pilot.",
        "crumb": "Language centers",
        "kicker": "For language centers",
        "h1": "TeachersDeck Suite for language centers",
        "lede": "From a single center to a chain of 50 or more: one flat price per campus, not per teacher, no seat fees for students or parents, and bigger discounts as your group grows.",
        "sections": [
            {"id": "sizes", "h2": "Pick the setup that fits", "blocks": [
                ("tiles", [
                    {"h": "One center", "p": "A campus plan from 800,000 VND a month for up to 8 teachers. Start with a 30-day free pilot."},
                    {"h": "2 to 3 centers", "p": "Each center on its own campus plan, so every site sizes its plan to its own teachers and students."},
                    {"h": "Chains of 4 to 24", "p": "One contract and one invoice, 10% off from 4 centers and 15% off with premium support from 10."},
                    {"h": "Large chains, 25 to 50+", "p": "20% off list or better, a custom quote, a named contact and a launch plan for every site."},
                ]),
            ]},
            {"id": "single", "h2": "One center: campus plans", "p": "One flat price per campus, not per teacher. Language centers pay no seat fees, whatever their size.", "blocks": [
                ("table", {"head": ["Plan", "Teachers", "Students", "Per month", "Per year", "Founding rate*"],
                           "rows": [["TeachersDeck Starter", "up to 8", "—", "800,000 VND", "8,000,000 VND", "560,000 VND / month"],
                                    ["TeachersDeck Standard", "up to 20", "—", "1,800,000 VND", "18,000,000 VND", "1,260,000 VND / month"],
                                    ["TeachersDeck Growth", "up to 40", "—", "3,200,000 VND", "32,000,000 VND", "2,240,000 VND / month"],
                                    ["Suite Starter", "up to 8", "up to 150", "1,500,000 VND", "15,000,000 VND", "1,050,000 VND / month"],
                                    ["Suite Standard", "up to 20", "up to 400", "3,000,000 VND", "30,000,000 VND", "2,100,000 VND / month"],
                                    ["Suite Growth", "up to 40", "up to 900", "5,200,000 VND", "52,000,000 VND", "3,640,000 VND / month"]],
                           "note": "Suite plans add StudentDeck, ParentDeck and AdminDeck. Yearly prices are 10 months, so two months are free. *Founding rate: 30% off for 12 months for centers that join through the 30-day free pilot, kept when you move up to Suite. Extra teacher seat 90,000 VND / month; extra 50 students 150,000 VND / month."}),
            ]},
            {"id": "chains", "h2": "Multi-site and chains: volume discounts", "p": "Discounts come off the list price of each campus plan and start at 4 campuses.", "blocks": [
                ("table", {"head": ["Campuses", "Discount", "Notes"],
                           "rows": [["1 to 3", "List price", "Each campus on its own plan"],
                                    ["4 to 9", "10% off", "On the list price of each campus plan"],
                                    ["10 to 24", "15% off", "Premium support included"],
                                    ["25 to 50+", "20% off or better", "Custom quote"],
                                    ["Two-year agreement", "Extra 5% off", "Added to any tier above"]]}),
                ("h3", "Examples, per year"),
                ("table", {"head": ["Group", "List price", "With the volume discount"],
                           "rows": [["4 centers on Suite Standard", "120,000,000 VND", "108,000,000 VND (10% off)"],
                                    ["10 centers on Suite Standard", "300,000,000 VND", "255,000,000 VND (15% off)"],
                                    ["25 centers on Suite Starter", "375,000,000 VND", "300,000,000 VND (20% off)"],
                                    ["50 centers on Suite Starter", "750,000,000 VND", "600,000,000 VND or less (20% off or better)"]],
                           "note": "Prices in VND, excluding VAT. The 50-center figure is the most you would pay at the 20% tier; chains of that size get a custom quote."}),
            ]},
            {"id": "group", "h2": "What every group agreement includes", "p": "From 4 centers up, the whole group runs on one agreement.", "blocks": [
                ("tiles", [
                    {"h": "One contract, one invoice", "p": "Every campus on a single agreement and a single VAT invoice."},
                    {"h": "Group overview in AdminDeck", "p": "Managers see every center's classes, activity and homework completion in one place."},
                    {"h": "A launch plan per campus", "p": "Onboarding for each center, with your brand on every classroom screen."},
                    {"h": "A named contact", "p": "One person who knows your group, with premium support included from 10 campuses and a quarterly review."},
                ]),
            ]},
            {"id": "why", "h2": "Built for language centers", "blocks": [
                ("tiles", [
                    {"h": "Vietnamese and English names", "p": "Class Builder keeps each student's Vietnamese name with an optional English name, so teachers use the name the class uses."},
                    {"h": "Parents see progress", "p": "Families follow points, homework and teacher notes in ParentDeck. They can choose ParentDeck Pro for 300,000 VND per child per year."},
                    {"h": "No seat fees", "p": "Language centers pay the campus plan only. Seat fees apply to international schools, not to centers."},
                    {"h": "Train your own trainers", "p": "Chains can book a train-the-trainer day for 8,000,000 VND, with materials, to onboard new sites in-house."},
                ]),
            ]},
            {"id": "faq", "h2": "Questions from language centers", "blocks": [
                ("faq", [
                    ("Do language centers pay seat fees?", "No. Language centers pay the campus plan only, whether they run one center or fifty. Seat fees apply only to international schools."),
                    ("When do volume discounts start?", "At 4 campuses: 10% off from 4 to 9, 15% off with premium support from 10 to 24, and 20% off or better from 25. A two-year agreement takes another 5% off."),
                    ("We have 50 or more centers. What do we pay?", "Chains of 25 or more get a custom quote at 20% off list or better. Tell us your number of centers, teachers and students and we'll prepare it."),
                    ("Can we try it before we commit?", "Yes. The 30-day free pilot gives up to 5 classrooms, free setup and no card needed. Centers that join through the pilot get 30% off the campus plan for 12 months."),
                    ("Can each center have a different plan?", "Yes. Each campus picks the plan that fits its teachers and students; the volume discount applies to the list price of each one."),
                ]),
            ]},
        ],
        "band": {"h2": "Get a quote for your center or chain", "p": "Tell us how many centers, teachers and students you have, and we'll reply by email and Zalo within one working day.",
                 "links": [("Request a quote", QUOTE), ("Book a demo", DEMO)]},
    },
    "vi": {
        "title": "TeachersDeck Suite cho trung tâm ngoại ngữ, từ 1 đến 50+ cơ sở",
        "description": "Công cụ lớp học cho trung tâm ngoại ngữ: một mức giá cố định mỗi cơ sở, không phí theo người dùng, giảm 10% đến 20%+ cho chuỗi 4, 10, 25 hoặc 50+ cơ sở.",
        "crumb": "Trung tâm ngoại ngữ",
        "kicker": "Dành cho trung tâm ngoại ngữ",
        "h1": "TeachersDeck Suite cho trung tâm ngoại ngữ",
        "lede": "Từ một trung tâm đến chuỗi từ 50 cơ sở: một mức giá cố định cho mỗi cơ sở, không tính theo giáo viên, không phí theo người dùng cho học sinh hay phụ huynh, và giảm giá nhiều hơn khi hệ thống lớn lên.",
        "sections": [
            {"id": "sizes", "h2": "Chọn mô hình phù hợp", "blocks": [
                ("tiles", [
                    {"h": "Một trung tâm", "p": "Gói cơ sở từ 800.000 VND mỗi tháng cho tối đa 8 giáo viên. Bắt đầu với 30 ngày dùng thử miễn phí."},
                    {"h": "2 đến 3 trung tâm", "p": "Mỗi trung tâm một gói cơ sở riêng, để mỗi nơi chọn gói theo số giáo viên và học sinh của mình."},
                    {"h": "Chuỗi 4 đến 24", "p": "Một hợp đồng, một hóa đơn, giảm 10% từ 4 trung tâm và giảm 15% kèm hỗ trợ cao cấp từ 10."},
                    {"h": "Chuỗi lớn, 25 đến 50+", "p": "Giảm từ 20% trở lên trên giá niêm yết, báo giá riêng, người phụ trách riêng và kế hoạch triển khai cho từng cơ sở."},
                ]),
            ]},
            {"id": "single", "h2": "Một trung tâm: các gói cơ sở", "p": "Một mức giá cố định cho mỗi cơ sở, không tính theo giáo viên. Trung tâm ngoại ngữ không trả phí theo người dùng, dù quy mô thế nào.", "blocks": [
                ("table", {"head": ["Gói", "Giáo viên", "Học sinh", "Mỗi tháng", "Mỗi năm", "Giá sáng lập*"],
                           "rows": [["TeachersDeck Starter", "tối đa 8", "—", "800.000 VND", "8.000.000 VND", "560.000 VND / tháng"],
                                    ["TeachersDeck Standard", "tối đa 20", "—", "1.800.000 VND", "18.000.000 VND", "1.260.000 VND / tháng"],
                                    ["TeachersDeck Growth", "tối đa 40", "—", "3.200.000 VND", "32.000.000 VND", "2.240.000 VND / tháng"],
                                    ["Suite Starter", "tối đa 8", "tối đa 150", "1.500.000 VND", "15.000.000 VND", "1.050.000 VND / tháng"],
                                    ["Suite Standard", "tối đa 20", "tối đa 400", "3.000.000 VND", "30.000.000 VND", "2.100.000 VND / tháng"],
                                    ["Suite Growth", "tối đa 40", "tối đa 900", "5.200.000 VND", "52.000.000 VND", "3.640.000 VND / tháng"]],
                           "note": "Các gói Suite bổ sung StudentDeck, ParentDeck và AdminDeck. Giá theo năm tính 10 tháng, tức tặng 2 tháng. *Giá sáng lập: giảm 30% trong 12 tháng cho trung tâm tham gia qua chương trình dùng thử 30 ngày, và vẫn giữ khi nâng cấp lên Suite. Thêm tài khoản giáo viên 90.000 VND / tháng; thêm 50 học sinh 150.000 VND / tháng."}),
            ]},
            {"id": "chains", "h2": "Nhiều cơ sở và chuỗi: giảm giá theo số lượng", "p": "Mức giảm tính trên giá niêm yết của từng gói cơ sở và bắt đầu từ 4 cơ sở.", "blocks": [
                ("table", {"head": ["Số cơ sở", "Mức giảm", "Ghi chú"],
                           "rows": [["1 đến 3", "Giá niêm yết", "Mỗi cơ sở một gói riêng"],
                                    ["4 đến 9", "Giảm 10%", "Trên giá niêm yết của từng gói cơ sở"],
                                    ["10 đến 24", "Giảm 15%", "Đã gồm hỗ trợ cao cấp"],
                                    ["25 đến 50+", "Giảm từ 20% trở lên", "Báo giá riêng"],
                                    ["Hợp đồng hai năm", "Giảm thêm 5%", "Cộng thêm vào mọi mức ở trên"]]}),
                ("h3", "Ví dụ, tính theo năm"),
                ("table", {"head": ["Hệ thống", "Giá niêm yết", "Sau giảm giá theo số lượng"],
                           "rows": [["4 trung tâm dùng Suite Standard", "120.000.000 VND", "108.000.000 VND (giảm 10%)"],
                                    ["10 trung tâm dùng Suite Standard", "300.000.000 VND", "255.000.000 VND (giảm 15%)"],
                                    ["25 trung tâm dùng Suite Starter", "375.000.000 VND", "300.000.000 VND (giảm 20%)"],
                                    ["50 trung tâm dùng Suite Starter", "750.000.000 VND", "Tối đa 600.000.000 VND (giảm từ 20% trở lên)"]],
                           "note": "Giá tính bằng VND, chưa gồm VAT. Con số cho 50 trung tâm là mức cao nhất ở bậc giảm 20%; chuỗi quy mô này được báo giá riêng."}),
            ]},
            {"id": "group", "h2": "Mọi thỏa thuận cho hệ thống đều bao gồm", "p": "Từ 4 trung tâm trở lên, cả hệ thống dùng chung một thỏa thuận.", "blocks": [
                ("tiles", [
                    {"h": "Một hợp đồng, một hóa đơn", "p": "Mọi cơ sở trong một thỏa thuận và một hóa đơn VAT."},
                    {"h": "Tổng quan hệ thống trong AdminDeck", "p": "Quản lý xem lớp học, mức hoạt động và tỷ lệ hoàn thành bài của mọi trung tâm ở cùng một nơi."},
                    {"h": "Kế hoạch triển khai cho từng cơ sở", "p": "Hướng dẫn cho từng trung tâm, với thương hiệu của bạn trên mọi màn hình lớp học."},
                    {"h": "Người phụ trách riêng", "p": "Một đầu mối hiểu hệ thống của bạn, đã gồm hỗ trợ cao cấp từ 10 cơ sở và rà soát hằng quý."},
                ]),
            ]},
            {"id": "why", "h2": "Phù hợp với trung tâm ngoại ngữ", "blocks": [
                ("tiles", [
                    {"h": "Tên tiếng Việt và tiếng Anh", "p": "Class Builder giữ tên tiếng Việt của học sinh kèm tên tiếng Anh tùy chọn, để giáo viên gọi đúng tên cả lớp vẫn dùng."},
                    {"h": "Phụ huynh theo dõi tiến độ", "p": "Gia đình xem điểm, bài tập và ghi chú của giáo viên trong ParentDeck, và có thể chọn ParentDeck Pro với 300.000 VND mỗi con mỗi năm."},
                    {"h": "Không phí theo người dùng", "p": "Trung tâm ngoại ngữ chỉ trả gói cơ sở. Phí theo người dùng chỉ áp dụng cho trường quốc tế."},
                    {"h": "Tự đào tạo đội ngũ", "p": "Chuỗi có thể đặt một ngày đào tạo người hướng dẫn với giá 8.000.000 VND, kèm tài liệu, để tự triển khai cơ sở mới."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu hỏi từ trung tâm ngoại ngữ", "blocks": [
                ("faq", [
                    ("Trung tâm ngoại ngữ có trả phí theo người dùng không?", "Không. Trung tâm ngoại ngữ chỉ trả gói cơ sở, dù có một hay năm mươi trung tâm. Phí theo người dùng chỉ áp dụng cho trường quốc tế."),
                    ("Giảm giá theo số lượng bắt đầu từ khi nào?", "Từ 4 cơ sở: giảm 10% từ 4 đến 9, giảm 15% kèm hỗ trợ cao cấp từ 10 đến 24, và giảm từ 20% trở lên từ 25. Hợp đồng hai năm được giảm thêm 5%."),
                    ("Chúng tôi có từ 50 trung tâm. Giá thế nào?", "Chuỗi từ 25 cơ sở được báo giá riêng, giảm từ 20% trở lên trên giá niêm yết. Hãy cho chúng tôi biết số trung tâm, giáo viên và học sinh để chúng tôi chuẩn bị."),
                    ("Chúng tôi có thể dùng thử trước không?", "Có. Chương trình dùng thử 30 ngày miễn phí gồm tối đa 5 lớp, miễn phí cài đặt và không cần thẻ. Trung tâm tham gia qua chương trình dùng thử được giảm 30% gói cơ sở trong 12 tháng."),
                    ("Mỗi trung tâm có thể dùng gói khác nhau không?", "Có. Mỗi cơ sở chọn gói phù hợp với số giáo viên và học sinh của mình; mức giảm theo số lượng áp dụng trên giá niêm yết của từng gói."),
                ]),
            ]},
        ],
        "band": {"h2": "Nhận báo giá cho trung tâm hoặc chuỗi của bạn", "p": "Cho chúng tôi biết số trung tâm, giáo viên và học sinh, chúng tôi sẽ phản hồi qua email và Zalo trong một ngày làm việc.",
                 "links": [("Yêu cầu báo giá", QUOTE), ("Đặt lịch demo", DEMO)]},
    },
}
