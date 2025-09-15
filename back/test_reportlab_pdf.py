#!/usr/bin/env python3
"""
Test ReportLab PDF generation to ensure Railway compatibility
"""
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_reportlab_pdf():
    """Test basic ReportLab PDF generation"""
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        print("✅ ReportLab imports successful")
        
        # Create a simple PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        story = []
        story.append(Paragraph("Test PDF Generation", styles['Title']))
        story.append(Paragraph("This is a test paragraph.", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        
        print(f"✅ PDF generated successfully: {len(pdf_data)} bytes")
        
        # Save test file
        with open('test_reportlab_output.pdf', 'wb') as f:
            f.write(pdf_data)
        print("✅ Test PDF saved as test_reportlab_output.pdf")
        
        return True
        
    except ImportError as e:
        print(f"❌ ReportLab import failed: {e}")
        print("Install with: pip install reportlab")
        return False
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing ReportLab PDF generation...")
    success = test_reportlab_pdf()
    if success:
        print("✅ ReportLab is working correctly!")
    else:
        print("❌ ReportLab test failed!")
        sys.exit(1)