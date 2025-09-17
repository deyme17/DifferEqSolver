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
        t_end: float,
        h: float = None,
        max_iter: int = 10
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
            h: ste
        Returns:
            Tuple of arrays (ts, ys):
                ts: Array of time points.
                ys: Array of corresponding y values.
        """
        h = (t_end - t0) / 10 if not h else h
        
        for _ in range(max_iter):
            method_inst1: ODEMethodInterface = method()
            method_inst1.reset()
            ts1, ys1 = ODESolver._solve_fixed_step(function, method_inst1, h, y0, t0, t_end)
            
            method_inst2: ODEMethodInterface = method()
            method_inst2.reset()
            ts2, ys2 = ODESolver._solve_fixed_step(function, method_inst2, h/2, y0, t0, t_end)
            
            if len(ts1) > 1 and len(ts2) > 1:
                ys2_interp = np.interp(ts1, ts2, ys2)
                max_diff = np.max(np.abs(ys2_interp - ys1))

                if max_diff < epsilon:
                    return ts2, ys2
            
            h = h / 2
            
            if h < epsilon * 1e-6:
                break
        
        return ts2, ys2
    
    @staticmethod
    def _solve_fixed_step(
        function: Callable[[float, float], float],
        method_inst: ODEMethodInterface,
        h: float,
        y0: float,
        t0: float,
        t_end: float
    ) -> tuple[np.ndarray, np.ndarray]:
        n_steps = int((t_end - t0) / h) + 1
        ts = np.linspace(t0, t_end, n_steps)
        ys = np.zeros_like(ts)
        ys[0] = y0

        for i in range(1, n_steps):
            actual_h = ts[i] - ts[i-1]
            ys[i] = method_inst.step(function, ts[i-1], ys[i-1], actual_h)

        return ts, ys