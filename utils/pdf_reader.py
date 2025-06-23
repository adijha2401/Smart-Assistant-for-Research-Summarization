import io
import pdfplumber

def extract_text_from_file(filename, content):
    try:
        if filename.endswith(".pdf"):
            text = ""
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()

        elif filename.endswith(".txt"):
            return content.decode("utf-8")

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise RuntimeError(f"Failed to read file: {e}")