from .methods import ODESolver, EulerMethod, RungeKuttaMethod, AdamsMethod
ode_solve_methods: list[ODESolver] = [EulerMethod, RungeKuttaMethod, AdamsMethod]