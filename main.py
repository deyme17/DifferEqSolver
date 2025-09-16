from tkinter import Tk
from gui.app_window import ODESolverApp

from core import ode_solve_methods
from utils.method_register import ODEMethodRegistry

for method in ode_solve_methods:
    ODEMethodRegistry.register(method)

if __name__ == '__main__':
    root = Tk()
    app = ODESolverApp(root)
    root.mainloop()
