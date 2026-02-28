
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
        self.north = 0b0111
        self.east = 0b1011
        self.south = 0b1101
        self.west = 0b1110
        self.nb_cell_to_fill = width * height
        self.dir: list = [self.north,
                          self.west,
                          self.south,
                          self.east]
        self.maze: list = []
        self.drawing: list = [[1, 0, 0, 0, 1, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 0, 1, 1, 1],
                              [0, 0, 1, 0, 1, 0, 0],
                              [0, 0, 1, 0, 1, 1, 1]]

        def check_open_area(self, pos: list):
            i = pos[0]
            j = pos[0]
            if (
                i > 0 and j > 0
                and i < self.height - 1 and j < self.width - 1
            ):
                weigth_square = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        weigth_square += self.maze[i+x][j+y]

    def print_maze(self, convert: str | None = None) -> None:
        '''print the maze
            convert: bin to print the maze in binary
                    int to print the maze in ints
                    hex to print the maze in hexa (Mandatory)
                    Nothing to print the maze in ascii'''
        with open(self.output_file, 'a') as f:
            f.write("ICIIIIIICIICIICI")
            if convert and convert != "yes" and convert != "hex":
                if convert == "bin":
                    func = bin
                elif convert == "int":
                    func = int
                for col in self.maze:
                    for cell in col:
                        f.write(func(cell))
                    f.write("\n")
            elif convert == "hex":
                hexa = ['0', '1', '2', '3', '4',
                        '5', '6', '7', '8', '9',
                        'A', 'B', 'C', 'D', 'E', 'F']
                maze = [[] for _ in range(self.height + 1)]
                for line in range(self.height):
                    for col in range(self.width):
                        maze[line].append(hexa[self.maze[line][col] % 16])
                for line in maze:
                    for cell in line:
                        f.write(cell)
                    f.write("\n")
            else:
                f.write(" ")
                for _ in range(self.width):
                    f.write("__")
                f.write("\n")
                for line in range(self.height):
                    f.write("|")
                    for col in range(self.width):
                        cell = self.maze[line][col]
                        if cell == 0b11111:
                            f.write("##")
                        elif cell == 98:
                            f.write("++")
                        else:
                            if (cell >> 1) & 1 == 1:
                                f.write("_")
                            else:
                                f.write(" ")
                            if cell >> 2 & 1 == 1:
                                f.write("|")
                            else:
                                if (cell >> 1) & 1 == 1:
                                    f.write("_")
                                else:
                                    f.write(" ")
                    f.write("\n")
                f.write(" ")
                f.write("\n")

    def is_in_bound(self, pos: list) -> bool:
        '''checks if the current position pos is not outside the maze
            pos: list of coords we want to check'''

        return (pos[0] < self.height and pos[0] >= 0
                and pos[1] < self.width and pos[1] >= 0)

    def put_in_maze(self, pos: list, value: int) -> None:
        '''put the wanted wall (value) at the position pos in maze'''

        line = pos[0]
        col = pos[1]
        if (
            self.is_in_bound(pos)
            and self.maze[line][col] < 0b11111
        ):
            self.maze[line][col] = self.maze[line][col] & value

    def init_maze(self) -> None:
        '''Init the maze, full of unexplored cells (only walls), and if
        possible draw the given drawing in the middle of the maze'''

        if self.width > 0 and self.height > 0:
            self.maze = [[0b1111 for _ in range(self.width)]
                         for _ in range(self.height)]
            can_draw = self.can_draw_42()
            for line in range(self.height):
                for col in range(self.width):
                    if (
                        can_draw
                        and line >= int(self.height/2) - 3
                        and line < len(self.drawing) + int(self.height/2) - 3
                        and col >= int(self.width/2) - 3
                        and col < len(self.drawing[0]) + int(self.width/2) - 3
                        and self.drawing[line - int(self.height/2) + 3]
                        [col - int(self.width/2) + 3] == 1
                    ):
                        self.maze[line][col] = 0b11111
                        self.nb_cell_to_fill -= 1
        else:
            raise MazeError("Invalid information:\
 width and height must be > 0")

    def can_draw_42(self) -> bool:
        '''checks if the maze is tall enough to draw the drawing'''

        return (
            len(self.drawing) <= self.height
            and len(self.drawing[0]) <= self.width
        )
