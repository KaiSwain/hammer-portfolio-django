import fitz  # PyMuPDF
from io import BytesIO
from django.http import FileResponse

def generate_certificate_pdf(template_path, page_index, fields, filename="certificate.pdf"):
    """
    Generate a customized certificate PDF by copying one page of a template
    and overlaying text with optional styles.

    Args:
        template_path (str): Path to the master PDF.
        page_index (int): 0-based index of the page to copy.
        fields (list): List of dicts with:
            {
                "text": str,
                "coords": (x, y),
                "fontsize": int (default=14),
                "color": (r, g, b) in range 0-1 (default=(0,0,0)),
                "align": "left"|"center"|"right" (default="left"),
                "font": str (PyMuPDF font name or custom)
            }
        filename (str): Output filename for the download.

    Returns:
        FileResponse: The generated PDF for download.
    """

    # ✅ Load the original PDF
    doc = fitz.open(template_path)

    # ✅ Copy the selected page into a new document
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
    page = new_doc[0]

    # ✅ Apply text overlays
    for field in fields:
        text = field.get("text", "")
        x, y = field.get("coords", (0, 0))
        fontsize = field.get("fontsize", 14)
        color = field.get("color", (0, 0, 0))  # default black
        align = field.get("align", "left")
        font = field.get("font", "helv")  # default: Helvetica (built-in)

        # ✅ Calculate alignment (center or right)
        if align != "left":
            text_width = fitz.get_text_length(text, fontname=font, fontsize=fontsize)
            if align == "center":
                x -= text_width / 2
            elif align == "right":
                x -= text_width

        # ✅ Insert text
        page.insert_text(
            (x, y),
            text,
            fontsize=fontsize,
            color=color,
            fontname=font
        )

    # ✅ Save into memory
    buffer = BytesIO()
    new_doc.save(buffer)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
