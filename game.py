import pygame
import chess
from config import *

class ChessGame:

    def __init__(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Python Chess")

        self.board = chess.Board()

        self.selected_square = None
        self.legal_moves = []

        self.last_move = None

        #DRAG VARIABLES
        self.dragging = False
        self.dragged_piece = None
        self.dragged_from = None
        self.drag_pos = (0,0)

        self.load_images()

    # -------------------------
    # LOAD IMAGES
    # -------------------------
    def load_images(self):

        self.pieces = {}

        names = ["wp","bp","wr","br","wn","bn","wb","bb","wq","bq","wk","bk"]

        for name in names:
            img = pygame.image.load(f"assets/pieces/{name}.png")
            img = pygame.transform.scale(img,(SQUARE_SIZE,SQUARE_SIZE))
            self.pieces[name] = img

    # -------------------------
    # DRAW BOARD
    # -------------------------
    def draw_board(self):

        for row in range(ROWS):
            for col in range(COLS):

                color = LIGHT if (row+col)%2==0 else DARK

                pygame.draw.rect(
                    self.screen,
                    color,
                    (col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
                )

    # -------------------------
    # LAST MOVE HIGHLIGHT
    # -------------------------
    def draw_last_move(self):

        if self.last_move is None:
            return

        for square in [self.last_move.from_square,self.last_move.to_square]:

            row = 7 - (square // 8)
            col = square % 8

            pygame.draw.rect(
                self.screen,
                LAST_MOVE,
                (col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),
                4
            )

    # -------------------------
    # CHECK HIGHLIGHT
    # -------------------------
    def draw_check(self):

        if not self.board.is_check():
            return

        king_square = self.board.king(self.board.turn)

        row = 7 - (king_square // 8)
        col = king_square % 8

        pygame.draw.rect(
            self.screen,
            CHECK_COLOR,
            (col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),
            5
        )

    # -------------------------
    # SELECTED PIECE
    # -------------------------
    def highlight_selected(self):

        if self.selected_square is None:
            return

        row = 7 - (self.selected_square // 8)
        col = self.selected_square % 8

        pygame.draw.rect(
            self.screen,
            SELECT_COLOR,
            (col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),
            4
        )

    # -------------------------
    # LEGAL MOVES
    # -------------------------
    def draw_moves(self):

        for move in self.legal_moves:

            square = move.to_square

            row = 7 - (square // 8)
            col = square % 8

            center = (
                col*SQUARE_SIZE + SQUARE_SIZE//2,
                row*SQUARE_SIZE + SQUARE_SIZE//2
            )

            pygame.draw.circle(
                self.screen,
                MOVE_COLOR,
                center,
                10
            )

    # -------------------------
    # DRAW PIECES
    # -------------------------
    def draw_pieces(self):

        for square in chess.SQUARES:
            if self.dragging and square == self.dragged_from:
                continue
            piece = self.board.piece_at(square)

            if piece is None:
                continue

            symbol = piece.symbol()

            key = "w"+symbol.lower() if symbol.isupper() else "b"+symbol

            row = 7 - (square // 8)
            col = square % 8

            x = col*SQUARE_SIZE
            y = row*SQUARE_SIZE

            self.screen.blit(self.pieces[key],(x,y))
    #DRAW DRAGGED PIECES
    def draw_dragged_piece(self):

        if not self.dragging:
            return

        symbol = self.dragged_piece.symbol()

        key = "w"+symbol.lower() if symbol.isupper() else "b"+symbol

        x = self.drag_pos[0] - SQUARE_SIZE//2
        y = self.drag_pos[1] - SQUARE_SIZE//2

        self.screen.blit(self.pieces[key],(x,y))

    # -------------------------
    # MOUSE → SQUARE
    # -------------------------
    def mouse_to_square(self,pos):

        x,y = pos

        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        row = 7 - row

        return chess.square(col,row)

    # -------------------------
    # HANDLE CLICK
    # -------------------------
    def handle_click(self,pos):

        square = self.mouse_to_square(pos)

        if self.selected_square is None:

            piece = self.board.piece_at(square)

            if piece and piece.color == self.board.turn:

                self.selected_square = square

                self.legal_moves = [
                    move for move in self.board.legal_moves
                    if move.from_square == square
                ]

        else:

            move = chess.Move(self.selected_square,square)

            if chess.square_rank(square) in [0,7]:
                move = chess.Move(self.selected_square,square,promotion=chess.QUEEN)

            if move in self.board.legal_moves:

                self.board.push(move)
                self.last_move = move

            self.selected_square = None
            self.legal_moves = []

    # -------------------------
    # RESET GAME
    # -------------------------
    def reset(self):

        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.last_move = None

    # -------------------------
    # GAME LOOP
    # -------------------------
    def run(self):

        running = True

        while running:

            for event in pygame.event.get():

                # CLOSE WINDOW
                if event.type == pygame.QUIT:
                    running = False

                #GAME RESET LOGIC
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                #MOUSE PRESS LOGIC
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()
                    square = self.mouse_to_square(pos)

                    piece = self.board.piece_at(square)

                    if piece and piece.color == self.board.turn:
                        self.dragging = True
                        self.dragged_piece = piece
                        self.dragged_from = square
                        self.drag_pos = pos
        
        #MOUSE MOVE LOGIC
                if event.type == pygame.MOUSEMOTION and self.dragging:

                    self.drag_pos = pygame.mouse.get_pos()
        
        #MOUSE RELEASE LOGIC
                if event.type == pygame.MOUSEBUTTONUP and self.dragging:

                    pos = pygame.mouse.get_pos()
                    target_square = self.mouse_to_square(pos)

                    for move in self.board.legal_moves:

                        if move.from_square == self.dragged_from and move.to_square == target_square:

                            self.board.push(move)
                            self.last_move = move
                            break

                    self.dragging = False
                    self.dragged_piece = None
                    self.dragged_from = None

            self.draw_board()
            self.draw_last_move()
            self.draw_check()
            self.highlight_selected()
            self.draw_moves()
            self.draw_pieces()
            self.draw_dragged_piece()
            pygame.display.update()

        pygame.quit()
