from agents import function_tool
from datetime import datetime, timezone, timedelta

@function_tool
def current_time() -> str:
    """Get current UTC time as ISO format string."""
    # Returns a timezone-aware ISO 8601 string (e.g., "2023-04-11T12:34:56.789012+00:00")
    return datetime.now(timezone.utc).isoformat()

@function_tool
def add_days(base_date: str, days: int) -> str:
    """Add a number of days to the provided date."""
    dt = datetime.fromisoformat(base_date)
    # Returns the new date as an ISO 8601 string; note that if the input date is timezone-naive,
    # you may want to enforce a timezone if needed.
    return (dt + timedelta(days=days)).isoformat()
