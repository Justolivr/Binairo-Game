import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class BinairoLogic:
    def __init__(self, game):
        self.game = game

    def apply_adjacent_rules(self): # this applies every adjacent rule for the binairo

        grid = self.game.grid
        h_constraints = self.game.h_constraints
        v_constraints = self.game.v_constraints
        N = self.game.N # size of the grid
        changed = False # flag to track if any changes were made

        # -----------------------------
        # Horizontal checks
        # -----------------------------
        for r in range(N):
            for c in range(N - 2):
                cell1, cell2, cell3 = grid[r][c], grid[r][c+1], grid[r][c+2] # initialise 3 consecutive cells
                cons12, cons23 = h_constraints[r][c], h_constraints[r][c+1] # initialise the constraints between them (1-2 and 2-3)

                # Forward check : first two cells known
                if cell1 is not None and cell2 is not None and cell3 is None:
                    if cons23 != ".": # if there is a constraint between cell2 and cell3
                        if cons23 == "=":
                            grid[r][c+2] = cell2
                        elif cons23 == "x":
                            grid[r][c+2] = 1 - cell2
                        changed = True 
                        print(f"H Fill: grid[{r}][{c+2}] = {grid[r][c+2]}")

                # Backward check: last two cells known
                if cell1 is None and cell2 is not None and cell3 is not None:
                    if cons12 != ".":
                        if cons12 == "=":
                            grid[r][c] = cell2
                        elif cons12 == "x":
                            grid[r][c] = 1 - cell2
                        changed = True
                        print(f"H Fill: grid[{r}][{c}] = {grid[r][c]}")

                # One known at front, two empty cells
                if cell1 is not None and cell2 is None and cell3 is None:
                    if cons12 != ".":
                        if cons12 == "=":
                            grid[r][c+1] = cell1
                        elif cons12 == "x":
                            grid[r][c+1] = 1 - cell1
                        changed = True
                        print(f"H Fill (1→2 empty): grid[{r}][{c+1}] = {grid[r][c+1]}")

                # One known at end, two empty cells
                if cell1 is None and cell2 is None and cell3 is not None:
                    if cons23 != ".":
                        if cons23 == "=":
                            grid[r][c+1] = cell3
                        elif cons23 == "x":
                            grid[r][c+1] = 1 - cell3
                        changed = True
                        print(f"H Fill (1→2 empty): grid[{r}][{c+1}] = {grid[r][c+1]}")

        # -----------------------------
        # Vertical checks
        # -----------------------------
        for c in range(N):
            for r in range(N - 2):
                cell1, cell2, cell3 = grid[r][c], grid[r+1][c], grid[r+2][c]
                cons12, cons23 = v_constraints[r][c], v_constraints[r+1][c]

                # Forward check: first two cells known
                if cell1 is not None and cell2 is not None and cell3 is None:
                    if cons23 != ".":
                        if cons23 == "=":
                            grid[r+2][c] = cell2
                        elif cons23 == "x":
                            grid[r+2][c] = 1 - cell2
                        changed = True
                        print(f"V Fill: grid[{r+2}][{c}] = {grid[r+2][c]}")

                # Backward check: last two cells known
                if cell1 is None and cell2 is not None and cell3 is not None:
                    if cons12 != ".":
                        if cons12 == "=":
                            grid[r][c] = cell2
                        elif cons12 == "x":
                            grid[r][c] = 1 - cell2
                        changed = True
                        print(f"V Fill: grid[{r}][{c}] = {grid[r][c]}")

                # One known at front, two empty cells
                if cell1 is not None and cell2 is None and cell3 is None:
                    if cons12 != ".":
                        if cons12 == "=":
                            grid[r+1][c] = cell1
                        elif cons12 == "x":
                            grid[r+1][c] = 1 - cell1
                        changed = True
                        print(f"V Fill (1→2 empty): grid[{r+1}][{c}] = {grid[r+1][c]}")

                # One known at end, two empty cells
                if cell1 is None and cell2 is None and cell3 is not None:
                    if cons23 != ".":
                        if cons23 == "=":
                            grid[r+1][c] = cell3
                        elif cons23 == "x":
                            grid[r+1][c] = 1 - cell3
                        changed = True
                        print(f"V Fill (1→2 empty): grid[{r+1}][{c}] = {grid[r+1][c]}")

        return changed



        



                



    
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
changed = solver.apply_adjacent_rules()  # note: call it as a function
if changed:
    print("After step (changes applied):")
else:
    print("After step (no changes):")

print("After applying logic step:")
game.print_grid_with_rules()




