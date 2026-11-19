
from src.retrieval.similarity_search import search_similar_chunks

question = input("Enter your question: ")

for top_k in [3, 5, 7]:

    print(f"\n========== TOP K: {top_k} ==========")

    results = search_similar_chunks(
        question=question,
        top_k=top_k
    )

    for index, result in enumerate(results, start=1):

        print(f"\nChunk {index}")
        print("Filename:", result["metadata"].get("filename"))
        print("Page:", result["metadata"].get("page_number"))
        print("Distance:", round(result["distance"], 4))
        print("Text:", result["text"][:500])

