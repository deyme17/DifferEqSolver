from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np



class GraphPlotter:
    """Plot numerical solutions of ODEs in a Tkinter frame."""
    def __init__(
        self, 
        master, 
        figsize: tuple[float, float] = (6, 4), 
        row: int = 2, 
        column: int = 0, 
        sticky: str = "nsew"
    ):
        """
        Initialize matplotlib figure and embed it into a Tkinter widget.
        Args:
            master: Parent Tkinter widget where the plot will be embedded.
            figsize (tuple[float, float], optional): Size of the figure in inches (width, height). Defaults to (6, 4).
            row (int, optional): Grid row position for the canvas. Defaults to 2.
            column (int, optional): Grid column position for the canvas. Defaults to 0.
            sticky (str, optional): Tkinter sticky option for canvas placement. Defaults to "nsew".
        """
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=row, column=column, sticky=sticky)

    def update_graph(self, ts: np.ndarray, ys: np.ndarray, 
                     y_label: str = "y", x_label: str = "t", 
                     real_answer: float = None) -> None:
        """
        Update the plot with new data.
        Args:
            ts (np.ndarray): Array of time points.
            ys (np.ndarray): Array of corresponding y values.
            y_label (str, optional): Label for y-axis and plot legend. Defaults to "y".
            x_label (str, optional): Label for x-axis and plot legend. Defaults to "t".
            real_answer (float, optional): If provided, draws a horizontal line indicating 
                the real/analytical solution for comparison. Defaults to None.
        """
        self.ax.clear()
        self.ax.plot(ts, ys, label=f"{y_label}({x_label})")
        
        if real_answer is not None:
            self.ax.axhline(real_answer, color="r", linestyle="--", label="Реальна відповідь")
        
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.legend()
        self.canvas.draw()