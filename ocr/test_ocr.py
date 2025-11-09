import os
from ocr.invoice_ocr import ocr_image, ocr_pdf, extract_invoice_fields

TEST_DIR = "data/test_invoices"

def main():
    for fname in os.listdir(TEST_DIR):
        path = os.path.join(TEST_DIR, fname)
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            raw_text = ocr_image(path)
        elif fname.lower().endswith('.pdf'):
            raw_text = ocr_pdf(path)
        else:
            print(f"Skipping unsupported file type: {fname}")
            continue
        fields = extract_invoice_fields(raw_text)
        print(f"\nFile: {fname}")
        print("Fields:", fields)
        print("--- Raw Text ---\n", raw_text[:500], '\n-----------------\n')

if __name__ == "__main__":
    main()
