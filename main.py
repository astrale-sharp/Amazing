from source.maze import Maze
from source.walker_pa import Walker
from source.find_way import SolveMaze
from source.parse import Parser
from pydantic import ValidationError
# from mlx import Mlx


def main(args):

    try:
        with open("config.txt", 'r') as f:
            args = f.read()

        args = Parser.parse(args)
        print(args)
        maze = Maze(**args)
        walk = Walker(maze)
        walk.walk_and_fill()
        content = maze.print_maze("hex")
        solvmaze = SolveMaze(maze)
        content += f"Entry: {args['entry']}\nExit: {args['exit']}\n"
        content += solvmaze.output_shortest_way()

        with open(maze.output_file, "w") as f:
            f.write(content)
    except (ValueError, ValidationError) as e:
        print("ERROR:", e)
    except FileNotFoundError:
        print("Please create a config.txt with the arguments:")
        print("""    WIDTH=<int>
    HEIGHT=<int>
    ENTRY=<int>,<int>
    EXIT=<int>,<int>
    OUTPUT_FILE=<filename>
    PERFECT=True|False
    [SEED=<str>]""")


if __name__ == "__main__":
    maze1 = {
        "height": 100,
        "width": 100,
        "entry": [49, 99],
        "exit": [99, 99],
        "output_file": "test.txt",
        "perfect": True,
    }

    maze2 = {
        "height": 6,
        "width": 6,
        "entry": [0, 0],
        "exit": [5, 5],
        "output_file": "test.txt",
        "perfect": False,
    }

    maze3 = {
        "height": 9,
        "width": 9,
        "entry": [0, 0],
        "exit": [8, 8],
        "output_file": "test.txt",
        "perfect": True,
    }

    # maze4 = {
    #         "height": 50,
    #         "width": 50,
    #         "entry": [0, 0],
    #         "exit": [49, 49],
    #         "output_file": "test.txt",
    #         "perfect": True
    #         }
    # maze5 = {
    #         "height": 50,
    #         "width": 50,
    #         "entry": [0, 0],
    #         "exit": [49, 49],
    #         "output_file": "test.txt",
    #         "perfect": False
    #         }
    mazes = [maze1]
    for maze in mazes:
        main(maze)
