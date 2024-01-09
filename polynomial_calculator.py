import numpy as np
import matplotlib.pyplot as plt

def calculate_polynomial(coefficients):
    x = np.linspace(-10, 10, 1000)
    y = np.polyval(coefficients, x)
    delta = None
    vertex = None
    # Calculate delta (for quadratic function)
    if len(coefficients)-1 == 2:
        a, b, c = coefficients
        delta = b**2 - 4*a*c
        p = round(-b/(2*a),2) 
        q = round(-delta/(4*a),2)
        vertex = [p, q]
    # Calculate roots
    roots = np.roots(coefficients)

    #  Calculating the first derivative for extreme places
    derivative_coefficients = np.polyder(coefficients)
    extrema_roots = np.roots(derivative_coefficients)
    return x, y, delta, roots, extrema_roots, vertex
