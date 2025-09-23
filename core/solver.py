from typing import Callable, Optional
import sympy as sp
import numpy as np
import time
from . import ODEMethodInterface


class ODESolver:
    """Numerical solver for ordinary differential equations (ODEs)."""
    
    @staticmethod
    def _validate_inputs(y0: float, t0: float, t_end: float, epsilon: float):
        """Validate solver inputs"""
        if not np.isfinite([y0, t0, t_end, epsilon]).all():
            raise ValueError("All parameters must be finite numbers")
        if epsilon <= 0:
            raise ValueError("Epsilon must be positive")
        if t_end <= t0:
            raise ValueError("t_end must be greater than t0")
    
    @staticmethod
    def solve(
        function: Callable[[float, float], float],
        method: type[ODEMethodInterface],
        epsilon: float,
        y0: float,
        t0: float,
        t_end: float,
        max_iter: int = None
    ) -> tuple[np.ndarray, np.ndarray, float]:
        """
        Solve an ODE y' = f(t, y) numerically using the selected method with a fixed step size.
        Args:
            function: Callable f(t, y) representing the ODE.
            epsilon: Desired accuracy (not used in fixed-step method, kept for compatibility).
            method: Numerical method cls for solving differential equations.
            y0: Initial value y(t0).
            t0: Initial time.
            t_end: End time.
            max_iter: Maximum number of steps (optional, defaults to 10000).
        Returns:
            Tuple of arrays (ts, ys, exec_time):
                ts: Array of time points.
                ys: Array of corresponding y values.
                exec_time: Execution time in seconds.
        """
        ODESolver._validate_inputs(y0, t0, t_end, epsilon)
        
        # Default step size
        max_iter = 10000 if max_iter is None else max_iter
        solver_method = method()
        
        start_time = time.time()
        if solver_method.support_adaptive:
            ts, ys = ODESolver._solve_adaptive(
                function, solver_method, epsilon, y0, t0, t_end, max_iter
            )
        else:
            h = (t_end - t0) * 0.01
            ts, ys = ODESolver._solve_fixed_step(
                function, solver_method, h, y0, t0, t_end, max_iter
            )
        exec_time = time.time() - start_time

        return ts, ys, exec_time

    @staticmethod
    def _solve_adaptive(
        function: Callable[[float, float], float],
        method_inst: ODEMethodInterface,
        epsilon: float,
        y0: float,
        t0: float,
        t_end: float,
        max_iter: int
    ) -> tuple[np.ndarray, np.ndarray]:
        ts, ys = [t0], [y0]
        t, y = t0, y0
        h  = (t_end - t0) * 0.01
        h_min = (t_end - t0) * 1e-12

        cnt = 0
        while t < t_end and cnt <= max_iter:
            if t + h > t_end:
                h = t_end - t

            y1 = method_inst.step(function, t, y, h)
            y_half = method_inst.step(function, t, y, h / 2)
            y2 = method_inst.step(function, t + h / 2, y_half, h / 2)
            error = abs(y2 - y1)

            if error < epsilon:
                t += h
                y = y2
                ts.append(t)
                ys.append(y)

                if error < epsilon / 4:
                    h *= 2
            else:
                h /= 2
                if h < h_min:
                    raise RuntimeError("Step size became too small")
                
            cnt += 1

        return np.array(ts), np.array(ys)

    @staticmethod
    def _solve_fixed_step(
        function: Callable[[float, float], float],
        method_inst: ODEMethodInterface,
        h: float,
        y0: float,
        t0: float,
        t_end: float,
        max_iter: int
    ) -> tuple[np.ndarray, np.ndarray]:
        n_steps = min(int((t_end - t0) / h) + 1, max_iter)
        ts = np.linspace(t0, t_end, n_steps)
        ys = np.zeros_like(ts)
        ys[0] = y0

        for i in range(1, n_steps):
            actual_h = ts[i] - ts[i-1]
            y_new = method_inst.step(function, ts[i-1], ys[i-1], actual_h)
            
            if not np.isfinite(y_new) or abs(y_new) > 1e10:
                return ts[:i], ys[:i]
            
            ys[i] = y_new

        return ts, ys
    
    @staticmethod
    def solve_analytical(equation_str: str, initial_condition: tuple[float, float]) -> Optional[tuple[Callable, str]]:
        """
        Solve ODE analytically using SymPy
        Args:
            equation_str: String representation of ODE right side (e.g., "t + y")
            initial_condition: Tuple (t0, y0)
        Returns:
            Callable function y(t) and exact solution (equation) or None if solution not found
        """
        try:
            t = sp.symbols('t')
            y_func = sp.Function('y')
            
            namespace = {'t': t, 'y': y_func(t), 'exp': sp.exp, 'sin': sp.sin, 'cos': sp.cos, 'log': sp.log}
            rhs = sp.sympify(equation_str, locals=namespace)
            ode_eq = sp.Eq(y_func(t).diff(t), rhs)
            solution = sp.dsolve(ode_eq, y_func(t))
            
            t0, y0 = initial_condition
            if hasattr(solution, 'rhs'):
                constants = list(solution.rhs.free_symbols - {t})
                if constants:
                    C = constants[0]
                    const_solutions = sp.solve(solution.rhs.subs(t, t0) - y0, C)
                    if const_solutions:
                        const_value = const_solutions[0]
                        particular_solution = solution.rhs.subs(C, const_value)
                    else:
                        particular_solution = solution.rhs
                else:
                    particular_solution = solution.rhs

                return sp.lambdify(t, particular_solution, 'numpy'), str(particular_solution)
                
        except Exception as e:
            print(f"Analytical solution error: {e}")
            return None