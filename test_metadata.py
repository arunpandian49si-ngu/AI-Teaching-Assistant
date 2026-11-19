
from src.utils.metadata import (
    generate_document_id,
    create_metadata
)

document_id = generate_document_id()

metadata = create_metadata(
    filename="data/uploads/sample.pdf",
    document_id=document_id,
    page_number=1
)

print(metadata)
