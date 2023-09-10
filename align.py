# This script is to generate timestamp-aligned motor-command dataset and imu dataset
from dv import AedatFile
import numpy as np

def cumtrapz_example(y, x):
    return np.cumsum(0.5 * ((x[1:] - x[:-1]) * (y[1:] + y[:-1])))

with AedatFile("/home/niwang/toy_record/vpr_recordings/dvSave-2023_08_11_19_26_05.aedat4") as f:
    # events will be a named numpy array
    events = np.hstack([packet for packet in f['events'].numpy()])
    motorcommands = np.loadtxt("/home/niwang/toy_record/vpr_recordings/0_motor_command.txt", dtype=str)
    timestamp_motor = []
    x_motor = []
    y_motor = []
    z_motor = []
    xang_motor = []
    yang_motor = []
    zang_motor = []
    for i in range(len(motorcommands)):
        timestamp_motor.append(float(motorcommands[i][0][:-1]))
        x_motor.append(float(motorcommands[i][1].replace("geometry_msgs.msg.Vector3(x=", "")[:-1]))
        y_motor.append(float(motorcommands[i][2].replace("y=", "")[:-1]))
        z_motor.append(float(motorcommands[i][3].replace("z=", "")[:-2]))
        xang_motor.append(float(motorcommands[i][4].replace("geometry_msgs.msg.Vector3(x=", "")[:-1]))
        yang_motor.append(float(motorcommands[i][5].replace("y=", "")[:-1]))
        zang_motor.append(float(motorcommands[i][6].replace("z=", "")[:-1]))

    timestamp_imu = []
    gyr = []
    acc = []
    for imu in f['imu']:
        timestamp_imu.append(imu.timestamp)  # millisecond resolution
        gyr.append(imu.gyroscope)
        acc.append(imu.accelerometer)

    # Align motor timestamp to IMU timestamp
    time_firstcommand = 0
    for idx, value in enumerate(acc):
        if abs(value[2]) > 0.05:  # Assuming value[2] represents the z-acceleration as before
            time_firstcommand = timestamp_imu[idx]
            break
    timestamp_motor_sync = (np.array(timestamp_motor) - timestamp_motor[0]) * 1000000 + time_firstcommand

    # Save the synchronized motor commands to a file
    synced_motor_data = np.column_stack((timestamp_motor_sync, x_motor, y_motor, z_motor, xang_motor, yang_motor, zang_motor))
    np.savetxt("/home/niwang/toy_record/vpr_recordings/synced_motor_commands.txt", synced_motor_data, header="timestamp,x,y,z,xang,yang,zang", fmt="%f")

    # Save the synchronized IMU data to a file
    gyr = np.array(gyr)
    acc = np.array(acc)
    synced_imu_data = np.column_stack((timestamp_imu, gyr[:,0], gyr[:,1], gyr[:,2], acc[:,0], acc[:,1], acc[:,2]))
    np.savetxt("/home/niwang/toy_record/vpr_recordings/synced_imu_data.txt", synced_imu_data, header="timestamp,gyr_x,gyr_y,gyr_z,acc_x,acc_y,acc_z", fmt="%f")
