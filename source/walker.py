from source.maze import Maze, Vector2  # todo disallowed import
from random import choice, randint, shuffle
from typing import List, Generator, Optional

# def is_north_set(bit: int) -> bool:
#     return bit & 1 != 0


# def is_east_set(bit: int) -> bool:
#     return bit >> 1 & 1 != 0


# def is_south_set(bit: int) -> bool:
#     return bit >> 2 & 1 != 0


# def is_west_set(bit: int) -> bool:
#     return bit >> 3 & 1 != 0


def backtrack(
    bounds: Vector2,
    entry: Vector2,
    exits: Optional[List[Vector2]] = None,
) -> Optional[List[Vector2]]:
    """ """
    # 0bXY
    # Y == 0 means non visited
    # X == 0 means not flooded
    map = [[0 for _ in range(bounds.x)] for _ in range(bounds.y)]
    possibility = [
        Vector2(1, 0),
        Vector2(-1, 0),
        Vector2(0, 1),
        Vector2(0, -1),
    ]

    def reset_dijkstra():
        for y in range(bounds.y):
            for x in range(bounds.x):
                map[y][x] &= 1

    def can_flood(pos: Vector2, path: List[Vector2]):
        reset_dijkstra()
        count = 0
        stack = [pos]
        while not len(stack) == 0:
            candidate = stack.pop()
            if map[candidate.y][candidate.x]:
                continue
            map[candidate.y][candidate.x] |= 0b10

            for new_candidate in [candidate + p for p in possibility[:]]:
                if (
                    is_in_bounds(new_candidate)
                    and not map[new_candidate.y][new_candidate.x] & 0b11
                ):
                    stack.append(new_candidate)

            count += 1
        return bounds.x * bounds.y <= count + len(path)

    def is_in_bounds(pos):
        return (
            pos.x >= 0 and pos.x < bounds.x and pos.y >= 0 and pos.y < bounds.y
        )

    def is_finishing(path):
        return len(path) == bounds.x * bounds.y and (
            not exits or path[-1] in exits
        )

    def remaining_exits(path):
        # return True
        if not exits:
            return True
        remainder = len(exits)
        for e in exits:
            if map[e.y][e.x] & 1:
                remainder -= 1
        return not (remainder == 0 and len(path) + 1 == bounds.x * bounds.y)

    def backtrack_rec(
        bounds: Vector2, path: List[Vector2], i: int
    ) -> Optional[List[Vector2]]:
        if len(path) == 0:
            path = [entry]
            map[entry.y][entry.x] = 1

        shuffle(possibility)
        for p in possibility[:]:
            candidate = path[-1] + p
            if not is_in_bounds(candidate):
                continue
            if map[candidate.y][candidate.x] & 1 != 0:
                continue
            if exits and not remaining_exits(path):
                continue
            if not can_flood(candidate, path):
                continue
            path.append(candidate)
            map[candidate.y][candidate.x] = 1
            if is_finishing(path):
                return path

            next = backtrack_rec(bounds, path, i + 1)
            if next:
                return next
            map[path[-1].y][path[-1].x] = 0
            path.pop()
        return None

    return backtrack_rec(bounds, [], 0)


