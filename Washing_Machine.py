import numpy as np
import matplotlib.pyplot as plt

time_minutes = list(range(54))

power_usage = [
    0, 0, 8, 8, 140, 140, 140, 140, 140, 2, 2, 2, 
    140, 140, 140, 140, 140, 8, 8, 8, 140, 140, 140, 140, 140, 2, 2, 2, 2, 2, 
    140, 140, 140, 140, 140, 8, 8, 8, 140, 140, 140, 140, 140, 2, 2, 2, 
    140, 140, 140, 140, 8, 8, 0, 0
]

np.random.seed(42)

def add_variation(power_list, variation_range):
    return [max(0, p + np.random.randint(-variation_range, variation_range + 1)) for p in power_list]

power_usage_varied = []
for p in power_usage:
    if p == 140:
        power_usage_varied.append(add_variation([p], 10)[0])
    elif p == 8:
        power_usage_varied.append(add_variation([p], 2)[0])
    elif p == 2:
        power_usage_varied.append(add_variation([p], 1)[0])
    else:
        power_usage_varied.append(0)

plt.figure(figsize=(10, 5))
plt.plot(time_minutes, power_usage_varied, marker='o', linestyle='-', color='b')

plt.xlabel("Time (Minutes)")
plt.ylabel("Power Usage (Watts)")
plt.title("Washing Machine Power Usage")
plt.xticks(range(0, 55, 5))
plt.yticks([0, 2, 8, 140])

plt.grid(True, linestyle="--", alpha=0.5)

plt.show()
