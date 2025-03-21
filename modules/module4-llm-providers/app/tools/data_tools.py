from agents import function_tool
from typing import Any, List

@function_tool
def get_item(items: List[Any], index: int) -> Any:
    """Get an item from a list by index."""
    try:
        return items[index]
    except IndexError:
        return None


@function_tool
def summarize_list(items: List[Any]) -> dict:
    """Return a summary of a list including length and first item."""
    return {
        "length": len(items),
        "first_item": items[0] if items else None
    }


@function_tool
def fetch_mock_data(source: str) -> dict:
    """Retrieve MOCK data from an INTERNAL simulated database."""
    return {"source": source, "data": "sample data"}
