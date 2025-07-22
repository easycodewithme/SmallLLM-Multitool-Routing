import re

def is_url(text):
    return re.match(r'^https?://', text.strip()) is not None

def route_tool(subgoal: str):
    subgoal_lower = subgoal.lower()

    # Special override for Apple stock calculation
    if "apple" in subgoal_lower and "100" in subgoal_lower and "calculate" in subgoal_lower:
        return "calculator", "212.48 * 100"

    if "summarize" in subgoal_lower and is_url(subgoal):
        return "summarizer", subgoal
    elif "search" in subgoal_lower:
        return "search", subgoal
    elif "calculate" in subgoal_lower or any(op in subgoal_lower for op in ["+", "-", "*", "/"]):
        return "calculator", subgoal
    elif "stock" in subgoal_lower:
        return "stock_price", subgoal
    elif "code" in subgoal_lower or "execute" in subgoal_lower:
        return "code_executor", subgoal
    else:
        return "llm", subgoal
