from borb.pdf import PDF
from io import BytesIO

template_path = "static/Certificates_Master.pdf"

try:
    with open(template_path, "rb") as pdf_file:
        result = PDF.loads(pdf_file)

        if isinstance(result, tuple):
            doc = result[0]
        else:
            doc = result

        print("Type of doc:", type(doc))

        # Try writing back to memory
        buffer = BytesIO()
        PDF.dumps(buffer, doc)
        buffer.seek(0)

        print("PDF re-serialized successfully. Size:", len(buffer.read()), "bytes")

except Exception as e:
    print("Error:", str(e))
    