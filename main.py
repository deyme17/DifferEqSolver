from tkinter import Tk
from gui.app_window import ODESolverApp

from core import EulerMethod
from utils.method_register import ODEMethodRegistry

ODEMethodRegistry.register(EulerMethod)

if __name__ == '__main__':
    root = Tk()
    app = ODESolverApp(root)
    root.mainloop()
