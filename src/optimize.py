"""Optimization example using OR-Tools.

Given a vector of forecasted loads and prices, this module creates a toy
optimization: choose which hours to shift flexible load to minimize cost while
respecting capacity constraints. This is purposely simple and intended to show
how OR-Tools can be wired into the pipeline.
"""
from ortools.linear_solver import pywraplp


def run_optimization(forecast, price, capacity=100.0, flexible_share=0.1):
    """Run a simple linear optimization.

    Args:
        forecast: list or array of forecasted loads (length T)
        price: list or array of prices (length T)
        capacity: max capacity per hour
        flexible_share: fraction of load that can be shifted across hours

    Returns:
        dict with chosen load schedule and objective value.
    """
    T = len(forecast)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        raise RuntimeError('OR-Tools solver not available')

    x = [solver.NumVar(0, capacity, f'x_{t}') for t in range(T)]

    # total flexible energy must equal flexible_share * sum(forecast)
    total_flex = flexible_share * sum(forecast)
    solver.Add(sum(x) == sum(forecast))

    # objective: minimize cost = sum(price[t] * x[t])
    objective = solver.Sum([price[t] * x[t] for t in range(T)])
    solver.Minimize(objective)

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError('Optimization failed')

    solution = [v.solution_value() for v in x]
    obj = solver.Objective().Value()
    return {"schedule": solution, "objective": obj}


if __name__ == '__main__':
    print('Run this via run_optimization(forecast, price)')
