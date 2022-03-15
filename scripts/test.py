import matplotlib.pyplot as plt
import random
plt.ion()
plt.plot([1.6, 2.7])

for i in range(50):
    print(i)
    plt.scatter(random.random(), random.random())
    plt.pause(0.25)  # adds each datapoint to the graph slowly but visible. 
    # Remove this to show the graph instantly
    # once its constructed.
