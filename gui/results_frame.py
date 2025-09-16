import tkinter as tk
from tkinter import ttk

class ResultsFrame:
    """Frame for displaying calculation results"""

    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        ...