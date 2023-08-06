import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from matplotlib import cm


def multivariate_normal(x, d, mean, cov):
    x_m = x - mean
    return (1. / (np.sqrt((2 * np.pi)**d * np.linalg.det(cov))) * np.exp(-(np.linalg.solve(cov, x_m).T.dot(x_m)) / 2))

def gen_surface(mean, cov, d):
    num_samples = 100                                                                     
    x1_s = np.linspace(-15, 15, num=num_samples)                                              

    x2_s = np.linspace(-15, 15, num=num_samples)
    x1, x2 = np.meshgrid(x1_s, x2_s)                                                      
    pdf = np.zeros((num_samples, num_samples))
    for i in range(num_samples):
        for j in range(num_samples):
            pdf[i,j] = multivariate_normal(np.matrix([[x1[i,j]], [x2[i,j]]]), d, mean, cov)
                                                                                        
    return x1, x2, pdf
d=2
r=0.7720
u=23
v=16
w=r*(u**(1/2))*(v**(1/2))                                                               
fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10,10))                              
bivariate_mean = np.matrix([[3], [2]])                                                  
bivariate_covariance = np.matrix([[23, w], [w, 16]])                                    
x1, x2, p = gen_surface(bivariate_mean, bivariate_covariance, d)                   

con = ax1.contourf(x1, x2, p, 100, cmap=cm.YlGnBu)
ax1.set_xlabel('$x_1$', fontsize=13)                                                   
ax1.set_ylabel('$x_2$', fontsize=13)                                                    
ax1.axis([-15, 15, -15, 15])                                                            
ax1.set_aspect('equal')                                                                
ax1.set_title('The Required Plot', fontsize=12)
plt.show()                                                                              
