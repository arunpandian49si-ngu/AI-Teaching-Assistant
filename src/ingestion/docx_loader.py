
from docx import Document


def extract_docx_text(docx_path):

    document = Document(docx_path)

    extracted_content = []

    # Extract paragraphs
    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            extracted_content.append(text)

    # Extract tables
    for table in document.tables:

        for row in table.rows:

            row_data = []

            for cell in row.cells:
                row_data.append(cell.text.strip())

            extracted_content.append(" | ".join(row_data))

    return extracted_content
