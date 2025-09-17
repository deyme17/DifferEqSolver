from typing import Callable
from abc import ABC, abstractmethod



class ODEMethodInterface(ABC):
    """Base class for ODE methods"""
    @abstractmethod
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        """
        Perform one integration step.
        Args:
            f: Function f(t, y) returning derivative dy/dt.
            t: Current time.
            y: Current state.
            h: Step size.
        Returns:
            Approximation of y at t+h.
        """
        pass

    def reset(self):
        """Reset method state (for methods that store previous values)"""
        pass


class EulerMethod(ODEMethodInterface):
    """Explicit Euler method"""
    display_name = "Метод Ейлера"
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        return y + h * f(t, y)
    

class RungeKuttaMethod(ODEMethodInterface):
    """Explicit Runge-Kutta method"""
    display_name = "Метод Рунге-Кутта"
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h,   y + h * k3)
        return y + h/6 * (k1 + 2*k2 + 2*k3 + k4)


class AdamsMethod(ODEMethodInterface):
    """Explicit Adams-Bashforth 4th order method"""
    display_name = "Метод Адамса"
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset stored values for new calculation"""
        self.prev_f_values = []
        self.step_count = 0
        self.rk_method = RungeKuttaMethod()
    
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        current_f = f(t, y)
        
        if self.step_count < 3:
            self.prev_f_values.append(current_f)
            self.step_count += 1
            return self.rk_method.step(f, t, y, h)
        
        if len(self.prev_f_values) == 3:
            self.prev_f_values.append(current_f)
        
        y_next = y + (h/24) * (
            55 * self.prev_f_values[3] -
            59 * self.prev_f_values[2] +
            37 * self.prev_f_values[1] -
            9 * self.prev_f_values[0]
        )
        self.prev_f_values[0] = self.prev_f_values[1]
        self.prev_f_values[1] = self.prev_f_values[2] 
        self.prev_f_values[2] = self.prev_f_values[3]
        self.prev_f_values[3] = f(t + h, y_next)
        
        self.step_count += 1
        return y_next