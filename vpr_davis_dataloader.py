# This script is to plot dataset 
# Author: Thorben
from dv import AedatFile
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view


def cumtrapz_example(y, x):
    return np.cumsum(0.5 * ((x[1:] - x[:-1]) * (y[1:] + y[:-1])))

with AedatFile("/home/niwang/first_record/dataset/dvSave-2023_08_11_19_26_05.aedat4") as f:
    # events will be a named numpy array
    events = np.hstack([packet for packet in f['events'].numpy()])
    motorcommands = np.loadtxt("/home/niwang/first_record/dataset/0_motor_command.txt", dtype=str)
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
    acc_average = [[] for _ in range(3)]
    for imu in f['imu']:
        timestamp_imu.append(imu.timestamp) # millisecond resolution
        gyr.append(imu.gyroscope)
        acc.append(imu.accelerometer)

    acc_average[0] = np.array(acc).T[0]
    acc_average[1] = np.array(acc).T[1]
    acc_average[2] = np.array(acc).T[2]
    v0 = sliding_window_view(acc_average[0],100)
    v1 = sliding_window_view(acc_average[1], 100)
    v2 = sliding_window_view(acc_average[2], 100)
    moving_average0 = v0.mean(axis=-1)
    moving_average1 = v1.mean(axis=-1)
    moving_average2 = v2.mean(axis=-1)
    timestamps = np.arange(len(moving_average2))

    moving_average2 = moving_average2 - np.mean(moving_average2[2000:8000])
    int_acc = cumtrapz_example(moving_average2, timestamps)

    print(timestamp_imu)

    begin = 12000
    end = 180000
    timesteps = range(begin, end, 1000)

    # Access information of all events by type
    timestamps_event, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']
    idx_begin = (np.abs(timestamps_event - timestamp_imu[begin])).argmin()
    idx_end = (np.abs(timestamps_event - timestamp_imu[end])).argmin()
    time_firstcommand = 0
    for idx, value in enumerate(moving_average2):
        if abs(value) > 0.05:
            time_firstcommand = timestamp_imu[idx]
            break
    timestamp_motor_sync = (np.array(timestamp_motor)-timestamp_motor[0])*1000000+time_firstcommand
    print(timestamp_motor_sync)
    idx_begin_mot = (np.abs(timestamp_motor_sync - timestamp_imu[begin])).argmin()
    idx_end_mot = (np.abs(timestamp_motor_sync - timestamp_imu[end])).argmin()

    print(timestamp_motor_sync[0])
    print(timestamp_imu[13000])

    fig = plt.figure()
    plt.subplot(411)
    plt.plot(timestamp_imu[begin:end], np.array(gyr).T[0][begin:end])
    plt.plot(timestamp_imu[begin:end], np.array(gyr).T[1][begin:end])
    #plt.plot(np.array(gyr).T[2][begin:end])
    plt.ylabel("turning velocity")
    plt.subplot(412)
    #plt.plot(moving_average0[begin:end])
    #plt.plot(moving_average1[begin:end]+0.9)
    plt.plot(timestamp_imu[begin:end], moving_average2[begin:end])
    plt.ylabel("forward acceleration")
    plt.subplot(413)
    plt.plot(timestamp_imu[begin:end], int_acc[begin:end])
    plt.ylabel("forward velocity")
    plt.subplot(414)
    plt.plot(timestamp_motor_sync[idx_begin_mot:idx_end_mot], x_motor[idx_begin_mot:idx_end_mot], ".")
    plt.plot(timestamp_motor_sync[idx_begin_mot:idx_end_mot], zang_motor[idx_begin_mot:idx_end_mot], ".")
    plt.ylabel("# events")
    plt.xlabel(["time (ms)"])
    plt.show()



