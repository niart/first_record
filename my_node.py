import rclpy
from rclpy.node import Node
import time

from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile, ReliabilityPolicy

qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

class DataRecorder(Node):

    def __init__(self):
        super().__init__('data_recorder')
        
        # Create files to record data
        self.odom_file = open('odometry_data.txt', 'w')
        self.motor_command_file = open('motor_commands.txt', 'w')
        self.imu_file = open('imu_data.txt', 'w')
        
        # Subscribers
        #self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, qos)
        self.motor_cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.motor_cmd_callback, 10)
        #self.imu_sub = self.create_subscription(Imu, '/imu', self.imu_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/oakd/rgb/preview/image_raw', self.imu_callback, qos)

    def motor_cmd_callback(self, msg):
        # Record the motor command data
        print('motor value is', msg)
        record = f"{ time.perf_counter()}, {msg.linear}, {msg.angular}\n"
        self.motor_command_file.write(record)        

    def odom_callback(self, msg):
        # Record the odometry data
        record = f"Time: {msg.header.stamp.sec}.{msg.header.stamp.nanosec}, Position: {msg.pose.pose.position}, Orientation: {msg.pose.pose.orientation}\n"
        self.odom_file.write(record)

    def imu_callback(self, msg):
        # Record the IMU data
        print('imu value is', msg)
        record = f"Time: {msg.header.stamp.sec}.{msg.header.stamp.nanosec}, Orientation: {msg.orientation}, Angular Velocity: {msg.angular_velocity}, Linear Acceleration: {msg.linear_acceleration}\n"
        self.imu_file.write(record)

    def __del__(self):
        # Close the files when the node is destroyed
        self.odom_file.close()
        self.motor_command_file.close()
        self.imu_file.close()

def main(args=None):
    rclpy.init(args=args)
    recorder = DataRecorder()
    rclpy.spin(recorder)
    recorder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
