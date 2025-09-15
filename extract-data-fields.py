import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import re
import csv
import json

# Optional: set Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_page(pdf_path, page_num):
    images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
    return pytesseract.image_to_string(images[0])

def find_receipt_starts(pdf_path, exact_title):
    doc = fitz.open(pdf_path)
    starts = []
    for i in range(len(doc)):
        text = ocr_page(pdf_path, i)
        if exact_title in text:
            starts.append(i)
    starts.append(len(doc))  # Add end marker
    return starts

def split_receipts(pdf_path, exact_title, output_dir):
    doc = fitz.open(pdf_path)
    starts = find_receipt_starts(pdf_path, exact_title)
    receipts = []

    for i in range(len(starts) - 1):
        receipt_doc = fitz.open()
        for j in range(starts[i], starts[i+1]):
            receipt_doc.insert_pdf(doc, from_page=j, to_page=j)
        filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_receipt_{i+1}.pdf"
        filepath = os.path.join(output_dir, filename)
        receipt_doc.save(filepath)
        receipts.append((filepath, starts[i], starts[i+1]))
    return receipts

def infer_fields(text):
    fields = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or len(line) > 100: continue
        match = re.match(r"(.{2,40})[:\-]\s*(.+)", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            fields[key] = value
    return fields

def extract_receipt_data(receipts, pdf_path):
    all_data = []
    for filename, start, end in receipts:
        full_text = ""
        for page_num in range(start, end):
            full_text += ocr_page(pdf_path, page_num) + "\n"
        fields = infer_fields(full_text)
        fields["Receipt File"] = os.path.basename(filename)
        fields["Source PDF"] = os.path.basename(pdf_path)
        all_data.append(fields)
    return all_data

def process_folder(folder_path, exact_title, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_receipt_data = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            receipts = split_receipts(pdf_path, exact_title, output_dir)
            data = extract_receipt_data(receipts, pdf_path)
            all_receipt_data.extend(data)

    # Save CSV
    keys = sorted({k for d in all_receipt_data for k in d.keys()})
    with open("all_receipts.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_receipt_data)

    # Save JSON
    with open("all_receipts.json", "w") as f:
        json.dump(all_receipt_data, f, indent=4)

# 🔧 Run the batch processor
folder_path = "./receipts"         # Folder containing PDFs
exact_title = "Sales Receipt"          # Exact title to split on
output_dir = "./split_receipts"    # Where to save individual receipt PDFs

process_folder(folder_path, exact_title, output_dir)
