from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import re
from dateutil import parser as dateparser

def ocr_image(path):
    """
    Extract text from an image file using Tesseract OCR.
    Converts image to grayscale for better OCR accuracy.
    """
    img = Image.open(path).convert('L')  # grayscale
    text = pytesseract.image_to_string(img, lang='eng')
    return text

def ocr_pdf(path):
    """
    Extract text from a PDF file (all pages) using pdf2image and Tesseract OCR.
    Converts each PDF page to an image and concatenates all text.
    """
    pages = convert_from_path(path, dpi=300)
    all_text = "\n".join([pytesseract.image_to_string(pg) for pg in pages])
    return all_text

def extract_invoice_fields(text):
    """
    Parse key fields from OCR raw text: invoice number, amount, currency, date, and vendor.
    Uses regex and dateutil parser with fallback on missing fields.
    """
    # Invoice number: typical patterns like "Invoice No:", "Inv", "Invoice"
    invoice_id = re.search(r'(Invoice\s*No|Inv\.?|Invoice)\s*[:\-]?\s*([A-Z0-9\-\/]+)', text, re.I)

    # Amount: keywords "Total", "Grand Total", "Amount Due" followed by currency amount
    amount = re.search(r'(Total(?:\s*Due)?|Grand Total|Amount Due)\s*[:\-]?\s*([₹$£]?\s*[\d,]+(?:\.\d{1,2})?)', text, re.I)

    # Currency symbols or codes (INR, USD, EUR, GBP)
    currency = re.search(r'(INR|USD|EUR|GBP|₹|\$|£)', text)

    # Date candidates: looks for MM/DD/YYYY, DD-MM-YYYY, or formats like "March 5, 2025"
    date_ = None
    date_candidates = re.findall(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\b', text)
    for d in date_candidates:
        try:
            date_ = dateparser.parse(d, fuzzy=True).date().isoformat()
            break
        except:
            continue

    # Vendor assumed from first line, limited to 50 characters
    vendor = text.strip().split('\n')[0][:50]

    return {
        "invoice_no": invoice_id.group(2).strip() if invoice_id else None,
        "amount": float(amount.group(2).replace(',', '').replace('₹', '').replace('$', '').replace('£','')) if amount else None,
        "currency": (currency.group(0).upper().replace('₹', 'INR').replace('$', 'USD').replace('£', 'GBP')) if currency else None,
        "date": date_,
        "vendor": vendor
    }
