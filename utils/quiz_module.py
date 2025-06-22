import os
import requests
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not found in environment variables.")

def generate_quiz(document_text):
    try:
        prompt = f"""Generate three logic-based or comprehension-focused questions based on the document below. Only return the questions as a numbered list.

Document:
{document_text}
"""

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that creates comprehension questions."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=body, timeout=30)
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        if not content:
            return ["Error: Empty response from quiz generation."]

        return [q.strip() for q in content.strip().split('\n') if q.strip()]

    except Exception as e:
        return [f"Error generating quiz: {e}"]


def evaluate_answers(document_text, user_answers):
    try:
        questions = generate_quiz(document_text)
        results = []

        for i, question in enumerate(questions):
            user_answer = user_answers[i] if i < len(user_answers) else ""

            prompt = f"""
Document:
{document_text}

Question: {question}
User's Answer: {user_answer}
Evaluate if this is correct. Say True/False and justify it.
"""

            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a teaching assistant that gives feedback on answers."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=body, timeout=30)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

            if not result:
                result = "No justification provided by model."

            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct": "True" in result,
                "justification": result.strip()
            })

        return results

    except Exception as e:
        return [{
            "question": "N/A",
            "user_answer": "N/A",
            "correct": False,
            "justification": f"Error evaluating answers: {e}"
        }]
