# This script is to make a robot trajectory merely from motor commands.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Read data from file
data = np.loadtxt('/home/niwang/toy_record/00_motor_command.txt', delimiter=',')

timestamps = data[:, 0]
v = data[:, 1]  # Linear velocity
w = data[:, 2]  # Angular velocity

# Initialize pose (x, y, theta)
x, y, theta = [0], [0], [180/(2*np.pi)] # rotate 180 degrees

# Set a threshold for the maximum allowable time gap (e.g., 0.5 seconds)
time_gap_threshold = 0.5

# Iterate through the data and compute the pose
for i in range(1, len(timestamps)):
    dt = timestamps[i] - timestamps[i-1]
    
    # If time gap exceeds the threshold, adjust dt to the threshold value
    if dt > time_gap_threshold:
        dt = time_gap_threshold
    
    # Update theta
    theta_new = theta[-1] + w[i] * dt
    theta.append(theta_new)
    
    # Update x and y
    dx = v[i] * np.cos(theta_new) * dt
    dy = v[i] * np.sin(theta_new) * dt
    
    x_new = x[-1] + dx
    y_new = y[-1] + dy
    
    x.append(x_new)
    y.append(y_new)

# Create a colormap to represent the trajectory timeline
norm = mcolors.Normalize(vmin=0, vmax=len(x))
colormap = plt.get_cmap('viridis')

# Plot the trajectory with heatmap
plt.figure(figsize=(8, 8))
for i in range(1, len(x)):
    plt.plot(x[i-1:i+1], y[i-1:i+1], color=colormap(norm(i)))

# Add a colorbar to indicate the timeline
sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, orientation='vertical')
cbar.set_label('Time Progression')

plt.title('Robot Movement Trajectory')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
