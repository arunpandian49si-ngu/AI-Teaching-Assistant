
from src.ingestion.pdf_loader import extract_pdf_text

pdf_path = "data/uploads/sample.pdf"

pages = extract_pdf_text(pdf_path)

for page in pages:
    print("\n-------------------------")
    print("Page:", page["page_number"])
    print("-------------------------")

    print(page["text"])
