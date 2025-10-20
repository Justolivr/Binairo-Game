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
                if grid[r][c] is not None:
                    row_str += str(grid[r][c])
                else:
                    row_str += "."
                if c < N-1:
                    if horizontal_constraints[r][c] is not None:
                        row_str += horizontal_constraints[r][c]
                    else:
                        row_str += ""
                print(row_str)
            
            if r < N-1:
                col_str = ""
                for c in range(N):
                    if vertical_constraints[r][c] is not None:
                        col_str += vertical_constraints[r][c]
                    else:
                        col_str += ""
                    if c < N-1:
                        col_str += " "
                print(col_str)    

                

        
        return 0


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