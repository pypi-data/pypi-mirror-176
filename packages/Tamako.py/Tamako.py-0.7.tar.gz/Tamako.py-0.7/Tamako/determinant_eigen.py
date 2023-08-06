import numpy as np
from scipy import linalg 

A = np.array([[23,12,9], [15,43,21],[11,14,26]])
B = np.array([6,-2,8])

det = linalg.det(A)

l,v = linalg.eig(A)

x = linalg.solve(A,B)

print("Determinant of A is: ", det)
print("Eigenvalues of A are: ", l)
print("Eigenvectors of A are: ", v)
print("Solution of the system of linear equations is: ", x)
