import tkinter as tk
from tkinter import ttk, messagebox
from core.comparison import MethodComparator
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
        
        self.compare_callback = None
        self._create_widgets()

    def _create_widgets(self):
        # title
        title_label = ttk.Label(self.frame, text="Порівняння методів розв'язування ДР", 
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # comparison button
        self.comp_btn = ttk.Button(self.frame, text="Порівняти всі методи", 
                                  command=self.compare_callback)
        self.comp_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        # results table
        cols = ("Метод", "Час виконання (с)", "Кількість точок", "Остання точка y")
        self.comp_tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.comp_tree.heading(col, text=col)
            if col == "Метод":
                self.comp_tree.column(col, width=120)
            else:
                self.comp_tree.column(col, width=130)
        self.comp_tree.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.comp_tree.yview)
        self.comp_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky="ns")
        
        # comparison plot
        self.comp_plotter = self.plotter_cls(master=self.frame, figsize=(8, 5),
                                           row=3, column=0, sticky="nsew")
        
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=2)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def set_compare_callback(self, callback):
        """Set callback function for comparison"""
        self.compare_callback = callback
        self.comp_btn.configure(command=callback)

    def update_comparison_results(self, results: dict):
        """
        Update comparison results table and plot
        Args:
            results: Dictionary with method names as keys and results as values
        """
        for row in self.comp_tree.get_children():
            self.comp_tree.delete(row)
        
        # update table
        for method_name, result in results.items():
            ts, ys = result['solution']
            last_y = ys[-1] if len(ys) > 0 else 0
            
            self.comp_tree.insert("", tk.END, values=(
                method_name,
                f"{result['execution_time']:.6f}",
                result['num_points'],
                f"{last_y:.6f}"
            ))
        
        # update comparison plot
        self._plot_comparison(results)

    def _plot_comparison(self, results: dict):
        """Plot all methods on the same graph for comparison"""
        self.comp_plotter.ax.clear()
        
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        linestyles = ['-', '--', '-.', ':', '-']
        
        for i, (method_name, result) in enumerate(results.items()):
            ts, ys = result['solution']
            color = colors[i % len(colors)]
            linestyle = linestyles[i % len(linestyles)]
            
            self.comp_plotter.ax.plot(ts, ys, color=color, linestyle=linestyle, 
                                    label=method_name, linewidth=2)
        
        self.comp_plotter.ax.set_xlabel('t')
        self.comp_plotter.ax.set_ylabel('y')
        self.comp_plotter.ax.legend()
        self.comp_plotter.ax.grid(True)
        self.comp_plotter.ax.set_title('Порівняння методів розв\'язування ДР')
        self.comp_plotter.canvas.draw()