
import os
import hashlib

from src.ingestion.pdf_loader import extract_pdf_text
from src.ingestion.docx_loader import extract_docx_text
from src.utils.metadata import generate_document_id, create_metadata


SUPPORTED_EXTENSIONS = [".pdf", ".docx"]


def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def get_document_intelligence(folder_path="data/uploads"):
    """
    Extract document-level information for the My Documents page.
    """

    reports = []

    if not os.path.exists(folder_path):
        return reports

    for filename in sorted(os.listdir(folder_path)):

        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        try:
            file_size = os.path.getsize(file_path)
            file_hash = calculate_file_hash(file_path)

            if extension == ".pdf":

                pages = extract_pdf_text(file_path)

                text = "\n".join(
                    page["text"] for page in pages
                )

                page_count = len(pages)

            else:

                paragraphs = extract_docx_text(file_path)

                text = "\n".join(paragraphs)

                # python-docx does not provide reliable page count.
                page_count = None

            word_count = len(text.split())
            character_count = len(text)

            reports.append({
                "filename": filename,
                "file_type": extension.replace(".", "").upper(),
                "file_size_bytes": file_size,
                "page_count": page_count,
                "word_count": word_count,
                "character_count": character_count,
                "file_hash": file_hash,
                "extraction_status": (
                    "Successful" if text.strip()
                    else "No readable text found"
                )
            })

        except Exception as error:

            reports.append({
                "filename": filename,
                "file_type": extension.replace(".", "").upper(),
                "file_size_bytes": (
                    os.path.getsize(file_path)
                    if os.path.exists(file_path) else 0
                ),
                "page_count": None,
                "word_count": 0,
                "character_count": 0,
                "file_hash": None,
                "extraction_status": f"Failed: {error}"
            })

    return reports


def load_documents(folder_path):

    all_documents = []

    if not os.path.exists(folder_path):
        return all_documents

    files = os.listdir(folder_path)

    for filename in files:

        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        document_id = generate_document_id()
        file_hash = calculate_file_hash(file_path)

        if extension == ".pdf":

            pages = extract_pdf_text(file_path)

            for page in pages:

                metadata = create_metadata(
                    filename=filename,
                    document_id=document_id,
                    page_number=page["page_number"]
                )

                metadata["file_hash"] = file_hash

                all_documents.append({
                    "text": page["text"],
                    "metadata": metadata
                })

        elif extension == ".docx":

            paragraphs = extract_docx_text(file_path)

            metadata = create_metadata(
                filename=filename,
                document_id=document_id
            )

            metadata["file_hash"] = file_hash

            for paragraph in paragraphs:

                if not paragraph.strip():
                    continue

                all_documents.append({
                    "text": paragraph,
                    "metadata": metadata.copy()
                })

    return all_documents
