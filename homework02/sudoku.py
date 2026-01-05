import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if col in (2, 5) else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Создать матрицу из списка значений
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix = []
    index = 0
    while index < len(values):
        matrix.append(values[index : index + n])
        index += n
    return matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Получить строку по координатам ячейки
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    line, _ = pos
    return list(grid[line])


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Получить столбец по координатам ячейки
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, column = pos
    vertical = []
    for line in grid:
        vertical.append(line[column])
    return vertical


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Получить значения из квадрата 3x3
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    y, x = pos
    start_y = (y // 3) * 3
    start_x = (x // 3) * 3
    square = []
    for i in range(start_y, start_y + 3):
        for j in range(start_x, start_x + 3):
            square.append(grid[i][j])
    return square


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти незаполненную ячейку
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if row[j] == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Определить доступные числа для ячейки
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    available = set("123456789")

    row_nums = set(get_row(grid, pos))
    col_nums = set(get_col(grid, pos))
    block_nums = set(get_block(grid, pos))

    used = row_nums.union(col_nums).union(block_nums)
    return available.difference(used)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решить головоломку судоку"""
    empty_cell = find_empty_positions(grid)

    if empty_cell is None:
        return grid

    y, x = empty_cell
    candidates = find_possible_values(grid, empty_cell)

    for num in candidates:
        grid[y][x] = num
        result = solve(grid)
        if result:
            return result
        grid[y][x] = "."

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """
    Проверить правильность решения
    """
    required = set("123456789")

    for i in range(9):
        if set(get_row(solution, (i, 0))) != required:
            return False

    for j in range(9):
        if set(get_col(solution, (0, j))) != required:
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if set(get_block(solution, (i, j))) != required:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Создать судоку с N заполненными ячейками"""
    empty_grid = [["." for _ in range(9)] for _ in range(9)]

    complete = solve(empty_grid)
    if complete is None:
        complete = [["1" for _ in range(9)] for _ in range(9)]

    puzzle = [row.copy() for row in complete]

    all_cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(all_cells)

    filled_count = min(N, 81)
    cells_to_clear = 81 - filled_count

    for i in range(cells_to_clear):
        if i < len(all_cells):
            r, c = all_cells[i]
            puzzle[r][c] = "."

    return puzzle


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
