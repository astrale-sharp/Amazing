from mazegen.vector2 import Vector2
from random import shuffle, choice


class DisjointSet:
    def __init__(self, pos: Vector2) -> None:
        self.pos: Vector2 = pos
        self.rank: int = 0
        self.parent: "DisjointSet" = self

    @classmethod
    def at(
        cls, sets: list[list["DisjointSet"]], pos: Vector2
    ) -> "DisjointSet":
        return sets[pos.y][pos.x]

    @classmethod
    def find(
        cls, sets: list[list["DisjointSet"]], pos: Vector2
    ) -> "DisjointSet":
        x = sets[pos.y][pos.x]
        while x != x.parent:
            x.parent = x.parent.parent
            x = x.parent
        return x

    @classmethod
    def merge(
        cls, sets: list[list["DisjointSet"]], pos1: Vector2, pos2: Vector2
    ) -> bool:
        x = cls.find(sets, pos1)
        y = cls.find(sets, pos2)
        if x is y:
            return False
        x.parent = y
        return True


class Kruskal:
    from mazegen.maze import Maze

    @staticmethod
    def get_direction(maze: Maze, move: int) -> Vector2:
        if move == maze.north:
            return Vector2(0, -1)
        if move == maze.south:
            return Vector2(0, 1)
        if move == maze.east:
            return Vector2(1, 0)
        if move == maze.west:
            return Vector2(-1, 0)
        raise ValueError("direction")

    @staticmethod
    def decomp_cell(maze: Maze, cell: int) -> list:
        """tells which walls of the current cell is open
        cell: int = an argument of the maze (ex: maze[line][col])
        --> Usefull to know wich way is open and ok to moove"""

        cell_open = []
        if cell & 1 == 0:
            cell_open.append(maze.north)
        if cell >> 1 & 1 == 0:
            cell_open.append(maze.east)
        if cell >> 2 & 1 == 0:
            cell_open.append(maze.south)
        if cell >> 3 & 1 == 0:
            cell_open.append(maze.west)
        return cell_open

    @staticmethod
    def kruskal(maze: Maze) -> None:
        walls = []
        sets: list[list[DisjointSet]] = [
            [DisjointSet(Vector2(x, y)) for x in range(maze.config.width)]
            for y in range(maze.config.height)
        ]
        for y in range(maze.config.height):
            for x in range(maze.config.width):
                cell_walls = [
                    maze.east,
                    maze.north,
                ]
                walls.extend([(Vector2(x, y), w) for w in cell_walls])
        shuffle(walls)
        for i, (pos, wall) in enumerate(walls):
            cells_dividing: list[Vector2] = [
                pos,
                pos + Kruskal.get_direction(maze, wall),
            ]
            if not maze.is_in_bound(cells_dividing[1]):
                continue
            if maze.maze[cells_dividing[1].y][cells_dividing[1].x] > 0b1111:
                continue
            if maze.maze[cells_dividing[0].y][cells_dividing[0].x] > 0b1111:
                continue
            if DisjointSet.merge(sets, cells_dividing[0], cells_dividing[1]):
                maze.put_in_maze(cells_dividing[0], wall)
                rev = {
                    maze.east: maze.west,
                    maze.west: maze.east,
                    maze.south: maze.north,
                    maze.north: maze.south,
                }
                maze.put_in_maze(cells_dividing[1], rev[wall])
                if maze.config.animate_generation:
                    maze.print_maze_on_terminal("Kruskal generation...", False)
        if not maze.config.perfect:
            count = 0
            shuffle(walls)
            for pos, wall in walls:
                if count < max(maze.config.height, maze.config.width):
                    cell_open_to = Kruskal.decomp_cell(maze, wall)
                    if (
                        len(cell_open_to) < 2
                        and maze.maze[pos.y][pos.x] < 0b1111
                    ):
                        open_wall = [
                            x for x in maze.dir if x not in cell_open_to
                        ]
                        shuffle(open_wall)
                        wall = choice(open_wall)
                        next_cell = pos + Kruskal.get_direction(maze, wall)
                        if (
                            maze.is_in_bound(next_cell)
                            and maze.maze[next_cell.y][next_cell.x] < 0b1111
                        ):
                            maze.put_in_maze(pos, wall)
                            rev = {
                                maze.east: maze.west,
                                maze.west: maze.east,
                                maze.south: maze.north,
                                maze.north: maze.south,
                            }
                            maze.put_in_maze(next_cell, rev[wall])
                            count += 1
                        if maze.config.animate_generation:
                            maze.print_maze_on_terminal(
                                "Kruskal generation...", False
                            )
                else:
                    break
