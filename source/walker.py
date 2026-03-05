from source.maze import Maze
from source.vector2 import Vector2
from random import random, choice
from typing import Tuple, List, Generator
from math import sqrt


def is_north_set(bit: int) -> bool:
    return bit & 1 != 0


def is_east_set(bit: int) -> bool:
    return bit >> 1 & 1 != 0


def is_south_set(bit: int) -> bool:
    return bit >> 2 & 1 != 0


def is_west_set(bit: int) -> bool:
    return bit >> 3 & 1 != 0


def broken_with_dir(
    self,
    pos: Vector2,
    next_pos: Vector2,
    direction: Vector2,
) -> Tuple[int, int]:
    """Returns new value for pos and next pos after breaking the wall"""
    if direction == Vector2(-1, 0):
        return (
            self.maze.at(pos) & 0b1110,
            self.maze.at(next_pos) & 0b1011,
        )
    elif direction == Vector2(1, 0):
        return (
            self.maze.at(pos) & 0b1011,
            self.maze.at(next_pos) & 0b1110,
        )
    elif direction == Vector2(0, -1):
        return (
            self.maze.at(pos) & 0b1101,
            self.maze.at(next_pos) & 0b0111,
        )
    elif direction == Vector2(0, 1):
        return (
            self.maze.at(pos) & 0b0111,
            self.maze.at(next_pos) & 0b1101,
        )
    else:
        raise ValueError()

def apply_move(
    self,
    pos: Vector2,
    next_pos: Vector2,
    direction: Vector2,
):
    (
        self.maze.maze[pos.y][pos.x],
        self.maze.maze[next_pos.y][next_pos.x],
    ) = self.broken_with_dir(pos, next_pos, direction)


def get_direction(self, move: int) -> Vector2:
    direction = 0, 0
    if move == 0b0001:
        direction = -1, 0
    if move == 0b0010:
        direction = 0, 1
    if move == 0b0100:
        direction = 1, 0
    if move == 0b1000:
        direction = 0, -1
    return Vector2(*direction)

def is_wall_broken_in_dir(
    self,
    pos: Vector2,
    next_pos: Vector2,
    direction: Vector2,
):
    return (
        (
            direction == Vector2(-1, 0)
            and not is_north_set(self.maze.at(pos))
            and not is_south_set(self.maze.at(next_pos))
        )
        or (
            direction == Vector2(1, 0)
            and not is_south_set(self.maze.at(pos))
            and not is_north_set(self.maze.at(next_pos))
        )
        or (
            direction == Vector2(0, -1)
            and not is_east_set(self.maze.at(pos))
            and not is_west_set(self.maze.at(next_pos))
        )
        or (
            direction == Vector2(0, 1)
            and not is_west_set(self.maze.at(pos))
            and not is_east_set(self.maze.at(next_pos))
        )
    )
