
from src.ingestion.document_manager import load_documents
from src.chunking.chunker import chunk_documents


# Step 1: Load PDF and DOCX documents
documents = load_documents("data/uploads")

print("Original records:", len(documents))


# Step 2: Generate chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    chunk_overlap=100
)

print("Total chunks:", len(chunks))


# Step 3: Display chunks
for index, chunk in enumerate(chunks, start=1):

    print("\n----------------------------")
    print("Chunk:", index)
    print("Metadata:", chunk["metadata"])
    print("Text:", chunk["text"])
