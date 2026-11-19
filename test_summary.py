
from src.teaching.summary_generator import SummaryGenerator


generator = SummaryGenerator(top_k=5)

topic = "Neural Networks"

result = generator.generate(topic)

print("\n========== STUDY NOTES ==========\n")

print(result["summary"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print(source)
