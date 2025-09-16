import numpy as np
from methods.slae_solver import ODESolver

class EulerMethod(ODESolver):
    display_name = "Метод Ейлера"

    def solve(self):
        ...