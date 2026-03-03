from typing import Any
from typing_extensions import Self


class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __add__(self, rhs: Any):
        if not isinstance(rhs, Vector2):
            raise ValueError(
                "+ operator not supported between Vector2 and {}".format(
                    type(rhs)
                )
            )
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs: Any):
        if not isinstance(rhs, Vector2):
            raise ValueError(
                "- operator not supported between Vector2 and {}".format(
                    type(rhs)
                )
            )
        return Vector2(self.x - rhs.x, self.y - rhs.y)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Vector2):
            raise ValueError(
                "== operator not supported between Vector2 and {}".format(
                    type(rhs)
                )
            )
        return rhs.x == self.x and rhs.y == self.y

    def is_in_bounds(self, bounds: Self) -> bool:
        return (
            self.x >= 0
            and self.x < bounds.x
            and self.y >= 0
            and self.y < bounds.y
        )
