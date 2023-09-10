# First-record
This repository contains necessary codes for my first recording and initial data processing

```my_node.py``` is the ROS2 node used to record motor commands.

### Plot a map merely from motor command.
```python plot_map.py``` 
<p align="center">
<img src="[https://github.com/niart/first_record/blob/35e53a1bda68915246fa04899714f70927ecae41/map.png]" width=50% height=50%>
</p>

### plot a map with translational velocity from motor commands and gyroscope from IMU 
First, run ```align.py``` to generate timestamp-aligned motor-command dataset and imu dataset

Second, ```python aligned_map.py```
