import os
import fitz  # PyMuPDF
from pathlib import Path

# 📁 Set your folder path containing PDFs
input_folder = 'C:/Users/Public/Split PDF/input/'
output_folder = 'C:/Users/Public/Split PDF/output/'
os.makedirs(output_folder, exist_ok=True)

# 🔍 Keyword that marks the start of a new receipt
receipt_keyword = "THIS IS THE TITLE WHERE SPLIT IS NEEDED"

def split_receipts_from_pdf(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    receipt_pages = []
    receipt_count = 0

    for i, page in enumerate(doc):
        text = page.get_text()
        if receipt_keyword in text:
            if receipt_pages:
                # Save previous receipt
                receipt_count += 1
                save_receipt(doc, receipt_pages, output_dir, receipt_count)
                receipt_pages = []
        receipt_pages.append(i)

    # Save the last receipt
    if receipt_pages:
        receipt_count += 1
        save_receipt(doc, receipt_pages, output_dir, receipt_count)

def save_receipt(doc, page_indices, output_dir, count):
    new_doc = fitz.open()
    for idx in page_indices:
        new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
    filename = f"receipt_{count}.pdf"
    new_doc.save(os.path.join(output_dir, filename))
    new_doc.close()

# 🚀 Process all PDFs in the folder
for file in Path(input_folder).glob("*.pdf"):
    print(f"Processing: {file.name}")
    split_receipts_from_pdf(str(file), output_folder)

print("✅ Done splitting receipts!")
