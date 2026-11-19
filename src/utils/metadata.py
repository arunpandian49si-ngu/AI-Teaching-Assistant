
import uuid
import os


def generate_document_id():
    return str(uuid.uuid4())


def create_metadata(filename, document_id, page_number=None):

    metadata = {
        "document_id": document_id,
        "filename": os.path.basename(filename)
    }

    if page_number is not None:
        metadata["page_number"] = page_number

    return metadata
