# This script is to make a map with translational velocity from motor commands and gyroscope from IMU data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load motor commands (linear velocity)
motor_commands = np.loadtxt('/home/niwang/toy_record/vpr_recordings/synced_motor_commands.txt')
timestamps_motor = motor_commands[:, 0]
v = motor_commands[:, 1]  # Linear velocity
theta_motor = motor_commands[:, 6]

# Load gyro data (angular velocity)
gyro_data = np.loadtxt('/home/niwang/toy_record/vpr_recordings/synced_imu_data.txt', skiprows=1) # Skip header
timestamps_gyro = gyro_data[:, 0] - 14000000
w = gyro_data[:, 2]  # Angular velocity
w = -np.deg2rad(w)

#plt.plot(w)
#plt.show()
# Resample angular velocity to align with motor timestamps
w_resampled = np.interp(timestamps_motor, timestamps_gyro, w)
print(timestamps_motor)

plt.plot(timestamps_motor, w_resampled)
plt.plot(timestamps_motor, theta_motor)
plt.show()

# Initialize pose (x, y, theta)
x, y, theta = [0], [0], [-np.pi/2.0]

# Set a threshold for the maximum allowable time gap (e.g., 0.5 seconds)
time_gap_threshold = 1000000

# Iterate through the data and compute the pose
for i in range(1, len(timestamps_motor)):
    dt = (timestamps_motor[i] - timestamps_motor[i-1]) / 1000000  # Assuming timestamps are in milliseconds
    
    # If time gap exceeds the threshold, adjust dt to the threshold value
    if dt > time_gap_threshold:
        dt = time_gap_threshold
    
    # Update theta
    theta_new = theta[-1] + w_resampled[i] * dt
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
plt.axis('equal')
plt.show()
