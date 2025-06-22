# ✅ utils/qa_module.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question(question: str, document: str) -> tuple[str, str]:
    """
    Answers a question using the given document and provides justification.
    Returns: (answer, justification)
    """
    prompt = f"""
    Read the following document and answer the question. Provide your answer and then cite the paragraph or section you used to support your answer.

    Document:
    {document}

    Question: {question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert assistant that answers precisely with justification."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        full_response = response.choices[0].message.content.strip()

        # Optional: naive separation if you format your prompt well
        if "Justification:" in full_response:
            answer_part, justification = full_response.split("Justification:", 1)
            return answer_part.strip(), justification.strip()
        else:
            return full_response, "Justification not clearly found."

    except Exception as e:
        return "Error processing question.", str(e)