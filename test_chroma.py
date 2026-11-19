
from src.ingestion.document_manager import load_documents
from src.chunking.chunker import chunk_documents
from src.embeddings.embedding_model import generate_embeddings
from src.vectorstore.chroma_store import store_embeddings

# 1. Load documents
documents = load_documents("data/uploads")

# 2. Create chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    chunk_overlap=100
)

# 3. Extract text
texts = [chunk["text"] for chunk in chunks]

# 4. Generate embeddings
embeddings = generate_embeddings(texts)

# 5. Store in ChromaDB
store_embeddings(chunks, embeddings)

print("Total chunks:", len(chunks))
