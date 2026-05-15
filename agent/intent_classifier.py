"""DistilBERT-based zero-shot intent classifier.

Uses Hugging Face's zero-shot-classification pipeline with a DistilBERT MNLI
checkpoint. Deterministic, runs on CPU in ~300-700 ms per query, no LLM call.

Falls back to None if confidence is below CONFIDENCE_THRESHOLD so the router
can use its deterministic keyword fallback.
"""

import os
from dotenv import load_dotenv

load_dotenv()

VALID_INTENTS = {"calculator", "search", "stock_price", "code_executor", "summarizer", "llm"}

LABEL_TO_INTENT = {
    "a math problem": "calculator",
    "a stock price question": "stock_price",
    "python code to execute": "code_executor",
    "a request to summarize a web page": "summarizer",
    "a web search for current information": "search",
    "casual conversation or general explanation": "llm",
}

_CANDIDATE_LABELS = list(LABEL_TO_INTENT.keys())
_HYPOTHESIS_TEMPLATE = "This query is {}."
_CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE", "0.30"))

_MODEL = os.getenv("INTENT_MODEL", "typeform/distilbert-base-uncased-mnli")
_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline
        _pipeline = pipeline(
            "zero-shot-classification",
            model=_MODEL,
            device=-1,
        )
    return _pipeline


def classify_intent(query: str) -> str | None:
    try:
        clf = _get_pipeline()
        result = clf(
            query,
            candidate_labels=_CANDIDATE_LABELS,
            hypothesis_template=_HYPOTHESIS_TEMPLATE,
            multi_label=False,
        )
        top_label = result["labels"][0]
        top_score = result["scores"][0]
        if top_score < _CONFIDENCE_THRESHOLD:
            return None
        intent = LABEL_TO_INTENT.get(top_label)
        return intent if intent in VALID_INTENTS else None
    except Exception:
        return None
