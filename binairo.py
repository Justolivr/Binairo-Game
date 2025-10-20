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

        N = len(grid)
        for c in range(N):
            for r in range(N-2):
                cell1 = grid[r][c]
                cell2 = grid[r+1][c]
                cell3 = grid[r+2][c]
                constr_12 = h_constraints[r][c]             # constraint between cell1 and cell2
                constr_23 = h_constraints[r][c+1]           # constraint between cell2 and cell3




    
class BinairoPrint:
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
puzzle = BinairoPrint.load_puzzle("puzzles/puzzle1.json")
BinairoPrint.print_grid_with_rules(puzzle)
