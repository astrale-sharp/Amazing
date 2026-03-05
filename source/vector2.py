from typing import Any
from typing_extensions import Self


class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

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

    def __mul__(self, rhs: Any):
        if isinstance(rhs, int):
            return Vector2(int(self.x * rhs), int(self.y * rhs))

        raise ValueError(
            "* operator not supported between Vector2 and {}".format(type(rhs))
        )

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

    def __repr__(self) -> str:
        return str(self)

    def as_tuple(self):
        return (self.x, self.y)

    def is_in_bounds(self, min_pos: Self, max_pos: Self) -> bool:
        return (
            self.x >= min_pos.x
            and self.x < max_pos.x
            and self.y >= min_pos.y
            and self.y < max_pos.y
        )
