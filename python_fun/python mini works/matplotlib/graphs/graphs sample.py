import numpy as np
from matplotlib import pyplot as plt

y = 200 + np.random.randn(100)
x = [x for x in range(len(y))]

plt.plot(x, y, '-')
plt.fill_between(x, y, 195, where=(y > 195), facecolor='b', alpha=0.6)

plt.title("Sample Visualization")
plt.show()