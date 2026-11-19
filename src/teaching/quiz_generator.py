
import json
import random
import re

from langchain_ollama import ChatOllama

from src.retrieval.retriever import DocumentRetriever
from src.teaching.teaching_prompts import build_quiz_prompt


class QuizGenerator:

    def __init__(self, top_k=5):

        self.retriever = DocumentRetriever(top_k=top_k)

        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.2,
            format="json"
        )

    # ==============================================
    # PARSE JSON
    # ==============================================

    def parse_questions(self, response_text):

        try:
            data = json.loads(response_text)

            if not isinstance(data, dict):
                return []

            questions = data.get("questions", [])

            if isinstance(questions, list):
                return questions

            return []

        except (json.JSONDecodeError, TypeError):
            return []

    # ==============================================
    # VALIDATE QUESTION
    # ==============================================

    def validate_question(self, question):

        if not isinstance(question, dict):
            return False

        required_keys = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        if not all(key in question for key in required_keys):
            return False

        question_text = question["question"]
        explanation = question["explanation"]
        options = question["options"]

        if not isinstance(question_text, str):
            return False

        if not isinstance(explanation, str):
            return False

        if not question_text.strip():
            return False

        if not explanation.strip():
            return False

        if not isinstance(options, dict):
            return False

        keys = ["A", "B", "C", "D"]

        if not all(key in options for key in keys):
            return False

        option_values = []

        for key in keys:

            value = options[key]

            if not isinstance(value, str):
                return False

            value = value.strip()

            if not value:
                return False

            option_values.append(value.casefold())

        # All four options must be different
        if len(set(option_values)) != 4:
            return False

        answer = str(
            question["correct_answer"]
        ).strip().upper()

        if answer not in keys:
            return False

        question["question"] = question_text.strip()
        question["explanation"] = explanation.strip()
        question["correct_answer"] = answer

        question["options"] = {
            key: options[key].strip()
            for key in keys
        }

        return True

    # ==============================================
    # SHUFFLE OPTIONS
    # ==============================================

    def shuffle_options(self, question):

        original_options = question["options"]

        correct_answer = question["correct_answer"]

        correct_text = original_options[correct_answer]

        values = list(original_options.values())

        random.SystemRandom().shuffle(values)

        new_options = {
            key: value
            for key, value in zip(
                ["A", "B", "C", "D"],
                values
            )
        }

        # Find the new correct answer position
        new_correct_answer = next(
            key
            for key, value in new_options.items()
            if value == correct_text
        )

        question["options"] = new_options

        question["correct_answer"] = new_correct_answer

        return question

    # ==============================================
    # GENERATE ONE QUESTION
    # ==============================================

    def generate_one_question(
        self,
        topic,
        context,
        existing_questions
    ):

        prompt = build_quiz_prompt(
            context=context,
            topic=topic,
            number_of_questions=1
        )

        prompt += f"""

IMPORTANT ADDITIONAL INSTRUCTIONS:

Generate exactly ONE new question.

Question must be based on the reference material.

There must be exactly four different options.

Only one option must be the correct answer.

The remaining three options must be clearly incorrect.

Do not create subjective or ambiguous questions.

Do not repeat these existing questions:
{json.dumps(existing_questions, ensure_ascii=False)}

The correct_answer field must contain only A, B, C or D.

Return JSON only.
"""

        response = self.llm.invoke(prompt)

        generated_questions = self.parse_questions(
            response.content
        )

        if not generated_questions:
            return None

        # Use the first generated question
        question = generated_questions[0]

        if not self.validate_question(question):
            return None

        return question

    # ==============================================
    # MAIN QUIZ GENERATION
    # ==============================================

    def generate(self, topic, number_of_questions=5):

        number_of_questions = max(
            1,
            min(int(number_of_questions), 20)
        )

        if not topic or not topic.strip():
            raise ValueError("Please enter a quiz topic.")

        # Retrieve relevant document content
        results = self.retriever.retrieve(topic)

        if not results:

            return {
                "questions": [],
                "sources": []
            }

        context_parts = []
        sources = []

        for result in results:

            text = result.get("text", "").strip()

            if text:
                context_parts.append(text)

            metadata = result.get("metadata", {})

            filename = metadata.get("filename", "Unknown")
            page = metadata.get("page_number", "N/A")

            source = f"{filename}, Page {page}"

            if source not in sources:
                sources.append(source)

        context = "\n\n".join(context_parts)

        # Keep the context manageable for the local model
        context = context[:6000]

        if not context.strip():

            return {
                "questions": [],
                "sources": []
            }

        questions = []
        seen_questions = set()

        # Retry only when a question is invalid or duplicated
        max_attempts_per_question = 8

        for question_number in range(number_of_questions):

            accepted = False

            for attempt in range(max_attempts_per_question):

                existing_questions = [
                    question["question"]
                    for question in questions
                ]

                try:

                    question = self.generate_one_question(
                        topic=topic,
                        context=context,
                        existing_questions=existing_questions
                    )

                except Exception:
                    continue

                if question is None:
                    continue

                question_text = question["question"].strip()

                # Normalize question for duplicate detection
                question_key = re.sub(
                    r"\s+",
                    " ",
                    question_text.casefold()
                )

                if question_key in seen_questions:
                    continue

                # Randomize the correct answer position
                question = self.shuffle_options(question)

                questions.append(question)

                seen_questions.add(question_key)

                accepted = True

                break

            if not accepted:

                raise ValueError(
                    f"Could not generate a valid question "
                    f"for question {question_number + 1} "
                    f"after {max_attempts_per_question} attempts. "
                    "Try a simpler topic or upload more relevant material."
                )

        if len(questions) != number_of_questions:

            raise ValueError(
                "Unable to generate the requested number of questions."
            )

        return {
            "questions": questions,
            "sources": sources
        }
