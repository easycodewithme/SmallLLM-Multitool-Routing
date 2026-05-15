import re

def extract_math_expression(text, memory=None):
    # If numbers exist in the text, extract them and multiply
    numbers = re.findall(r'\d+\.?\d*', text)
    if len(numbers) == 2:
        return f"{numbers[0]} * {numbers[1]}"
    
    # If memory exists, try pulling the last stock price
    if memory:
        for entry in reversed(memory):
            if entry["tool"] == "stock_price":
                match = re.search(r"\$?(\d+\.\d+)", entry["result"])
                if match:
                    price = match.group(1)
                    shares = re.search(r"(\d+)\s+shares", text)
                    if shares:
                        return f"{price} * {shares.group(1)}"
    return None

def calculate(text, memory=None):
    try:
        expression = extract_math_expression(text, memory)
        if not expression:
            return "Could not parse a valid math expression."
        result = eval(expression, {"__builtins__": {}})
        return f"{expression} = {result:.2f}"
    except Exception as e:
        return f"Calculator Error: {str(e)}"

_POWER_PATTERNS = [
    (r"square(?:d)?\s+of\s+(\d+\.?\d*)", r"(\1**2)"),
    (r"(\d+\.?\d*)\s+squared", r"(\1**2)"),
    (r"cube(?:d)?\s+of\s+(\d+\.?\d*)", r"(\1**3)"),
    (r"(\d+\.?\d*)\s+cubed", r"(\1**3)"),
    (r"(\d+\.?\d*)\s+to\s+the\s+power\s+of\s+(\d+\.?\d*)", r"(\1**\2)"),
    (r"(\d+\.?\d*)\s*\^\s*(\d+\.?\d*)", r"(\1**\2)"),
]

_WORD_TO_OP = [
    (r"\bplus\b", "+"),
    (r"\bminus\b", "-"),
    (r"\btimes\b", "*"),
    (r"\bmultiplied\s+by\b", "*"),
    (r"\bdivided\s+by\b", "/"),
    (r"\bmod(?:ulo)?\b", "%"),
]

_EXPR_RE = re.compile(r"[0-9\.\+\-\*/%\(\)\s]+")


def calculate_expression(text: str) -> str:
    try:
        s = text.lower()
        for pat, repl in _POWER_PATTERNS:
            s = re.sub(pat, repl, s)
        for pat, repl in _WORD_TO_OP:
            s = re.sub(pat, repl, s)

        expr = None
        for candidate in _EXPR_RE.findall(s):
            cleaned = candidate.strip()
            if cleaned and any(ch.isdigit() for ch in cleaned):
                expr = cleaned
                break

        if not expr:
            return "❌ Could not parse a valid math expression."

        result = eval(expr, {"__builtins__": None}, {})
        if isinstance(result, float) and not result.is_integer():
            return f"{expr} = {round(result, 4)}"
        return f"{expr} = {int(result) if isinstance(result, float) else result}"
    except Exception as e:
        return f"❌ Calculator Error: {e}"

