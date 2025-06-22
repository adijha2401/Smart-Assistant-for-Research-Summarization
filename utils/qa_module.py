import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not found in environment variables.")

def answer_question(question, document_text):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""Read the document below and answer the following question. Then provide a short justification referencing relevant sections of the document.

Document:
{document_text}

Question:
{question}
"""

        body = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a document reasoning assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Safe extraction
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not content:
            return "No response from model.", "Empty or unexpected response format."

        if "Justification:" in content:
            answer, justification = content.split("Justification:", 1)
        else:
            answer = content
            justification = "Not explicitly provided."

        return answer.strip(), justification.strip()

    except Exception as e:
        return "Error answering question.", str(e)