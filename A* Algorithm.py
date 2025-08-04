import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, end):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    goal_node = Node(end)
    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == goal_node.position:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_set.add(current.position)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor_pos = (current.position[0] + dx, current.position[1] + dy)
            if (0 <= neighbor_pos[0] < len(grid) and
                0 <= neighbor_pos[1] < len(grid[0]) and
                grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and
                neighbor_pos not in closed_set):

                neighbor = Node(neighbor_pos, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor_pos, goal_node.position)
                neighbor.f = neighbor.g + neighbor.h

                if any(open_node.position == neighbor.position and open_node.f <= neighbor.f for open_node in open_list):
                    continue

                heapq.heappush(open_list, neighbor)

    return None

# Manual input
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

grid = []
print("Enter the grid row by row (0 = free, 1 = wall):")
for i in range(rows):
    row = list(map(int, input(f"Row {i}: ").split()))
    if len(row) != cols:
        raise ValueError("Row length must match number of columns")
    grid.append(row)

start = tuple(map(int, input("Enter start position (row col): ").split()))
goal = tuple(map(int, input("Enter goal position (row col): ").split()))

path = astar(grid, start, goal)

if path:
    print("Shortest Path Found:")
    for step in path:
        print(step)
else:
    print("No path found")


"""import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0
        self.h = 0 
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, end):
    open_list = []
    closed_set = set()

    start_node = Node(start)
    goal_node = Node(end)

    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == goal_node.position:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_set.add(current.position)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor_pos = (current.position[0] + dx, current.position[1] + dy)

            if (0 <= neighbor_pos[0] < len(grid) and
                0 <= neighbor_pos[1] < len(grid[0]) and
                grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and
                neighbor_pos not in closed_set):

                neighbor = Node(neighbor_pos, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor_pos, goal_node.position)
                neighbor.f = neighbor.g + neighbor.h

                if any(open_node.position == neighbor.position and open_node.f <= neighbor.f for open_node in open_list):
                    continue

                heapq.heappush(open_list, neighbor)

    return None

grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
end = (4, 4)

path = astar(grid, start, end)
print("Shortest Path:", path) """
