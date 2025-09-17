from typing import Callable, Optional
import sympy as sp
import numpy as np
import time
from methods import ODEMethodInterface


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
    ) -> tuple[np.ndarray, np.ndarray, float]:
        """
        Solve an ODE y' = f(t, y) numerically using the selected method.
        Args:
            function: Callable f(t, y) representing the ODE.
            epsilon: Desired accuracy of the solution.
            method: Numerical method for solving differencial equations.
            y0: Initial value y(t0).
            t0: Initial time.
            t_end: End time.
            h: step size
        Returns:
            Tuple of arrays (ts, ys, exec_time):
                ts: Array of time points.
                ys: Array of corresponding y values.
                exec_time: Execution time in seconds.
        """
        h = (t_end - t0) / 10 if not h else h
        
        start_time = time.time()
        
        for _ in range(max_iter):
            method_inst1 = method()
            method_inst1.reset()
            ts1, ys1 = ODESolver._solve_fixed_step(function, method_inst1, h, y0, t0, t_end)
            
            method_inst2 = method()
            method_inst2.reset()
            ts2, ys2 = ODESolver._solve_fixed_step(function, method_inst2, h/2, y0, t0, t_end)
            
            if len(ts1) > 1 and len(ts2) > 1:
                ys2_interp = np.interp(ts1, ts2, ys2)
                max_diff = np.max(np.abs(ys2_interp - ys1))

                if max_diff < epsilon:
                    exec_time = time.time() - start_time
                    return ts2, ys2, exec_time
            
            h = h / 2
            
            if h < epsilon * 1e-6:
                break
        
        exec_time = time.time() - start_time
        return ts2, ys2, exec_time
    
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
    
    @staticmethod
    def solve_analytical(equation_str: str, initial_condition: tuple[float, float]) -> Optional[Callable]:
        """
        Solve ODE analytically using SymPy
        Args:
            equation_str: String representation of ODE right side (e.g., "t + y")
            initial_condition: Tuple (t0, y0)
        Returns:
            Callable function y(t) or None if solution not found
        """
        try:
            t = sp.symbols('t')
            y = sp.Function('y')(t)
            
            # parse & solve
            rhs = sp.sympify(equation_str)
            ode_eq = sp.Eq(y.diff(t), rhs)
            solution = sp.dsolve(ode_eq, y)
            
            # ini cond
            t0, y0 = initial_condition
            if hasattr(solution, 'rhs'):
                # fimf cnst
                constants = list(solution.rhs.free_symbols - {t})
                if constants:
                    C = constants[0]
                    const_value = sp.solve(solution.rhs.subs(t, t0) - y0, C)[0]
                    particular_solution = solution.rhs.subs(C, const_value)
                else:
                    particular_solution = solution.rhs
                
                return sp.lambdify(t, particular_solution, 'numpy')
                
        except Exception as e:
            print(f"Analytical solution error: {e}")
            return None