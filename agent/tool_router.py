"""Hybrid intent router.

Stage 1 — deterministic short-circuits (highest priority, never wrong):
  * `summarize` + URL  -> summarizer
  * `execute code:` / `run code:` prefix -> code_executor

Stage 2 — keyword router for high-confidence patterns:
  * math operators or "calculate" / "compute" -> calculator
  * "stock" / "share price" / "ticker" -> stock_price
  * realtime keywords (weather, news, today, ...) -> search
  * "search for ..." -> search
  * greetings / thanks -> llm

Stage 3 — DistilBERT zero-shot classifier for genuinely ambiguous cases
  (typically "what is X", "tell me about X", "how does X work").
"""

import re
from agent.intent_classifier import classify_intent

REALTIME_KEYWORDS = (
    "weather", "temperature", "forecast", "rain", "snow", "humidity",
    "news", "headline", "today", "tonight", "tomorrow", "currently",
    "currently", "current", "now", "latest", "score", "live", "happening",
)

GREETINGS = ("hi", "hello", "hey", "yo", "hola", "thanks", "thank you", "bye", "goodbye", "ok", "okay")

MATH_WORDS = ("calculate", "compute", "what is", "what's", "plus", "minus", "times",
              "divided", "square", "cube", "cubed", "squared", "power")

_URL_RE = re.compile(r"https?://\S+")
_DIGIT_OP_RE = re.compile(r"\d.*[+\-*/^].*\d|\d.*[+\-*/^]|\d\s*\^\s*\d")
_CODE_PREFIX_RE = re.compile(
    r"^\s*(?:execute|run)\s+(?:code|this|the\s+following|python)?\s*[:\-]?\s*",
    re.IGNORECASE,
)


def is_url(text: str) -> bool:
    return _URL_RE.search(text) is not None


def extract_url(text: str) -> str | None:
    m = _URL_RE.search(text)
    return m.group(0) if m else None


def _looks_like_math(s: str) -> bool:
    if _DIGIT_OP_RE.search(s):
        return True
    if "calculate" in s or "compute" in s:
        return True
    has_digits = any(c.isdigit() for c in s)
    math_phrases = (
        "plus", "minus", "times", "multiplied by", "divided by",
        "square of", "cube of", "squared", "cubed",
        "to the power of", "modulo", " mod ",
    )
    if has_digits and any(w in s for w in math_phrases):
        return True
    return False


def _looks_like_stock(s: str) -> bool:
    return any(w in s for w in ("stock price", "share price", "stock of",
                                "price of", "ticker"))


def _looks_like_search(s: str) -> bool:
    if s.startswith("search ") or "search for" in s or "google " in s:
        return True
    if any(kw in s for kw in REALTIME_KEYWORDS):
        return True
    return False


def _is_greeting(s: str) -> bool:
    s = s.strip(".,!?")
    if s in GREETINGS:
        return True
    return any(s.startswith(g + " ") or s == g for g in GREETINGS)


def route_tool(subgoal: str) -> tuple[str, str]:
    s = subgoal.lower().strip()

    # ---- Stage 1: deterministic short-circuits ----
    url = extract_url(subgoal)
    if "summarize" in s and url:
        return "summarizer", url

    code_match = _CODE_PREFIX_RE.match(subgoal)
    if code_match and code_match.end() < len(subgoal):
        code = subgoal[code_match.end():].strip()
        if code:
            return "code_executor", code

    # ---- Stage 2: keyword router for high-confidence patterns ----
    if _is_greeting(s):
        return "llm", subgoal

    if _looks_like_math(s):
        return "calculator", subgoal

    if _looks_like_stock(s):
        return "stock_price", subgoal

    if _looks_like_search(s):
        return "search", subgoal

    # ---- Stage 3: DistilBERT zero-shot for ambiguous cases ----
    intent = classify_intent(subgoal)
    if intent is None:
        return "llm", subgoal

    if intent == "summarizer":
        return ("summarizer", url) if url else ("llm", subgoal)
    if intent == "code_executor":
        return "llm", subgoal  # without an explicit prefix, don't trust this
    return intent, subgoal
