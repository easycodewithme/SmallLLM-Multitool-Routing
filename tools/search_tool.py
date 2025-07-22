from duckduckgo_search import DDGS

def search(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=1)
            for r in results:
                return r.get("body", "No summary available.")
        return "No results found."
    except Exception as e:
        return f"Search Error: {str(e)}"
