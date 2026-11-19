
from src.ingestion.docx_loader import extract_docx_text

docx_path = "data/uploads/sample.docx"

content = extract_docx_text(docx_path)

for item in content:

    print(item)
