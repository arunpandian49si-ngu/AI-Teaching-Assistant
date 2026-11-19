
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents, chunk_size=500, chunk_overlap=100):

    # Create the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []

    # Process every extracted document record
    for record_index, document in enumerate(documents):

        text = document["text"].strip()

        if not text:
            continue

        # Divide the text into smaller chunks
        text_chunks = splitter.split_text(text)

        # Store each chunk with its metadata
        for chunk_index, chunk_text in enumerate(text_chunks):

            metadata = document["metadata"].copy()

            metadata["chunk_id"] = (
                f"{metadata['document_id']}_{record_index}_{chunk_index}"
            )

            metadata["chunk_index"] = chunk_index

            all_chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })

    return all_chunks
