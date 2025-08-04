import copy
import heapq

# Constants
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

def print_board(board):
    print("\n".join([" | ".join(row) for row in board]))
    print()

def check_winner(board):
    lines = []

    for row in board:
        lines.append(row)
    for col in zip(*board):
        lines.append(col)
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line.count(line[0]) == 3 and line[0] != EMPTY:
            return line[0]
    return None

def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def heuristic(board):
    winner = check_winner(board)
    if winner == AI:
        return -10
    elif winner == PLAYER:
        return 10
    else:
        return 0

# --- DFS Implementation ---

def dfs(board, player):
    winner = check_winner(board)
    if winner or is_full(board):
        return heuristic(board), None

    if player == AI:
        best = float('inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            new_board = copy.deepcopy(board)
            new_board[i][j] = AI
            score, _ = dfs(new_board, PLAYER)
            if score < best:
                best = score
                best_move = move
        return best, best_move
    else:
        best = float('-inf')
        best_move = None
        for move in get_available_moves(board):
            i, j = move
            new_board = copy.deepcopy(board)
            new_board[i][j] = PLAYER
            score, _ = dfs(new_board, AI)
            if score > best:
                best = score
                best_move = move
        return best, best_move

# --- A* Implementation ---

def a_star(board):
    pq = []
    heapq.heappush(pq, (heuristic(board), board, True, None)) 

    visited = set()

    while pq:
        _, current, is_ai_turn, move_to_reach = heapq.heappop(pq)
        key = str(current)
        if key in visited:
            continue
        visited.add(key)

        winner = check_winner(current)
        if winner or is_full(current):
            return heuristic(current), move_to_reach

        for move in get_available_moves(current):
            i, j = move
            new_board = copy.deepcopy(current)
            new_board[i][j] = AI if is_ai_turn else PLAYER
            score = heuristic(new_board)
            heapq.heappush(pq, (score, new_board, not is_ai_turn, move if move_to_reach is None else move_to_reach))

    return 0, None

# --- Game Loop ---

def play_game(strategy="dfs"):
    board = [[EMPTY] * 3 for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        # Player move
        row, col = map(int, input("Enter your move (row col): ").split())
        if board[row][col] != EMPTY:
            print("Invalid move. Try again.")
            continue
        board[row][col] = PLAYER
        print_board(board)

        if check_winner(board) == PLAYER:
            print("You win!")
            break
        elif is_full(board):
            print("Draw!")
            break

        # AI move
        print(f"AI is thinking using {strategy.upper()}...")
        if strategy == "dfs":
            _, move = dfs(board, AI)
        else:
            _, move = a_star(board)

        if move:
            board[move[0]][move[1]] = AI
            print_board(board)
        else:
            print("Draw!")
            break

        if check_winner(board) == AI:
            print("AI wins!")
            break
        elif is_full(board):
            print("Draw!")
            break

# Example usage
if __name__ == "__main__":
    mode = input("Choose strategy for AI (dfs/a*): ").strip().lower()
    play_game(strategy=mode)
