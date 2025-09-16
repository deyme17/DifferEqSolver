import tkinter as tk
from tkinter import Tk, ttk, messagebox
import time

from . import InputFrame, ResultsFrame
from core import ODESolver, GraphPlotter
from utils.method_register import ODEMethodRegistry



class ODESolverApp:
    """Main application class"""
    def __init__(self, 
                 root: Tk, 
                 input_frame_cls: InputFrame, 
                 result_frame_cls: ResultsFrame,
                 solver: ODESolver, 
                 plotter: GraphPlotter
                 ):
        """
        Initialize the main ODE solver application.
        Args:
            root: The main Tkinter root window.
            input_frame: Frame handling user input for the ODE problem.
            result_frame: Frame responsible for displaying numerical results and performance metrics.
            solver: Numerical solver instance used for integrating differential equations.
            plotter: Class responsible for rendering solution plots.
        """
        self.root = root
        self.solver = solver
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

        self.input_frame = input_frame_cls(self.tab1, self.calculate, ODEMethodRegistry.get_method_choices())
        self.results_frame = result_frame_cls(self.tab2, plotter)

    def _configure_style(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 9))
        style.configure('TButton', padding=5, font=('Helvetica', 9))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))

    def calculate(self):
        try:
            equation = self.input_frame.get_equation()
            params = self.input_frame.get_inputs()
            y0, t0, t_end, eps, method, real_answer = params.values()

            # start timer
            start = time.time()
            ts, ys = self.solver.solve(
                epsilon=eps,
                method=method,
                equation=equation,
                y0=y0, t0=t0, t_end=t_end
            )
            exec_time = time.time() - start

            # update results
            self.results_frame.update_results(ts, ys, exec_time, real_answer)
            self.tab_control.select(self.tab2)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))