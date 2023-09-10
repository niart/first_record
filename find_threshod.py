# This script is to find median time gap between consecutive timestamps
import numpy as np

# Read data from file
data = np.loadtxt('00_motor_command.txt', delimiter=',')

timestamps = data[:, 0]

# Calculate the gaps between consecutive timestamps
time_gaps = np.diff(timestamps)

# Compute the median time gap
median_gap = np.median(time_gaps)

print(f"The median time gap between consecutive timestamps is: {median_gap:.4f} seconds")

