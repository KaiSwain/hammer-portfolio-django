"""
grid_overlay.py
-------------------
Purpose:
Adds a coordinate grid overlay on every page of your PDF template.
Helps you visually find exact X,Y positions for placing text.

How to run:
1. Ensure Certificates_Master.pdf is in the static folder.
2. Run:
   python grid_overlay.py
3. Open Certificates_Grid.pdf and note down coordinates.
"""

import fitz  # PyMuPDF

# ✅ Paths
input_path = "static/Certificates_Master.pdf"
output_path = "static/Certificates2_Grid.pdf"

# ✅ Open the original template
doc = fitz.open(input_path)

# ✅ Loop through each page
for page_index, page in enumerate(doc):
    # ✅ Add small coordinate labels every 50 points
    for x in range(0, 1000, 25):  # Horizontal
        for y in range(0, 1000, 25):  # Vertical
            page.insert_text(
                (x, y),           # Position
                f"{x},{y}",       # Label text
                fontsize=6,       # Small font
                color=(0, 0, 0)   # Black
            )

# ✅ Save the updated file
doc.save(output_path)
print(f"✅ Grid overlay created: {output_path}")
print("➡ Open this file and use coordinates for your text placement.")
