from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    final_size: int
    _size: int

    def __init__(self, final_size: int):
        self.final_size = final_size
        self._size = int((self.final_size - 1) / 2)

    @abstractmethod
    def carve_maze(self):
        pass
