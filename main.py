from tkinter import Tk
from gui.app_window import ODESolverApp, InputFrame, ResultsFrame, ComparisonFrame

from core import ode_solve_methods, ODESolver, GraphPlotter, MethodComparator
from utils.method_register import ODEMethodRegistry

for method in ode_solve_methods:
    ODEMethodRegistry.register(method)



if __name__ == '__main__':
    root = Tk()
    app = ODESolverApp(
                    root=root,
                    solver=ODESolver(),
                    register=ODEMethodRegistry(),
                    comparator=MethodComparator(),
                    input_frame_cls=InputFrame,
                    result_frame_cls=ResultsFrame,
                    comparison_frame_cls = ComparisonFrame,
                    plotter_cls=GraphPlotter
                    )
    root.mainloop()
