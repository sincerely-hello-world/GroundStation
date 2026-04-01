from PyQt5.QtCore import pyqtSignal, QObject

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup,ReentrantCallbackGroup
from std_msgs.msg import String
from sensor_msgs.msg import Image,CompressedImage

# 自定义消息和服务的数据类型
from uav_car_interfaces.msg import T265Data
from uav_car_interfaces.srv import ControlService

import threading

import cv2
from cv_bridge import CvBridge
import numpy as np

class ROS2_bridgeNode(Node, QObject):
    bridge = CvBridge()

    qrcode_image = pyqtSignal(object)
    qrcode = pyqtSignal(str,list)
    qr_set = set()                  # 用于快速去重
    qr_order = list()
    

    cmd_result = pyqtSignal(bool,str)
    position = pyqtSignal(str,float,float,float,int)
    pos = None
    

    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
 
    def __init__(self,name='Ground'):
        # super().__init__(name)
        QObject.__init__(self)
        Node.__init__(self, name)
        self.get_logger().info("ros2 node launch success:%s!" % name)
        
  
        self.client_command = self.create_client(ControlService,"command_service")
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.position_callback, 10,callback_group=self.topic_t265_cb_group)
        self.topic_qrcode_sub = self.create_subscription(String,"qrcode_data_topic",self.qrcode_callback,10 ,callback_group=self.topic_cb_group)
        self.topic_qrcode_image_sub =self.create_subscription(Image,"/image/image_qrcode",self.qrcode_image_callback,10 ,callback_group=self.img_cb_group)
        self.topic_qrcode_compressedimage_sub =self.create_subscription(CompressedImage,"/image/image_qrcode/compressed",self.qrcode_compressedimage_callback,10 ,callback_group=self.img_cb_group)
        
        self.topic_uart4_pub_MCU2 = self.create_publisher(String, 'uart_sender4_data_topic',10)
        self.topic_uart4_sub_MCU2 = self.create_subscription(String, 'uart_reader4_data_topic', self.MCU2_callback,10)

    def MCU2_callback(self, msg: String):
        self.MCU2msg = msg
        self.get_logger().info(f'MCU2 send back: {msg.data}')


    def position_callback(self, msg: T265Data): # topic_t265_sub的回调函数，接收T265Data消息并更新位置信息
        info = f"X:{msg.pos_x+0.0:+6.3f}m, Y:{msg.pos_y+0.0:+6.3f}m, Z:{msg.pos_z+0.0:+6.3f}m, C:{msg.confidence}" #H:{msg.tof_z+0.0:+6.3f}"
        # self.get_logger().info(info)
        self.pos = msg
        self.position.emit(info, msg.pos_x, msg.pos_y, msg.pos_z, msg.confidence)

    
    def send_command(self, cmd:String):
        if rclpy.ok() and self.client_command.wait_for_service(timeout_sec = 0.15)==False:
            err_msg = f"发送 {cmd} 失败: ROS2 服务 [ControlService] 未启动或超时"
            self.get_logger().error(err_msg)
            self.cmd_result.emit(False, err_msg)
            return # ！！！非常重要：必须 return，不要往下走 call_async
        # 1️⃣ 先创建 future  # . 只有服务就绪了，才执行后续发送逻辑
        request = ControlService.Request()
        request.req = cmd
        future = self.client_command.call_async(request)
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

    def qrcode_callback(self, msg:String):
        qrcode = msg.data
        if self.pos is not None:
            if self.pos.pos_x > 1.35 :
                if qrcode not in self.qr_set:
                    self.qr_set.add(qrcode)
                    self.qr_order.append(qrcode)

        self.get_logger().info(f"识别到QR码: {qrcode}")
        self.qrcode.emit(qrcode, self.qr_order)

    def qrcode_image_callback(self, msg):
        # image
        cv_qrimage = self.bridge.imgmsg_to_cv2(msg,desired_encoding="rgb8")
        self.qrcode_image.emit(cv_qrimage)

    def qrcode_compressedimage_callback(self, msg):
        # compressedimage bridge m
        # cv_qrimage=self.bridge.compressed_imgmsg_to_cv2(msg)
        
        # compressedimage cv2 m
        nparr = np.frombuffer(msg.data, np.uint8)
        cv_qrimage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # self.get_logger().info(f"ok: image")
        cv_qrimage = cv2.cvtColor(cv_qrimage, cv2.COLOR_BGR2RGB)               
        self.qrcode_image.emit(cv_qrimage)

def start_bridgeNode_spin(node):
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.remove_node(node)
        node.destroy_node()
        rclpy.shutdown()