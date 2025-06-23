# utils/quiz_module.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz(document: str) -> list[str]:
    prompt = f"""
    Based on the following document, create 3 logic-based or comprehension-focused questions that test understanding. Number them 1 to 3.

    Document:
    {document}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a tutor bot who makes thoughtful questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw = response.choices[0].message.content.strip()
        lines = raw.split("\n")
        questions = [line.lstrip("1234567890. ") for line in lines if line.strip()]
        return questions[:3]

    except Exception as e:
        return [f"Error generating quiz: {str(e)}"]


def evaluate_answers(document: str, questions: list[str], user_answers: list[str]) -> list[dict]:
    results = []

    for i, question in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else ""
        prompt = f"""
You are an evaluator. Determine if the user's answer is correct based on the document.
Provide:
- Question
- User's answer
- Correctness (Yes/No)
- Justification (based on document)

Document:
{document}

Q: {question}
A: {user_answer}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a teaching assistant that gives feedback on answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            feedback = response.choices[0].message.content.strip()

            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct": "yes" in feedback.lower(),
                "justification": feedback
            })

        except Exception as e:
            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct": False,
                "justification": str(e)
            })

    return results
