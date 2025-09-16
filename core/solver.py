from typing import Callable
import numpy as np
from . import ODEMethodInterface



class ODESolver:
    """Numerical solver for ordinary differential equations (ODEs)."""
    @staticmethod
    def solve(
        function: Callable[[float, float], float],
        method: ODEMethodInterface,
        epsilon: float,
        y0: float,
        t0: float,
        t_end: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Solve an ODE y' = f(t, y) numerically using the selected method.
        Args:
            function: Callable f(t, y) representing the ODE.
            epsilon: Desired accuracy of the solution.
            method: Numerical method for solving differencial equations.
            y0: Initial value y(t0).
            t0: Initial time.
            t_end: End time.
        Returns:
            Tuple of arrays (ts, ys):
                ts: Array of time points.
                ys: Array of corresponding y values.
        """
        method_inst: ODEMethodInterface = method()
        n_steps = int((t_end - t0) / epsilon) + 1
        ts = np.linspace(t0, t_end, n_steps)
        ys = np.zeros_like(ts)
        ys[0] = y0

        for i in range(1, n_steps):
            h = ts[i] - ts[i-1]
            ys[i] = method_inst.step(function, ts[i-1], ys[i-1], h)

        return ts, ys