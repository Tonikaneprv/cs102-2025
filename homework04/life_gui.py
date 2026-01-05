import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode((life.cols * cell_size, life.rows * cell_size))

    def draw_lines(self) -> None:
        width, height = self.screen.get_size()
        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[i][j] == 1 else pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False
                print("Игра завершена!")

        pygame.quit()
