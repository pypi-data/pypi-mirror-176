#  Write a python program to plot the functions 𝑓(𝑥) = sin(𝑥2 + 𝑥) and 
# 𝑓(𝑥) = cos(𝑥2) ranging from −2𝜋 to 2𝜋 in 
# (a) a single frame and (b) side by side. Also mention the title and legends in the figure. 

import matplotlib.pyplot as plt
import numpy as np

n1 = 2 * -np.pi
n2 = 2 * np.pi
x = np.linspace(n1, n2, 256)
c = np.cos(x**2)
plt.plot(x,c)
plt.title("Cosine Function")
plt.show()

s = np.sin(x**2 + x)
plt.plot(x,s)
plt.title("sine(x^2 + x)")
plt.show()