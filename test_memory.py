
from src.memory.conversation_memory import ConversationMemory
from src.rag_pipeline import RAGPipeline


# ==========================================
# TEST 1: BASIC CONVERSATION MEMORY
# ==========================================

print("\n========== BASIC MEMORY TEST ==========")

memory = ConversationMemory()

session_id = "student_1"

memory.add_message(
    session_id,
    "user",
    "What is Artificial Intelligence?"
)

memory.add_message(
    session_id,
    "assistant",
    "AI enables machines to perform tasks requiring human intelligence."
)

memory.add_message(
    session_id,
    "user",
    "Give me an example."
)

print(memory.format_history(session_id))


# ==========================================
# TEST 2: RAG PIPELINE MEMORY INTEGRATION
# ==========================================

print("\n========== RAG PIPELINE MEMORY TEST ==========")

pipeline = RAGPipeline()

student_session = "student_2"

# First question
first = pipeline.ask(
    "What is Artificial Intelligence?",
    session_id=student_session
)

print("\nFIRST ANSWER:")
print(first["answer"])


# Second question
second = pipeline.ask(
    "Explain it with an example.",
    session_id=student_session
)

print("\nSECOND ANSWER:")
print(second["answer"])


# Check saved conversation
print("\nSAVED CONVERSATION:")

print(
    pipeline.memory.format_history(student_session)
)
