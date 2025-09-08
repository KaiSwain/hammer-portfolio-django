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
    This handles simple HTML structure with proper formatting.
    """
    import fitz  # PyMuPDF
    import re
    from html import unescape
    
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # US Letter size
    
    # Parse HTML content with proper formatting
    text_content = _parse_html_content(html)
    
    # Add a title
    title_rect = fitz.Rect(50, 50, 562, 100)
    page.insert_textbox(
        title_rect,
        "🏗️ PERSONALITY SUMMARY 🏗️",
        fontsize=16,
        fontname="helv-bold",
        color=(0, 0, 0),
        align=1  # Center align
    )
    
    # Set up main content area
    content_rect = fitz.Rect(50, 110, 562, 742)  # Start below title
    
    # Insert main content with proper formatting
    try:
        page.insert_textbox(
            content_rect,
            text_content,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=0  # Left align
        )
    except Exception as e:
        # Fallback: split into smaller chunks if content is too long
        lines = text_content.split('\n')
        y_pos = 120
        line_height = 14
        
        for line in lines:
            if y_pos > 730:  # Near bottom of page
                # Add new page if needed
                page = doc.new_page(width=612, height=792)
                y_pos = 50
            
            # Check if line is a header (all caps with equals)
            if line.strip() and '=' in line and line.isupper():
                # This is a header - make it bold and larger
                page.insert_text(
                    (50, y_pos),
                    line.strip(),
                    fontsize=12,
                    fontname="helv-bold",
                    color=(0, 0, 0)
                )
                y_pos += line_height + 5
            elif line.strip():
                # Regular content
                # Check if it's a bullet point
                if line.strip().startswith('•'):
                    page.insert_text(
                        (70, y_pos),  # Indent bullet points
                        line.strip(),
                        fontsize=10,
                        fontname="helv",
                        color=(0, 0, 0)
                    )
                else:
                    page.insert_text(
                        (50, y_pos),
                        line.strip(),
                        fontsize=10,
                        fontname="helv",
                        color=(0, 0, 0)
                    )
                y_pos += line_height
            else:
                # Empty line - add some space
                y_pos += line_height / 2
    
    # Convert to bytes
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def _parse_html_content(html: str) -> str:
    """
    Parse HTML content and extract text with proper sequential formatting.
    """
    import re
    from html import unescape
    
    # Remove HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    content_parts = []
    
    # Parse HTML sequentially to maintain order
    # Split by major elements and process in order
    elements = re.split(r'(<h[1-3][^>]*>.*?</h[1-3]>|<p[^>]*>.*?</p>|<ul[^>]*>.*?</ul>)', html, flags=re.DOTALL | re.IGNORECASE)
    
    for element in elements:
        element = element.strip()
        if not element:
            continue
            
        # Process headers
        h_match = re.match(r'<h[1-3][^>]*>(.*?)</h[1-3]>', element, re.DOTALL | re.IGNORECASE)
        if h_match:
            header_text = re.sub(r'<[^>]+>', '', h_match.group(1)).strip()
            if header_text:
                content_parts.append(f"\n{header_text.upper()}\n{'='*len(header_text)}\n")
            continue
        
        # Process paragraphs
        p_match = re.match(r'<p[^>]*>(.*?)</p>', element, re.DOTALL | re.IGNORECASE)
        if p_match:
            p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            if p_text:
                content_parts.append(f"{p_text}\n\n")
            continue
        
        # Process unordered lists
        ul_match = re.match(r'<ul[^>]*>(.*?)</ul>', element, re.DOTALL | re.IGNORECASE)
        if ul_match:
            ul_content = ul_match.group(1)
            li_items = re.findall(r'<li[^>]*>(.*?)</li>', ul_content, re.DOTALL | re.IGNORECASE)
            if li_items:
                for li_content in li_items:
                    li_text = re.sub(r'<[^>]+>', '', li_content).strip()
                    if li_text:
                        content_parts.append(f"• {li_text}\n")
                content_parts.append("\n")
            continue
        
        # If it's just text content, clean and add it
        if not re.search(r'<[^>]+>', element):
            clean_text = unescape(element).strip()
            if clean_text:
                content_parts.append(f"{clean_text}\n\n")
    
    # If no structured content found, fall back to simple cleaning
    if not content_parts:
        clean_text = re.sub(r'<[^>]+>', '', html)
        clean_text = unescape(clean_text).strip()
        content_parts.append(clean_text)
    
    # Join all parts and clean up
    result = ''.join(content_parts)
    result = unescape(result)
    
    # Clean up excessive newlines but preserve structure
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
    
    return result.strip()
