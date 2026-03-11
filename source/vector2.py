from typing import Any, Tuple, List


class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, rhs: Any) -> "Vector2":
        if not isinstance(rhs, Vector2):
            raise ValueError(
                "+ operator not supported between Vector2 and {}".format(
                    type(rhs)
                )
            )
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs: Any) -> "Vector2":
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

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def as_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    @classmethod
    def from_iter(cls, tup: Tuple[int, int] | List[int]) -> "Vector2":
        return cls(tup[0], tup[1])

    def inverted(self) -> Any:
        return Vector2(self.y, self.x)
