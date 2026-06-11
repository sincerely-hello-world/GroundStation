from PyQt5.QtCore import pyqtSignal, QObject

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Image,CompressedImage
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

from GroundStation.navPoints import *

# 自定义消息和服务的数据类型
from uav_car_interfaces.msg import T265Data
from uav_car_interfaces.srv import ControlService

import cv2
from cv_bridge import CvBridge
import numpy as np
import json,re,threading

class ROS2_bridgeNode(Node, QObject):
    bridge = CvBridge()

    qrcode_image = pyqtSignal(object)
    qrcode  = pyqtSignal(str)
    qr_set = set()                  # 用于快速去重
    qr_order = list()

    qrcode2_image = pyqtSignal(object)

    flycamera_signal = pyqtSignal(str)

    log_signal = pyqtSignal(str)


    cmd_result = pyqtSignal(bool,str)
    flyOdom = pyqtSignal(str,float,float,float,int)
    carOdom = pyqtSignal(float,float)

    pos = None
    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_qrcode_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
 
    def __init__(self,name='Bridge'):
        # super().__init__(name)
        QObject.__init__(self)
        Node.__init__(self, node_name=name)
        self.get_logger().info("ros2 node launch success:%s!" % name)
        
        # 服务
        self.command_client = self.create_client(ControlService,"command_service")# 无人机的控制服务
        self.talk_client  = self.create_client(ControlService, 'talk_service') #无人机的控制节点的服务
        
        # 订阅
        self.topic_uart4_sub_MCU2 = self.create_subscription(String, 'uart_reader4_data_topic', self.MCU2_callback,10)
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.fly_odom_callback, 10,callback_group=self.topic_t265_cb_group)
        self.topic_qrcode_sub = self.create_subscription(String,"qrcode_data_topic",self.qrcode_callback,10 ,callback_group=self.topic_qrcode_cb_group)
        self.topic_fly_camera_sub = self.create_subscription(Point, 'fly/camera/data', self.fly_camera_callback, 10,  callback_group=self.topic_qrcode_cb_group)
        self.car_odom_sub = self.create_subscription(Odometry, 'car/odom', self.car_odom_callback, 10) # 消防车里程计 
            # debug
        self.log_topic_sub = self.create_subscription(String,"log_topic",self.log_topic_callback,10 ,callback_group=self.topic_qrcode_cb_group)
        

        # self.topic_qrcode_compressedimage_sub   =self.create_subscription(CompressedImage,"/image/image_qrcode/compressed",self.qrcode_compressedimage_callback,10 ,callback_group=self.img_cb_group)
        # self.topic_qrcode_image_sub =self.create_subscription(Image,"/image/image_qrcode",self.qrcode_image_callback,10 ,callback_group=self.img_cb_group)
        # def qrcode_image_callback(self, msg):
        #     cv_qrimage = self.bridge.imgmsg_to_cv2(msg,desired_encoding="rgb8")
        #     self.qrcode_image.emit(cv_qrimage)

 
        # 发布
        self.topic_flyServo_pub = self.create_publisher(String,'fly/servo10',  10) # 投放用的duoji #10外侧 # 30内侧
        self.car_control_pub = self.create_publisher(String, 'car/driver/control', 10)# stopCar, unlockCar 前往某个目标点 等指令,暂时不写手动控制了，没必要，只留个停止/启动即可
        self.car_cmd_vel_pub = self.create_publisher(Twist, 'car/driver/cmd_vel', 10) #线速度控制，仅手动 比较抽象不写了
        self.car_fireArea_pub = self.create_publisher(String,'fire/area',  10) # 

    def fly_camera_callback(self, msg: Point):
        # Point 类型的坐标直接访问
        # self.flycamera_data = msg  # 或者保存整个 msg
        data_str = f'火源偏移: x={msg.x:4.2f},y={msg.y:4.2f}'  # ✅ 直接使用 msg.x, msg.y
        self.flycamera_signal.emit(data_str)
        self.get_logger().info(f'bridgenode-无人机flycam_data: {data_str}')
    def qrcode_callback(self, msg:String):
        return
        qrcode = msg.data
        self.get_logger().info(f"qrcode 识别到QR码: {qrcode}")
        self.qrcode.emit(qrcode)
    def MCU2_callback(self, msg: String):
        self.MCU2msg = msg
        # self.get_logger().info(f'MCU2 send back: {msg.data}')

    def car_odom_callback(self, msg: Odometry):
        # 接收里程计数据，更新位置即可
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.carOdom.emit(x, y)
        # self.get_logger().info(f'car_odom_callback: {x:6.3f}, {y:6.3f}')

    def log_topic_callback(self, msg: String):
        var_json = json.loads(msg.data)
        label = var_json.get('label', '没有label这个键值对')
        info = var_json.get('info', '没有info这个键值对')

        self.get_logger().info(f'bridge-log: 标签: {label}, 信息: {info}')

        if label=='fly' and info =='over':
            self.log_signal.emit(f"无人机: 无人机巡航结束")
        elif label=='fly' and info =='start':
            self.log_signal.emit(f"无人机: 无人机巡航开始")
        elif label=='car' and info =='over':
            self.log_signal.emit(f"消防车: 消防车灭火结束")
        elif label=='car' and info =='start':
            self.log_signal.emit(f"消防车: 消防车灭火开始")
        else:
            self.log_signal.emit(f"{label}: {info}")
        
    def fly_odom_callback(self, msg: T265Data): # topic_t265_sub的回调函数，接收T265Data消息并更新位置信息
        info = f"X:{msg.pos_x+0.0:+6.3f}m, Y:{msg.pos_y+0.0:+6.3f}m, Z:{msg.pos_z+0.0:+6.3f}m, C:{msg.confidence}"
        # self.get_logger().debug(info)
        self.pos = msg
        self.flyOdom.emit(info, msg.pos_x, msg.pos_y, msg.pos_z, msg.confidence)

    def send_talk(self, task:String):
        if rclpy.ok() and self.talk_client.service_is_ready()==False:
            err_msg = f"发送 {task} 失败: ROS2 服务 [ControlService] 未启动或超时"
            self.get_logger().error(err_msg)
            return # ！！！非常重要：必须 return，不要往下走 call_async
        # 1️⃣ 先创建 future  # . 只有服务就
        request = ControlService.Request()
        request.req = task
        future = self.talk_client.call_async(request)
        future.add_done_callback(lambda fut: self.talk_future_done(fut, task))
        self.get_logger().info(f"发送 {task} 成功")
    
    def talk_future_done(self, future, task):
        try:
            response = future.result()  # 會 raise 如果有 exception
            info_str = f"{task} 响应成功 → {response.echo}"   
            self.get_logger().info(info_str)
            if response.echo == 'undefined task':
                self.cmd_result.emit(False, f'无人机无效任务{task},请重置任务')
            elif response.echo == 'task is running':
                self.cmd_result.emit(False, f'无人机任务{task}正在执行中,请勿重复执行')
            elif response.echo == 'task is shutdown': # 地面站通知飞机退出程序shitdown-navNode
                # self.cmd_result.emit(False, f'任务{task}已退出')
                pass
            elif response.echo == 'task is reset ':
                self.cmd_result.emit(False, f'无人机任务重置完成')

        except Exception as e:
            err_msg = f"{task} 响应失败: {str(e)}"
            self.cmd_result.emit(False, err_msg)
            self.get_logger().error(err_msg)

    def send_command(self, cmd:String):
        if rclpy.ok() and self.command_client.service_is_ready() == False:
            err_msg = f"发送 {cmd} 失败: ROS2 服务 [ControlService] 未启动或超时"
            self.get_logger().error(err_msg)
            self.cmd_result.emit(False, err_msg)
            return # ！！！非常重要：必须 return，不要往下走 call_async
        # 1️⃣ 先创建 future  # . 只有服务就绪了，才执行后续发送逻辑
        request = ControlService.Request()
        request.req = cmd
        future = self.command_client.call_async(request)
        future.add_done_callback(lambda fut: self.command_future_done(fut, cmd))
    
    def command_future_done(self, future, original_cmd):
        # 這段會在 executor 的 thread 執行（非主執行緒）
        try:
            response = future.result()  # 會 raise 如果有 exception
            info_str = f"{original_cmd} 发送成功 → {response.echo}"   
            # self.cmd_result.emit(True, info_str) #cheng gong bu tanchuang
            self.get_logger().info(info_str)
        except Exception as e:
            err_msg = f"{original_cmd} 发送失敗: {str(e)}"
            self.cmd_result.emit(False, err_msg)
            self.get_logger().error(err_msg)


    def qrcode_compressedimage_callback(self, msg):
        ## compressedimage bridge method
        # cv_qrimage=self.bridge.compressed_imgmsg_to_cv2(msg)
        
        ## compressedimage cv2 method
        nparr = np.frombuffer(msg.data, np.uint8)
        cv_qrimage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv_qrimage = cv2.cvtColor(cv_qrimage, cv2.COLOR_BGR2RGB)               
        self.qrcode_image.emit(cv_qrimage)
    def qrcode_compressedimage2_callback(self, msg):
        ## compressedimage bridge method
        # cv_qrimage=self.bridge.compressed_imgmsg_to_cv2(msg)
        
        ## compressedimage cv2 method
        nparr = np.frombuffer(msg.data, np.uint8)
        cv_qrimage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv_qrimage = cv2.cvtColor(cv_qrimage, cv2.COLOR_BGR2RGB)               
        self.qrcode2_image.emit(cv_qrimage)

def start_ros2Node_spin(node_list):
    """
    启动一个 MultiThreadedExecutor，管理多个 ROS 2 节点。
    
    :param node_list: List of rclpy.Node instances
    """
    if not node_list:
        raise ValueError("node_list 不能为空")

    executor = rclpy.executors.MultiThreadedExecutor(num_threads = 4)
    
    # 将所有节点添加到 executor
    for node in node_list:
        executor.add_node(node)

    try:
        executor.spin()  # 阻塞运行，直到被中断
    finally:
        # 清理资源：先移除节点，再销毁
        for node in node_list:
            executor.remove_node(node)
            node.destroy_node()
        rclpy.shutdown()