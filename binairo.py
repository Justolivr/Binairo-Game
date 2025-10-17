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
    def print_grid_with_constraints(grid, horizontal_constraints, vertical_constraints):
        N = len(grid)
        for r in range(N): # for each row in the grid
            row_str = "" # initialise an empty string
            for c in range(N): # for each column in the grid
                row_str = row_str + str(grid[r][c]) if grid[r][c] is not None else "."
                

        
        return 0


# Step 1: Load puzzle
puzzle = BinairoGame.load_puzzle("puzzles/puzzle1.json")

# Step 2: Convert grid symbols into Python values
grid = BinairoGame.convert_grid(puzzle["grid"])

# Step 3: Print information
print("Puzzle name:", puzzle["name"])
print("Grid:")
for row in grid:
    display_row = [str(x) if x is not None else "." for x in row]
    print(" ".join(display_row))

# Step 4: Print constraints (ensure key names match JSON!)
print("Horizontal constraints:", puzzle.get("h_constraints"))
print("Vertical constraints:", puzzle.get("v_constraints"))