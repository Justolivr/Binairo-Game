import tkinter as tk
from tkinter import messagebox
import threading

from binairo import BinairoGame, BinairoLogic
import puzzlegen as pg

N = pg.N  # 8

CELL_PX = 56
GIVEN_COLOR = "#dbe4f0"      # light blue-grey for pre-filled clues
EMPTY_COLOR = "#ffffff"
WRONG_COLOR = "#f8d0d0"      # highlight for user mistakes on check
BORDER = "#333333"
VAL_COLORS = {0: "#1e5aa8", 1: "#a81e1e"}  # blue for 0, red for 1


class BinairoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binairo")

        self.solution = None      # full solution grid, for hints / validation
        self.given_mask = None    # True where the cell was a starting clue (locked)
        self.game = None
        self.solver = None

        self._build_ui()
        self.new_game()

    # ---------------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------------
    def _build_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        tk.Button(toolbar, text="New Puzzle", command=self.new_game_async).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Check", command=self.check_solution).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Hint", command=self.give_hint).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Solve", command=self.solve_puzzle).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Reset", command=self.reset_puzzle).pack(side=tk.LEFT, padx=4)

        self.status_var = tk.StringVar(value="Generating puzzle...")
        tk.Label(self.root, textvariable=self.status_var, anchor="w").pack(side=tk.TOP, fill=tk.X, padx=8)

        self.canvas = tk.Canvas(
            self.root,
            width=CELL_PX * N + 2,
            height=CELL_PX * N + 2,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.on_click)

    # ---------------------------------------------------------------
    # Game lifecycle
    # ---------------------------------------------------------------
    def new_game_async(self):
        """Generate a puzzle on a background thread so the UI doesn't freeze."""
        self.status_var.set("Generating puzzle...")
        self.canvas.delete("all")
        threading.Thread(target=self._generate_and_load, daemon=True).start()

    def _generate_and_load(self):
        puzzle, solution = pg.generate_puzzle(N)
        self.root.after(0, lambda: self._load_puzzle(puzzle, solution))

    def new_game(self):
        # First launch: block briefly (generation takes well under a second)
        puzzle, solution = pg.generate_puzzle(N)
        self._load_puzzle(puzzle, solution)

    def _load_puzzle(self, puzzle, solution):
        self.solution = solution
        self.given_mask = [[puzzle[r][c] is not None for c in range(N)] for r in range(N)]

        puzzle_data = pg.puzzle_to_data(puzzle, name="Random Puzzle")
        self.game = BinairoGame(puzzle_data)
        self.solver = BinairoLogic(self.game)

        clue_count = sum(1 for row in puzzle for v in row if v is not None)
        self.status_var.set(f"New puzzle — {clue_count} clues given. Click a cell to cycle . -> 0 -> 1.")
        self.draw_board()

    def reset_puzzle(self):
        """Clear all non-given cells back to blank."""
        for r in range(N):
            for c in range(N):
                if not self.given_mask[r][c]:
                    self.game.grid[r][c] = None
        self.status_var.set("Board reset to starting clues.")
        self.draw_board()

    # ---------------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------------
    def draw_board(self, wrong_cells=None):
        wrong_cells = wrong_cells or set()
        self.canvas.delete("all")
        grid = self.game.grid

        for r in range(N):
            for c in range(N):
                x0, y0 = c * CELL_PX, r * CELL_PX
                x1, y1 = x0 + CELL_PX, y0 + CELL_PX

                if (r, c) in wrong_cells:
                    fill = WRONG_COLOR
                elif self.given_mask[r][c]:
                    fill = GIVEN_COLOR
                else:
                    fill = EMPTY_COLOR

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=BORDER)

                val = grid[r][c]
                if val is not None:
                    self.canvas.create_text(
                        x0 + CELL_PX / 2, y0 + CELL_PX / 2,
                        text=str(val),
                        font=("Helvetica", 20, "bold"),
                        fill=VAL_COLORS[val],
                    )

        # thicker outer border
        self.canvas.create_rectangle(1, 1, CELL_PX * N + 1, CELL_PX * N + 1, outline=BORDER, width=3)

    # ---------------------------------------------------------------
    # Interaction
    # ---------------------------------------------------------------
    def on_click(self, event):
        c = event.x // CELL_PX
        r = event.y // CELL_PX
        if not (0 <= r < N and 0 <= c < N):
            return
        if self.given_mask[r][c]:
            return  # can't edit starting clues

        current = self.game.grid[r][c]
        nxt = {None: 0, 0: 1, 1: None}[current]
        self.game.grid[r][c] = nxt
        self.draw_board()

        if all(v is not None for row in self.game.grid for v in row):
            self.check_solution(silent_if_correct=False)

    # ---------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------
    def check_solution(self, silent_if_correct=True):
        wrong = set()
        for r in range(N):
            for c in range(N):
                v = self.game.grid[r][c]
                if v is not None and v != self.solution[r][c]:
                    wrong.add((r, c))

        self.draw_board(wrong_cells=wrong)

        if wrong:
            self.status_var.set(f"{len(wrong)} cell(s) look wrong — highlighted in red.")
        else:
            filled = all(v is not None for row in self.game.grid for v in row)
            if filled:
                self.status_var.set("Solved correctly! 🎉")
                if not silent_if_correct:
                    messagebox.showinfo("Binairo", "Congratulations, you solved it!")
            else:
                self.status_var.set("No mistakes so far — keep going.")

    def give_hint(self):
        empties = [(r, c) for r in range(N) for c in range(N) if self.game.grid[r][c] is None]
        if not empties:
            self.status_var.set("Board is already full — try Check.")
            return
        r, c = empties[0]
        # Fill exactly this one cell from the known solution. We deliberately
        # do NOT run solver.solve() on the live board here — that propagates
        # logic across the whole grid and can cascade into solving the
        # entire puzzle in one click if it happens to be fully deducible.
        self.game.grid[r][c] = self.solution[r][c]
        self.status_var.set(f"Hint: filled cell ({r}, {c}).")
        self.draw_board()

    def solve_puzzle(self):
        for r in range(N):
            for c in range(N):
                self.game.grid[r][c] = self.solution[r][c]
        self.status_var.set("Solved for you — here's the full solution.")
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = BinairoApp(root)
    root.mainloop()