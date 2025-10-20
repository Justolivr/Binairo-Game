import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class BinairoGame:
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
    def print_grid_with_constraints(grid, h_constraints, v_constraints):
        def format_constraint(c, vertical=False):
            if not c:
                return " "
            if c == "=":
                return "‖" if vertical else "="
            if c == "x":
                return "⊗" if vertical else "x"
            return c
        
        N = len(grid)
        cell_w = 3

        print("    " + " ".join([f"{i:^{cell_w}}" for i in range(N)]))
        print("  " + "┌" + "┬".join(["─" * cell_w for _ in range(N)]) + "┐")

        for r in range(N):
            # row of cells + horizontal constraints
            row_str = f"{r} │"
            for c in range(N):
                val = str(grid[r][c]) if grid[r][c] is not None else "."
                row_str += f"{val:^{cell_w}}"
                if c < N - 1:
                    h = h_constraints[r][c] if h_constraints[r][c] else " "
                    row_str += f"{h:^{cell_w}}"
            row_str += "│"
            print(row_str)

            # row of vertical constraints
            if r < N - 1:
                v_row = "  │"
                for c in range(N):
                    v = v_constraints[r][c] if v_constraints[r][c] else " "
                    v_row += f"{v:^{cell_w}}"
                    if c < N - 1:
                        v_row += " " * cell_w
                v_row += "│"
                print(v_row)

        print("  " + "└" + "┴".join(["─" * cell_w for _ in range(N)]) + "┘")


# Step 1: Load puzzle
puzzle = BinairoGame.load_puzzle("puzzles/puzzle1.json")

# Step 2: Convert grid symbols into Python values
grid = BinairoGame.convert_grid(puzzle["grid"])
horizontal_constraints = puzzle["horizontal_constraints"]
vertical_constraints = puzzle["vertical_constraints"]

BinairoGame.print_grid_with_constraints(grid, horizontal_constraints, vertical_constraints)


# Step 3: Print information
print("\nPuzzle name:", puzzle["name"])
print("Grid:\n")
for row in grid:
    display_row = [str(x) if x is not None else "." for x in row]
    print(" ".join(display_row))

# Step 4: Print constraints (ensure key names match JSON!)
print("Horizontal constraints:", puzzle.get("h_constraints"))
print("Vertical constraints:", puzzle.get("v_constraints"))