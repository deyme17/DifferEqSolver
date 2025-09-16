import tkinter as tk
from tkinter import ttk
from core import GraphPlotter



class ResultsFrame:
    """Frame for displaying results and plot"""
    def __init__(self, parent, plotter_cls: GraphPlotter):
        """
        Initialize the results frame for numerical solution display and plotting.
        Args:
            parent: Parent Tkinter widget where this frame is placed.
            plotter: GraphPlotter instance responsible for rendering solution plots.
        """
        self.parent = parent
        self.plotter_cls = plotter_cls
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self._create_widgets()

    def _create_widgets(self):
        # execution time
        self.time_label = ttk.Label(self.frame, text="Час виконання: -")
        self.time_label.grid(row=0, column=0, sticky="w")

        # results
        cols = ("t", "y(t)")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=10)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, sticky="nsew", pady=10)

        # graph
        self.plotter = self.plotter_cls(master=self.frame, figsize=(5, 3),
                                        row=2, column=0, sticky="nsew")

        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def update_results(self, ts: list[float], ys: list[float], exec_time: float, real_answer: float = None):
        """Updates table and graph"""
        # update execution time
        self.time_label.config(text=f"Час виконання: {exec_time:.4f} c")

        # update table
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t, y in zip(ts, ys):
            self.tree.insert("", tk.END, values=(f"{t:.4f}", f"{y:.4f}"))

        # update graph
        self.plotter.update_graph(ts, ys, y_lb="y", x_lb="t", real_answer=real_answer)