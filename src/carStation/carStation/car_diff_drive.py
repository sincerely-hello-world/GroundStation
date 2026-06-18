import rclpy, math
from rclpy.node import Node
from std_msgs.msg import Float32, String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from carStation.car_uart_parse import *

import tf_transformations

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
# 创建 Best Effort 的 QoS Profile
best_effort_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=2  # 保留最近2条消息
)

class DiffDriveController(Node):
    def __init__(self):
        super().__init__('diff_drive')
        self.cb_odom = MutuallyExclusiveCallbackGroup()
        self.cb_obs = MutuallyExclusiveCallbackGroup()
        # Subscriber for odometry

        # ===== 位姿状态 =====
        self.x = 0.0          # 全局x坐标(米)
        self.y = 0.0          # 全局y坐标(米)
        self.theta = 0.0      # 全局航向角(弧度)
        self.v_x = 0.0        # 全局当前线速度
        self.v_theta = 0.0    # 全局当前角速度
 
        self.velocity_calc = VelocityCalculator()
        self.cmd_msg = String(data= f"$spd:{int(0)},{int(-0)},{int(-0)},{int(0)}#") # 存储最新的/cmd_vel命令，供定时器发布
        
        self.stopCarFlag = False# 是否停车？
        self.handControlCarFlag = False # 中止接收 logical端的任务发布，接收手动控制
        self.okCarFlag = False # 目标点逼近完成标志

        # 是否遇到火源标志：
        self.wait_obs_flag = False
        self.timer_obs_wait = None
        self.obs = [car_aim(x=0,y=0,label='上一次火源位置'),car_aim(x=0,y=0,label='现在火源位置')] # 本地检测到火源位置,上一次火源位置
 

        self.aim = car_aim(label='init',status='NO') # 目标位姿状态
        self.create_timer(0.05, self.timer_pub_car_control) # 定时发布控制命令（需要持续发送，控制改变频率）

        # ===== ROS2接口 =====
        
        # 发布最原始的控制数据给MCU
        self.car_uart_pub = self.create_publisher(String, topic='car/driver/cmd_topic', qos_profile=best_effort_qos)
        # 发布控制命令给/cmd_vel话题，供上层使用（目前仅发布，后续可添加PID控制等）       
        self.cmd_vel_pub = self.create_publisher(Twist, 'car/driver/cmd_vel', 10)
        # 状态发布：当前已执行到位
        self.car_pos_status_pub = self.create_publisher(String, 'car/pos/status', 10 )
        # 发布log
        self.log_topic_pub = self.create_publisher(String,"log_topic",10 )

        # 订阅 话题获取速度控制指令和里程计数据
        self.car_odom_sub = self.create_subscription(Odometry, 'car/odom', self.car_odom_callback, 10, callback_group=self.cb_odom) # T265里程计数据 
        self.cmd_vel_sub = self.create_subscription(Twist, 'car/driver/cmd_vel', self.cmd_vel_callback, 10) # 基层驱动：接收/cmd_vel，转为 线速度和角速度，发布给串口节点输出控制
        self.control_sub = self.create_subscription(String, "car/driver/control",self.control_callback,10) # 最顶层抽象：接收目标位姿状态
        # 触发停车： 有火源点停止一下
        self.obstacle_sub =self.create_subscription(String, 'car/obstacle',self.obstacle_callback,10)

 
        self.get_logger().info('已订阅 /cmd_vel 话题')  # 添加这行确认
        
        ## 编码电机里程计数据发布/odom和TF 【已弃用】
        # self.odom_pub = self.create_publisher( Odometry,'/odom',10)
        # self.tf_broadcaster = TransformBroadcaster(self)
        ## 订阅串口话题获取编码器里程计数据 【已弃用】
        # self.car_uart_sub = self.create_subscription(String, topic='car/driver/recv_topic', callback=self.encoder_odom_callback, qos_profile=10)
        ## -----------------

    def send_log_json(self, label:str, info:str):
        self.get_logger().info(f"{label}:{info}")
        json_dumps = json.dumps({'label':label,'info':info})
        self.log_topic_pub.publish(String(data=json_dumps))
        

            
    def obstacle_callback(self, msg:String):
        if msg.data != 'N':
            self.obs[1].x = self.x # 更新现在检测到的位置
            self.obs[1].y = self.y #
            dis = max(abs( (self.obs[0].x - self.obs[1].x)) , abs((self.obs[0].y - self.obs[1].y)) )
            if dis > 0.10:  # 两次触发位置 > 10cm ，进行停车
                self.wait_obs_flag = True
                self.obs_wait_2s()
            # self.get_logger().info(f'xy={self.obs[0].x:.2f},{self.obs[0].y:.2f},x1y={self.obs[1].x:.2f},{self.obs[1].y:.2f},dis:{dis:.2f}m, flag:{self.wait_osb_flag}')
        pass
    def obs_wait_2s(self):
        # self.get_logger().info(f'停车任务触发======')
        if self.timer_obs_wait is not None:
            return # 如果已经在等待了，就不要反复重置时间了
        else:
            # self.get_logger().info(f'停车定时器启动*******')
            # ⚠️ 绝对不要写 self.obs[0] = self.obs[1]
            # 正确做法：只同步 X 和 Y 的数值，保持对象和 label 的独立性
            self.obs[0].x = self.obs[1].x
            self.obs[0].y = self.obs[1].y
            self.timer_obs_wait = self.create_timer(3.8, self.obstacle_wait)

    def obstacle_wait(self):
        self.wait_obs_flag=False
        if self.timer_obs_wait is not None:
            self.timer_obs_wait.cancel()
            self.timer_obs_wait = None
        # self.get_logger().info(f'停车结束，继续行驶------------')



