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
    
    def print_grid_with_rules(puzzle):
        grid = puzzle["grid"]
        h_constraints = puzzle["horizontal_constraints"]
        v_constraints = puzzle["vertical_constraints"]

        N = len(grid)

        # --- Print the grid ---
        print("Grid:")
        for r, row in enumerate(grid):
            display_row = [str(cell) for cell in row]
            print(" ".join(display_row))
        print()

        # --- Horizontal constraints ---
        print("Horizontal constraints (between cells in same row):")
        for r, row in enumerate(h_constraints):
            for c, val in enumerate(row):
                if val != ".":
                    print(f"Row {r}, cols {c}-{c+1}: {val}")
        print()

        # --- Vertical constraints ---
        print("Vertical constraints (between rows in same column):")
        for r, row in enumerate(v_constraints):
            for c, val in enumerate(row):
                if val != ".":
                    print(f"Cols {c}, rows {r}-{r+1}: {val}")
        print()

# Step 1: Load puzzle
puzzle = BinairoGame.load_puzzle("puzzles/puzzle1.json")
BinairoGame.print_grid_with_rules(puzzle)
