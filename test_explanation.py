
from src.rag_pipeline import RAGPipeline

rag = RAGPipeline(top_k=3)

question = "Explain neural networks."

# Beginner explanation
print("\n===== BEGINNER LEVEL =====")

result = rag.ask(
    question,
    level="beginner"
)

print(result["answer"])


# Intermediate explanation
print("\n===== INTERMEDIATE LEVEL =====")

result = rag.ask(
    question,
    level="intermediate"
)

print(result["answer"])


# Advanced explanation
print("\n===== ADVANCED LEVEL =====")

result = rag.ask(
    question,
    level="advanced"
)

print(result["answer"])
