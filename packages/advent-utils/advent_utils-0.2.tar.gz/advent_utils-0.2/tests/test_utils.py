from __future__ import annotations
from advent_utils import map_movements
import pytest
from typing import Callable

# ==================================================
#   map_movements()
# ==================================================

@pytest.mark.parametrize("key,expected", [("^", (0, 1)), ("v", (0, -1)), ("<", (-1, 0)), (">", (1, 0))])
def test_map_movements(key: str, expected: tuple[int, int]) -> None:
    movements: dict[str, Callable] = map_movements("^", "v", "<", ">")

    assert movements[key]((0, 0)) == expected