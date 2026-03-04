from source.maze import Maze
from source.walker_pa import Walker
from source.find_way import SolveMaze
from source.parse import Parser
from pydantic import ValidationError
import sys
# from mlx import Mlx


def main():

    try:
        with open(sys.argv[1], 'r') as f:
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
    except ValidationError as e:
        print(e)
    except (ValueError) as e:
        print("ERROR:", e)
    except IndexError:
        print("ERROR: No configuration txt given as argument. \
Please run python3 a_maze_ing <filename>.txt")
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
    main()