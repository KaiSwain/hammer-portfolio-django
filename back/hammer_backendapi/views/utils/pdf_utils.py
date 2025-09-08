import fitz  # PyMuPDF
from io import BytesIO
from django.http import FileResponse
from django.conf import settings

# WeasyPrint functionality disabled due to system library conflicts
WEASYPRINT_AVAILABLE = False
HTML = None

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
        text = field.get("text", "") or ""  # Ensure text is never None
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





def html_to_pdf_bytes(html: str, base_url: str | None = None) -> bytes:
    """
    Render HTML to PDF bytes using PyMuPDF. 
    Falls back to WeasyPrint if available, otherwise uses PyMuPDF text rendering.
    """
    if WEASYPRINT_AVAILABLE:
        # Use WeasyPrint if available
        pdf = HTML(string=html, base_url=base_url).write_pdf()
        return pdf
    else:
        # Use PyMuPDF as fallback for basic HTML to PDF conversion
        return _html_to_pdf_pymupdf(html)

def _html_to_pdf_pymupdf(html: str) -> bytes:
    """
    Convert basic HTML to PDF using PyMuPDF.
    This handles simple HTML structure but not complex CSS styling.
    """
    import fitz  # PyMuPDF
    import re
    from html import unescape
    
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # US Letter size
    
    # Basic HTML parsing - extract text content and apply simple formatting
    # Remove HTML tags and extract content
    text_content = _parse_html_content(html)
    
    # Set up text insertion parameters
    rect = fitz.Rect(50, 50, 562, 742)  # Margins: 50 points on all sides
    
    # Insert text with basic formatting
    try:
        page.insert_textbox(
            rect,
            text_content,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=0  # Left align
        )
    except Exception as e:
        # Fallback to simpler text insertion if textbox fails
        page.insert_text(
            (50, 70),
            text_content,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0)
        )
    
    # Convert to bytes
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def _parse_html_content(html: str) -> str:
    """
    Parse HTML content and extract text with basic formatting.
    """
    import re
    from html import unescape
    
    # Remove HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # Extract title/header content
    content_parts = []
    
    # Process h1, h2, h3 tags
    h_tags = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html, re.DOTALL | re.IGNORECASE)
    for h_tag in h_tags:
        clean_header = re.sub(r'<[^>]+>', '', h_tag).strip()
        if clean_header:
            content_parts.append(f"\n{clean_header.upper()}\n" + "="*len(clean_header) + "\n")
    
    # Process p tags
    p_tags = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
    for p_tag in p_tags:
        clean_p = re.sub(r'<[^>]+>', '', p_tag).strip()
        if clean_p:
            content_parts.append(f"{clean_p}\n")
    
    # Process li tags
    li_tags = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL | re.IGNORECASE)
    if li_tags:
        content_parts.append("\n")
        for li_tag in li_tags:
            clean_li = re.sub(r'<[^>]+>', '', li_tag).strip()
            if clean_li:
                content_parts.append(f"• {clean_li}\n")
    
    # If no structured content found, just clean all HTML
    if not content_parts:
        clean_text = re.sub(r'<[^>]+>', '', html)
        clean_text = unescape(clean_text).strip()
        content_parts.append(clean_text)
    
    # Join all parts and clean up
    result = ''.join(content_parts)
    result = unescape(result)
    
    # Clean up multiple newlines
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)
    
    return result.strip()
