import numpy as np
from matplotlib import pyplot as plt

from src.eigenlearn import eigenlearn

x = np.arange(-256,256)
M_l = np.exp(-1*((np.matmul(np.expand_dims(x,axis=1),np.expand_dims(0.1+0.01*np.random.rand(2000),axis=0)))**2)) + \
      np.exp(-1*((np.matmul(np.expand_dims(x-128,axis=1),np.expand_dims(0.1+0.01*np.random.rand(2000),axis=0)))**2))
# plt.imshow(M_l)
# plt.title("training set")
# plt.show()
Z,r,S = eigenlearn.learn(M_l,r=3,beta=10)

M = (1+np.random.rand(512)) * np.exp(-1*((np.matmul(np.expand_dims(x,axis=1),np.expand_dims(0.1+0.01*np.random.rand(512),axis=0)))**2)) +\
    (1+np.random.rand(512)) * np.exp(-1*((np.matmul(np.expand_dims(x-125,axis=1),np.expand_dims(0.1+0.01*np.random.rand(512),axis=0)))**2))
plt.imshow(M)
plt.title("orginal data")
plt.show()
M_noisy = M + np.random.normal(0,2,M.shape)
plt.imshow(M_noisy)
plt.title("noisy data")
plt.show()

S = eigenlearn.solve(M_noisy,Z)
plt.imshow(S)
plt.title("denoised data")
plt.show()

# plt.plot(20+M_l[:,256])
plt.plot(15+M[:,256])
plt.plot(0+M_noisy[:,256])
plt.plot(10+S[:,256])
plt.legend(["ground truth","noisy","denoised"])
plt.show()