def create_line(size: int):
    arr = []
    if size <= 5:
        return [size]
    if size % 5 == 0:
        for _ in range(size // 5):
            arr.append(5)
    if size % 5 == 1:
        for i, _ in enumerate(range(size // 5 + 1)):
            if i >= int(size / 5) - 1:
                arr.append(3)
            else:
                arr.append(5)
    if size % 5 == 2:
        for i, _ in enumerate(range(int(size / 5) + 1)):
            if i == int(size / 5) - 1:
                arr.append(4)
            elif i == int(size / 5):
                arr.append(3)
            else:
                arr.append(5)
    if size % 5 == 3:
        for i, _ in enumerate(range(int(size / 5) + 1)):
            if i == int(size / 5) - 1:
                arr.append(4)
            elif i == int(size / 5):
                arr.append(4)
            else:
                arr.append(5)
    if size % 5 == 4:
        for i, _ in enumerate(range(int(size / 5) + 1)):
            if i == int(size / 5):
                arr.append(4)
            else:
                arr.append(5)

    return arr


def chunk_planner(array: List[List[int]]) -> List[List[List[int]]]:
    if len(array) == 0:
        return []
    if len(array) <= 5 and len(array[0]) <= 5:
        return [array]

    size = Vector2(len(array[0]), len(array))
    arr = []
    xline = create_line(size.x)
    for y in create_line(size.y):
        l = []
        for x in xline:
            l.append((x, y))
        arr.append(l)
    if len(arr) <= 5 and len(arr[0]) <= 5:
        return [arr]
    return [arr] + chunk_planner(arr)


class RecChunkWalker:
    """
    Using backtrack to solve each step, divides the maze in 3x3 to 5x5 chunks:

    1. decide and store all sizes
    2. solve first chunk at abstraction level n
    3. At abstraction level n - 1 You are provided with the path,
        solve your chunks one by one while following the abstract path that was given to you

    From the ground up:
    level 0 from entry given by the path using direction decide where on the wall of the chunk
      is the exit.
    level 1: decide which chunk is the exit.
    level 2: decide which chunk of chunk is the exit.
    """

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def chunk(self, chunk_idx: Vector2, chunk_size: Vector2, bounds: Vector2):
        min_pos = Vector2(
            chunk_idx.x * chunk_size.x,
            chunk_idx.y * chunk_size.y,
        )
        max_pos = Vector2(
            (
                (chunk_idx.x + 1) * (chunk_size.x + 1)
                if chunk_idx.x != bounds.x - 1
                else self.maze.width
            ),
            (
                (chunk_idx.y + 1) * (chunk_size.y + 1)
                if chunk_idx.y != bounds.y - 1
                else self.maze.height
            ),
        )
        return (min_pos, max_pos)

    def walk(self) -> Generator[Vector2]:
        """"""

        if self.maze.height == 0 or self.maze.width == 0:
            return
        start_position = self.maze.entry
        pos = Vector2(start_position[0], start_position[1])
        yield pos

        # does precision error kill us here?
        chunk_bounds, chunk_size = (
            (
                Vector2(6, 6),
                Vector2(self.maze.width // 6, self.maze.height // 6),
            )
            if self.maze.width >= 36 and self.maze.height >= 36
            else (Vector2(1, 1), Vector2(self.maze.width, self.maze.height))
        )
        for chunk_line in range(chunk_bounds.y):
            for chunk_col in range(chunk_bounds.x):
                min_pos, max_pos = self.chunk(
                    Vector2(chunk_col, chunk_line), chunk_size, chunk_bounds
                )

        # for chunk in path:
        #     direction = chunk - direction
        #     self.break_wall_between_chunks(
        #         direction, chunk, chunk_size, chunk_bounds
        #     )
        #     if not self.maze.perfect:
        #         self.rand_break_more_walls(chunk, chunk_size, chunk_bounds)
        #     direction = chunk

    # def break_wall_between_chunks(
    #     self, direction: Vector2, chunk: Vector2, chunk_size, bounds: Vector2
    # ):
    #     min_pos, max_pos = self.chunk(chunk, chunk_size, bounds)

    #     while True:
    #         pos = Vector2(
    #             randint(min_pos.x, min_pos.y), randint(max_pos.x, max_pos.y)
    #         )
    #         if self.maze_valid_after_move(
    #             direction,
    #             pos,
    #             Vector2(0, 0),
    #             Vector2(self.maze.width, self.maze.height),
    #         ):
    #             break
    #     self.break_walls_in_direction(pos, pos + direction, direction)

    # def broken_with_dir(
    #     self,
    #     pos: Vector2,
    #     next_pos: Vector2,
    #     direction: Vector2,
    # ) -> Tuple[int, int]:
    #     """Returns new value for pos and next pos after breaking the wall"""
    #     if direction == Vector2(-1, 0):
    #         return (
    #             self.maze.at(pos) & self.maze.west,
    #             self.maze.at(next_pos) & self.maze.east,
    #         )
    #     elif direction == Vector2(1, 0):
    #         return (
    #             self.maze.at(pos) & self.maze.east,
    #             self.maze.at(next_pos) & self.maze.west,
    #         )
    #     elif direction == Vector2(0, -1):
    #         return (
    #             self.maze.at(pos) & self.maze.north,
    #             self.maze.at(next_pos) & self.maze.south,
    #         )
    #     elif direction == Vector2(0, 1):
    #         return (
    #             self.maze.at(pos) & self.maze.south,
    #             self.maze.at(next_pos) & self.maze.north,
    #         )
    #     else:
    #         raise ValueError()

    # def break_walls_in_direction(
    #     self,
    #     pos: Vector2,
    #     next_pos: Vector2,
    #     direction: Vector2,
    # ):
    #     (
    #         self.maze.maze[pos.y][pos.x],
    #         self.maze.maze[next_pos.y][next_pos.x],
    #     ) = self.broken_with_dir(pos, next_pos, direction)

    # def get_valid_moves(
    #     self,
    #     pos: Vector2,
    #     min_pos: Vector2,
    #     max_pos: Vector2,
    # ):
    #     return list(
    #         filter(
    #             lambda direction: self.maze_valid_after_move(
    #                 direction, pos, min_pos, max_pos
    #             ),
    #             [
    #                 Vector2(-1, 0),
    #                 Vector2(1, 0),
    #                 Vector2(0, 1),
    #                 Vector2(0, -1),
    #             ],
    #         )
    #     )

    # def get_direction(self, move: int) -> Vector2:
    #     direction = 0, 0
    #     if move == 0b0001:
    #         direction = -1, 0
    #     if move == 0b0010:
    #         direction = 0, 1
    #     if move == 0b0100:
    #         direction = 1, 0
    #     if move == 0b1000:
    #         direction = 0, -1
    #     return Vector2(*direction)

    # def is_wall_broken_in_dir(
    #     self,
    #     pos: Vector2,
    #     next_pos: Vector2,
    #     direction: Vector2,
    # ):
    #     return (
    #         (
    #             direction == Vector2(-1, 0)
    #             and not is_north_set(self.maze.at(pos))
    #             and not is_south_set(self.maze.at(next_pos))
    #         )
    #         or (
    #             direction == Vector2(1, 0)
    #             and not is_south_set(self.maze.at(pos))
    #             and not is_north_set(self.maze.at(next_pos))
    #         )
    #         or (
    #             direction == Vector2(0, -1)
    #             and not is_east_set(self.maze.at(pos))
    #             and not is_west_set(self.maze.at(next_pos))
    #         )
    #         or (
    #             direction == Vector2(0, 1)
    #             and not is_west_set(self.maze.at(pos))
    #             and not is_east_set(self.maze.at(next_pos))
    #         )
    #     )
