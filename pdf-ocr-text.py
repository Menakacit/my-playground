import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Set path to Tesseract executable if not in PATH
# Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 📁 Folder containing PDFs
pdf_folder = 'C:/Users/Public/Split PDF/input/'
output_folder = 'C:/Users/Public/Split PDF/output'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# 🔁 Loop through all PDFs in the folder
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing: {filename}")

        # Convert PDF to images
        images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler\Library\bin')
        


        # OCR each page
        full_text = ''
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            full_text += f"\n--- Page {i+1} ---\n{text}"

        # Save to text file
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"Saved OCR output to: {output_path}")
