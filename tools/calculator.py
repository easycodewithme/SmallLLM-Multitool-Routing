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

def calculate_expression(expression: str) -> str:
    try:
        # Look for the first valid math expression with numbers and operators
        # This ignores irrelevant text and safely extracts just the expression
        match = re.search(r'([0-9\.\+\-\*/\s\(\)]+)', expression)
        if not match:
            return "❌ Could not parse a valid math expression."

        expr = match.group(1).strip()

        # Evaluate the expression securely
        result = eval(expr, {"__builtins__": None}, {})
        return f"{expr} = {round(result, 2)}"
    except Exception as e:
        return f"❌ Calculator Error: {str(e)}"

