
import chromadb

from chromadb.utils.batch_utils import create_batches


# =====================================================
# DATABASE CONNECTION
# =====================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="teaching_documents"
)


# =====================================================
# CHECK WHETHER DOCUMENT IS ALREADY INDEXED
# =====================================================

def is_document_indexed(filename, file_hash):

    results = collection.get(
        where={"filename": filename},
        include=["metadatas"]
    )

    metadatas = results.get("metadatas", [])

    if not metadatas:
        return False

    return all(
        metadata.get("file_hash") == file_hash
        for metadata in metadatas
    )


# =====================================================
# GET ALL INDEXED DOCUMENTS
# =====================================================

def get_indexed_documents():

    results = collection.get(
        include=["metadatas"]
    )

    document_summary = {}

    for metadata in results.get("metadatas", []):

        filename = metadata.get("filename", "Unknown")

        if filename not in document_summary:

            document_summary[filename] = {
                "filename": filename,
                "chunks": 0,
                "file_hash": metadata.get("file_hash", "")
            }

        document_summary[filename]["chunks"] += 1

    return list(document_summary.values())


# =====================================================
# DELETE DOCUMENT EMBEDDINGS
# =====================================================

def delete_document_embeddings(filename):

    collection.delete(
        where={"filename": filename}
    )

    print(f"Deleted embeddings for: {filename}")


# =====================================================
# DELETE OLD DOCUMENT VERSIONS
# =====================================================

def delete_existing_documents(filenames):

    for filename in set(filenames):

        collection.delete(
            where={"filename": filename}
        )


# =====================================================
# STORE EMBEDDINGS SAFELY IN CHROMA BATCHES
# =====================================================

def store_embeddings(chunks, embeddings):

    if not chunks:
        return

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count do not match."
        )

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        metadata = chunk["metadata"]

        ids.append(metadata["chunk_id"])
        documents.append(chunk["text"])
        metadatas.append(metadata)

    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()

    batches = create_batches(
        api=client,
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    total = len(ids)
    stored = 0

    for batch in batches:

        batch_ids = batch[0]
        batch_embeddings = batch[1]
        batch_metadatas = batch[2]
        batch_documents = batch[3]

        collection.upsert(
            ids=batch_ids,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
            documents=batch_documents
        )

        stored += len(batch_ids)

        print(f"Stored {stored}/{total} chunks")

    print("All embeddings stored successfully!")
