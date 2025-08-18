# hammer_backendapi/views/utils/pdf_utils_master.py
from io import BytesIO
from typing import Dict, List
from django.http import FileResponse
import fitz  # PyMuPDF

def _normalize_color_rgb01(rgb):
    # Accept (0..1) or (0..255); return (0..1)
    r, g, b = rgb or (0, 0, 0)
    if max(r, g, b) > 1:
        return (r/255.0, g/255.0, b/255.0)
    return (r, g, b)

def generate_master_pdf_pymupdf(
    template_path: str,
    page_fields_map: Dict[int, List[dict]],  # 1-based page index -> list of field dicts
    filename: str = "Certificates_Master_filled.pdf",
) -> FileResponse:
    """
    Copy ALL pages from template and overlay text on specified pages.
    page_fields_map keys are 1-based (human-friendly).
    Each field = {
      "text": str,
      "coords": (x, y),              # PyMuPDF coords (bottom-left origin)
      "fontsize": int,               # default 14
      "color": (r,g,b) in 0..1 or 0..255,
      "align": "left"|"center"|"right",
      "font": "helv"|"tiro"|"times" ... (PyMuPDF font name)
    }
    """
    src = fitz.open(template_path)
    out = fitz.open()
    # Copy ALL pages into new doc
    out.insert_pdf(src)  # preserves every filler page

    # Iterate target pages and draw fields
    for page_1based, fields in (page_fields_map or {}).items():
        if not (1 <= page_1based <= out.page_count):
            continue
        page = out[page_1based - 1]
        for f in fields or []:
            text = f.get("text", "") or ""
            x, y = (f.get("coords") or (0, 0))
            fontsize = f.get("fontsize", 14)
            color = _normalize_color_rgb01(f.get("color") or (0, 0, 0))
            align = (f.get("align") or "left").lower()
            font = f.get("font", "helv")

            # alignment (measure text width)
            if align != "left":
                tw = fitz.get_text_length(text, fontname=font, fontsize=fontsize)
                if align == "center":
                    x = x - (tw / 2.0)
                elif align == "right":
                    x = x - tw

            page.insert_text(
                (x, y),
                text,
                fontsize=fontsize,
                color=color,
                fontname=font,
            )

    buf = BytesIO()
    out.save(buf)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=filename, content_type="application/pdf")
