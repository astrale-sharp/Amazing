from source.maze import Maze
from source.walker_pa import Walker
from source.find_way import SolveMaze
import time


# init values
args = {
        "height": 10,
        "width": 10,
        "entry": [0, 0],
        "exit": [9, 0],
        "output_file": "test",
        "perfect": True
        }

# create a maze object
test = Maze(**args)

# create an empty maze
test.init_maze()

# print it
test.print_maze()

# init a walker (a valid and initiated maze as argument)
walk = Walker(test)

# walk through the empty maze and generate it
walk.walk_and_fill()

# print the new maze
test.print_maze()

# init the solver
solvmaze = SolveMaze(test)

# outpouts the shortest way, and the time it took
x = time.time()
print(solvmaze.output_shortest_way())
print(time.time() - x)