#------------------------------
## 逻辑控制层函数：控制载具逼近目标位置/朝向
#------------------------------
    def control_callback(self, msg:String):
        ctl = msg.data
        if ctl == 'stopCar':
            self.stopCarFlag = True
            self.send_log_json("消防车","接收到停车指令")
        elif ctl == 'unlockCar':
            self.stopCarFlag = False
            self.send_log_json("消防车","接收到解锁指令")
        # elif ctl == 'handControlCar':
        #     self.handControlCarFlag = True
        # elif ctl == 'unHandControlCar':
        #     self.handControlCarFlag = False
        else:
            x, y, deg,label, status = decode_aim(ctl)                 
            self.aim =  car_aim(x=x, y=y, deg=deg,label=label,status=status) # 更新目标位姿状态

    def timer_pub_car_control(self):
        # 定时发布控制命令（如果需要持续发送）
        twist = Twist()
        twist.linear.x = 0.0    
        twist.angular.z = 0.0   
        if self.wait_obs_flag == True or self.stopCarFlag == True:
            self.cmd_vel_pub.publish(twist) # 发布 角速度0 线速度0  停车信号
            return

        # if self.turn_flag == True:
        #     twist.angular.z, flag = compute_rotation_cmd(self.theta, self.aim.yaw) # 计算旋转命令
        # self.get_logger().info(f"当前弧度{self.theta:.2f}, 角度{math.degrees(self.theta):.2f}")
        if self.aim is not None:
            twist.linear.x, twist.angular.z, flag = compute_pose_to_pose_command(self.x, self.y, self.theta, self.aim.x, self.aim.y, self.aim.yaw) # 计算位姿控制命令（目前仅计算）
        
            if flag:
                self.aim.status='OK'
                self.car_pos_status_pub.publish(String(data=encode_status(self.aim.label, self.aim.status)))
            else:
                self.aim.status='NO'
                self.car_pos_status_pub.publish(String(data=encode_status(self.aim.label, self.aim.status)))

        self.cmd_vel_pub.publish(twist) # 发布 角速度 线速度

#------------------------------
## 驱动层函数：线速度，角速度发布
#------------------------------
    def cmd_vel_callback(self, msg):
        """
        接收/cmd_vel,转发给STM32
        """
        v_left, v_right = self.velocity_calc.set_speed(msg.linear.x, msg.angular.z)
        # 构造命令字符串  逆向求解出目标速度
        # $spd:0,0,0,0# # 转为四个轮子各自速度
        M1 = v_left*1000 
        M3 = M1
        M2 = v_right*1000# 右轮速度  
        M4 = M2
        cmd_vel = f"$spd:{int(M1)},{int(-M2)},{int(-M3)},{int(M4)}#"
        # self.get_logger().info(f"线速度={msg.linear.x:.3f} m/s, 角速度={msg.angular.z:.3f} rad/s")
        # 发布给串口节点
        self.cmd_msg.data = cmd_vel
        self.car_uart_pub.publish(self.cmd_msg)
 
