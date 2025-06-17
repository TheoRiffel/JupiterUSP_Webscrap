from typing import Any, Optional, TypeVar

T = TypeVar("T")


def format_none_value(value: Optional[Any], none_str="N/A"):
    if value:
        return str(value)
    return none_str


def get_value_or_none(array: list[T], index: int) -> T | None:
    try:
        return array[index]
    except:
        return None
