# Write a python program to find the 
# minimum value of the function 𝑓(𝑥) = 3𝑥2 + 8 sin(𝑥) for −15 ≤ 𝑥 ≤ 15. 
# Also show the minimum value in the graph

import matplotlib.pyplot as plt

import numpy as np
from scipy import optimize as spop

def fn(x):
    return 3*x**2 + 8*np.sin(x)

x = np.linspace(-15, 15, 0.1)
plt.plot(x, fn(x))

res = spop.minimize(fn, x0=0)
print(res)
print("Minimum value of the function is: %.4f", res.x)
plt.plot(res.x, fn(res.x), 'o', label = 'Minimum value')
plt.title("Graph of the function")
plt.legend(["data", "minimum point"], loc="best")
plt.show()