#------------------------------
## 数据层函数： 里程计更新
#------------------------------
    def car_odom_callback(self, msg:Odometry):
        # 接收里程计数据，更新位姿状态
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        quat = msg.pose.pose.orientation
        (roll, pitch, yaw) = tf_transformations.euler_from_quaternion(quaternion=[quat.x, quat.y, quat.z, quat.w]) # sxyz return (roll, pitch, yaw)
        self.theta = yaw
        # self.get_logger().info(f"里程计更新: x={self.x:.3f} m, y={self.y:.3f} m, theta={math.degrees(self.theta):.2f} deg")
        pass

 
#------------------------------
## 数据层函数： 编码电机里程计更新 【已弃用】
#------------------------------
    # def encoder_odom_callback(self, msg):
    #     """
    #     接收串口节点发布的里程计数据，更新小车位姿状态，并发布/odom和TF
    #     """
    #     # 解析串口反馈的编码器数据，更新位姿状态
    #     if msg.data.startswith("$MAll:") and msg.data.endswith("#"):
    #         left_dist, right_dist = get_dis_left_right(msg.data)
    #         self.v_x, self.v_theta, self.x, self.y, self.theta = self.velocity_calc.update(left_dist, right_dist)
            
    #         import tf_transformations
    #         raw_quat = tf_transformations.quaternion_from_euler(0, 0, self.theta) # 姿态(转为四元数)
    #         quat = Quaternion(x=raw_quat[0], y=raw_quat[1], z=raw_quat[2], w=raw_quat[3])

    #         # 发布里程计消息
    #         odom_msg = Odometry()
    #         odom_msg.header.stamp = self.get_clock().now().to_msg()
    #         odom_msg.header.frame_id = 'odom'
    #         odom_msg.child_frame_id = 'base_link'
    #         odom_msg.pose.pose.position.x = self.x   # 位置
    #         odom_msg.pose.pose.position.y = self.y
    #         odom_msg.pose.pose.position.z = 0.0
    #         odom_msg.pose.pose.orientation = quat  # 姿态(四元数)

    #          # 位置协方差(简化模型)
    #         odom_msg.pose.covariance[0] = 0.01   # x方差
    #         odom_msg.pose.covariance[7] = 0.01   # y方差
    #         odom_msg.pose.covariance[35] = 0.01  # theta方差
            
    #         # 速度
    #         odom_msg.twist.twist.linear.x = self.v_x
    #         odom_msg.twist.twist.linear.y = 0.0
    #         odom_msg.twist.twist.linear.z = 0.0
    #         odom_msg.twist.twist.angular.x = 0.0
    #         odom_msg.twist.twist.angular.y = 0.0
    #         odom_msg.twist.twist.angular.z = self.v_theta

    #         # 速度协方差
    #         odom_msg.twist.covariance[0] = 0.01   # vx方差
    #         odom_msg.twist.covariance[35] = 0.01  # omega方差
    #         self.odom_pub.publish(odom_msg)
    
    #         # 广播TF
    #         t = TransformStamped()
    #         t.header.stamp = self.get_clock().now().to_msg()
    #         t.header.frame_id = 'odom'
    #         t.child_frame_id = 'base_link'
    #         t.transform.translation.x = self.x
    #         t.transform.translation.y = self.y
    #         t.transform.translation.z = 0.0
    #         t.transform.rotation = quat
    #         self.tf_broadcaster.sendTransform(t)


    # def euler_to_quaternion(self, roll, pitch, yaw):
    #     """
    #     欧拉角转四元数
    #     """
    #     qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - \
    #          math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    #     qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + \
    #          math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    #     qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - \
    #          math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    #     qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + \
    #          math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    #     quat = Quaternion()
    #     quat.x = qx
    #     quat.y = qy
    #     quat.z = qz
    #     quat.w = qw
    #     return quat