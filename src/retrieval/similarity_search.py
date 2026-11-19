
from src.vectorstore.chroma_store import collection
from src.embeddings.embedding_model import generate_embeddings


def search_similar_chunks(question, top_k=3):

    # Convert student question into an embedding
    question_embedding = generate_embeddings([question])

    # Search ChromaDB
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k
    )

    retrieved_chunks = []

    # Extract matching documents
    for index in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return retrieved_chunks
