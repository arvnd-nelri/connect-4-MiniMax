import datetime
import pygame
import sys
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 'a'
AI = 'b'
EMPTY = ' '
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

player=[]
ai=[]

def create_board():
    return [[' ' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    for row in board:
        print(row)

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

def draw_board(board, screen, winner_message=""):
    wood_texture = pygame.image.load('wood_texture.jpg') 
    wood_texture = pygame.transform.scale(wood_texture, (WIDTH, HEIGHT))
    screen.blit(wood_texture, (0, 0))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.circle(screen, (0, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS)
            pygame.draw.circle(screen, (144,238,144), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS,3)
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, (200, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS)
                pygame.draw.circle(screen, (255, 255, 255), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS, 3)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, (200, 200, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS)
                pygame.draw.circle(screen, (255, 255, 255), (c * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - ((r + 1) * SQUARE_SIZE - SQUARE_SIZE // 2)), RADIUS, 3)

    pygame.draw.rect(screen, (150, 150, 150), (0, SQUARE_SIZE, WIDTH, HEIGHT - SQUARE_SIZE), 5)

    font = pygame.font.SysFont("algerian", 75)
    if winner_message:
        label = font.render(winner_message, 1, (255, 255, 255))
        text_width, text_height = label.get_size()
        screen.blit(label, ((WIDTH - text_width) // 2, 10))
    pygame.display.update()

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == ' ':
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 20
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 50
    elif window.count(opponent_piece) == 2 and window.count(EMPTY) == 2:
        score -= 20

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


def choose_difficulty_screen():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Choose Difficulty")
    clock = pygame.time.Clock()

    difficulty = ""

    # Load wooden texture background
    wood_texture = pygame.image.load('wood_texture.jpg').convert()

    while True:
        screen.blit(wood_texture, (0, 0))  # Draw wooden texture background

        # Draw buttons with solid color
        easy_button = pygame.Rect(50, 50, 300, 50)
        medium_button = pygame.Rect(50, 120, 300, 50)
        hard_button = pygame.Rect(50, 190, 300, 50)

        # Draw button background
        pygame.draw.rect(screen, (153, 217, 234), easy_button)
        pygame.draw.rect(screen, (255, 250, 205), medium_button)
        pygame.draw.rect(screen, (255, 160, 122), hard_button)

        # Add border effect for buttons
        border_width = 3
        border_color = (0, 0, 0)
        pygame.draw.rect(screen, border_color, easy_button, border_width)
        pygame.draw.rect(screen, border_color, medium_button, border_width)
        pygame.draw.rect(screen, border_color, hard_button, border_width)

        font = pygame.font.SysFont('algerian', 30)
        easy_text = font.render("Easy", True, (0, 0, 0))
        medium_text = font.render("Medium", True, (0, 0, 0))
        hard_text = font.render("Hard", True, (0, 0, 0))

        screen.blit(easy_text, (201 - easy_text.get_width() // 2, 75 - easy_text.get_height() // 2))
        screen.blit(medium_text, (201 - medium_text.get_width() // 2, 145 - medium_text.get_height() // 2))
        screen.blit(hard_text, (201 - hard_text.get_width() // 2, 215 - hard_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_button.collidepoint(mouse_pos):
                    difficulty = "Easy"
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = "Medium"
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = "Hard"

        pygame.display.update()
        clock.tick(60)

        if difficulty:
            pygame.quit()
            return difficulty

def set_minimax_depth(difficulty):
    if difficulty == "Easy":
        return random.choice([1, 2])
    elif difficulty == "Medium":
        return random.choice([3, 4])
    elif difficulty == "Hard":
        return random.choice([5, 6])



def main():
    pygame.init()

    chosen_difficulty = choose_difficulty_screen()
    minimax_depth = set_minimax_depth(chosen_difficulty)

    pygame.init()

    pygame.display.set_caption("Count 4 Connect")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board = create_board()
    print_board(board)
    game_over = False
    turn = PLAYER
    print("Depth :",minimax_depth)
    draw_board(board, screen)  # Initial drawing of the board

    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER:
                    col = event.pos[0] // SQUARE_SIZE
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, turn)
                        player.append(col+1)

                        if winning_move(board, PLAYER):
                            print("Player wins!")
                            game_over = True

                        turn = AI
                        draw_board(board, screen)

        # AI's turn
        if turn == AI and not game_over:
            col, _ = minimax(board, minimax_depth, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)
                ai.append(col+1)
                if winning_move(board, AI):
                    print("AI wins!")
                    game_over = True

                turn = PLAYER
                draw_board(board, screen)

        if len(get_valid_locations(board)) == 0:
            print("It's a tie!")
            game_over = True

    # Display the winner message for 3 seconds before quitting
    winner_message = ""
    if winning_move(board, PLAYER):
        winner_message = "Player wins!"
    elif winning_move(board, AI):
        winner_message = "AI wins!"
    else:
        winner_message = "It's a tie!"

    draw_board(board, screen, winner_message)
    pygame.display.update()
    # pygame.time.delay(3000)  # Display the winner message for 3 seconds
    # pygame.quit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Player: ",player)
                print("AI: ",ai)
                with open ("Results.txt","a") as f:
                    f.write(f"Date : {datetime.datetime.now()}\n")
                    f.write("Depth: "+str(minimax_depth)+"\n")
                    f.write("Player: "+str(player)+"\n")
                    f.write("AI: "+str(ai)+"\n")
                    f.write("Winner: "+winner_message+"\n\n")
                sys.exit()

if __name__ == "__main__":
    main()
