from typing import Any, Optional


def format_none_value(value: Optional[Any], none_str="N/A"):
    if value:
        return str(value)
    return none_str
