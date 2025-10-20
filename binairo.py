import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class BinairoLogic:
    def __init__(self, game):
        self.game = game

    def next_adj_rule(self):
        grid = self.game.grid
        h_constraints = self.game.h_constraints
        v_constraints = self.game.v_constraints
        N = self.game.N

        changed = False

        # Horizontal checks
        for r in range(N):
            for c in range(N-2):
                cell1 = grid[r][c]
                cell2 = grid[r][c+1]
                cell3 = grid[r][c+2]
                constr_12 = h_constraints[r][c]             # constraint between cell1 and cell2
                constr_23 = h_constraints[r][c+1]           # constraint between cell2 and cell3

                # Forward checking
                if cell1 is not None and cell2 is not None and cell3 is None:
                    if constr_23 != ".":  # checks if there is a constraint
                        if constr_23 == "=":   # if there is a = constraint between cell2 and cell3
                            grid[r][c+2] = cell2 # adj cell must be the same as the first cell
                        elif constr_23 == "x": # if there is a x constraint betwwen cell2 and cell3
                            grid[r][c+2] = 1 - cell2 # if cell2 is 0, grid[r][c+2] = 1; if cell2 is 1, then grid[r][c+2] = 0
                        changed = True
                        print(f"H Fill: grid[{r}][{c+2}] set to {grid[r][c+2]}")

                # Backward checking
                if cell1 is None and cell2 is not None and cell3 is not None:
                    if constr_12 != ".":
                        if constr_12 == "=":
                            grid[r][c] = cell2
                        elif constr_12 == "x":
                            grid[r][c] = 1 - cell2
                        changed = True
                        print(f"H Fill: grid[{r}][{c}] set to {grid[r][c]}")
        # Vertical check            
        for c in range(N):
            for r in range(N-2):
                cell1 = grid[r][c]
                cell2 = grid[r+1][c]
                cell3 = grid[r+2][c]
                constr_12 = v_constraints[r][c]
                constr_23 = v_constraints[r+1][c]

                # Forward checking
                if cell1 is not None and cell2 is not None and cell3 is None:
                    if constr_23 != ".":
                        if constr_23 == "=":
                            grid[r+2][c] = cell2
                        elif constr_23 == "x":
                            grid[r+2][c] = 1 - cell2
                        changed = True
                        print(f"V Fill: grid[{r+2}][{c}] set to {grid[r+2][c]}")
                    
                if cell1 is None and cell2 is not None and cell3 is not None:
                    if constr_12 != ".":
                        if constr_12 == "=":
                            grid[r][c] = cell2
                        elif constr_12 == "x":
                            grid[r][c] = 1 - cell2
                        changed = True
                        print(f"V Fill: grid[{r}][{c}] set to {grid[r][c]}")

        return changed
    def solve_steps(self):
        return self.next_adj_rule()
            

        



                



    
class BinairoGame:
    def __init__(self, puzzle_data):
        self.name = puzzle_data["name"]
        self.grid = [
            [None if cell == "." else int(cell) for cell in row]
            for row in puzzle_data["grid"]
        ]
        self.h_constraints = puzzle_data["horizontal_constraints"]
        self.v_constraints = puzzle_data["vertical_constraints"]
        self.N = len(self.grid)

    @staticmethod
    def load_puzzle(file_path):
        with open(file_path, 'r') as file:
            puzzle_data = json.load(file)
        return puzzle_data
    
    @staticmethod
    def convert_grid(symbols):
        grid = [] # Initialize an empty list to hold the grid
        for row in symbols:
            new_row = []
            for s in row:
                print(repr(s))
                if s == ".":
                    new_row.append(None) # Appending None for empty cells
                else:
                    new_row.append(int(s)) # Appending value onto the row - must be an Integer 
            grid.append(new_row)
        return grid
    
    def print_grid_with_rules(self):
        print("Grid:")
        for r, row in enumerate(self.grid):
            display_row = [str(cell) if cell is not None else "." for cell in row]
            print(" ".join(display_row))
        print()

        print("Horizontal constraints (between cells in same row):")
        for r, row in enumerate(self.h_constraints):
            for c, val in enumerate(row):
                if val != ".":
                    print(f"Row {r}, cols {c}-{c+1}: {val}")
        print()

        print("Vertical constraints (between rows in same column):")
        for r, row in enumerate(self.v_constraints):
            for c, val in enumerate(row):
                if val != ".":
                    print(f"Cols {c}, rows {r}-{r+1}: {val}")
        print()

# Step 1: Load puzzle
# Step 1: Load puzzle as dictionary
puzzle_data = BinairoGame.load_puzzle("puzzles/puzzle1.json")

# Step 2: Create a BinairoGame instance
game = BinairoGame(puzzle_data)

# Step 3: Create a solver instance
solver = BinairoLogic(game)

print("Initial puzzle:")
game.print_grid_with_rules()

# Step 4: Apply logic
changed = solver.next_adj_rule()  # note: call it as a function
changed = solver.next_adj_rule()  # note: call it as a function
if changed:
    print("After step (changes applied):")
else:
    print("After step (no changes):")

print("After applying logic step:")
game.print_grid_with_rules()




