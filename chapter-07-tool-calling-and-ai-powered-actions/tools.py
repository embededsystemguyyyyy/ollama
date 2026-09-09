# tools.py
# Plain Python functions with type hints and docstrings, ready to be
# passed directly to ollama.chat() as tools.

import json
import math
import requests
from chroma_store import DocumentStore

_store = None  # lazily initialized so importing this module doesn't require a live DB


def _get_store() -> DocumentStore:
    global _store
    if _store is None:
        _store = DocumentStore(path="./chroma_db")
    return _store


def calculate(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression, e.g. '12 * (4 + 3)'.
    Only supports numbers and + - * / ( ) ** operators, nothing else.
    """
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression) <= allowed_chars:
        return "Error: expression contains unsupported characters."

    try:
        # eval() here is deliberately restricted to a whitelist of characters
        # above   never eval() untrusted input without a character whitelist.
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


def search_documents(query: str) -> str:
    """
    Search the local knowledge base of indexed documents for information
    relevant to the query. Returns the top matching passages.
    """
    store = _get_store()
    if store.count() == 0:
        return "The knowledge base is empty. No documents have been indexed."

    results = store.search(query, top_k=3)
    formatted = "\n\n".join(
        f"[Source: {r['source']}] {r['text'][:300]}" for r in results
    )
    return formatted or "No relevant documents found."


def get_weather(city: str) -> str:
    """Get the current weather conditions for a given city name."""
    try:
        # Open-Meteo's geocoding + forecast APIs, no API key required.
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        ).json()

        if not geo.get("results"):
            return f"Could not find location data for '{city}'."

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        forecast = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=10,
        ).json()

        current = forecast.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")

        return f"Current weather in {city}: {temp}°C, wind speed {wind} km/h."
    except Exception as exc:
        return f"Error fetching weather: {exc}"


AVAILABLE_TOOLS = {
    "calculate": calculate,
    "search_documents": search_documents,
    "get_weather": get_weather,
}
