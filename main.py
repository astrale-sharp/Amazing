from source.maze import Maze
from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()


def mymouse(button, x, y, extra: Maze):
    pass


def mykey(keynum, extra: Maze):
    if keynum == 65307 or keynum == 113:
        m.mlx_loop_exit(mlx_ptr)
        m.mlx_mouse_hook(win_ptr, None, None)


test = Maze(5, 5, [0, 0], [19, 19], "test", False)
test.init_maze()  # move into __init__?


win_ptr = m.mlx_new_window(
    mlx_ptr,
    test.cell_size * test.width + 1,
    test.cell_size * test.height + 1,
    "a_main_window",
)

img_ptr = m.mlx_new_image(
    mlx_ptr, test.cell_size * test.width + 1, test.cell_size * test.height + 1
)

m.mlx_mouse_hook(win_ptr, mymouse, test)
m.mlx_key_hook(win_ptr, mykey, test)

test.maze[2][3] = 0
test.maze[3][2] = 0
test.maze[2][2] = 0
test.maze[3][3] = 0
# raise Exception(test.maze[2][2])
test.to_image(m, img_ptr)
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

test.draw_maze()
test.print_maze("bin")
test.print_maze()

m.mlx_loop(mlx_ptr)

m.mlx_destroy_window(mlx_ptr, win_ptr)
data, _, _, _ = m.mlx_get_data_addr(img_ptr)
m.mlx_release(mlx_ptr)
