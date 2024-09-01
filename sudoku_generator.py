import numpy as np
import random
from copy import deepcopy

BLANK_BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Shuffles list in a random order
def shuffle(list):
    list_copy = list[:]
    random.shuffle(list_copy)
    return list_copy

# Checks if number is valid in specific row
def row_valid(board, row, num):
    return num not in board[row]

# Checks if number is valid in specific column
def col_valid(board, col, num):
    return num not in [board[row][col] for row in range(9)]

# Checks if number is valid in specific box
def box_valid(board, row, col, num):
    box_start_row = row - row % 3 # top left corner
    box_start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[box_start_row + i][box_start_col + j] == num:
                return False
    return True

def safe_to_place(board, row, col, num):
    return row_valid(board, row, num) and col_valid(board, col, num) and box_valid(board, row, col, num)



# Finds next empty cell in grid
def next_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


# Recursively fills the Sudoku board using backtracking
def fill_puzzle(board, counter=[0]):
    empty_cell = next_empty_cell(board)
    # If no more empty cells, board is finished
    if not empty_cell:
        return True
    
    row, col = empty_cell
    for num in shuffle(num_list):
        # Random generation can result in heavy backtracking and long wait
        # Abort and retry if if more than 20_000_000 iterations
        counter[0] += 1
        if counter[0] > 20_000_000:
            raise Exception("Recursion Timeout")
        if safe_to_place(board, row, col, num):
            board[row][col] = num
            if fill_puzzle(board, counter):
                return True
            board[row][col] = 0
    return False # Triggers previous round to go to next num if unable to place any numbers


# Generates completely solved Sudoku board
def new_solved_board():
    board = [row[:] for row in BLANK_BOARD]
    fill_puzzle(board)
    return board


def multiple_possible_solutions(board):
    solutions = []
    
    def backtrack(board):
        empty_cell = next_empty_cell(board)
        if not empty_cell:
            solutions.append(deepcopy(board))
            return len(solutions) > 1  # Stop once we find more than one solution
        
        row, col = empty_cell
        for num in num_list:
            if safe_to_place(board, row, col, num):
                board[row][col] = num
                if backtrack(board):
                    return True
                board[row][col] = 0
        return False
    
    backtrack(deepcopy(board))
    return len(solutions) > 1


# Removes a specified number of cells from the board to create a playable puzzle
def poke_holes(board, holes):
    removed_vals = []

    while len(removed_vals) < holes:
        val = random.randint(0, 80)
        row, col = val // 9, val % 9

        # If cell already empty, restart loop
        if board[row][col] == 0:
            continue

        original_value = board[row][col]
        removed_vals.append((row, col, original_value)) # store removed val
        board[row][col] = 0 # poke hole in board (i.e. set to 0)
        
        if multiple_possible_solutions(deepcopy(board)):
            board[row][col] = original_value
            removed_vals.pop()


    return removed_vals, board

# Generates a new playable Sudoku puzzle creating a solved board, 
# then poking holes in it
def new_starting_board(holes):
    while True:
        try:
            solved_board = new_solved_board()
            removed_vals, starting_board = poke_holes(deepcopy(solved_board), holes)
            return removed_vals, starting_board, solved_board
        except Exception as e:
            print(f"Error: {e}. Retrying...")

# Example usage:
holes = 40  # Number of holes to poke in the board
removed_vals, starting_board, solved_board = new_starting_board(holes)