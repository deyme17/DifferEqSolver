import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from gui.input_frame import InputFrame
from gui.results_frame import ResultsFrame
from utils.method_register import ODEMethodRegistry

class ODESolverApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Розв'язання Диференціальних рівнянь")
        self.root.geometry("900x600")

        self._configure_style()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # tabs
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Вхідні дані')
        self.tab_control.add(self.tab2, text='Результати')

        for tab in (self.tab1, self.tab2):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

        self.input_frame = InputFrame(self.tab1, self.calculate, ODEMethodRegistry.get_method_choices())
        self.results_frame = ResultsFrame(self.tab2)

    def _configure_style(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 9))
        style.configure('TButton', padding=5, font=('Helvetica', 9))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))

    def calculate(self):
        ...