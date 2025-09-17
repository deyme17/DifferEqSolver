import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from sympy import sympify, symbols, lambdify
from sympy.core.sympify import SympifyError



class InputFrame:
    """Frame for entering ODE parameters"""
    def __init__(self, parent, calculate_callback: Callable, method_choices: list[tuple[str, str]]):
        """
        Initialize the input frame for ODE parameters.
        Args:
            parent: Parent Tkinter widget where this frame is placed.
            calculate_callback: Function to be called when the user triggers calculation.
            method_choices: List of available ODE solving methods as (key, label) tuples.
        """
        self.parent = parent
        self.calculate_callback = calculate_callback
        self.method_choices = method_choices

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self._create_widgets()

    def _create_widgets(self):
        row = 0

        # equation
        ttk.Label(self.frame, text="y' = ").grid(row=row, column=0, sticky="w")
        self.eq_entry = ttk.Entry(self.frame)
        self.eq_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # y0
        ttk.Label(self.frame, text="y₀:").grid(row=row, column=0, sticky="w")
        self.y0_entry = ttk.Entry(self.frame)
        self.y0_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # t0
        ttk.Label(self.frame, text="t₀:").grid(row=row, column=0, sticky="w")
        self.t0_entry = ttk.Entry(self.frame)
        self.t0_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # t_end
        ttk.Label(self.frame, text="t_end:").grid(row=row, column=0, sticky="w")
        self.tend_entry = ttk.Entry(self.frame)
        self.tend_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # epsilon
        ttk.Label(self.frame, text="ε (точність):").grid(row=row, column=0, sticky="w")
        self.eps_entry = ttk.Entry(self.frame)
        self.eps_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # step h
        ttk.Label(self.frame, text="Крок h (opt.):").grid(row=row, column=0, sticky="w")
        self.h_entry = ttk.Entry(self.frame)
        self.h_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # max steps
        ttk.Label(self.frame, text="Макс. к-сть кроків (opt.):").grid(row=row, column=0, sticky="w")
        self.max_steps_entry = ttk.Entry(self.frame)
        self.max_steps_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # method
        ttk.Label(self.frame, text="Метод:").grid(row=row, column=0, sticky="w")
        self.method_var = tk.StringVar()

        # split keys and labels
        self.method_keys = [key for key, label in self.method_choices]
        method_labels = [label for key, label in self.method_choices]

        self.method_combo = ttk.Combobox(
            self.frame, textvariable=self.method_var, values=method_labels, state="readonly"
        )
        self.method_combo.grid(row=row, column=1, sticky="ew", padx=5)
        if method_labels:
            self.method_combo.current(0)
        row += 1

        # calc
        calc_btn = ttk.Button(self.frame, text="Обчислити", command=self.calculate_callback)
        calc_btn.grid(row=row, column=0, columnspan=2, pady=15, sticky="ew")

        # default values
        self.y0_entry.insert(0, "0")
        self.t0_entry.insert(0, "0.0")
        self.tend_entry.insert(0, "2.0")
        self.eps_entry.insert(0, "0.001")
        self.h_entry.insert(0, "0.1")

        self.frame.columnconfigure(1, weight=1)

    def get_inputs(self):
        """Returns dict with all input data with improved validation"""
        method_idx = self.method_combo.current()
        try:
            y0 = float(self.y0_entry.get())
            t0 = float(self.t0_entry.get())
            t_end = float(self.tend_entry.get())
            epsilon = float(self.eps_entry.get())

            h_str = self.h_entry.get().strip()
            h = float(h_str) if h_str else None
            
            max_steps_str = self.max_steps_entry.get().strip()
            max_steps = int(max_steps_str) if max_steps_str else None
            
            self._validate_inputs(t_end, t0, epsilon, y0, h, max_steps)
            return {
                "y0": y0,
                "t0": t0,
                "t_end": t_end,
                "h": h,
                "epsilon": epsilon,
                "max_steps": max_steps,
                "method": self.method_keys[method_idx],
            }
        except ValueError as e:
            messagebox.showerror("Помилка", f"Некоректне числове значення: {e}")
            raise
    
    @staticmethod
    def _validate_inputs(t_end: float, t0: float, epsilon: float, y0: float, h: float, max_steps: int) -> None:
        """Validates inputs and raise ValueError if input is not valid"""
        if t_end <= t0:
            raise ValueError("t_end має бути більше за t0")
        if epsilon <= 0:
            raise ValueError("Точність (epsilon) має бути додатним числом")
        if abs(y0) > 1e10:
            raise ValueError("Початкове значення y0 занадто велике")
        if h and (h <= 0 or h > (t_end - t0)):
            raise ValueError("Невалідний крок h")
        if max_steps and max_steps <= 0:
            raise ValueError("Максимальна кількість кроків має бути додатною")

    def get_function(self) -> Callable[[float, float], float]:
        """
        Parse the user input equation string into a callable function f(t, y).
        Returns:
            allable f(t, y) representing the ODE y' = f(t, y).
        """
        expr_str = self.eq_entry.get()
        t, y = symbols("t y")
        try:
            expr = sympify(expr_str)
            func = lambdify((t, y), expr, "numpy")
            return func
        except SympifyError:
            messagebox.showerror("Помилка", f"Неправильне рівняння: {expr_str}")
            raise ValueError(f"Invalid equation: {expr_str}")
        
    def get_equation(self) -> str:
        """
        Returns an equation that user inputted.
        """
        return self.eq_entry.get()