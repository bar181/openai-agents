from agents import function_tool
from datetime import datetime, timezone, timedelta

@function_tool
def current_time() -> str:
    """Get current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat()

@function_tool
def add_days(base_date: str, days: int) -> str:
    """Add a number of days to the provided date."""
    dt = datetime.fromisoformat(base_date)
    return (dt + timedelta(days=days)).isoformat()
