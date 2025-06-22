# ✅ utils/quiz_module.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz(document: str) -> list[str]:
    """
    Generates 3 logic/comprehension questions from the given document.
    """
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


def evaluate_answers(document: str, user_answers: list[str]) -> list[dict]:
    """
    Evaluates user answers and provides feedback with correctness and justification.
    """
    prompt = f"""
    Evaluate the following user answers against the document. For each, give:
    - Original question
    - User answer
    - Correctness (Yes/No)
    - Justification

    Document:
    {document}

    User Answers:
    {user_answers}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a logical evaluator bot."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        text = response.choices[0].message.content.strip()

        # NOTE: This could be parsed more robustly based on format
        feedback_list = []
        for i, line in enumerate(text.split("\n\n")):
            feedback_list.append({
                "question": f"Q{i+1}",
                "user_answer": user_answers[i] if i < len(user_answers) else "",
                "correct": "Yes" if "yes" in line.lower() else "No",
                "justification": line.strip()
            })

        return feedback_list

    except Exception as e:
        return [{"question": f"Q{i+1}", "user_answer": user_answers[i], "correct": "Error", "justification": str(e)} for i in range(len(user_answers))]
