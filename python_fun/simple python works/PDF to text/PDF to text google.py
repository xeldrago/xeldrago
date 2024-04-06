import pytesseract
from pdf2image import convert_from_path

# Path to the PDF file
pdf_path = 'input.pdf'

# Convert PDF pages to images
pages = convert_from_path(pdf_path)

# Extract text from each page using Tesseract OCR
text = ''
for page in pages:
    text += pytesseract.image_to_string(page)

# Output the extracted text
print(text)
