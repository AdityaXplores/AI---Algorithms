import tkinter as tk
from tkinter import ttk, messagebox
import time
import heapq
import copy

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver: DFS vs A*")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.algorithm = tk.StringVar(value="DFS")
        self.nodes_explored = 0
        self.setup_board()
        self.setup_controls()

    def setup_board(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 20), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry

    def setup_controls(self):
        ttk.Label(self.root, text="Algorithm:").grid(row=9, column=0)
        algo_menu = ttk.Combobox(self.root, textvariable=self.algorithm, values=["DFS", "A*"], width=10)
        algo_menu.grid(row=9, column=1, columnspan=2)

        tk.Button(self.root, text="Solve", command=self.solve, bg='green', fg='white').grid(row=9, column=3, columnspan=2)
        tk.Button(self.root, text="Clear", command=self.clear, bg='red', fg='white').grid(row=9, column=5, columnspan=2)

        self.status = ttk.Label(self.root, text="")
        self.status.grid(row=10, column=0, columnspan=9, pady=10)

    def read_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def write_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
        self.status.config(text="")

    def solve(self):
        board = self.read_board()
        self.nodes_explored = 0
        start = time.time()

        if self.algorithm.get() == "DFS":
            solved = self.solve_dfs(board)
        else:
            solved = self.solve_astar(board)

        end = time.time()
        if solved:
            self.write_board(board)
            self.status.config(text=f"✅ {self.algorithm.get()} | Nodes: {self.nodes_explored} | Time: {end - start:.4f}s")
        else:
            messagebox.showerror("Unsolvable", "No solution found.")

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        r, c = 3 * (row//3), 3 * (col//3)
        for i in range(r, r+3):
            for j in range(c, c+3):
                if board[i][j] == num:
                    return False
        return True

    def solve_dfs(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        self.nodes_explored += 1
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_dfs(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def solve_astar(self, board):
        def heuristic(b):
            return sum(row.count(0) for row in b)

        def next_states(b):
            for i in range(9):
                for j in range(9):
                    if b[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, i, j, num):
                                new_board = copy.deepcopy(b)
                                new_board[i][j] = num
                                yield new_board
                        return

        heap = []
        h = heuristic(board)
        heapq.heappush(heap, (h, board))

        visited = set()

        while heap:
            _, current = heapq.heappop(heap)
            self.nodes_explored += 1

            state_key = str(current)
            if state_key in visited:
                continue
            visited.add(state_key)

            if heuristic(current) == 0:
                board[:] = current
                return True

            for child in next_states(current):
                heapq.heappush(heap, (heuristic(child), child))

        return False

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
