from enum import Enum

import pyxel

import settings
from level import Level


class Direction(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Player:
    x: int
    y: int
    direction: Direction
    level: Level

    def __init__(self, x: int, y: int, level: Level):
        self.level = level
        self.x, self.y = self.level.randomize_start()

    def _move(self):
        match self.direction:
            case Direction.UP:
                if self.level.is_wall(self.x, self.y - 1):
                    return
                self.y = (self.y - 1) % pyxel.width
            case Direction.RIGHT:
                if self.level.is_wall(self.x + 1, self.y):
                    return

                self.x = (self.x + 1) % pyxel.width
            case Direction.DOWN:
                if self.level.is_wall(self.x, self.y + 1):
                    return

                self.y = (self.y + 1) % pyxel.width
            case Direction.LEFT:
                if self.level.is_wall(self.x - 1, self.y):
                    return

                self.x = (self.x - 1) % pyxel.width
            case _:
                return

        if self.level.is_finish(self.x, self.y):
            self.x, self.y = self.level.randomize_start()
            self.level.complete()

    def _input(self):
        if pyxel.btn(settings.KEY_CONTROL_UP):
            self.direction = Direction.UP
        elif pyxel.btn(settings.KEY_CONTROL_RIGHT):
            self.direction = Direction.RIGHT
        elif pyxel.btn(settings.KEY_CONTROL_DOWN):
            self.direction = Direction.DOWN
        elif pyxel.btn(settings.KEY_CONTROL_LEFT):
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.NONE

    def update(self):
        self._input()
        self._move()

    def draw_player(self):
        # Draw player
        pyxel.pset(self.x, self.y, settings.COL_PLAYER)

    def draw_light(self):
        # Draw light
        pyxel.rect(self.x - 3, self.y - 3, 7, 7, settings.COL_LIGHT_1)
        pyxel.rect(self.x - 2, self.y - 2, 5, 5, settings.COL_LIGHT_2)
        pyxel.rect(self.x - 1, self.y - 1, 3, 3, settings.COL_LIGHT_3)
