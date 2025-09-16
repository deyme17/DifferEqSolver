import tkinter as tk
from tkinter import ttk
import numpy as np

class InputFrame:
    """Frame for input data"""
    def __init__(self, parent, calculate_callback, method_choices):
        self.parent = parent
        self.calculate_callback = calculate_callback
        self.method_choices = method_choices

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        ...