
from src.retrieval.retriever import DocumentRetriever

# Create retriever
retriever = DocumentRetriever(top_k=3)

# Student question
question = "Explain neural networks."

# Retrieve relevant information
results = retriever.retrieve(question)

print("Student Question:", question)

for index, result in enumerate(results, start=1):

    print("\n------------------------")
    print("Retrieved Chunk:", index)

    print("Source:", result["metadata"]["filename"])

    print("Content:")
    print(result["text"])
