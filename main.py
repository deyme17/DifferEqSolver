from tkinter import Tk
from gui.app_window import ODESolverApp, InputFrame, ResultsFrame

from core import ode_solve_methods, ODESolver, GraphPlotter
from utils.method_register import ODEMethodRegistry

for method in ode_solve_methods:
    ODEMethodRegistry.register(method)



if __name__ == '__main__':
    root = Tk()
    app = ODESolverApp(
                    root=root,
                    solver=ODESolver(),
                    register=ODEMethodRegistry(),
                    input_frame_cls=InputFrame,
                    result_frame_cls=ResultsFrame,
                    plotter=GraphPlotter
                    )
    root.mainloop()
