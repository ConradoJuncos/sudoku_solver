import random
import time

def print_sudoku(sudoku):
    for i in range(9):
        print()
        for j in range(9):
            print(sudoku[i][j], end=' ')
    print()
    print()

def check_row(sudoku, row):
    seen = set()
    for i in range(9):
        num = sudoku[row][i]
        if num in seen:
            return False
        if num != 0:
            seen.add(num)
    return True
    
def check_column(sudoku, col):
    seen = set()
    for i in range(9):
        num = sudoku[i][col]
        if num in seen:
            return False
        if num != 0:
            seen.add(num)
    return True

def get_square_row_and_col(row, col):
    return (row // 3) * 3, (col // 3) * 3

def check_square(sudoku, row, col):
    square_row, square_col = get_square_row_and_col(row, col)
    seen = set()
    for i in range(3):
        for j in range(3):
            num = sudoku[square_row + i][square_col + j]
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
    return True

def check_board(sudoku, row, col):
    if check_row(sudoku, row) and check_column(sudoku, col) and check_square(sudoku, row, col):
        return True
    return False

def global_check_board(sudoku):
    for i in range(9):
        if not check_row(sudoku, i):
            return False
        if not check_column(sudoku, i):
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not check_square(sudoku, i, j):
                return False
    return True

def create_sudoku_with_n_numbers(n):
    sudoku = [
    [0, 0, 0, 7, 0, 0, 0, 0, 1],
    [0, 8, 0, 0, 0, 0, 0, 0, 4],
    [0, 6, 0, 0, 0, 9, 0, 0, 7],
    [6, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 3, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 4, 8, 0, 0, 0, 2, 0],
    [0, 0, 7, 0, 0, 0, 8, 0, 9],
    [0, 0, 0, 6, 9, 4, 1, 0, 0],
    [4, 0, 0, 2, 0, 0, 0, 0, 0]
]

    return sudoku

def search_closest_zero(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j
    return -1, -1

def insert_number(sudoku):
    row, col = search_closest_zero(sudoku)
    if row == -1 and col == -1:
        return True

    for i in range(9):
        sudoku[row][col] = i + 1
        if check_board(sudoku, row, col):
            if insert_number(sudoku):
                return True
        sudoku[row][col] = 0
    return False

def solve_sudoku(sudoku):
    print("Solving sudoku...")
    if insert_number(sudoku):
        if not global_check_board(sudoku):
            print("Invalid solution")
            return False
        print("Sudoku solved!")
    else:
        print("No solution found")
    print_sudoku(sudoku)

if __name__ == "__main__":
    numbers_in_sudoku = 25
    if numbers_in_sudoku < 0 or numbers_in_sudoku > 55:
        print("Invalid number of numbers, setting to 17")
        numbers_in_sudoku = 17
    sudoku = create_sudoku_with_n_numbers(numbers_in_sudoku)
    print("Sudoku created:")
    print_sudoku(sudoku)
    start_time = time.time()
    solve_sudoku(sudoku)
    end_time = time.time()
    solve_time = end_time - start_time
    print("Solving time: {:.4f} seconds".format(solve_time))