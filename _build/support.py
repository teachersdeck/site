"""Support page (/support/, /vi/support/): how to reach us, what to include, quick answers, useful links."""
EMAIL = "jerry@myteachersdeck.com"
PRIVACY_EMAIL = "teachersdeck@gmail.com"
ZALO = "https://zalo.me/0705247680"
DEMO_SITE = "https://teachersdeck.github.io/demo/"
SITE = "https://myteachersdeck.com"


def contact(lang):
    t = {
        "en": [("amber", "Email", "The best way to report a problem or ask a question.", f"mailto:{EMAIL}", EMAIL),
               ("matcha", "Zalo", "For a quick question, message us on Zalo.", ZALO, "Message on Zalo"),
               ("indigo", "Privacy and child safety", "Questions about a child's data, or a safety concern.", f"mailto:{PRIVACY_EMAIL}", PRIVACY_EMAIL)],
        "vi": [("amber", "Email", "Cách tốt nhất để báo lỗi hoặc đặt câu hỏi.", f"mailto:{EMAIL}", EMAIL),
               ("matcha", "Zalo", "Câu hỏi nhanh, hãy nhắn cho chúng tôi qua Zalo.", ZALO, "Nhắn Zalo"),
               ("indigo", "Quyền riêng tư và an toàn trẻ em", "Câu hỏi về dữ liệu của trẻ, hoặc một lo ngại về an toàn.", f"mailto:{PRIVACY_EMAIL}", PRIVACY_EMAIL)],
    }[lang]
    tiles = "".join(f'<a class="tile t-{c}" href="{h}"><h3>{a}</h3><p>{p}</p><span class="more">{l} →</span></a>' for c, a, p, h, l in t)
    return f'<div class="tiles n3 sup-contact">{tiles}</div>'


def links(lang):
    v = "vi/" if lang == "vi" else ""
    items = {
        "en": [("Try the live demo", DEMO_SITE), ("Pricing", f"{SITE}/{v}pricing/"), ("Request a quote", f"{SITE}/quote/"),
               ("Child privacy policy", f"{SITE}/student-privacy/")],
        "vi": [("Dùng thử bản demo", DEMO_SITE), ("Bảng giá", f"{SITE}/{v}pricing/"), ("Yêu cầu báo giá", f"{SITE}/quote/"),
               ("Chính sách quyền riêng tư trẻ em (tiếng Anh)", f"{SITE}/student-privacy/")],
    }[lang]
    return '<div class="more-apps">' + "".join(f'<a class="btn" href="{h}">{t}</a>' for t, h in items) + "</div>"


