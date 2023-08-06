# fitted linear and cubic interpolation into 30 intermediate points based on the following data
# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# y = [12, 43, 56,34,23,54,65,67,86,65]

import matplotlib.pyplot as plt

import numpy as np
from scipy.interpolate import interp1d

x = np.linspace(1, 10, 30)
y = (12, 43, 56,34,23,54,65,67,86,65)

f1 = interp1d(x, y, kind='linear')
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(1, 10, 30)
plt.plot(x, y, 'o', xnew, f1(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()