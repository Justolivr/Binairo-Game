import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

class BinairoLogic:
    def __init__(self, game):
        self.game = game

    def apply_adjacent_rules(self): # If 2 adj cells are linked by X's or ='s, and one is known, then fill the other.
  
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
                # Must be opposite values
                    if cell1 is not None and cell2 is None:
                        grid[r][c + 1] = 1 - cell1
                        changed = True
                        print(f"H Fill (x): grid[{r}][{c+1}] = {grid[r][c+1]}")
                    elif cell2 is not None and cell1 is None:
                        grid[r][c] = 1 - cell2
                        changed = True
                        print(f"H Fill (x): grid[{r}][{c}] = {grid[r][c]}")

                elif cons == "=":
                    # Must be same values
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

    def apply_equal_number_rule(self): # if row/col has >half X's or ='s, then fill the rest with opposite values.
        changed = False
        N = self.game.N
        grid = self.game.grid
        half = N // 2

        for r in range(N):
            row = grid[r]
            n_zero = row.count(0)
            n_one = row.count(1)
            empty_cells = [c for c, val in enumerate(row) if val is None]

            if n_zero == half:
                for c in empty_cells:
                    row[c] = 1
                    changed = True
                    print(f"Row fill: grid[{r}][{c}] = 1")
            elif n_one == half:
                for c in empty_cells:
                    row[c] = 0
                    changed = True
                    print(f"Row fill: grid[{r}][{c}] = 0")

        for c in range(N):
            col = [grid[r][c] for r in range(N)]
            n_zero = col.count(0)
            n_one = col.count(1)
            empty_cells = [r for r, val in enumerate(col) if val is None]

            if n_zero == half:
                for r in empty_cells:
                    grid[r][c] = 1
                    changed = True
                    print(f"Column fill: grid[{r}][{c}] = 1")
            elif n_one == half:
                for r in empty_cells:
                    grid[r][c] = 0
                    changed = True
                    print(f"Column fill: grid[{r}][{c}] = 0")

        return changed

    def check_for_triple(self):# Check that we don't have 3 X's or 3 ='s in a row.
        changed = False
        N = self.game.N
        grid = self.game.grid

        for r in range(N):
            for c in range(N - 2):
                cells = [grid[r][c], grid[r][c + 1], grid[r][c + 2]]
                # Option 1 : X X .
                if cells[0] is not None and cells[1] == cells[0] and cells[2] is None:
                    grid[r][c + 2] = 1 - cells[0]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c+2}] = {grid[r][c+2]} (no three rule)")
                # Option 2 : . X X
                if cells[2] is not None and cells[1] == cells[2] and cells[0] is None:
                    grid[r][c] = 1 - cells[2]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c}] = {grid[r][c]} (no three rule)")
                # Option 3 : X . X
                if cells[0] is not None and cells[2] == cells[0] and cells[1] is None:
                    grid[r][c + 1] = 1 - cells[0]
                    changed = True
                    print(f"Row {r}: grid[{r}][{c+1}] = {grid[r][c+1]} (no three rule)")

        for c in range(N):
            for r in range(N - 2):
                cells = [grid[r][c], grid[r + 1][c], grid[r + 2][c]]
                # Option 1 : = = .
                if cells[0] is not None and cells[1] == cells[0] and cells[2] is None:
                    grid[r + 2][c] = 1 - cells[0]
                    changed = True
                    print(f"Col {c}: grid[{r+2}][{c}] = {grid[r+2][c]} (no three rule)")
                # Option 2 : . = =
                if cells[2] is not None and cells[1] == cells[2] and cells[0] is None:
                    grid[r][c] = 1 - cells[2]
                    changed = True
                    print(f"Col {c}: grid[{r}][{c}] = {grid[r][c]} (no three rule)")
                # Option 3 : = . =
                if cells[0] is not None and cells[2] == cells[0] and cells[1] is None:
                    grid[r + 1][c] = 1 - cells[0]
                    changed = True
                    print(f"Col {c}: grid[{r+1}][{c}] = {grid[r+1][c]} (no three rule)")

        return changed

    def apply_unique_completion_rule(self): # No two rows/cols can be identical. If filling creates a duplicate, then fill other way round instead
        changed = False
        N = self.game.N
        grid = self.game.grid

        # --- Rows ---
        complete_rows = [row for row in grid if None not in row]
        for r in range(N):
            row = grid[r]
            if row.count(None) != 2:
                continue

            i1, i2 = [i for i, v in enumerate(row) if v is None]
            for guess in [(0, 1), (1, 0)]:
                candidate = row.copy()
                candidate[i1], candidate[i2] = guess
                if candidate in complete_rows:
                    other = (1 - guess[0], 1 - guess[1])
                    grid[r][i1], grid[r][i2] = other
                    changed = True
                    print(f"Row {r} unique completion: [{i1}]={other[0]}, [{i2}]={other[1]}")
                    break

        # --- Columns ---
        cols = [[grid[r][c] for r in range(N)] for c in range(N)]
        complete_cols = [col for col in cols if None not in col]
        for c in range(N):
            col = cols[c]
            if col.count(None) != 2:
                continue

            i1, i2 = [i for i, v in enumerate(col) if v is None]
            for guess in [(0, 1), (1, 0)]:
                candidate = col.copy()
                candidate[i1], candidate[i2] = guess
                if candidate in complete_cols:
                    other = (1 - guess[0], 1 - guess[1])
                    grid[i1][c], grid[i2][c] = other
                    changed = True
                    print(f"Col {c} unique completion: [{i1}]={other[0]}, [{i2}]={other[1]}")
                    break

        return changed

    def solve(self): # Keep applying all 4 rules until there are none to be applied (when the board is completed)
        while True:
            changed = False
            changed |= self.apply_adjacent_rules()
            changed |= self.apply_equal_number_rule()
            changed |= self.check_for_triple()
            changed |= self.apply_unique_completion_rule()
            if not changed:
                break

    def is_solved(self):
        return all(cell is not None for row in self.game.grid for cell in row)

    def is_valid(self):
        # Checks that puzzle hasn't broken any rule
        N = self.game.N
        grid = self.game.grid
        half = N // 2

        # No three in a row (rows and columns)
        for r in range(N):
            for c in range(N - 2):
                a, b, c_ = grid[r][c], grid[r][c + 1], grid[r][c + 2]
                if a is not None and a == b == c_:
                    return False
        for c in range(N):
            for r in range(N - 2):
                a, b, c_ = grid[r][c], grid[r + 1][c], grid[r + 2][c]
                if a is not None and a == b == c_:
                    return False

        # Equal count so far shouldn't exceed half
        for r in range(N):
            row = grid[r]
            if row.count(0) > half or row.count(1) > half:
                return False
        for c in range(N):
            col = [grid[r][c] for r in range(N)]
            if col.count(0) > half or col.count(1) > half:
                return False

        # No duplicate complete rows/cols
        complete_rows = [row for row in grid if None not in row]
        if len(complete_rows) != len({tuple(row) for row in complete_rows}):
            return False
        cols = [[grid[r][c] for r in range(N)] for c in range(N)]
        complete_cols = [col for col in cols if None not in col]
        if len(complete_cols) != len({tuple(col) for col in complete_cols}):
            return False

        # Adjacency constraints
        for r in range(N):
            for c in range(N - 1):
                cons = self.game.h_constraints[r][c]
                a, b = grid[r][c], grid[r][c + 1]
                if a is None or b is None:
                    continue
                if cons == "x" and a == b:
                    return False
                if cons == "=" and a != b:
                    return False
        for c in range(N):
            for r in range(N - 1):
                cons = self.game.v_constraints[r][c]
                a, b = grid[r][c], grid[r + 1][c]
                if a is None or b is None:
                    continue
                if cons == "x" and a == b:
                    return False
                if cons == "=" and a != b:
                    return False

        return True

    def count_solutions(self, limit=2):
        # Count number of valid solutions that exist.
        self.solve()
 
        if not self.is_valid():
            return 0
        if self.is_solved():
            return 1
 
        N = self.game.N
        grid = self.game.grid
 
        target = None
        for r in range(N):
            for c in range(N):
                if grid[r][c] is None:
                    target = (r, c)
                    break
            if target:
                break
        r, c = target
 
        total = 0
        for guess in (0, 1):
            trial_grid = [row.copy() for row in grid]
            trial_grid[r][c] = guess
 
            trial_game = BinairoGame.__new__(BinairoGame)
            trial_game.name = self.game.name
            trial_game.grid = trial_grid
            trial_game.h_constraints = self.game.h_constraints
            trial_game.v_constraints = self.game.v_constraints
            trial_game.N = N
 
            trial_solver = BinairoLogic(trial_game)
            total += trial_solver.count_solutions(limit - total)
            if total >= limit:
                return total
 
        return total
    
    def solve_with_backtracking(self): # Backtrack if our four rules doesn't produce a distinct board - guess and check remaining empty cells. Returns True if full valid solution is found
        self.solve()

        if not self.is_valid():
            return False
        if self.is_solved():
            return True

        N = self.game.N
        grid = self.game.grid

        # Pick the first empty cell to branch on
        target = None
        for r in range(N):
            for c in range(N):
                if grid[r][c] is None:
                    target = (r, c)
                    break
            if target:
                break
        r, c = target

        for guess in (0, 1):
            # Work on a deep copy so a failed guess never corrupts state
            trial_grid = [row.copy() for row in grid]
            trial_grid[r][c] = guess

            trial_game = BinairoGame.__new__(BinairoGame)
            trial_game.name = self.game.name
            trial_game.grid = trial_grid
            trial_game.h_constraints = self.game.h_constraints
            trial_game.v_constraints = self.game.v_constraints
            trial_game.N = N

            trial_solver = BinairoLogic(trial_game)
            if trial_solver.solve_with_backtracking():
                self.game.grid = trial_game.grid
                return True

        return False


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
        with open(file_path, "r") as file:
            return json.load(file)

    def print_grid_with_rules(self):
        print("Grid:")
        for row in self.grid:
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


if __name__ == "__main__":
    puzzle_data = BinairoGame.load_puzzle("puzzles/puzzle2.json")
    game = BinairoGame(puzzle_data)
    solver = BinairoLogic(game)

    print("Initial puzzle:")
    game.print_grid_with_rules()

    solved = solver.solve_with_backtracking()

    print("Final state:")
    game.print_grid_with_rules()

    if solved:
        print("Puzzle fully solved!")
    else:
        print("No valid solution found — check the puzzle constraints for a contradiction.")