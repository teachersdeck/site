"""Live preview box for inner pages: the same .live widget as the home page's app cards (assets/site.js loads it),
larger, and loaded automatically when it scrolls into view (data-autoload)."""
import html

T = {
    "en": {"h2": "See it live", "bar": "Live demo", "open": "Open full demo ↗", "play": "Preview the live demo",
           "p": "This is the real demo, running on this page with sample data. Click it to open the full demo in its own window."},
    "vi": {"h2": "Xem trực tiếp", "bar": "Bản demo trực tuyến", "open": "Mở bản demo đầy đủ ↗", "play": "Xem trước bản demo",
           "p": "Đây là bản demo thật, chạy ngay trên trang này với dữ liệu mẫu. Bấm vào để mở bản demo đầy đủ trong cửa sổ riêng."},
}


def section(lang, src, name, title):
    t = T[lang]
    e = lambda s: html.escape(s, quote=True)  # noqa: E731
    box = (f'<div class="live live-lg" data-live="{e(name)}" data-src="{e(src)}" data-title="{e(title)}" data-autoload>'
           f'<div class="live-bar"><i></i><i></i><i></i><span>{e(t["bar"])} · {e(title)}</span>'
           f'<a href="{e(src)}" target="_blank" rel="noopener" data-demo-window="{e(name)}">{e(t["open"])}</a></div>'
           f'<div class="live-view"><button type="button" class="live-play"><svg viewBox="0 0 16 16" aria-hidden="true">'
           f'<path d="M4.5 2.8v10.4L13 8z" fill="currentColor"/></svg><span>{e(t["play"])}</span></button></div></div>')
    return {"id": "live", "h2": t["h2"], "p": t["p"], "blocks": [("html", box)]}
