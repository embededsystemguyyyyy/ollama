# search_tool.py
# A simple web search tool using the free DuckDuckGo HTML endpoint,
# no API key required. Good enough for a research agent build-along;
# swap in a proper search API for production use.

import requests
from bs4 import BeautifulSoup


def web_search(query: str) -> str:
    """Search the web and return a short list of result titles and snippets."""
    try:
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".result__body")[:5]

        if not results:
            return "No search results found."

        formatted = []
        for r in results:
            title_el = r.select_one(".result__title")
            snippet_el = r.select_one(".result__snippet")
            title = title_el.get_text(strip=True) if title_el else "Untitled"
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            formatted.append(f"- {title}: {snippet}")

        return "\n".join(formatted)
    except Exception as exc:
        return f"Search failed: {exc}"
pip install beautifulsoup4
