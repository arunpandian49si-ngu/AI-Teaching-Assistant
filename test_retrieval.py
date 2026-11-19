
from src.retrieval.similarity_search import search_similar_chunks

question = "What is artificial intelligence?"

results = search_similar_chunks(
    question,
    top_k=3
)

print("\nStudent Question:", question)

for index, result in enumerate(results, start=1):

    print("\n-----------------------------")
    print("Result:", index)

    print("Document:", result["metadata"]["filename"])

    print("Page:", result["metadata"].get("page_number", "N/A"))

    print("Distance:", result["distance"])

    print("Retrieved Text:")
    print(result["text"])
