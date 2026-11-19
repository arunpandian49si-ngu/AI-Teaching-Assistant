from src.teaching.teaching_prompts import build_teaching_prompt

context = """
Artificial Intelligence is the simulation of
human intelligence by machines.

Machine Learning is a subset of AI that enables
systems to learn from data.
"""

question = "Explain Artificial Intelligence."

prompt = build_teaching_prompt(
    context=context,
    question=question
)

print(prompt)