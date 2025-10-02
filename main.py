import tkinter as tk
import argparse
from collections import deque

from map_reader import map_reader
from graphics import SkyscraperPuzzleGUI
from CSP import CSP
from Solver import Solver


def longest_increasing_sequence(arr):
    """Find the length of the longest increasing sequence starting from the beginning."""
    length = 1
    max = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max:
            length += 1
            max = arr[i]
    return length

def distinction_constraint(*args):
    ans = len(set(args)) == len(args)
    return ans

def visibility_constraint(*args, clues, direction):
    if direction == 'left' or direction == 'down':
        ordering = args
    else: 
        ordering = args[::-1]

    visible = 0
    max_height = 0
    for height in ordering:
        if height > max_height:
            visible += 1
            max_height = height
    return (visible == clues)


# Main part of the code to run the GUI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skyscraper Puzzle Solver")

    parser.add_argument(
        "-m",
        "--map",
        type=int,
        choices=[i for i in range(3, 100)],
        help="Map must be less than 100 and greater than 2",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-MAC",
        "--maintaining_arc_consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )

    args = parser.parse_args()
    clues = map_reader(args.map)  # clues= [top, bottom, left, right]
    grid_size = len(clues[0])

    csp = CSP()
    
        # Here are the variables
    for i in range(grid_size):
        for j in range(grid_size):
            variable = (i, j)
            csp.add_variable(variable, range(1, grid_size + 1))

    print("CSP's info")
    print("vars & domains:")
    for variable, domain in csp.variables.items():
        print(f"{variable}: {domain}")

    # adding the distinction constraints
    for i in range(grid_size):
        # distinction constraint for row i
        csp.add_constraint(distinction_constraint, [(i,j) for j in range(grid_size)])

        # distinction constraint for column i
        csp.add_constraint(distinction_constraint, [(j,i) for j in range(grid_size)])

    top, bottom, left, right = clues

    # constraints for visibility of skyscrapers for row i
    for i in range(grid_size):
        # left constraint
        def see_from_left(*args, clues=left[i]):
            return visibility_constraint(*args, clues=clues, direction='left')
        
        # right constraint
        def see_from_right(*args, clues=right[i]):
            return visibility_constraint(*args, clues=clues, direction='right')
        
        csp.add_constraint(see_from_left, [(i,j) for j in range(grid_size)])
        csp.add_constraint(see_from_right, [(i,j) for j in range(grid_size)])

    # constraints for visibility of skyscrapers for column i
    for i in range(grid_size):
        # top constraint function
        def see_from_top(*args, clues=top[i]):
            return visibility_constraint(*args, clues=clues, direction='down')
        
        # bottom constraint function
        def see_from_bottom(*args, clues=bottom[i]):
            return visibility_constraint(*args, clues=clues, direction='up')
        
        csp.add_constraint(see_from_top, [(j,i) for j in range(grid_size)])
        csp.add_constraint(see_from_bottom, [(j,i) for j in range(grid_size)])

    root = tk.Tk()
    root.title("Skyscraper Puzzle")

    # Center the window
    window_width, window_height = 600, 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    solver = Solver(csp, args.lcv, args.mrv, args.maintaining_arc_consistency)

    puzzle = SkyscraperPuzzleGUI(root, grid_size, solver)

    # Adding clues to the GUI
    for j in range(1, grid_size + 1):
        puzzle.add_clue(0, j, clues[0][j - 1], "down")  # Top clue pointing down
        puzzle.add_clue(grid_size + 1, j, clues[1][j - 1], "up")  # Bottom clue pointing up
    for i in range(1, grid_size + 1):
        puzzle.add_clue(i, 0, clues[2][i - 1], "right")  # Left clue pointing right
        puzzle.add_clue(i, grid_size + 1, clues[3][i - 1], "left")  # Right clue pointing left

    root.mainloop()