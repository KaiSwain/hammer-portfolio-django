#!/usr/bin/env python3
"""
PDF Page Deletion Tool for Certificate Master
Usage: python delete_pdf_pages.py
"""

import fitz  # PyMuPDF
import os

def delete_pdf_pages():
    # Path to the certificate master PDF
    pdf_path = "static/Certificates_Master.pdf"
    backup_path = "static/Certificates_Master_backup.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found!")
        return
    
    # Create backup
    print("Creating backup...")
    import shutil
    shutil.copy2(pdf_path, backup_path)
    print(f"Backup created: {backup_path}")
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    print(f"\nPDF has {len(doc)} pages")
    print("Current pages:")
    for i in range(len(doc)):
        print(f"  Page {i + 1}")
    
    # Get pages to delete
    while True:
        try:
            pages_input = input("\nEnter page numbers to delete (comma-separated, 1-based): ")
            if not pages_input.strip():
                print("No pages specified. Exiting.")
                doc.close()
                return
            
            # Parse page numbers
            page_nums = [int(x.strip()) - 1 for x in pages_input.split(",")]  # Convert to 0-based
            
            # Validate page numbers
            invalid_pages = [p + 1 for p in page_nums if p < 0 or p >= len(doc)]
            if invalid_pages:
                print(f"Invalid page numbers: {invalid_pages}")
                continue
            
            break
        except ValueError:
            print("Please enter valid page numbers.")
    
    # Sort in descending order to delete from end to beginning
    page_nums.sort(reverse=True)
    
    # Delete pages
    print(f"\nDeleting pages: {[p + 1 for p in page_nums]}")
    for page_num in page_nums:
        doc.delete_page(page_num)
    
    # Save the modified PDF
    doc.save(pdf_path)
    doc.close()
    
    print(f"\nPDF updated successfully!")
    print(f"New page count: {fitz.open(pdf_path).__len__()}")
    print(f"Original backup saved as: {backup_path}")

if __name__ == "__main__":
    delete_pdf_pages()