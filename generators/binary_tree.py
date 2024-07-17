from enum import Enum
from random import randint

import numpy as np

from generators.generator import MazeGenerator


class BinaryTreeGenerator(MazeGenerator):
    _tosses: np.ndarray

    class Bias(Enum):
        NORTH_EAST = 0
        NORTH_WEST = 1
        SOUTH_EAST = 2
        SOUTH_WEST = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bias = self._bias()

        self._make_tosses()

    def _bias(self):
        return BinaryTreeGenerator.Bias(randint(0, 3))

    def _make_tosses(self):
        self._tosses = np.random.binomial(1, 0.5, size=(self._size, self._size))

        match self.bias:
            case BinaryTreeGenerator.Bias.NORTH_EAST:
                self._tosses[:, -1] = 1
                self._tosses[0] = 0
            case BinaryTreeGenerator.Bias.NORTH_WEST:
                self._tosses[:, 0] = 1
                self._tosses[0] = 0
            case BinaryTreeGenerator.Bias.SOUTH_EAST:
                self._tosses[:, -1] = 1
                self._tosses[-1] = 0
            case BinaryTreeGenerator.Bias.SOUTH_WEST:
                self._tosses[:, 0] = 1
                self._tosses[-1] = 0

    def carve_maze(self):
        output_grid = np.ones((self.final_size, self.final_size), dtype=int)

        for i in range(self._size):
            w = i * 2 + 1
            for j in range(self._size):
                k = j * 2 + 1
                toss = self._tosses[i, j]
                output_grid[w, k] = 0

                match self.bias:
                    case (
                        BinaryTreeGenerator.Bias.NORTH_EAST
                        | BinaryTreeGenerator.Bias.SOUTH_EAST
                    ):
                        if toss == 0 and k + 2 < self._size * 2 + 1:
                            output_grid[w, k + 1] = 0
                            output_grid[w, k + 2] = 0
                    case (
                        BinaryTreeGenerator.Bias.NORTH_WEST
                        | BinaryTreeGenerator.Bias.SOUTH_WEST
                    ):
                        if toss == 0 and k - 2 > 0:
                            output_grid[w, k - 1] = 0
                            output_grid[w, k - 2] = 0

                match self.bias:
                    case (
                        BinaryTreeGenerator.Bias.NORTH_EAST
                        | BinaryTreeGenerator.Bias.NORTH_WEST
                    ):
                        if toss == 1 and w - 2 > 0:
                            output_grid[w - 1, k] = 0
                            output_grid[w - 2, k] = 0
                    case (
                        BinaryTreeGenerator.Bias.SOUTH_EAST
                        | BinaryTreeGenerator.Bias.SOUTH_WEST
                    ):
                        if toss == 1 and w + 2 < self._size * 2 + 1:
                            output_grid[w + 1, k] = 0
                            output_grid[w + 2, k] = 0

        return output_grid.reshape(-1)
