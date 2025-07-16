import fitz
import pytesseract
from pdf2image import convert_from_path
import os


def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()

        if len(text.strip()) < 50:
            print("[INFO] Native text extraction failed or is too short. Falling back to OCR...")
            text = ocr_pdf(pdf_path)
    except Exception as e:
        print(f"[ERROR] Failed to open or parse PDF natively: {e}")
        print("[INFO] Falling back to OCR...")
        text = ocr_pdf(pdf_path)

    return text.strip()

def ocr_pdf(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for i, img in enumerate(images):
            print(f"[OCR] Processing page {i+1}...")
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
    return text

def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(image_path)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR on image failed: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <document_path>")
    else:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"File '{path}' not found.")
        else:
            print("[INFO] Extracting text...")
            if path.lower().endswith((".jpg", ".png", ".jpeg")):
                output = extract_text_from_image(path)
            else:
                output = extract_text_from_pdf(path)

            with open("context.txt", "w", encoding="utf-8") as f:
                f.write(output)
            print("[INFO] Extracted text saved to context.txt")
