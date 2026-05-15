import os
import sys
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from dotenv import load_dotenv
load_dotenv()

from agent.tool_router import route_tool
from agent.interaction import chat_response
from agent.memory import add_to_memory

from tools.calculator import calculate_expression
from tools.search_tool import search
from tools.code_executor import execute_code
from tools.summarizer import summarize_url
from tools.stock_price import get_stock_price


def run_subgoal(subgoal: str) -> tuple[str, str]:
    routed = route_tool(subgoal)
    if isinstance(routed, tuple):
        tool, payload = routed
    else:
        tool, payload = routed, subgoal

    try:
        if tool == "calculator":
            result = calculate_expression(payload)
        elif tool == "search":
            result = search(payload)
        elif tool == "stock_price":
            result = get_stock_price(payload)
        elif tool == "code_executor":
            result = execute_code(payload)
        elif tool == "summarizer":
            result = summarize_url(payload)
        else:
            result = chat_response(payload)
    except Exception as e:
        result = f"Error: {e}"

    return tool, result


def run_query(query: str) -> None:
    tool, result = run_subgoal(query)
    print(f"\n[tool: {tool}]\n{result}")
    add_to_memory({"query": query, "tool": tool, "result": str(result)})


def print_interactive_banner() -> None:
    model = os.getenv("LLM_MODEL", "gemma3:1b")
    print("=" * 64)
    print(f"  LLM Multitool Agent  |  Model: {model}")
    print(f"  Runtime: Ollama @ {os.getenv('OLLAMA_HOST', 'http://localhost:11434')}")
    print("=" * 64)
    print("Interactive mode. Type 'exit' or 'quit' to leave.\n")
    print("Available tools & capabilities:")
    print("  - calculator    : evaluates arithmetic expressions")
    print("                    e.g. '132 + 345', '8 cubed', '25 * 18'")
    print("  - search        : DuckDuckGo web search for general queries")
    print("                    e.g. 'search for async python best practices'")
    print("  - stock_price   : live stock price via yfinance (use ticker or name)")
    print("                    e.g. 'find current stock price of Apple'")
    print("  - code_executor : runs Python code snippets and returns stdout")
    print("                    e.g. 'execute code: print(sum(range(1,11)))'")
    print("  - summarizer    : extracts/summarizes a web article from a URL")
    print("                    e.g. 'summarize https://example.com/article'")
    print("  - llm fallback  : reasons over the goal when no tool fits")
    print()
    print("How it works: your query is routed directly to the best tool,")
    print("and the result is saved to logs/.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="llm-multitool-agent",
        description="Goal-driven multi-tool LLM agent (local Gemma 3n via Ollama).",
    )
    parser.add_argument("query", nargs="*", help="Goal/query to run. If omitted, enters interactive mode.")
    args = parser.parse_args()

    os.makedirs(os.path.join(CURRENT_DIR, "logs"), exist_ok=True)

    if args.query:
        run_query(" ".join(args.query))
        return

    print_interactive_banner()
    while True:
        try:
            query = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break
        run_query(query)


if __name__ == "__main__":
    main()
