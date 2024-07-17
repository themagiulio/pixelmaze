from enum import Enum
from random import randint

from generators import BinaryTreeGenerator, GeneratorSwitcher
import pyxel

import settings


class Level:
    maze: list[int] = []
    completed_levels: int = 0
    generator_switcher: GeneratorSwitcher = GeneratorSwitcher()
    finish: list[int]
    size: int

    class Block(Enum):
        NONE = 0
        WALL = 1
        FINISH = 2

    def __init__(self, size: int = settings.SIZE):
        self.size = size
        self._generate_maze()

    def _blank_maze(self) -> list[int]:
        maze = []

        maze += [1 for _ in range(self.size)]
        maze += ([1] + [0 for _ in range(self.size - 2)] + [1]) * (self.size - 2)
        maze += [1 for _ in range(self.size)]

        return maze

    def _block(self, block_type: int) -> Block:
        match block_type:
            case 1:
                return Level.Block.WALL
            case 2:
                return Level.Block.FINISH
            case _:
                return Level.Block.NONE

    def _block_at(self, x: int, y: int) -> Block:
        block_type = self.maze[x + self.size * y]
        return self._block(block_type)

    def _block_at_index(self, index: int) -> Block:
        block_type = self.maze[index]
        return self._block(block_type)

    def _generate_maze(self):
        self.maze = self._blank_maze()
        generator = self.generator_switcher.generator_class(self.size)

        self.maze = generator.carve_maze()
        self._randomize_finish()

    def _randomize(self, can_wall: bool = False):
        x, y = randint(1, self.size - 1), randint(1, self.size - 1)

        if self.is_wall(x, y) and not can_wall:
            return self._randomize()

        return x, y

    def _randomize_finish(self):
        x, y = self._randomize()
        self.maze[x + self.size * y] = 2

    def complete(self):
        self.completed_levels += 1
        self._generate_maze()

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                block = self._block_at_index(self.size * j + i)
                # print(self.w * i + j, block_type)
                match block:
                    case Level.Block.WALL:
                        pyxel.pset(
                            i,
                            j,
                            settings.COL_WALL
                            if settings.SHOW_WALL
                            else settings.COL_BACKGROUND,
                        )
                    case Level.Block.FINISH:
                        pyxel.pset(i, j, settings.COL_FINISH)
                    case _:
                        pass
                        # pyxel.pset(i, j, 3)
        # pyxel.quit()

    def is_wall(self, x: int, y: int) -> bool:
        block = self._block_at(x, y)
        return block == Level.Block.WALL

    def is_finish(self, x: int, y: int) -> bool:
        block = self._block_at(x, y)
        return block == Level.Block.FINISH

    def randomize_start(self):
        return self._randomize()

    def update(self):
        self.generator_switcher.update()
