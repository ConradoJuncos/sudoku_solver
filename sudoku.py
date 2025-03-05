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

def check_square(sudoku):
    # Made via brute force. Could be optimized to search only the square affected by the insert (using the coordinates to determine
    #   which square to search)
    # Also similar behavior to check_row and check_column
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            # Makes a set for every square in steps of 3
            seen = set()
            for row in range(3):
                for col in range(3):
                    # If the number is in the set, it returns False
                    # If not, then it adds the number to the set and keeps going
                    num = sudoku[box_row + row][box_col + col]
                    if num in seen:
                        return False
                    if num != 0:
                        seen.add(num)
    return True

def check_board(sudoku, row, col):
    # The board will be valid if all rows, columns and squares are valid
    # TODO: Optimize to not check every single row column and square for each inserted number, only the affected ones
    if check_row(sudoku, row) and check_column(sudoku, col) and check_square(sudoku):
        return True
    return False

def create_sudoku_with_n_numbers(n):
    # For creating sudoku with numpy to use numba for optimization
    # sudoku = np.zeros((9, 9), dtype=np.int32)

    # Creates the sudoku as a 9x9 matrix with all zeros
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
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
            else:
                # If the board is invalid, sets the cell back to 0 and doesn't add to the counter
                sudoku[row][col] = 0

    return sudoku

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

# TODO: keep a list of already tried cells to avoid trying them again (fixes infinite loop)

# Worst case, insert_number() has time complexity of O(9^81), which is technically O(1), but this is the first
#   candidate to optimization
def insert_number(sudoku):
    # Searches closest zero and gets its coordinates
    row, col = search_closest_zero(sudoku)
    # If no more zeros are found, the coordinates are -1 -1 and the sudoku is solved, returns True and cuts the recursion
    if row == -1 and col == -1:
        return True

    # Inserts every possible number in the cell
    for i in range(9):
        sudoku[row][col] = i + 1
        # Checks if inserting the number makes the board into an invalid state
        if check_board(sudoku, row, col):
            # If the board is valid, recursively calls the function to insert the next number
            if insert_number(sudoku):
                return True
        # If the board is invalid, sets the cell back to 0 and tries the next number
        sudoku[row][col] = 0
    # If no number can be inserted in the cell, returns False
    # Note: There is an error in which if there is no possible number to insert in any cell, the program will never stop
    return False

def solve_sudoku(sudoku):
    print("Solving sudoku...")
    # Recursive call to insert_number, which will solve the sudoku
    if insert_number(sudoku):
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

if __name__ == "__main__":
    numbers_in_sudoku = int(input("Insert the number of numbers in the sudoku (between 0 and 55): "))
    # numbers_in_sudoku = 25
    if numbers_in_sudoku < 0 or numbers_in_sudoku > 55:
        print("Invalid number of numbers, setting to 17")
        numbers_in_sudoku = 17
    # Creates the sudoku board with n numbers randomly placed
    sudoku = create_sudoku_with_n_numbers(numbers_in_sudoku)
    print("Sudoku created:")
    # Prints the unsolved sudoku
    print_sudoku(sudoku)
    # Starts the timer to solve the sudoku
    start_time = time.time()
    # Solves the sudoku
    solve_sudoku(sudoku)
    # Ends the timer
    end_time = time.time()
    # Calculates and shows how long it took to solve the sudoku (maybe use a function to do this? not very useful IMO)
    solve_time = end_time - start_time
    print("Solving time: {:.3f} seconds".format(solve_time))