
from sentence_transformers import SentenceTransformer


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts, batch_size=64):

    if not texts:
        return []

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings
