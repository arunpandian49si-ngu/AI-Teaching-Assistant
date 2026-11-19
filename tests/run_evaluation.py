
from src.evaluation.evaluator import (
    evaluate_rag,
    print_evaluation_summary
)

results = evaluate_rag()

print_evaluation_summary(results)
