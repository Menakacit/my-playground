import pytesseract
from PIL import Image

# Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load a test image
img = Image.new('RGB', (100, 30), color = (255, 255, 255))
text = pytesseract.image_to_string(img)
print(text)


