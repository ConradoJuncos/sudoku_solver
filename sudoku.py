import random
import time
# import numpy as np
# from numba import njit

def print_sudoku(sudoku):
    for i in range(9):
        print()
        for j in range(9):
            print(sudoku[i][j], end=' ')
    print()
    print()

def check_row(sudoku):
    for row in sudoku:
        seen = set()
        for num in row:
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
    return True

def check_column(sudoku):
    for col in range(9):
        seen = set()
        for row in range(9):
            num = sudoku[row][col]
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
    return True

def check_square(sudoku):
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            seen = set()
            for row in range(3):
                for col in range(3):
                    num = sudoku[box_row + row][box_col + col]
                    if num in seen:
                        return False
                    if num != 0:
                        seen.add(num)
    return True

def check_board(sudoku):
    if check_row(sudoku) and check_column(sudoku) and check_square(sudoku):
        return True
    return False

def create_sudoku_with_n_numbers(n):
    # For creating sudoku with numpy to use numba for optimization
    # sudoku = np.zeros((9, 9), dtype=np.int32)
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    count = 0

    while count < n:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)

        if sudoku[row][col] == 0:
            sudoku[row][col] = num
            if check_board(sudoku):
                count += 1
            else:
                sudoku[row][col] = 0

    return sudoku

def search_closest_zero(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j
    return -1, -1

def insert_number(sudoku):
    coord_row, coord_col = search_closest_zero(sudoku)
    if coord_row == -1 and coord_col == -1:
        return True

    for i in range(9):
        sudoku[coord_row][coord_col] = i + 1
        if check_board(sudoku):
            if insert_number(sudoku):
                return True
        sudoku[coord_row][coord_col] = 0
    return False

def solve_sudoku(sudoku):
    print("Solving sudoku...")
    if insert_number(sudoku):
        print("Sudoku solved!")
    else:
        print("No solution found")
    print_sudoku(sudoku)

if __name__ == "__main__":
    numbers_in_sudoku = int(input("Insert the number of numbers in the sudoku (between 0 and 55): "))
    # numbers_in_sudoku = 25
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
    print("Solving time: {:.3f} seconds".format(solve_time))