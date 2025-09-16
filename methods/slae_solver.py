from abc import ABC, abstractmethod

class ODESolver(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def solve(self):
        pass