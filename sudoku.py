import random
import time
import numpy as np
from numba import njit

def print_sudoku(sudoku):
    for i in range(9):
        print()
        for j in range(9):
            print(sudoku[i][j], end=' ')
    print()
    print()

@njit
def check_row(sudoku, row):
    seen = set()
    for i in range(9):
        num = sudoku[row][i]
        if num in seen:
            return False
        if num != 0:
            seen.add(num)
    return True

@njit
def check_column(sudoku, col):
    seen = set()
    for i in range(9):
        num = sudoku[i][col]
        if num in seen:
            return False
        if num != 0:
            seen.add(num)
    return True

@njit
def get_square_row_and_col(row, col):
    # Returns the row and column of the top left cell of the square the cell is in
    return (row // 3) * 3, (col // 3) * 3

@njit
def check_square(sudoku, row, col):
    # Gets the row and column of the top left cell of the square the cell is in
    square_row, square_col = get_square_row_and_col(row, col)
    seen = set()
    # Similar algorithm to check_row and check_column, but for the square
    for i in range(3):
        for j in range(3):
            num = sudoku[square_row + i][square_col + j]
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
    return True

@njit
def check_board(sudoku, row, col):
    # Check if the row, column and square affected by the input are valid
    if check_row(sudoku, row) and check_column(sudoku, col) and check_square(sudoku, row, col):
        return True
    return False

@njit
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

@njit
def create_sudoku_with_n_numbers(n, inserts):
    # Creates the sudoku with numpy to use numba for optimization
    # Creates the sudoku as a 9x9 matrix with all zeros
    sudoku = np.zeros((9, 9), dtype=np.int32)

    # Initializes a counter to keep track of how many numbers have been inserted
    inserted_numbers_counter = 0

    while inserted_numbers_counter < n:
        # Randomly selects a row, column and number to insert in the sudoku
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)

        # Checks if the cell is already filled
        if sudoku[row][col] == 0:
            # If the cell is empty, inserts the number and checks if the board is still valid
            sudoku[row][col] = num
            if check_board(sudoku, row, col):
                # Adds one to the inserted numbers counter
                inserted_numbers_counter += 1
                inserts[num - 1] += 1
            else:
                # If the board is invalid, sets the cell back to 0 and doesn't add to the counter
                sudoku[row][col] = 0

    return sudoku, inserts

@njit
def search_closest_zero(sudoku):
    # Searches for closest zero from top left to bottom right via brute force
    # Should send some parameters to tell which columns and rows to ignore (full ones)
    #   Could also keep track of which numbers have already been finished to not try them again (
    #       would need to keep track of which numbers are in which rows and columns and it doesnt seem worth it
    #           because i would just do a continue, so the for cycle keeps going, only skips searching the sudoku)
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j
    return -1, -1

@njit
def insert_number(sudoku, inserts):
    # Searches closest zero and gets its coordinates
    row, col = search_closest_zero(sudoku)
    # If no more zeros are found, the coordinates are -1 -1 and the sudoku is solved, returns True and cuts the recursion
    if row == -1 and col == -1:
        return True, inserts

    # Inserts every possible number in the cell
    for i in range(9):
        sudoku[row][col] = i + 1
        # Checks if inserting the number makes the board into an invalid state
        if check_board(sudoku, row, col):
            inserts[i] += 1
            # If the board is valid, recursively calls the function to insert the next number
            if insert_number(sudoku, inserts)[0]:
                return True, inserts
        # If the board is invalid, sets the cell back to 0 and tries the next number
        sudoku[row][col] = 0
    # If no number can be inserted in the cell, returns False
    # Note: (NOT CHECKED, could just take a really long time to finish) There is an error in which if 
    #   there is no possible number to insert in any cell, the program will never stop
    return False, inserts

def solve_sudoku(sudoku, inserts):
    print("Solving sudoku...")
    # Recursive call to insert_number, which will solve the sudoku
    if insert_number(sudoku, inserts)[0]:
        # Checks if the sudoku has been correctly solved
        if not global_check_board(sudoku):
            print("Invalid solution")
            return False
        print("Sudoku solved!")
    else:
        print("No solution found")
    # Prints the sudoku regardless of if it was solved or not
    print_sudoku(sudoku)

def test(sudoku):
    print("Test")
    print("Row 0 ")
    for i in range(9):
        print(sudoku[0][i], end=' ')
    print("End Row")
    print("Col 0 ")
    for i in range(9):
        print(sudoku[i][0], end=' ')
    print("End Col")
    print("End Test")

def start_program():
    # numbers_in_sudoku = int(input("Insert the number of numbers in the sudoku (between 0 and 55): "))
    # Used for running the program without input
    numbers_in_sudoku = 17
    if numbers_in_sudoku < 0 or numbers_in_sudoku > 55:
        print("Invalid number of numbers, setting to 17")
        numbers_in_sudoku = 17
    # Creates the sudoku board with n numbers randomly placed
    print("Creating sudoku")
    start_time = time.time()
    # Creates three lists with 9 zeros to show the number of inserts of each number, row and column
    inserts = [0] * 9
    # row_inserts = [0] * 9
    # col_inserts = [0] * 9
    sudoku, inserts = create_sudoku_with_n_numbers(numbers_in_sudoku, inserts)
    end_time = time.time()
    print("Creating time: {:.4f} seconds".format(end_time - start_time))
    print("Sudoku created:")
    # Prints the unsolved sudoku
    print_sudoku(sudoku)
    start_time = time.time()
    # Solves the sudoku
    solve_sudoku(sudoku, inserts)
    print("Inserts: ", inserts)
    end_time = time.time()
    solve_time = end_time - start_time
    print("Solving time: {:.4f} seconds".format(solve_time))

if __name__ == "__main__":
    option = 1
    while option == 1:
        start_program()
        option = int(input("Do you want to solve another sudoku? (1 for yes, 0 for no): "))
    print("Exiting program")
