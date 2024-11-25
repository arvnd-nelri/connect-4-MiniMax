ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 'P'
AI = 'A'
EMPTY = ' '

def create_board():
    return [[' ' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    for row in board:
        print('|', end=' ')
        for col in row:
            print(col, end=' | ')
        print()
    print('-' * (COLUMN_COUNT * 4 + 1))

def print_board_new(board):
    print(f"|{'---|' * 7}")
    for r in range(ROW_COUNT-1, -1, -1):
        print("|", end="")
        for c in range(COLUMN_COUNT):
            print(f" {board[r][c]} ", end="|")
        print()
        print(f"|{'---|' * 7}")
    print()

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == ' ':
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))
    if maximizing_player:
        value = -float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, AI)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, PLAYER)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def main():
    board = create_board()
    game_over = False

    print_board_new(board)
    while not game_over:

        # Player's turn
        col = int(input("Player's turn (0-6): "))
        while not is_valid_location(board, col):
            print("Invalid location!")
            col = int(input("Player's turn (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER)
            print_board_new(board)
            if winning_move(board, PLAYER):
                print("Player wins!")
                game_over = True

        # AI's turn
        if not game_over:
            col, _ = minimax(board, 5, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)
                print_board_new(board)
                if winning_move(board, AI):
                    print("AI wins!")
                    game_over = True

        if len(get_valid_locations(board)) == 0:
            print_board(board)
            print("It's a tie!")
            game_over = True

if __name__ == "__main__":
    main()
