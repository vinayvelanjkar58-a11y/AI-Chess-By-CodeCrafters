import pygame
import chess
from stockfish import Stockfish
import time

# --- Initialize Stockfish ---
stockfish = Stockfish(path=r"C:\Users\Asus\OneDrive\Attachments\stockfish-windows-x86-64-avx2.exe")

# --- Initialize pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 640  # Extra width for eval bar
SQUARE_SIZE = HEIGHT // 8
EVAL_BAR_WIDTH = WIDTH - HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Powered Chess (By Code Crafters)")

# --- Colors ---
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
SELECTED = (246, 246, 105)
HIGHLIGHT = (255, 255, 100)
MOVE_DOT = (0, 180, 0)
WHITE_BAR = (245, 245, 245)
BLACK_BAR = (50, 50, 50)
GREEN = (0, 255, 0)
TEXT_COLOR = (20, 20, 20)
BG_COLOR = (25, 25, 25)
BUTTON_COLOR = (80, 80, 200)
BUTTON_HOVER = (100, 100, 255)

# --- Load Piece Images ---
pieces = ["wp", "bp", "wn", "bn", "wb", "bb", "wr", "br", "wq", "bq", "wk", "bk"]
images = {}
for piece in pieces:
    images[piece] = pygame.transform.scale(
        pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
    )

# --- Board Setup ---
board = chess.Board()
selected_square = None
valid_moves = []
highlighted_square = None
highlight_time = 0
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 80)


def draw_text_center(text, font, color, y):
    """Helper: Draw centered text"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)


def start_menu():
    """Start menu before the game begins"""
    menu = True
    while menu:
        screen.fill(BG_COLOR)
        draw_text_center("AI Powered Chess", title_font, (255, 255, 255), HEIGHT // 3)
        draw_text_center("(By Code Crafters)", font, (180, 180, 180), HEIGHT // 3 + 60)

        mx, my = pygame.mouse.get_pos()

        # Buttons
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

        for button, label in [(start_button, "Start Game"), (quit_button, "Quit")]:
            color = BUTTON_HOVER if button.collidepoint(mx, my) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button, border_radius=10)
            draw_text_center(label, font, (255, 255, 255), button.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mx, my):
                    menu = False  # Start the game
                if quit_button.collidepoint(mx, my):
                    pygame.quit()
                    exit()


def draw_board():
    """Draw board, pieces, and eval bar"""
    screen.fill((0, 0, 0))

    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Highlight last move
            if highlighted_square and time.time() - highlight_time < 0.7:
                h_row, h_col = highlighted_square
                if row == h_row and col == h_col:
                    pygame.draw.rect(screen, HIGHLIGHT, rect)

            # Highlight selected piece
            if selected_square is not None:
                sel_row = 7 - chess.square_rank(selected_square)
                sel_col = chess.square_file(selected_square)
                if row == sel_row and col == sel_col:
                    pygame.draw.rect(screen, SELECTED, rect)

            # Draw pieces
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                name = f"{piece.color and 'w' or 'b'}{piece.symbol().lower()}"
                screen.blit(images[name], rect)

    # Draw valid move indicators
    for move_sq in valid_moves:
        col = chess.square_file(move_sq)
        row = 7 - chess.square_rank(move_sq)
        center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
        pygame.draw.circle(screen, MOVE_DOT, center, 8)

    draw_eval_bar()
    draw_status()
    pygame.display.flip()


def draw_eval_bar():
    """Evaluation bar (white down, black up)"""
    stock_eval = stockfish.get_evaluation()
    if stock_eval["type"] == "cp":
        score = stock_eval["value"] / 100.0
    else:
        score = 10 if stock_eval["value"] > 0 else -10

    score = max(-5, min(5, score))
    white_ratio = (score + 5) / 10

    bar_rect = pygame.Rect(HEIGHT, 0, EVAL_BAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLACK_BAR, bar_rect)
    pygame.draw.rect(screen, WHITE_BAR, (HEIGHT, (1 - white_ratio) * HEIGHT, EVAL_BAR_WIDTH, white_ratio * HEIGHT))
    pygame.draw.line(screen, GREEN, (HEIGHT, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)


def draw_status():
    """Show game state messages"""
    if board.is_checkmate():
        msg = "Checkmate! You Lost!" if board.turn else "Checkmate! You Win!"
    elif board.is_stalemate():
        msg = "Draw - Stalemate!"
    elif board.is_check():
        msg = "Check!"
    else:
        msg = ""

    if msg:
        text = font.render(msg, True, TEXT_COLOR)
        rect = text.get_rect(center=(HEIGHT // 2, HEIGHT // 2))
        pygame.draw.rect(screen, (255, 255, 200), rect.inflate(20, 10))
        screen.blit(text, rect)


def get_square_under_mouse(pos):
    """Get chess square from mouse click"""
    x, y = pos
    if x > HEIGHT:
        return None
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)


# --- Start Menu ---
start_menu()

# --- Game Loop ---
running = True
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_under_mouse(event.pos)
            if square is None:
                continue

            piece = board.piece_at(square)

            # Select
            if selected_square is None:
                if piece and piece.color == board.turn:
                    selected_square = square
                    valid_moves = [m.to_square for m in board.legal_moves if m.from_square == square]

            # Move
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    stockfish.set_fen_position(board.fen())

                    highlighted_square = (7 - chess.square_rank(square), chess.square_file(square))
                    highlight_time = time.time()
                    draw_board()
                    pygame.time.wait(700)

                    # AI move
                    ai_move = stockfish.get_best_move()
                    if ai_move:
                        ai_move_obj = chess.Move.from_uci(ai_move)
                        board.push(ai_move_obj)
                        stockfish.set_fen_position(board.fen())

                        to_sq = ai_move_obj.to_square
                        highlighted_square = (7 - chess.square_rank(to_sq), chess.square_file(to_sq))
                        highlight_time = time.time()

                selected_square = None
                valid_moves = []

pygame.quit()
