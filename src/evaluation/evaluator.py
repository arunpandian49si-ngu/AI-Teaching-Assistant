
import json

from src.retrieval.retriever import DocumentRetriever
from src.rag_pipeline import RAGPipeline


# ==========================================
# LOAD EVALUATION DATASET
# ==========================================

def load_test_questions(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================
# KEYWORD COVERAGE
# ==========================================

def calculate_keyword_coverage(text, keywords):

    if not keywords:
        return 0.0

    text = text.lower()

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword.lower() in text
    ]

    return len(matched_keywords) / len(keywords) * 100


# ==========================================
# RAG EVALUATION
# ==========================================

def evaluate_rag(file_path="tests/evaluation_questions.json"):

    questions = load_test_questions(file_path)

    retriever = DocumentRetriever(top_k=3)
    rag = RAGPipeline(top_k=3)

    results = []

    for index, item in enumerate(questions, start=1):

        question = item["question"]
        expected_answer = item["expected_answer"]
        keywords = item["expected_keywords"]

        print(f"\nEvaluating Question {index}: {question}")

        # Step 1: Retrieve relevant chunks
        retrieved_chunks = retriever.retrieve(question)

        retrieved_context = " ".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        retrieval_score = calculate_keyword_coverage(
            retrieved_context,
            keywords
        )

        # Step 2: Generate RAG answer
        response = rag.ask(question)

        generated_answer = response["answer"]

        answer_score = calculate_keyword_coverage(
            generated_answer,
            keywords
        )

        # Step 3: Save evaluation result
        result = {
            "question": question,
            "expected_answer": expected_answer,
            "generated_answer": generated_answer,
            "retrieval_score": round(retrieval_score, 2),
            "answer_score": round(answer_score, 2),
            "sources": response["sources"]
        }

        results.append(result)

        print("Retrieval Score:", retrieval_score, "%")
        print("Answer Score:", answer_score, "%")
        print("Generated Answer:", generated_answer)

    return results


# ==========================================
# EVALUATION SUMMARY
# ==========================================

def print_evaluation_summary(results):

    if not results:
        print("No evaluation results available.")
        return

    average_retrieval = sum(
        result["retrieval_score"] for result in results
    ) / len(results)

    average_answer = sum(
        result["answer_score"] for result in results
    ) / len(results)

    print("\n========== EVALUATION SUMMARY ==========")

    print("Total Questions:", len(results))

    print("Average Retrieval Score:",
          round(average_retrieval, 2), "%")

    print("Average Answer Score:",
          round(average_answer, 2), "%")

    print("========================================")
