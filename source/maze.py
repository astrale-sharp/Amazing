import random
from mlx import Mlx
from typing import Any


class MazeError(Exception):
    pass


class Maze:
    def __init__(self, height: int, width: int,
                 entry: list, exit: list,
                 output_file: str, perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.maze: list = []
        self.north = 0b0111
        self.west = 0b1011
        self.south = 0b1101
        self.east = 0b1110
        self.dir: list = [self.north,
                          self.west,
                          self.south,
                          self.east]
        self.drawing: list = [[1, 0, 0, 0, 1, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 0, 1, 1, 1],
                              [0, 0, 1, 0, 1, 0, 0],
                              [0, 0, 1, 0, 1, 1, 1]]

    def print_maze(self, convert: str | None = None) -> None:
        if convert:
            # affiche les valeurs du tableau
            if convert == "hex":
                func = hex
            elif convert == "bin":
                func = bin
            elif convert == "int":
                func = int
            for col in self.maze:
                for cell in col:
                    print(func(cell), end="\t")
                    if (cell) <= 15:
                        print("\t", end="")
                print()
        else:
            # affiche le tableau version joli
            print(" ")
            for _ in range(self.width):
                print("__", end="")
            print()
            for line in range(self.height):
                print("|", end="")
                for col in range(self.width):
                    cell = self.maze[line][col]
                    if line == self.entry[0] and col == self.entry[1]:
                        print("S ", end="")
                    elif cell == 0b11111:
                        print("##", end="")
                    elif line == self.exit[0] and col == self.exit[1]:
                        print(" E", end="")
                    else:
                        if (cell >> 1) & 1 == 1:
                            print("_", end="")
                        else:
                            print(" ", end="")
                        if cell & 1 == 1:
                            print("|", end="")
                        else:
                            if (cell >> 1) & 1 == 1:
                                print("_", end="")
                            else:
                                print(" ", end="")
                print()
            print(" ", end="")
            print()

    def is_in_bound(self, pos) -> bool:
        return (pos[0] < self.height and pos[0] >= 0
                and pos[1] < self.width and pos[1] >= 0)

    def put_in_maze(self, pos: list, value: int) -> None:
        # casse le mur value a la position pos
        line = pos[0]
        col = pos[1]
        if (
            self.is_in_bound(pos)
            and self.maze[line][col] < 0b11111
        ):
            self.maze[line][col] = self.maze[line][col] & value

    def init_maze(self) -> None:
        # init un maze que avec murs
        if self.width > 0 and self.height > 0:
            self.maze = [[0b1111 for _ in range(self.width)]
                         for _ in range(self.height)]
            self.put_in_maze(self.entry, 0b0000)
            self.put_in_maze(self.exit, 0b0000)
        else:
            raise MazeError("Invalid information:\
 width and height must be > 0")

    def can_draw_42(self) -> bool:
        return (
            len(self.drawing) <= self.height
            and len(self.drawing[0]) <= self.width
        )

    def cross_border(self, value: int, line: int, col: int):
        # retourne true si on risque de traverser la limite
        if (value == self.north and line == 0):
            return (True)
        elif (value == self.south and line == self.height - 1):
            return (True)
        elif (value == self.east and col == self.width - 1):
            return (True)
        elif (value == self.west and col == 0):
            return (True)
        else:
            return (False)

    def draw_maze(self) -> None:
        can_draw = self.can_draw_42()
        for line in range(self.height):
            for col in range(self.width):
                # dessine le 42 pendant le parcours du tableau
                if (
                    can_draw
                    and line >= int(self.height / 2) - 3
                    and line < len(self.drawing) + int(self.height / 2) - 3
                    and col >= int(self.width / 2) - 3
                    and col < len(self.drawing[0]) + int(self.width / 2) - 3
                    and self.drawing[line - int(self.height / 2) + 3][
                        col - int(self.width / 2) + 3
                    ]
                    == 1
                ):
                    self.maze[line][col] = 0b11111
                # choisist un nombre dedirection au hasard, casse les murs
        # walker = Walker()
        # walker.walk()

    def to_background_image(self, m: Mlx, img_ptr: Any):
        data, _, line_size, format = m.mlx_get_data_addr(img_ptr)
        for line in range(self.height * self.cell_size):
            for col in range(self.width * self.cell_size):
                r, g, b, a = 100, 100, 200, 254
                if 2 * 100 <= col <= 4 * 100 and 2 * 100 <= line <= 4 * 100:
                    r, g, b, a = 255, 0, 0, 254
                if format == 0:
                    data[4 * col + line * line_size] = b
                    data[4 * col + line * line_size + 1] = g
                    data[4 * col + line * line_size + 2] = r
                    data[4 * col + line * line_size + 3] = a
                else:
                    data[4 * col + line * line_size] = a
                    data[4 * col + line * line_size + 1] = r
                    data[4 * col + line * line_size + 2] = g
                    data[4 * col + line * line_size + 3] = b

    def to_image(self, m: Mlx, img_ptr: Any):
        data, _, line_size, format = m.mlx_get_data_addr(img_ptr)
        self.to_background_image(m, img_ptr)

        def write_line(start, incr, color=(0, 0, 0, 255)):
            for _ in range(self.cell_size):
                r, g, b, a = color
                print(start)
                if format == 0:
                    data[start] = b
                    data[start + 1] = g
                    data[start + 2] = r
                    data[start + 3] = a
                else:
                    data[start] = a
                    data[start + 1] = r
                    data[start + 2] = g
                    data[start + 3] = b
                start += incr

        for line in range(self.height):
            for col in range(self.width):
                if self.maze[line][col] & 0b1000:
                    write_line(
                        self.cell_size * 4 * col
                        + self.cell_size * line_size * line,
                        4,
                    )
                if self.maze[line][col] & 0b0100:
                    write_line(
                        self.cell_size * 4 * (col + 1)
                        + self.cell_size * line_size * line,
                        line_size,
                    )
                if self.maze[line][col] & 0b0010:
                    write_line(
                        self.cell_size * 4 * col
                        + self.cell_size * line_size * (line + 1)
                        - line_size,
                        4,
                    )
                if self.maze[line][col] & 0b0001:
                    write_line(
                        self.cell_size * 4 * (col)
                        + self.cell_size * line_size * line,
                        line_size,
                    )
