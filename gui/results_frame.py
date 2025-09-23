import tkinter as tk
from tkinter import ttk
import numpy as np
from core.plotter import GraphPlotter
from typing import Callable



class ResultsFrame:
    """Frame for displaying results and plot"""
    def __init__(self, parent, plotter_cls: GraphPlotter):
        """
        Initialize the results frame for numerical solution display and plotting.
        Args:
            parent: Parent Tkinter widget where this frame is placed.
            plotter_cls: GraphPlotter class responsible for rendering solution plots.
        """
        self.parent = parent
        self.plotter_cls = plotter_cls
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.analytical_solution = None
        self._create_widgets()

    def _create_widgets(self):
        # execution time
        self.time_label = ttk.Label(self.frame, text="Час виконання: -")
        self.time_label.grid(row=0, column=0, sticky="w")
        
        # analytical solution label
        self.analytical_label = ttk.Label(self.frame, text="Точний розв'язок: не знайдено")
        self.analytical_label.grid(row=1, column=0, sticky="w")
        
        # results table
        cols = ("t", "y(t)", "y_точне(t)", "похибка")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # graph
        self.plotter: GraphPlotter = self.plotter_cls(master=self.frame, figsize=(8, 4),
                                        row=3, column=0, sticky="nsew")
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def set_analytical_solution(self, analytical_func: Callable, equation_str: str, analytical_equation_str: str):
        """Set the analytical solution function"""
        self.analytical_solution = analytical_func
        if analytical_func:
            self.analytical_label.config(text=f"Точний розв'язок для y' = {equation_str}   ->   {analytical_equation_str}")

    def update_results(self, ts: np.ndarray, ys: np.ndarray, exec_time: float):
        """Updates table and graph with numerical results"""
        # update execution time
        self.time_label.config(text=f"Час виконання: {exec_time:.6f} с")
        
        # update table
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        analytical_ys = None
        if self.analytical_solution:
            try:
                analytical_ys = np.array([self.analytical_solution(t) for t in ts])
            except:
                analytical_ys = None
                
        step = max(1, len(ts) // 20)  # show at most 20 points
        for i in range(0, len(ts), step):
            t, y_num = ts[i], ys[i]
            if analytical_ys is not None:
                y_analytical = analytical_ys[i]
                error = abs(y_analytical - y_num)
                self.tree.insert("", tk.END, values=(
                    f"{t:.4f}", f"{y_num:.6f}", f"{y_analytical:.6f}", f"{error:.6f}"
                ))
            else:
                self.tree.insert("", tk.END, values=(
                    f"{t:.4f}", f"{y_num:.6f}", "-", "-"
                ))
        
        # update graph
        self.plotter.update_graph(ts, ys, y_label="y", x_label="t", 
                                 analytical_ys=analytical_ys if analytical_ys is not None else None)