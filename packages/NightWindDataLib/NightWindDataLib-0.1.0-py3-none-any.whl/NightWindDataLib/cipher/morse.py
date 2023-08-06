import json
from arcade import *
from arcade import color

with open("images_morse/morse.json", "r") as f:
    morse = json.load(f)

WIDTH = 300
HEIGHT = 200
TITLE = "发报机"


class Morse(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        set_background_color(color.WHITE)
        self.letter = " "
        self.morse = " "
        self.di = load_sound("images_morse/di.wav")
        self.do = load_sound("images_morse/do.wav")

    def on_draw(self):
        start_render()
        x, y = WIDTH / 2, HEIGHT / 2

        draw_text(self.letter, x, y + 15, color.BLUE,
                  font_size=30, font_name=("SimHei", "PingFang"),
                  anchor_x="center", anchor_y="center")
        draw_text(self.morse, x, y - 15, color.RED,
                  font_size=30, font_name=("SimHei", "PingFang"),
                  anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, modifiers: int):
        try:
            code = chr(symbol).upper()
            if code in morse.keys():
                self.letter = code
                self.morse = morse[code]

                for sound in self.morse:
                    if sound == ".":
                        play_sound(self.di)
                        pause(0.1)
                    elif sound == "-":
                        play_sound(self.do)
                        pause(0.3)

        except OverflowError:
            pass


if __name__ == '__main__':
    game = Morse(WIDTH, HEIGHT, TITLE)
    run()
