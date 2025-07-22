import contextlib
import io

def execute_code(code: str) -> str:
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
    except Exception as e:
        return f"Code Execution Error: {str(e)}"
    return output.getvalue()
