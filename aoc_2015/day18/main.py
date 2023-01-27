import numpy as np
from scipy import signal
import arcade
from aoc_util.inputs import parse_input

DAY = 18
YEAR = 2015

ROW_COUNT = 100
COL_COUNT = 100

CELL_WIDTH = 2
CELL_HEIGHT = 2
MARGIN = 0

WINDOW_WIDTH = (CELL_WIDTH+MARGIN)*COL_COUNT+MARGIN
WINDOW_HEIGHT = (CELL_HEIGHT+MARGIN)*ROW_COUNT+MARGIN


class Main(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self._frame = 0

        self.background_color = arcade.color.BLACK

        self.grid = np.zeros((COL_COUNT, ROW_COUNT), dtype=int)

        for y, row in enumerate(parse_input((DAY, YEAR))):
            for x, point in enumerate(row):
                self.grid[ROW_COUNT-1-y][x] = 1 if point == '#' else 0

        self.corners_on()

        self.kernel = np.ones((3, 3), dtype=int)
        self.kernel[1, 1] = 0

        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []

        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for col in range(COL_COUNT):
                x = col * (CELL_WIDTH + MARGIN) + (CELL_WIDTH/2 + MARGIN)
                y = row * (CELL_HEIGHT + MARGIN) + (CELL_HEIGHT/2 + MARGIN)
                sprite = arcade.SpriteSolidColor(
                    CELL_WIDTH, CELL_HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

        self.grid_sprites = np.array(self.grid_sprites)
        self.set_colours()

    def on_draw(self):
        self._frame += 1
        self.clear()

        self.step()
        # self.corners_on()
        self.set_colours()

        self.grid_sprite_list.draw()
        if self._frame == 100:
            print(sum(sum(row) for row in self.grid))

    def step(self):

        on = self.grid == 1
        off = self.grid == 0
        counts = signal.convolve2d(self.grid, self.kernel, mode='same')
        on_lower_condition = counts >= 2
        on_upper_condition = counts <= 3
        off_condition = counts == 3
        self.grid = ((on & on_lower_condition & on_upper_condition)
                     | (off & off_condition)).astype(int)

    def set_colours(self):
        for sprite in self.grid_sprites[self.grid == 1]:
            sprite.color = arcade.color.AIR_FORCE_BLUE
        for sprite in self.grid_sprites[self.grid == 0]:
            sprite.color = arcade.color.WHITE

    def corners_on(self):
        self.grid[0, 0] = 1
        self.grid[0, -1] = 1
        self.grid[-1, 0] = 1
        self.grid[-1, -1] = 1

    # def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
    #     self.step()
    #     self.corners_on()
    #     self.set_colours()


def main():
    window = Main(WINDOW_WIDTH, WINDOW_HEIGHT, 'test')
    arcade.run()


if __name__ == '__main__':
    main()
