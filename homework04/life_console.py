import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                char = "█" if self.life.curr_generation[i][j] == 1 else " "
                screen.addch(i + 1, j + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)  # Скрыть курсор

        try:
            while True:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                self.life.step()

                if self.life.is_max_generations_exceeded or not self.life.is_changing:
                    break

                curses.napms(100)
        finally:
            curses.endwin()
