import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class BinairoLogic:
    def __init__(self, game):
        self.game = game

    def apply_adjacent_rules(self):
        changed = False
        grid = self.game.grid
        N = self.game.N
        h_constraints = self.game.h_constraints
        v_constraints = self.game.v_constraints

        # --- Horizontal constraints ---
        for r in range(N):
            for c in range(N - 1):
                cell1, cell2 = grid[r][c], grid[r][c + 1]
                cons = h_constraints[r][c]

                if cons == "x":
                    # Must be opposite
                    if cell1 is not None and cell2 is None:
                        grid[r][c + 1] = 1 - cell1
                        changed = True
                        print(f"H Fill (x): grid[{r}][{c+1}] = {grid[r][c+1]}")
                    elif cell2 is not None and cell1 is None:
                        grid[r][c] = 1 - cell2
                        changed = True
                        print(f"H Fill (x): grid[{r}][{c}] = {grid[r][c]}")

                elif cons == "=":
                    # Must be the same
                    if cell1 is not None and cell2 is None:
                        grid[r][c + 1] = cell1
                        changed = True
                        print(f"H Fill (=): grid[{r}][{c+1}] = {grid[r][c+1]}")
                    elif cell2 is not None and cell1 is None:
                        grid[r][c] = cell2
                        changed = True
                        print(f"H Fill (=): grid[{r}][{c}] = {grid[r][c]}")

        # --- Vertical constraints ---
        for c in range(N):
            for r in range(N - 1):
                cell1, cell2 = grid[r][c], grid[r + 1][c]
                cons = v_constraints[r][c]

                if cons == "x":
                    if cell1 is not None and cell2 is None:
                        grid[r + 1][c] = 1 - cell1
                        changed = True
                        print(f"V Fill (x): grid[{r+1}][{c}] = {grid[r+1][c]}")
                    elif cell2 is not None and cell1 is None:
                        grid[r][c] = 1 - cell2
                        changed = True
                        print(f"V Fill (x): grid[{r}][{c}] = {grid[r][c]}")

                elif cons == "=":
                    if cell1 is not None and cell2 is None:
                        grid[r + 1][c] = cell1
                        changed = True
                        print(f"V Fill (=): grid[{r+1}][{c}] = {grid[r+1][c]}")
                    elif cell2 is not None and cell1 is None:
                        grid[r][c] = cell2
                        changed = True
                        print(f"V Fill (=): grid[{r}][{c}] = {grid[r][c]}")

        return changed
    
    def apply_equal_number_rule(self):
        changed = False
        N = self.game.N
        grid = self.game.grid

        for r in range(N):
            row = grid[r]
            n_zero = row.count(0)
            n_one = row.count(1)
            e_cells = [c for c, val in enumerate(row) if val is None]

            if n_zero == N/2:
                for c in e_cells:
                    row[c] = 1
                    changed = True
                    print(f"Row fill: grid[{r}][{c}] = 1")
            elif n_one == N/2:
                for c in e_cells:
                    row[c] = 0
                    changed = True
                    print(f"Row fill: grid[{r}][{c}] = 0")

        for c in range(N):
            col = [grid[r][c] for r in range(N)]
            n_zero = col.count(0)
            n_one = col.count(1)
            e_cells = [r for r, val in enumerate(col) if val is None]

            if n_zero == N/2:
                for r in e_cells:
                    grid[r][c] = 1
                    changed = True
                    print(f"Column fill: grid[{r}][{c}] = 1")
            elif n_one == N/2:
                for r in e_cells:
                    grid[r][c] = 0
                    changed = True
                    print(f"Column fill: grid[{r}][{c}] = 0")
        return changed
    
    def check_for_triple(self):
        changed = False
        N = self.game.N
        grid = self.game.grid
    
        
        for r in range(N):
            for c in range(N-2):
                cells= [grid[r][c], grid[r][c+1],grid[r][c+2]]
                # Pattern 1: X X .
                if cells[0] is not None and cells[1] == cells[0] and cells[2] is None:
                    grid[r][c+2] = 1 - cells[0]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c+2}] = {grid[r][c+2]} (no three rule)")

                # Pattern 2: . X X
                if cells[2] is not None and cells[1] == cells[2] and cells[0] is None:
                    grid[r][c] = 1 - cells[2]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c}] = {grid[r][c]} (no three rule)")

                # Pattern 3: X . X
                if cells[0] is not None and cells[2] == cells[0] and cells[1] is None:
                    grid[r][c+1] = 1 - cells[0]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c+1}] = {grid[r][c+1]} (no three rule)")
        
        for c in range(N):
            for r in range(N - 2):
                cells = [grid[r][c], grid[r+1][c], grid[r+2][c]]

                # Pattern 1: X X .
                if cells[0] is not None and cells[1] == cells[0] and cells[2] is None:
                    grid[r+2][c] = 1 - cells[0]
                    changed = True
                    print(f"Col {c}: grid[{r+2}][{c}] = {grid[r+2][c]} (no three rule)")

                # Pattern 2: . X X
                if cells[2] is not None and cells[1] == cells[2] and cells[0] is None:
                    grid[r][c] = 1 - cells[2]
                    changed = True
                    print(f"Col {c}: grid[{r}][{c}] = {grid[r][c]} (no three rule)")

                # Pattern 3: X . X
                if cells[0] is not None and cells[2] == cells[0] and cells[1] is None:
                    grid[r+1][c] = 1 - cells[0]
                    changed = True
                    print(f"Col {c}: grid[{r+1}][{c}] = {grid[r+1][c]} (no three rule)")

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

# Step 1: Load puzzle as dictionary
puzzle_data = BinairoGame.load_puzzle("puzzles/puzzle1.json")

# Step 2: Create a BinairoGame instance
game = BinairoGame(puzzle_data)

# Step 3: Create a solver instance
solver = BinairoLogic(game)

print("Initial puzzle:")
game.print_grid_with_rules()

# Step 4: Apply logic iteratively
while True:
    changed = False

    # Apply adjacent rules
    changed |= solver.apply_adjacent_rules()

    # Apply equal number rule
    changed |= solver.apply_equal_number_rule()

    changed |= solver.check_for_triple()

    if not changed:
        # No more changes possible, stop iterating
        break

print("After applying logic (final state):")
game.print_grid_with_rules()




