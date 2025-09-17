from typing import Callable
from . import ODEMethodInterface, ODESolver



class MethodComparator:
    """Compare different ODE solving methods"""
    @staticmethod
    def compare_methods(
        function: Callable,
        epsilon: float,
        y0: float,
        t0: float,
        t_end: float,
        methods: list[ODEMethodInterface],
        h: float = None,
        max_iter: int = None
    ) -> dict[str, dict]:
        """
        Compare multiple ODE solving methods
        Returns: dictionary with method names as keys and results as values
        """
        results = {}
        
        for method_class in methods:
            method_name = method_class.display_name
            
            ts, ys, exec_time = ODESolver.solve(
                function=function,
                method=method_class,
                epsilon=epsilon,
                y0=y0, t0=t0, t_end=t_end,
                h=h, max_iter=max_iter
            )
            num_points = len(ts)
            
            results[method_name] = {
                'execution_time': exec_time,
                'num_points': num_points,
                'solution': (ts, ys)
            }
        
        return results