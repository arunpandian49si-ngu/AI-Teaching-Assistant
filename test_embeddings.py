
from src.ingestion.document_manager import load_documents
from src.chunking.chunker import chunk_documents
from src.embeddings.embedding_model import generate_embeddings

# Step 1: Load documents
documents = load_documents("data/uploads")

# Step 2: Create chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    chunk_overlap=100
)

# Step 3: Extract chunk text
texts = [chunk["text"] for chunk in chunks]

# Step 4: Generate embeddings
embeddings = generate_embeddings(texts)

# Step 5: Display results
print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nFirst chunk:")
print(texts[0])

print("\nFirst embedding:")
print(embeddings[0])

print("\nDimensions:", len(embeddings[0]))
