import tkinter as tk
from tkinter import ttk
from typing import Callable



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
        # y0
        ttk.Label(self.frame, text="y₀:").grid(row=0, column=0, sticky="w")
        self.y0_entry = ttk.Entry(self.frame)
        self.y0_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # t0
        ttk.Label(self.frame, text="t₀:").grid(row=1, column=0, sticky="w")
        self.t0_entry = ttk.Entry(self.frame)
        self.t0_entry.grid(row=1, column=1, sticky="ew", padx=5)

        # t_end
        ttk.Label(self.frame, text="t_end:").grid(row=2, column=0, sticky="w")
        self.tend_entry = ttk.Entry(self.frame)
        self.tend_entry.grid(row=2, column=1, sticky="ew", padx=5)

        # epsilon
        ttk.Label(self.frame, text="ε (точність):").grid(row=3, column=0, sticky="w")
        self.eps_entry = ttk.Entry(self.frame)
        self.eps_entry.grid(row=3, column=1, sticky="ew", padx=5)

        # method
        ttk.Label(self.frame, text="Метод:").grid(row=4, column=0, sticky="w")
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(self.frame, textvariable=self.method_var, values=self.method_choices, state="readonly")
        self.method_combo.grid(row=4, column=1, sticky="ew", padx=5)
        if self.method_choices:
            self.method_combo.current(0)

        # calc
        calc_btn = ttk.Button(self.frame, text="Обчислити", command=self.calculate_callback)
        calc_btn.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")

        self.frame.columnconfigure(1, weight=1)

    def get_inputs(self):
        """Returns dict with all input data"""
        return {
            "y0": float(self.y0_entry.get()),
            "t0": float(self.t0_entry.get()),
            "t_end": float(self.tend_entry.get()),
            "epsilon": float(self.eps_entry.get()),
            "method": self.method_var.get()
        }
    
    def get_equation(self):
        ...
