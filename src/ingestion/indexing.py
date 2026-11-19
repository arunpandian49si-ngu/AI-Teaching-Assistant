
from src.ingestion.document_manager import load_documents
from src.chunking.chunker import chunk_documents
from src.embeddings.embedding_model import generate_embeddings

from src.vectorstore.chroma_store import (
    is_document_indexed,
    delete_existing_documents,
    store_embeddings
)


# =====================================================
# CONFIGURATION
# =====================================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

PROCESSING_BATCH_SIZE = 64
EMBEDDING_BATCH_SIZE = 32


# =====================================================
# INCREMENTAL DOCUMENT INDEXING
# =====================================================

def index_uploaded_documents(folder_path="data/uploads"):

    print("\nStarting document processing...")

    # Step 1: Extract documents
    documents = load_documents(folder_path)

    if not documents:
        print("No documents found.")
        return 0

    print(f"Extracted {len(documents)} document sections.")

    # Step 2: Identify new or modified documents
    pending_documents = []
    skipped_files = set()
    file_status = {}

    for document in documents:

        metadata = document["metadata"]

        filename = metadata["filename"]
        file_hash = metadata["file_hash"]

        # Check each file only once
        if filename not in file_status:

            indexed = is_document_indexed(
                filename=filename,
                file_hash=file_hash
            )

            file_status[filename] = indexed

        if file_status[filename]:

            skipped_files.add(filename)

        else:

            pending_documents.append(document)

    print(f"Already indexed files skipped: {len(skipped_files)}")

    # Step 3: Check whether processing is required
    if not pending_documents:

        print("All documents are already up to date.")

        # Positive return value indicates existing documents are ready.
        return 1

    changed_files = {
        document["metadata"]["filename"]
        for document in pending_documents
    }

    print(f"New or modified files: {len(changed_files)}")

    # Step 4: Create chunks only for pending documents
    chunks = chunk_documents(
        pending_documents,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    if not chunks:

        print("No readable text chunks found.")
        return 0

    total_chunks = len(chunks)

    print(f"Created {total_chunks} chunks.")

    # Step 5: Delete old versions of changed documents
    delete_existing_documents(changed_files)

    # Step 6: Generate embeddings and store in batches
    for start in range(0, total_chunks, PROCESSING_BATCH_SIZE):

        end = min(
            start + PROCESSING_BATCH_SIZE,
            total_chunks
        )

        current_chunks = chunks[start:end]

        texts = [
            chunk["text"]
            for chunk in current_chunks
        ]

        print(
            f"Generating embeddings: {start + 1}-{end} "
            f"of {total_chunks}"
        )

        embeddings = generate_embeddings(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE
        )

        store_embeddings(
            current_chunks,
            embeddings
        )

        print(
            f"Completed processing: {end}/{total_chunks}"
        )

    print("\nDocument indexing completed successfully.")

    return total_chunks
