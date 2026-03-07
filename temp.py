import pygame
from config import *

class ChessGame:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Python Chess")

    def draw_board(self):

        for row in range(ROWS):
            for col in range(COLS):

                if (row + col) % 2 == 0:
                    color = LIGHT
                else:
                    color = DARK

                pygame.draw.rect(
                    self.screen,
                    color,
                    (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def run(self):

        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_board()

            pygame.display.update()

        pygame.quit()
