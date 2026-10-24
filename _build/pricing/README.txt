Price sheet builder (not published by GitHub Pages: the folder starts with an underscore).

build_v3.py makes TeachersDeck_Pricing_Sheet_EN_v3.pdf and _VI_v3.pdf from the v2 sheets:
it adds the universities page after international schools, renumbers to 9 pages and updates
the cross-references. Changed words are removed from the PDF and redrawn in Carlito (fonts/,
SIL Open Font License), so copy-paste and search only find the current text.

  python _build/pricing/build_v3.py . OUTPUT_FOLDER

Needs Python with pypdf and reportlab. pdftext.py holds the helpers (find, strip and redraw
text; draw tables in the sheet's style).
