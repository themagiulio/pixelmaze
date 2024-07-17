import pyxel

import settings
from level import Level
from player import Player


class App:
    level: Level
    player: Player

    def __init__(self):
        self.level = Level(settings.SIZE)
        self.player = Player(1, 1, self.level)

        pyxel.init(
            settings.SIZE,
            settings.SIZE,
            display_scale=12,
            capture_scale=6,
            title="Pixel Maze",
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.level.update()

    def draw(self):
        pyxel.cls(settings.COL_BACKGROUND)

        if settings.SHOW_LIGHT:
            self.player.draw_light()

        self.level.draw()
        self.player.draw_player()


if __name__ == "__main__":
    App()
