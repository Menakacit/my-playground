import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import os

# Optional: Set path to tesseract executable if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.medianBlur(img, 3)
    return img

def ocr_pdf(pdf_path, output_dir="ocr_output"):
    os.makedirs(output_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=300)

    for i, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"page_{i+1}.png")
        page.save(img_path, "PNG")

        processed_img = preprocess_image(img_path)
        text = pytesseract.image_to_string(processed_img, lang='eng')

        with open(os.path.join(output_dir, f"page_{i+1}.txt"), "w", encoding="utf-8") as f:
            f.write(text)

    print(f"OCR completed. Text files saved in '{output_dir}'.")

# Example usage
ocr_pdf("your_scanned_document.pdf")
