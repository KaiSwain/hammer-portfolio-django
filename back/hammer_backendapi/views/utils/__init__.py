# Import non-WeasyPrint functions safely
from .pdf_master import generate_master_pdf_pymupdf

# Lazy import functions that depend on WeasyPrint
def generate_certificate_pdf(*args, **kwargs):
    """Lazy wrapper for generate_certificate_pdf"""
    from .pdf_utils import generate_certificate_pdf as _generate_certificate_pdf
    return _generate_certificate_pdf(*args, **kwargs)

def html_to_pdf_bytes(*args, **kwargs):
    """Lazy wrapper for html_to_pdf_bytes"""
    from .pdf_utils import html_to_pdf_bytes as _html_to_pdf_bytes
    return _html_to_pdf_bytes(*args, **kwargs)

