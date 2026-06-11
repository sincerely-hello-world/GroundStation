from time import sleep
import serial,threading,json

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from std_msgs.msg import String,Float32,Int8
from functools import partial
import numpy as np
from periphery import GPIO

from carStation.tofsense import TOFSense_M

class CarToFPublisher(Node):
    def __init__(self):
        super().__init__('CarToF')
        # 创建互斥回调组，确保同一时间只有一个tof传感器串口读写回调在执行，否则会崩溃
        self.cb_g1 = MutuallyExclusiveCallbackGroup() 
        self.cb_g2 = MutuallyExclusiveCallbackGroup()
        
        # 障碍物阈值设置
        self.obs_thred_max = 0.71 #米
        self.obs_thred_min = 0.07 #米

        self.uart3 = serial.Serial("/dev/ttyS3",921600)
        self.uart4 = serial.Serial("/dev/ttyS4",921600)
        sleep(0.5) # 等待串口稳定，确保ToF传感器初始化完成
        self.TOF3 = TOFSense_M(self.uart3)
        self.TOF4 = TOFSense_M(self.uart4)

        self.lock_ = threading.Lock()

        self.dis = [0,0]
        self.init_tof_ok= [False,False]
        self.LED = [GPIO(35, "out"), GPIO(54, "out")]
        self.LED[0].write(False)
        self.LED[1].write(False)
        self.LED_timer = [None, None]

        self.pub1 = self.create_publisher(Float32, 'car/tof3', 10)
        self.pub2 = self.create_publisher(Float32, 'car/tof4', 10)
        self.pub_obs  = self.create_publisher(String, 'car/obstacle', 10)

        self.timer_ToFsensor0 = self.create_timer(0.05, partial(self.ToFsensor_read, TOF=self.TOF3, index=0, publisher=self.pub1), callback_group=self.cb_g1) # 定时器，负责读取ToF传感器数据并发布

        self.timer_ToFsensor1 = self.create_timer(0.05, partial(self.ToFsensor_read, TOF=self.TOF4, index=1, publisher=self.pub2), callback_group=self.cb_g2) # 定时器，负责读取ToF传感器数据并发布

        self.timer_ToF_obstacle = self.create_timer(0.04 , self.ToF_obstacle) # 定时器，负责读取ToF传感器数据并发布
        # 发布log
        self.log_topic_pub = self.create_publisher(String,"log_topic",10 )
    def send_log_json(self, label:str, info:str):
        self.get_logger().info(f"{label}:{info}")
        json_dumps = json.dumps({'label':label,'info':info})
        self.log_topic_pub.publish(String(data=json_dumps))
    
    def ToF_obstacle(self):
        # with self.lock_:
        a = (self.obs_thred_min < self.dis[0] and  self.dis[0] < self.obs_thred_max)  
        b = (self.obs_thred_min < self.dis[1] and  self.dis[1] < self.obs_thred_max)
        # self.get_logger().info(f"ToF0: {self.dis[0]:.2f} m; ToF1:{self.dis[1]:.2f} m")
            
        if a and b:
            self.pub_obs.publish(String(data='B'))  # 两个都符合
        elif a:
            self.pub_obs.publish(String(data='L'))  # 只有左边符合
        elif b:
            self.pub_obs.publish(String(data='R'))  # 只有右边符合
        else:
            self.pub_obs.publish(String(data='N'))  # 都不符合

    def ToFsensor_read(self,TOF: TOFSense_M, index:int, publisher: rclpy.publisher.Publisher = None):
        data = TOF.get_data() # Tof传感器的 M系列 读取距离值 8*8点阵测距
        if not data or data == {0}:  # 拦截 None、空值，以及读取失败的 {0} 
            self.dis[index] =  0.35
            publisher.publish(Float32(data=self.dis[index]))
            if self.init_tof_ok[index] == False: # 没有链接成功才打印，连接成功后一般是误读
                self.get_logger().warning(f"ToFsensor{index} 掉电/错误连接/读取数据错误, failed")
        else:
            if self.init_tof_ok[index] == False: # 一次连接成功 打印一次日志
                self.init_tof_ok[index]= True
                self.send_log_json("消防车", f"Tof传感器{index}正常")

            dis_raw = data['dis']  
            sta_raw = data['dis_status']  # if data['dis_status'][idx] == 0: # 确保可信
            # 将64个点的一维数组重塑为 8*8 的二维矩阵
            dis_matrix_8x8 = np.array(dis_raw).reshape(8, 8) 
            sta_matrix_8x8 = np.array(sta_raw).reshape(8, 8) 
            # 【修改点】提取最中间 2*2 的区域 (第3-5行，第3-5列)
            center_dis = dis_matrix_8x8[3:5, 3:5]
            center_status = sta_matrix_8x8[3:5, 3:5]
            #  空间筛选：只保留状态正常的像素（通常 0 或 255 代表有效，NOOPLOOP 核心可信状态通常为 0，请对照手册）
            # 这里筛选出所有 status == 0 的距离值
            valid_mask = (center_status == 0)
            valid_distances = center_dis[valid_mask]

            if len(valid_distances) > 0:
                # np.median 返回 numpy 类型，转为 float 存入
                self.dis[index] = float(np.median(valid_distances))
            else:
                # 【修复点】如果中心区域没有可信点，给一个默认值（比如 0.35 或 0.0），避免直接沿用初始的 int 类型
                self.dis[index] = 0.0
                # self.get_logger().warning(f"ToFsensor{index} 中心区域无有效数据/距离过远")

            # 确保万无一失，发布时再包裹一层 float()
            publisher.publish(Float32(data=float(self.dis[index])))

            if  self.obs_thred_min <self.dis[index] and self.dis[index] < self.obs_thred_max:
                self.shutdown_led_delay(index)

#   data = TOF.get_data()  # P_F 系列读取距离值
#   if isinstance(data, dict) and (dis := data.get("dis", 0)) > 0:
#       self.get_logger().info(f"ToFsensor{index} 距离: {dis:.2f} m")
#       publisher.publish(Float32(data=dis))
 
            

    def led_turn_off(self,index):
        self.LED[index].write(False)
        self.LED_timer[index].cancel()
        self.LED_timer[index] = None
        # self.get_logger().info(f'LED{index} trigger off')

    def shutdown_led_delay(self, index):
        # self.get_logger().info(f'LED{index} trigger on')
        self.LED[index].write(True)
        if self.LED_timer[index] is not None:
            self.LED_timer[index].cancel()
            self.LED_timer[index] = None
        self.LED_timer[index] = self.create_timer(1.11, partial(self.led_turn_off, index))