# tools/summarizer.py

import fitz  # PyMuPDF

def summarize_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()

        if not text:
            return "PDF is empty or unreadable."

        # Simple summary fallback (LLM optional here)
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"PDF Summary Error: {str(e)}"

# tools/summarizer.py

from newspaper import Article

def summarize_url(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article.summary
    except Exception as e:
        return f"Error summarizing URL: {e}"

