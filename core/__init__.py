from .methods import ODEMethodInterface, EulerMethod, RungeKuttaMethod, AdamsMethod
ode_solve_methods: list[ODEMethodInterface] = [EulerMethod, RungeKuttaMethod, AdamsMethod]

from .solver import ODESolver
from .plotter import GraphPlotter
from .comparison import MethodComparator