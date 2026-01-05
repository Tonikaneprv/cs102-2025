from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(matrix: List[List[Union[str, int]]], pos: Tuple[int, int]) -> List[List[Union[str, int]]]:
    a, b = pos
    last_idx = len(matrix[0]) - 1
    way = choice(("up", "right"))
    if way == "up":
        if a > 1:
            matrix[a - 1][b] = " "
        elif b < last_idx - 1:
            matrix[a][b + 1] = " "
    else:
        if b < last_idx - 1:
            matrix[a][b + 1] = " "
        elif a > 1:
            matrix[a - 1][b] = " "
    return matrix


def bin_tree_maze(h: int = 15, w: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    field = create_grid(h, w)
    free_positions = []

    for i, line in enumerate(field):
        for j, _ in enumerate(line):
            if i % 2 == 1 and j % 2 == 1:
                field[i][j] = " "
                free_positions.append((i, j))

    for pos_now in free_positions:
        remove_wall(field, pos_now)

    if random_exit:
        in_x, out_x = randint(0, h - 1), randint(0, h - 1)
        in_y = randint(0, w - 1) if in_x in {0, h - 1} else choice((0, w - 1))
        out_y = randint(0, w - 1) if out_x in {0, h - 1} else choice((0, w - 1))
    else:
        in_x, in_y = 0, w - 2
        out_x, out_y = h - 1, 1

    field[in_x][in_y], field[out_x][out_y] = "X", "X"
    return field


def get_exits(labyrinth: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    outputs = []
    for r, line in enumerate(labyrinth):
        for c, elem in enumerate(line):
            if elem == "X":
                outputs.append((r, c))
                if len(outputs) == 2:
                    return outputs
    return outputs


def make_step(labyrinth: List[List[Union[str, int]]], step_num: int) -> List[List[Union[str, int]]]:
    rows_cnt = len(labyrinth)
    cols_cnt = len(labyrinth[0])
    next_step = step_num + 1
    for r_idx in range(rows_cnt):
        for c_idx in range(cols_cnt):
            if labyrinth[r_idx][c_idx] == step_num:
                adj_cells = [
                    (r_idx, c_idx + 1),
                    (r_idx, c_idx - 1),
                    (r_idx + 1, c_idx),
                    (r_idx - 1, c_idx),
                ]
                for nx, ny in adj_cells:
                    if 0 <= nx < rows_cnt and 0 <= ny < cols_cnt and labyrinth[nx][ny] == 0:
                        labyrinth[nx][ny] = next_step
    return labyrinth


def shortest_path(
    labyrinth: List[List[Union[str, int]]], finish: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    rows_cnt = len(labyrinth)
    cols_cnt = len(labyrinth[0])
    fx, fy = finish
    start_val = labyrinth[fx][fy]
    if isinstance(start_val, str):
        return None
    current_val = start_val
    route = [(fx, fy)]
    if start_val == 1:
        return route
    while True:
        current_val -= 1
        if current_val < 1:
            break
        adj_cells = [(fx, fy + 1), (fx, fy - 1), (fx + 1, fy), (fx - 1, fy)]
        for ax, ay in adj_cells:
            if 0 <= ax < rows_cnt and 0 <= ay < cols_cnt and labyrinth[ax][ay] == current_val:
                route.append((ax, ay))
                fx, fy = ax, ay
                break
    return route


def encircled_exit(labyrinth: List[List[Union[str, int]]], point: Tuple[int, int]) -> bool:
    rows_cnt = len(labyrinth)
    cols_cnt = len(labyrinth[0])
    px, py = point
    if (px in {0, rows_cnt - 1}) and (py in {0, cols_cnt - 1}):
        return True
    if px == 0 and labyrinth[px + 1][py] != " ":
        return True
    if px == rows_cnt - 1 and labyrinth[px - 1][py] != " ":
        return True
    if py == 0 and labyrinth[px][py + 1] != " ":
        return True
    if py == cols_cnt - 1 and labyrinth[px][py - 1] != " ":
        return True
    return False


def solve_maze(
    field: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    field = deepcopy(field)
    exit_points = get_exits(field)
    if len(exit_points) == 1:
        return field, exit_points[0]
    for exit_point in exit_points:
        if encircled_exit(field, exit_point):
            return field, None
    for r_idx, line in enumerate(field):
        for c_idx, elem in enumerate(line):
            if elem == " ":
                field[r_idx][c_idx] = 0
    start_x, start_y = exit_points[0]
    field[start_x][start_y] = 1
    end_x, end_y = exit_points[1]
    field[end_x][end_y] = 0
    current_step = 1
    while field[end_x][end_y] == 0:
        make_step(field, current_step)
        current_step += 1
        if current_step > len(field) * len(field[0]):
            return field, None
    route = shortest_path(field, (end_x, end_y))
    return field, route


def add_path_to_grid(
    field: List[List[Union[str, int]]], route: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if route:
        for i, line in enumerate(field):
            for j, _ in enumerate(line):
                if (i, j) in route:
                    field[i][j] = "X"
    return field


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
