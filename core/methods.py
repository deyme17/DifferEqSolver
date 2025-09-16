from typing import Callable
from abc import ABC, abstractmethod

class ODESolver(ABC):
    """Base class for ODE solvers"""
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

class EulerMethod(ODESolver):
    """Explicit Euler method"""
    display_name = "Метод Ейлера"
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        return y + h * f(t, y)
    
class RungeKuttaMethod(ODESolver):
    """Explicit Runge-Kutta method"""
    display_name = "Метод Рунге-Кутта"
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h,   y + h * k3)
        return y + h/6 * (k1 + 2*k2 + 2*k3 + k4)

class AdamsMethod(ODESolver):
    """Explicit Adams method"""
    display_name = "Метод Адамса"
    
    def __init__(self):
        self.prev_f = None
    
    def step(self, f: Callable, t: float, y: float, h: float) -> float:
        if self.prev_f is None:
            self.prev_f = f(t, y)
            return y + h * self.prev_f
        else:
            f_curr = f(t, y)
            y_next = y + h/2 * (3*f_curr - self.prev_f)
            self.prev_f = f_curr
            return y_next