SUPPORT = {
    "slug": "support",
    "en": {
        "title": "Support: TeachersDeck Suite",
        "description": "Get help with TeachersDeck, StudentDeck, ParentDeck and AdminDeck: email or Zalo, what to include when you report a problem, and quick answers.",
        "crumb": "Support",
        "kicker": "Support",
        "h1": "How can we help?",
        "lede": "Email us or message us on Zalo. We usually reply within one working day.",
        "cta": [("Email support", f"mailto:{EMAIL}"), ("Message on Zalo", ZALO)],
        "sections": [
            {"id": "contact", "h2": "Contact us", "blocks": [("html", contact("en"))]},
            {"id": "report", "h2": "Reporting a problem?", "p": "Include these and we can help faster.", "blocks": [
                ("tiles", [
                    {"h": "Which app", "p": "TeachersDeck, StudentDeck, ParentDeck or AdminDeck, and the version number from its Settings or About screen."},
                    {"h": "Where you use it", "p": "Your browser or device, and whether it runs in a tab, as your Chrome new tab, or in ClassIn or Canvas."},
                    {"h": "What happened", "p": "What you did, what you expected, and what you saw instead. A screenshot helps a lot."},
                ]),
            ]},
            {"id": "faq", "h2": "Quick answers", "blocks": [
                ("faq", [
                    ("Is TeachersDeck Suite free?", "A free plan covers the everyday classroom tools. Pro unlocks the full widget set with a licence key, and Enterprise solutions are available for schools."),
                    ("Do students need an email address or account?", "No. Students join a class with a class code and a PIN, with no email address and no personal account."),
                    ("Where is classroom data stored?", "A teacher's classroom data is stored on their own device. Cloud features are optional, and a student's journal never leaves their device."),
                    ("Do I need to install anything?", "No install wizard. Open TeachersDeck in a browser, or load it as your Chrome new tab."),
                    ("Can I try it before I buy?", "Yes. The live demo runs every app in your browser with sample data, and schools can ask for a 30-day free pilot."),
                ]),
            ]},
            {"id": "links", "h2": "Useful links", "blocks": [("html", links("en"))]},
        ],
        "band": {"h2": "Still stuck?", "p": "Send us a message and we'll help you sort it out.",
                 "links": [("Email support", f"mailto:{EMAIL}"), ("Message on Zalo", ZALO)]},
    },
    "vi": {
        "title": "Hỗ trợ: TeachersDeck Suite",
        "description": "Nhận hỗ trợ cho TeachersDeck, StudentDeck, ParentDeck và AdminDeck: email hoặc Zalo, cần gửi gì khi báo lỗi, và câu trả lời nhanh.",
        "crumb": "Hỗ trợ",
        "kicker": "Hỗ trợ",
        "h1": "Chúng tôi có thể giúp gì?",
        "lede": "Gửi email hoặc nhắn Zalo cho chúng tôi. Chúng tôi thường trả lời trong một ngày làm việc.",
        "cta": [("Gửi email hỗ trợ", f"mailto:{EMAIL}"), ("Nhắn Zalo", ZALO)],
        "sections": [
            {"id": "contact", "h2": "Liên hệ", "blocks": [("html", contact("vi"))]},
            {"id": "report", "h2": "Báo lỗi?", "p": "Gửi kèm những thông tin này để chúng tôi giúp nhanh hơn.", "blocks": [
                ("tiles", [
                    {"h": "Ứng dụng nào", "p": "TeachersDeck, StudentDeck, ParentDeck hay AdminDeck, và số phiên bản trong mục Cài đặt hoặc Giới thiệu."},
                    {"h": "Bạn dùng ở đâu", "p": "Trình duyệt hoặc thiết bị, và bạn mở trong một tab, làm trang tab mới của Chrome, hay trong ClassIn hoặc Canvas."},
                    {"h": "Chuyện gì đã xảy ra", "p": "Bạn đã làm gì, bạn mong đợi điều gì, và thực tế bạn thấy gì. Ảnh chụp màn hình sẽ giúp rất nhiều."},
                ]),
            ]},
            {"id": "faq", "h2": "Câu trả lời nhanh", "blocks": [
                ("faq", [
                    ("TeachersDeck Suite có miễn phí không?", "Gói miễn phí bao gồm các công cụ lớp học hằng ngày. Gói Pro mở khóa toàn bộ widget bằng khóa bản quyền, và có giải pháp Enterprise cho nhà trường."),
                    ("Học sinh có cần email hoặc tài khoản không?", "Không. Học sinh tham gia lớp bằng mã lớp và mã PIN, không cần email và không cần tài khoản cá nhân."),
                    ("Dữ liệu lớp học được lưu ở đâu?", "Dữ liệu lớp học của giáo viên được lưu trên thiết bị của chính họ. Tính năng đám mây là tùy chọn, và nhật ký của học sinh không bao giờ rời khỏi thiết bị."),
                    ("Có cần cài đặt gì không?", "Không cần trình cài đặt. Mở TeachersDeck trên trình duyệt, hoặc dùng làm trang tab mới của Chrome."),
                    ("Tôi có thể dùng thử trước khi mua không?", "Có. Bản demo chạy mọi ứng dụng ngay trên trình duyệt với dữ liệu mẫu, và nhà trường có thể đăng ký dùng thử miễn phí 30 ngày."),
                ]),
            ]},
            {"id": "links", "h2": "Liên kết hữu ích", "blocks": [("html", links("vi"))]},
        ],
        "band": {"h2": "Vẫn chưa giải quyết được?", "p": "Nhắn cho chúng tôi, chúng tôi sẽ giúp bạn.",
                 "links": [("Gửi email hỗ trợ", f"mailto:{EMAIL}"), ("Nhắn Zalo", ZALO)]},
    },
}
