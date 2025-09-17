import tkinter as tk
from tkinter import Tk, ttk, messagebox

from .input_frame import InputFrame
from .results_frame import ResultsFrame
from .comparison_frame import ComparisonFrame

from core import ODESolver, GraphPlotter, MethodComparator
from utils.method_register import ODEMethodRegistry



class ODESolverApp:
    """Main application class"""
    def __init__(self, 
                 root: Tk, 
                 solver: ODESolver, 
                 comparator: MethodComparator,
                 register: ODEMethodRegistry,
                 input_frame_cls: InputFrame, 
                 result_frame_cls: ResultsFrame,
                 comparison_frame_cls: ComparisonFrame,
                 plotter_cls: GraphPlotter
                 ):
        """
        Initialize the main ODE solver application.
        Args:
            root: The main Tkinter root window.
            solver: Numerical solver instance used for integrating differential equations.
            register: Register of all ODE solving method used for handle method selection.
            comparator: Class for handle comparing different ODE solving methods
            input_frame: Frame handling user input for the ODE problem.
            result_frame: Frame responsible for displaying numerical results and performance metrics.
            comparison_frame_cls: Frame responsible for comparing various methods.
            plotter_cls: Class responsible for rendering solution plots.
        """
        self.root = root
        self.root.title("Розв'язання Диференціальних рівнянь")
        self.root.geometry("700x700")

        self.solver: ODESolver = solver
        self.register: ODEMethodRegistry = register
        self.comparator: MethodComparator = comparator

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
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Вхідні дані')
        self.tab_control.add(self.tab2, text='Результати')
        self.tab_control.add(self.tab3, text='Порівняння методів')

        for tab in (self.tab1, self.tab2, self.tab3):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

        self.input_frame: InputFrame = input_frame_cls(self.tab1, self.calculate, self.register.get_method_choices())
        self.results_frame: ResultsFrame = result_frame_cls(self.tab2, plotter_cls)
        self.comparison_frame: ComparisonFrame = comparison_frame_cls(self.tab3, plotter_cls)
        
        # comparison callback
        self.comparison_frame.set_compare_callback(self.compare_methods)

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
            function = self.input_frame.get_function()
            params = self.input_frame.get_inputs()
            y0, t0, t_end, h, eps, max_iter, method_id = params.values()
            method = self.register.get_method(method_id)

            # analytical solution
            equation_str = self.input_frame.get_equation()
            analytical_func = self.solver.solve_analytical(equation_str, (t0, y0))
            if analytical_func:
                self.results_frame.set_analytical_solution(analytical_func, equation_str)

            # solve numerically
            ts, ys, exec_time = self.solver.solve(
                function=function,
                epsilon=eps,
                method=method,
                y0=y0, t0=t0, t_end=t_end,
                h=h, max_iter=max_iter
            )
            # update results
            self.results_frame.update_results(ts, ys, exec_time)
            self.tab_control.select(self.tab2)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))
    
    def compare_methods(self):
        """Compare all methods for current problem"""
        try:
            function = self.input_frame.get_function()
            params = self.input_frame.get_inputs()
            y0, t0, t_end, _, eps, _, _ = params.values()
            
            # compare methods
            methods = self.register.get_all_methods()
            results = self.comparator.compare_methods(
                function, eps, y0, t0, t_end, methods
            )
            # update comparison frame
            self.comparison_frame.update_comparison_results(results)
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка порівняння: {str(e)}")