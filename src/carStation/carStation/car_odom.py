import rclpy, math
from rclpy.node import Node
from std_msgs.msg import String,Float32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

# First import the library
import pyrealsense2 as rs
import numpy as np
import transformations as tf

import math as m

def my_pose_data(data):
    H_aeroRef_T265Ref = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) #直接读初始状态！
    H_T265body_aeroBody = np.linalg.inv(H_aeroRef_T265Ref)

    # pose xyz
    # print("Position: {}".format((data.translation.z, data.translation.x, data.translation.y)))   # pos:  z+ = 前 x+ = 左 y+ = 上

    # orientation quaternion -> RPY
    H_aeroRef_T265Ref = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) #直接读初始状态！
    H_T265body_aeroBody = np.linalg.inv(H_aeroRef_T265Ref)
    H_T265Ref_T265body = tf.quaternion_matrix([data.rotation.w, data.rotation.x,data.rotation.y,data.rotation.z]) # in transformations, Quaternions w+ix+jy+kz are represented as [w, x, y, z]!

    # transform to aeronautic coordinates (body AND reference frame!)
    H_aeroRef_aeroBody = H_aeroRef_T265Ref.dot( H_T265Ref_T265body.dot( H_T265body_aeroBody ))
    rpy_rad = np.array( tf.euler_from_matrix(H_aeroRef_aeroBody, 'sxzy') ) # Rz(yaw)*Ry(pitch)*Rx(roll) body w.r.t. reference frame # 原版sxyz  调换顺序，解除-90~90的限制

    # print("Frame #{}".format(pose.frame_number))
    # print("RPY [deg]: {}".format(rpy_rad*180/m.pi))
    # print("0 1 2 [deg]: {}".format(rpy_rad*180/m.pi))
    yaw = rpy_rad[2]
    my_yaw = yaw*180/m.pi
    # print("My yaw : {:.3f}[deg]".format(my_yaw))
    return yaw # 返回弧度



class CarOdomPublisher(Node):
    def __init__(self):
        super().__init__('CarOdom')
        self.cb_odom = MutuallyExclusiveCallbackGroup()
        # 位姿状态
        self.x = 0.0          # 全局x坐标(米)  # 前
        self.y = 0.0          # 全局y坐标(米)  # 左
        self.theta = 0.0      # 全局航向角(弧度) # 0 = 前, +90 = 左, -90 = 右

        # Declare RealSense pipeline, encapsulating the actual device and sensors
        self.pipe = rs.pipeline()
        # Build config object and request pose data
        self.cfg = rs.config()
        self.cfg.enable_stream(rs.stream.pose)
        # Start streaming with requested config
        self.pipe.start(self.cfg)

        # 发布者
        self.car_odom_pub = self.create_publisher( Odometry,'car/odom',10)
        self.car_yaw_pub = self.create_publisher(Float32,'car/yaw',10) # 发布纯yaw角度，方便调试
        # TF广播
        self.car_odom_tf_broadcaster = TransformBroadcaster(self)

        self.timer_car_odom = self.create_timer(0.02, self.car_odom_callback, callback_group= self.cb_odom) # 50Hz发布里程计和TF
        self.get_logger().info(f'{self.get_name()}已启动，正在发布里程计数据和TF...')

    def car_odom_callback(self):
        frames = self.pipe.wait_for_frames()
        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()
            yaw = my_pose_data(data)

            # pose xyz
            # print("Position: {}".format((data.translation.z, data.translation.x, data.translation.y)))   # pos:  z+ = 前 x+ = 左 y+ = 上
            self.x = data.translation.z   # pos:  z+ = 前 x+ = 左 y+ = 上
            self.y = data.translation.x
            self.theta = yaw # 为弧度

            import tf_transformations
            raw_quat = tf_transformations.quaternion_from_euler(0, 0, yaw) # 姿态(转为四元数)
            quat = Quaternion(x=raw_quat[0], y=raw_quat[1], z=raw_quat[2], w=raw_quat[3])
            # 四元数转换为欧拉角 (弧度制)
            # (roll, pitch, yaw) = tf_transformations.euler_from_quaternion(quaternion=[quat.x, quat.y, quat.z, quat.w])
            # self.get_logger().info(f"roll={roll:.3f} rad, pitch={pitch:.3f} rad, yaw={yaw:.3f} rad")
            # 发布里程计消息
            odom_msg = Odometry()
            odom_msg.header.stamp = self.get_clock().now().to_msg()
            odom_msg.header.frame_id = 'car_odom'
            odom_msg.child_frame_id = 'car_base_link'
            odom_msg.pose.pose.position.x = self.x   # 位置
            odom_msg.pose.pose.position.y = self.y
            odom_msg.pose.pose.position.z = 0.0
            odom_msg.pose.pose.orientation = quat  # 姿态(四元数)

            # 位置协方差(简化模型)
            odom_msg.pose.covariance[0] = 0.01   # x方差
            odom_msg.pose.covariance[7] = 0.01   # y方差
            odom_msg.pose.covariance[35] = 0.01  # theta方差

            # # 速度
            # odom_msg.twist.twist.linear.x = 0.0
            # odom_msg.twist.twist.linear.y = 0.0
            # odom_msg.twist.twist.linear.z = 0.0
            # odom_msg.twist.twist.angular.x = 0.0
            # odom_msg.twist.twist.angular.y = 0.0
            # odom_msg.twist.twist.angular.z = 0.0

            # self.get_logger().info(f"T265里程计更新: x={self.x:.3f} m, y={self.y:.3f} m, theta={math.degrees(self.theta):.2f} deg")

            # # 速度协方差
            odom_msg.twist.covariance[0] = 0.01   # vx方差
            odom_msg.twist.covariance[35] = 0.01  # omega方差
            

            self.car_odom_pub.publish(odom_msg)
            self.car_yaw_pub.publish(Float32(data=self.theta)) # 发布纯yaw角度，方便调试

            # 广播TF
            t = TransformStamped()
            t.header.stamp = odom_msg.header.stamp #  self.get_clock().now().to_msg()
            t.header.frame_id = 'car_odom'
            t.child_frame_id = 'car_base_link'
            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0
            t.transform.rotation = quat

            self.car_odom_tf_broadcaster.sendTransform(t)