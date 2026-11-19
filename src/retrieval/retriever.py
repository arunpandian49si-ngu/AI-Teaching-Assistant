
from src.retrieval.similarity_search import search_similar_chunks


class DocumentRetriever:

    def __init__(self, top_k=3):
        self.top_k = top_k

    def retrieve(self, question):

        results = search_similar_chunks(
            question=question,
            top_k=self.top_k
        )

        return results
