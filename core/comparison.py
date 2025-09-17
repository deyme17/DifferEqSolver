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
        methods: list[ODEMethodInterface]
    ) -> dict[str, dict]:
        """
        Compare multiple ODE solving methods
        Returns: dictionary with method names as keys and results as values
        """
        results = {}
        
        for method_class in methods:
            method_name: ODEMethodInterface = method_class.display_name
            
            # Solve with current method
            ts, ys, exec_time = ODESolver.solve(
                function, method_class, epsilon, y0, t0, t_end
            )
            
            # Count integration points
            num_points = len(ts)
            
            results[method_name] = {
                'execution_time': exec_time,
                'num_points': num_points,
                'solution': (ts, ys)
            }
        
        return results