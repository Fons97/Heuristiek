import matplotlib.pyplot as plt
import numpy as np



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

x = np.array([8, 2, 2, 5, 5, 7, 7])
y = np.array([2, 2, 4, 4, 6, 6, 4])
z = np.array([1, 1, 1, 1, 1, 1, 1])


ax.scatter(x, y, z, 'o')
ax.plot(x, y, z)


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
