from source.maze import Maze
from source.walker_pa import Walker
from source.walker import backtrack, Vector2, chunk_planner
from source.find_way import SolveMaze
import time

arr = [[0 for k in range(500)] for y in range(499)]
for k in chunk_planner(arr):
    for y in k:
        for x in y:
            print(x, end=" ")
        print()
    print("===")
# entry = Vector2(4, 4)

# res: list[Vector2] | None = []
# while True:
#     x = time.time()
#     res: list[Vector2] | None = backtrack(Vector2(5 , 5), entry, [Vector2(0, 0),Vector2(0, 2), Vector2(0, 1)])
#     print("Solve time {:.4}s".format(time.time() - x))
#     if res is None:
#         break
#     from turtle import Turtle

#     t = Turtle()
#     t.teleport(*(entry * 40).as_tuple())
#     for k in res:
#         t.goto((k * 40).as_tuple())
#     time.sleep(0.2)
#     t.clear()
# print("NONE")
# exit()


def main(args):

    return
    # create a maze object
    maze = Maze(**args)
    maze.draw_maze()
    # init a walker (a valid and initiated maze as argument)
    # walk = Walker(maze)
    walker = WalkerAc(maze)
    # walk through the empty maze and generate it
    x = time.time()

    for k in walker.walk():
        print("yielded ", k)
        print(maze.print_maze())
        # input()
        # print("\033c")
        # pass
    # walk.walk_and_fill()
    # print(maze.print_maze())
    return
    print("Creation time", time.time() - x)

    # store the hexa maze(MANDATORY)
    content = maze.print_maze("hex")

    # init the solver
    x = time.time()
    solvmaze = SolveMaze(maze)
    print("Resolution time", time.time() - x)

    # store the shortest way(MANDATORY)
    # content += solvmaze.output_shortest_way()

    with open(maze.output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    maze1 = {
        "height": 6,
        "width": 6,
        "entry": [0, 0],
        "exit": [5, 5],
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
    mazes = [maze1, maze2, maze3]
    for maze in mazes:
        main(maze)
