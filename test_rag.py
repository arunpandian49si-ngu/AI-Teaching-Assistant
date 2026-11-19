from src.rag_pipeline import RAGPipeline

# Initialize RAG
rag = RAGPipeline(top_k=3)

while True:

    question = input("\nAsk your question (type exit to stop): ")

    if question.lower() == "exit":
        break

    result = rag.ask(question)

    print("\n========== AI ANSWER ==========")
    print(result["answer"])

    print("\n========== SOURCES ==========")

    for source in result["sources"]:
        print(source)