try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


def search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        snippets = []
        for r in results:
            body = r.get("body") or r.get("snippet") or ""
            title = r.get("title", "")
            if body:
                snippets.append(f"- {title}: {body}" if title else f"- {body}")
        return "\n".join(snippets) if snippets else "No results found."
    except Exception as e:
        return f"Search Error: {e}"
