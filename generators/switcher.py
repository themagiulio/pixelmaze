from enum import Enum

import pyxel

import settings
from generators.binary_tree import BinaryTreeGenerator


class GeneratorSwitcher:
    _generator: int = 0

    class Generator(Enum):
        BINARY_TREE = 0

    def __init__(self, default_generator: Generator = Generator.BINARY_TREE):
        self._generator = default_generator.value

    def _input(self):
        if pyxel.btnp(settings.KEY_SWITCH_GENERATOR):
            if self._generator < len(GeneratorSwitcher.Generator) - 1:
                self._generator += 1
            else:
                self._generator = 0

            print(f"Switched maze generator to {self.generator}.")

    def update(self):
        self._input()

    @property
    def generator(self) -> Generator:
        return GeneratorSwitcher.Generator(self._generator)

    @property
    def generator_class(self):
        match self.generator:
            case GeneratorSwitcher.Generator.BINARY_TREE:
                return BinaryTreeGenerator
