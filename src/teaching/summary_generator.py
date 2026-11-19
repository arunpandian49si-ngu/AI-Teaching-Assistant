
from src.retrieval.retriever import DocumentRetriever
from src.llm.ollama_client import get_llm

from src.teaching.teaching_prompts import (
    build_summary_prompt
)


class SummaryGenerator:

    def __init__(self, top_k=5):
        """
        Initialize retriever and LLM.
        """

        self.retriever = DocumentRetriever(
            top_k=top_k
        )

        self.llm = get_llm()

    def generate(self, topic):
        """
        Generate a summary for the given topic
        using retrieved document information.
        """

        # Step 1: Validate topic
        if not topic or not topic.strip():
            return {
                "summary": "Please provide a valid topic.",
                "sources": []
            }

        # Step 2: Retrieve relevant document chunks
        results = self.retriever.retrieve(topic)

        if not results:
            return {
                "summary": "No relevant information found in the uploaded documents.",
                "sources": []
            }

        # Step 3: Prepare context and source information
        context_parts = []
        sources = []

        for result in results:

            metadata = result.get("metadata", {})

            filename = metadata.get(
                "filename", "Unknown"
            )

            page = metadata.get(
                "page_number", "N/A"
            )

            source = f"{filename}, Page {page}"

            context_parts.append(
                f"[Source: {source}]\n{result['text']}"
            )

            if source not in sources:
                sources.append(source)

        # Step 4: Combine retrieved chunks
        context = "\n\n".join(context_parts)

        # Step 5: Build summary prompt
        prompt = build_summary_prompt(
            context=context,
            topic=topic
        )

        # Step 6: Generate response using LLM
        response = self.llm.invoke(prompt)

        # Step 7: Return summary and sources
        return {
            "summary": response.content,
            "sources": sources
        }
