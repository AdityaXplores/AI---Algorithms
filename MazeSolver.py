import tkinter as tk
from tkinter import messagebox
import time
from queue import PriorityQueue, Queue

# Maze Grid: 0 = free, 1 = wall
MAZE = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
]

ROWS, COLS = len(MAZE), len(MAZE[0])
CELL_SIZE = 40

START = (0, 0)
GOAL = (9, 9)

class MazeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Maze Solver (BFS & A*)")
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='white')
        self.canvas.pack()
        self.draw_grid()

        self.info = tk.Label(root, text="Select algorithm to solve.")
        self.info.pack(pady=5)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        tk.Button(self.btn_frame, text="Solve with BFS", command=self.solve_bfs).pack(side=tk.LEFT, padx=10)
        tk.Button(self.btn_frame, text="Solve with A*", command=self.solve_astar).pack(side=tk.LEFT, padx=10)

    def draw_grid(self, path=None):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                if MAZE[i][j] == 1:
                    color = "black"
                elif (i, j) == START:
                    color = "blue"
                elif (i, j) == GOAL:
                    color = "red"
                elif path and (i, j) in path:
                    color = "green"
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def draw_path(self, path, color):
        for i, j in path:
            if (i, j) not in (START, GOAL):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def neighbors(self, i, j):
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS and MAZE[ni][nj] == 0:
                yield (ni, nj)

    def solve_bfs(self):
        start_time = time.time()
        visited = [[False]*COLS for _ in range(ROWS)]
        queue = Queue()
        queue.put((START, [START]))
        visited[START[0]][START[1]] = True
        nodes_explored = 0

        while not queue.empty():
            (i, j), path = queue.get()
            nodes_explored += 1
            if (i, j) == GOAL:
                self.draw_grid(path)
                self.info.config(text=f"BFS: Path length={len(path)}, Nodes={nodes_explored}, Time={1000*(time.time()-start_time):.2f}ms")
                return
            for ni, nj in self.neighbors(i, j):
                if not visited[ni][nj]:
                    visited[ni][nj] = True
                    queue.put(((ni, nj), path + [(ni, nj)]))

        messagebox.showinfo("BFS", "No path found!")

    def solve_astar(self):
        start_time = time.time()
        visited = [[False]*COLS for _ in range(ROWS)]
        pq = PriorityQueue()
        pq.put((0 + self.heuristic(START), 0, START, [START]))
        nodes_explored = 0

        while not pq.empty():
            f, g, (i, j), path = pq.get()
            nodes_explored += 1
            if (i, j) == GOAL:
                self.draw_grid(path)
                self.info.config(text=f"A*: Path length={len(path)}, Nodes={nodes_explored}, Time={1000*(time.time()-start_time):.2f}ms")
                return
            if visited[i][j]: continue
            visited[i][j] = True
            for ni, nj in self.neighbors(i, j):
                if not visited[ni][nj]:
                    new_g = g + 1
                    pq.put((new_g + self.heuristic((ni, nj)), new_g, (ni, nj), path + [(ni, nj)]))

        messagebox.showinfo("A*", "No path found!")

    def heuristic(self, pos):
        return abs(pos[0] - GOAL[0]) + abs(pos[1] - GOAL[1])


if __name__ == "__main__":
    root = tk.Tk()
    gui = MazeGUI(root)
    root.mainloop()
