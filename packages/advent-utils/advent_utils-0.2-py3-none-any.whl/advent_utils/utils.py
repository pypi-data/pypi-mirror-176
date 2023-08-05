from __future__ import annotations
from typing import Callable

def map_movements(up: str, down: str, left: str, right: str) -> dict[str, Callable]:
    """
    Map keys to the directions up, down, left, right.

    Args:
        up (str): The key for moving up
        down (str):  The key for moving down
        left (str): The key for moving left
        right (str): The key for moving right
    
    Returns:
        dict[str, Callable]: A dictionary of movements
    """
    return {
        up: lambda c: (c[0], c[1] + 1),
        down: lambda c: (c[0], c[1] - 1),
        left: lambda c: (c[0] - 1, c[1]),
        right: lambda c: (c[0] + 1, c[1])
    }