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

        # step h
        ttk.Label(self.frame, text="Крок h (opt.):").grid(row=row, column=0, sticky="w")
        self.h_entry = ttk.Entry(self.frame)
        self.h_entry.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # epsilon
        ttk.Label(self.frame, text="ε (точність):").grid(row=row, column=0, sticky="w")
        self.eps_entry = ttk.Entry(self.frame)
        self.eps_entry.grid(row=row, column=1, sticky="ew", padx=5)
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

        self.frame.columnconfigure(1, weight=1)

    def get_inputs(self):
        """Returns dict with all input data"""
        method_idx = self.method_combo.current()
        try:
            return {
                "y0": float(self.y0_entry.get()),
                "t0": float(self.t0_entry.get()),
                "t_end": float(self.tend_entry.get()),
                "h": float(self.h_entry.get()),
                "epsilon": float(self.eps_entry.get()),
                "max_steps": int(self.max_steps_entry.get()) if self.max_steps_entry.get().strip() else None,
                "method": self.method_keys[method_idx],
            }
        except ValueError as e:
            messagebox.showerror("Помилка", f"Некоректне числове значення: {e}")
            raise

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