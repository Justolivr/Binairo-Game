import random
from binairo import BinairoGame, BinairoLogic # import every rule from the Binairo Game


N = 8 # fixed board size - In future, might add multiple sizes.

def _empty_puzzle_data(n=N):
    # return empty grid in csv
    return {
        "name": "generated",
        "grid": [["." for _ in range(n)] for _ in range(n)],
        "horizontal_constraints": [["." for _ in range(n - 1)] for _ in range(n)],
        "vertical_constraints": [["." for _ in range(n)] for _ in range(n - 1)],
    }

def generate_full_solution(n=N, max_attempts=200): # produces randomly generated grid
    # Need loop to randomly assign each value.
    for _ in range(max_attempts):
        game = BinairoGame(_empty_puzzle_data(n))
        solver = BinairoLogic(game)
        grid = game.grid

        cells = [(r,c) for r in range(n) for c in range(n)]

        def backtrack(idx):
            if idx == len(cells):
                return True
            r,c = cells[idx]
            options = [0,1]
            random.shuffle(options) # randomly assign
            for v in options:
                grid[r][c] = v
                if solver.is_valid():
                    if backtrack(idx + 1):
                        return True
            grid[r][c] = None
            return False
        if backtrack(0):
            return grid
    raise RuntimeError("Failed to generate full solution.")
    
    

def _has_unique_solution(grid, n=N):
    puzzle_data = {
        "name": "check",
        "grid": [["." if v is None else str(v) for v in row] for row in grid],
        "horizontal_constraints": [["." for _ in range(n - 1)] for _ in range(n)],
        "vertical_constraints": [["." for _ in range(n)] for _ in range(n - 1)],
    }
    game = BinairoGame(puzzle_data)
    solver = BinairoLogic(game)
    return solver.count_solutions(limit=2) == 1

def generate_puzzle(n=N, min_clues = 20, max_clues = 28): # Generate Binairo: start from random solution, then remove cells one at a time until no more can be safely removed (e.g. before use of backtracking)
    solution = generate_full_solution(n)
    grid = [row.copy() for row in solution]
 
    cells = [(r, c) for r in range(n) for c in range(n)]
    random.shuffle(cells)
 
    for (r, c) in cells:
        clue_count = sum(1 for row in grid for v in row if v is not None)
        if clue_count <= min_clues:
            break
 
        backup = grid[r][c]
        grid[r][c] = None
        if not _has_unique_solution(grid, n):
            grid[r][c] = backup  # removing this one made it ambiguous
 
    return grid, solution
 

def puzzle_to_data(grid, name="Random Puzzle", n=N): # convert grid into JSON
    return {
        "name": name,
        "grid": [["." if v is None else str(v) for v in row] for row in grid],
        "horizontal_constraints": [["." for _ in range(n - 1)] for _ in range(n)],
        "vertical_constraints": [["." for _ in range(n)] for _ in range(n - 1)],
    }

if __name__ == "__main__":
    puzzle, solution = generate_puzzle()
    game = BinairoGame(puzzle_to_data(puzzle))
    print("Generated puzzle:")
    game.print_grid_with_rules()
 
    clue_count = sum(1 for row in puzzle for v in row if v is not None)
    print(f"Clues given: {clue_count} / {N * N}")