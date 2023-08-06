from arcade import *
from arcade import key

WIDTH = 700
HEIGHT = 730
TITLE = "加密信件"
MOVE = 1


class Letter(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = Sprite("images_letter/信.png")
        self.bg.center_x = WIDTH // 2
        self.bg.center_y = HEIGHT // 2
        self.tool = Sprite("images_letter/密码卡.png")
        self.tool.center_x = self.tool.width // 2
        self.tool.center_y = self.tool.height // 2

    def on_draw(self):
        start_render()
        self.bg.draw()
        self.tool.draw()

    def on_update(self, delta_time: float):
        self.tool.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.UP:
            self.tool.change_y = MOVE
        elif symbol == key.DOWN:
            self.tool.change_y = -MOVE
        elif symbol == key.RIGHT:
            self.tool.change_x = MOVE
        elif symbol == key.LEFT:
            self.tool.change_x = -MOVE

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == key.UP or symbol == key.DOWN:
            self.tool.change_y = 0
        if symbol == key.LEFT or symbol == key.RIGHT:
            self.tool.change_x = 0


if __name__ == '__main__':
    window = Letter(WIDTH, HEIGHT, TITLE)
    run()
