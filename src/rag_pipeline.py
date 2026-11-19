
from src.teaching.teaching_prompts import build_teaching_prompt
from src.retrieval.retriever import DocumentRetriever
from src.llm.ollama_client import get_llm
from src.memory.conversation_memory import ConversationMemory


class RAGPipeline:

    def __init__(self, top_k=3):

        # Initialize document retriever
        self.retriever = DocumentRetriever(top_k=top_k)

        # Initialize LLM
        self.llm = get_llm()

        # Initialize conversation memory
        self.memory = ConversationMemory(max_history=10)

    def ask(
        self,
        question,
        level="beginner",
        session_id="default",
        teaching_mode="concept"
    ):
        """
        Generate an answer using retrieved documents,
        conversation history, explanation level and teaching mode.
        """

        # Validate inputs
        if not question or not question.strip():
            return {
                "answer": "Please enter a question.",
                "sources": []
            }

        if level not in ["beginner", "intermediate", "advanced"]:
            raise ValueError("Invalid explanation level.")

        if teaching_mode not in [
            "concept",
            "real_world",
            "step_by_step"
        ]:
            raise ValueError("Invalid teaching mode.")

        question = question.strip()

        # Step 1: Get previous conversation
        conversation_history = self.memory.format_history(session_id)

        # Step 2: Retrieve relevant document chunks
        results = self.retriever.retrieve(question)

        if not results:
            answer = (
                "I could not find relevant information "
                "in the uploaded documents."
            )

            # Save unanswered question and response too
            self.memory.add_message(session_id, "user", question)
            self.memory.add_message(session_id, "assistant", answer)

            return {
                "answer": answer,
                "sources": []
            }

        # Step 3: Prepare document context
        context_parts = []
        sources = []

        for index, result in enumerate(results, start=1):

            metadata = result.get("metadata", {})

            filename = metadata.get("filename", "Unknown")
            page = metadata.get("page_number", "N/A")

            source = f"{filename}, Page {page}"

            context_parts.append(
                f"[Source {index}: {source}]\n"
                f"{result['text']}"
            )

            if source not in sources:
                sources.append(source)

        context = "\n\n".join(context_parts)

        # Step 4: Build teaching prompt
        prompt = build_teaching_prompt(
            context=context,
            question=question,
            level=level,
            conversation_history=conversation_history,
            teaching_mode=teaching_mode
        )

        # Step 5: Generate answer using LLM
        response = self.llm.invoke(prompt)

        answer = response.content

        # Step 6: Save conversation history
        self.memory.add_message(
            session_id,
            "user",
            question
        )

        self.memory.add_message(
            session_id,
            "assistant",
            answer
        )

        # Step 7: Return answer and sources
        return {
            "answer": answer,
            "sources": sources
        }
