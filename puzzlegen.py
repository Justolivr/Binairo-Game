import random
from binairo import BinairoGame, BinairoLogic # import every rule from the Binairo Game


N = 8 # fixed board size - In future, might add multiple sizes.

def _empty_puzzle_data(n=N):
    # return empty grid in csv
    return{}

def generate_full_solution(n=N, max_attempts=200): # produces randomly generated grid
    # Need loop to randomly assign each value.
    return False

def _has_unique_solution(grid, n=N):
    return False

def generate_puzzle(n=N, min_clues = 20, max_clues = 28): # Generate Binairo: start from random solution, then remove cells one at a time until no more can be safely removed (e.g. before use of backtracking)
    return False