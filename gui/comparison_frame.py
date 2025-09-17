import tkinter as tk
from tkinter import ttk
import numpy as np
from core.plotter import GraphPlotter


class ComparisonFrame:
    """Frame for comparing different ODE solving methods"""
    def __init__(self, parent, plotter_cls: GraphPlotter):
        """
        Initialize the comparison frame.
        Args:
            parent: Parent Tkinter widget where this frame is placed.
            plotter_cls: GraphPlotter class for rendering comparison plots.
        """
        self.parent = parent
        self.plotter_cls: GraphPlotter = plotter_cls
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.analytical_solution = None
        self._create_widgets()

    def _create_widgets(self):
        # title
        title_label = ttk.Label(self.frame, text="Порівняння методів розв'язування ДР", 
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # results table
        cols = ("Метод", "Час виконання (с)", "Кількість точок", "Макс. похибка", "Середня похибка")
        self.comp_tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.comp_tree.heading(col, text=col)
            if col == "Метод":
                self.comp_tree.column(col, width=120)
            else:
                self.comp_tree.column(col, width=110)
        self.comp_tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.comp_tree.yview)
        self.comp_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")
        
        # comparison plot
        self.res_plotter: GraphPlotter = self.plotter_cls(master=self.frame, figsize=(8, 5),
                                           row=2, column=0, sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=2)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def set_analytical_solution(self, analytical_func):
        """Set the analytical solution function for error calculation"""
        self.analytical_solution = analytical_func

    def update_comparison_results(self, results: dict):
        """
        Update comparison results table and plot with error analysis
        Args:
            results: Dictionary with method names as keys and results as values
        """
        for row in self.comp_tree.get_children():
            self.comp_tree.delete(row)

        error_results = {}
        for method_name, result in results.items():
            ts, ys = result['solution']
            
            if self.analytical_solution:
                analytical_ys = np.array([self.analytical_solution(t) for t in ts])
                
                #  calc errors
                errors = np.abs(analytical_ys - ys)
                max_error = np.max(errors) if len(errors) > 0 else 0
                mean_error = np.mean(errors) if len(errors) > 0 else 0

                error_results[method_name] = {
                    'ts': ts,
                    'errors': errors,
                    'execution_time': result['execution_time'],
                    'num_points': result['num_points'],
                    'max_error': max_error,
                    'mean_error': mean_error
                }
                # update table
                self.comp_tree.insert("", tk.END, values=(
                    method_name,
                    f"{result['execution_time']:.6f}",
                    result['num_points'],
                    f"{max_error:.6f}",
                    f"{mean_error:.6f}"
                ))
                # update plot
                self.res_plotter.update_comparison_graph(error_results)
            else:
                self.comp_tree.insert("", tk.END, values=(
                    method_name,
                    f"{result['execution_time']:.6f}",
                    result['num_points'],
                    "N/A",
                    "N/A"
                ))