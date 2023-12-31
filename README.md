# First-record
This repository contains necessary codes for my first recording and initial data processing

```my_node.py``` is the ROS2 node used to record motor commands.

### 1. Plot a map merely from motor command.
```python plot_map.py``` 
<p align="center">
<img src="https://github.com/niart/first_record/blob/710ecb5cac7bc13c5d935f7b82239cdbc1d2b397/merely_motor_command0.png" width=50% height=50%>
</p>

### 2. Plot a map with translational velocity from motor commands and gyroscope from IMU 
First, run ```align.py``` to generate timestamp-aligned motor-command dataset and imu dataset

Second, ```python aligned_map.py```
<p align="center">
<img src="https://github.com/niart/first_record/blob/710ecb5cac7bc13c5d935f7b82239cdbc1d2b397/map_motor_imu0.png" width=50% height=50%>
</p>

### 3. Have a look at the drifts of events and IMU
run ```python vpr_davis_dataloader.py``` and will obtain:
<p align="center">
<img src="https://github.com/niart/first_record/blob/6cf3beb9aea5517b2d52d51430c4c6bd8168f446/drift.png" width=50% height=50%>
</p>

### 4. The ground truth trajectory from motion capture system:
run ```python vpr_davis_dataloader.py``` and will obtain:
<p align="center">
<img src="https://github.com/niart/first_record/blob/6cf3beb9aea5517b2d52d51430c4c6bd8168f446/ground_truth.png" width=50% height=50%>
</p>
