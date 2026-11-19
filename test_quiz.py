
from src.teaching.quiz_generator import QuizGenerator


generator = QuizGenerator(top_k=5)

topic = "Neural Networks"

result = generator.generate(
    topic=topic,
    number_of_questions=5
)

print("\n========== AI GENERATED QUIZ ==========\n")

print(result["quiz"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print(source)
