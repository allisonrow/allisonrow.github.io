from flask import Flask, render_template, request
import numpy as np
from sudoku_solver import solve
from copy import deepcopy
from sudoku_generator import *

app = Flask(__name__)



@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/solver', methods=['GET', 'POST'])
def solver():
    if request.method == 'POST':
        # Get the board from the form
        board = []
        user_inputs = []
        for i in range(9):
            row = []
            user_row = []
            for j in range(9):
                value = request.form.get(f'cell-{i}-{j}')
                if value == '':
                    row.append(0)
                    user_row.append(False)
                else:
                    row.append(int(value))
                    user_row.append(True)
            board.append(row)
            user_inputs.append(user_row)

        # Convert to numpy array
        #board = np.array(board)
        
        # Solve the puzzle
        solve(board)

        return render_template('solver.html', board=board, solved=True, user_inputs=user_inputs)

    # Initial page load (empty board)
    empty_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    empty_user_inputs = [[False] * 9 for _ in range(9)]
    return render_template('solver.html', board=empty_board, solved=False, user_inputs=empty_user_inputs)

@app.route('/generator')
def generator():
    holes = 50  # Number of holes to poke in the generated puzzle
    removed_vals, starting_board, solved_board = new_starting_board(holes)
    user_inputs = [[False] * 9 for _ in range(9)]
    return render_template('generator.html', board=starting_board, solved_board=solved_board)

if __name__ == '__main__':
    app.run(debug=True)


