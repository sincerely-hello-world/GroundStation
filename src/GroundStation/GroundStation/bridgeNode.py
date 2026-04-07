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

import cv2
from cv_bridge import CvBridge
import numpy as np
import json,re,threading

class ROS2_bridgeNode(Node, QObject):
    bridge = CvBridge()

    qrcode_image = pyqtSignal(object)
    qrcode  = pyqtSignal(str,list)
    qr_set = set()                  # 用于快速去重
    qr_order = list()

    qrcode2_image = pyqtSignal(object)
    qrcode2 = pyqtSignal(str,list)
    qr_set2 = set()                  # 用于快速去重
    qr_order2 = list()

    qrcode_result = pyqtSignal(str)
    qrcode_result_dict = dict()
   
    cmd_result = pyqtSignal(bool,str)
    position = pyqtSignal(str,float,float,float,int)
    pos = None
    
    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_qrcode_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
 
    def __init__(self,name='Ground'):
        # super().__init__(name)
        QObject.__init__(self)
        Node.__init__(self, name)
        self.get_logger().info("ros2 node launch success:%s!" % name)
        
  
        self.command_client = self.create_client(ControlService,"command_service")
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.position_callback, 10,callback_group=self.topic_t265_cb_group)
        self.topic_qrcode_sub = self.create_subscription(String,"qrcode_data_topic",self.qrcode_callback,10 ,callback_group=self.topic_qrcode_cb_group)
        self.topic_qrcode2_sub = self.create_subscription(String,"qrcode2_data_topic",self.qrcode2_callback,10 ,callback_group=self.topic_qrcode_cb_group)

        self.topic_qrcode_compressedimage_sub   =self.create_subscription(CompressedImage,"/image/image_qrcode/compressed",self.qrcode_compressedimage_callback,10 ,callback_group=self.img_cb_group)
        self.topic_qrcode2_compressedimage_sub =self.create_subscription(CompressedImage,"/image/image_qrcode2/compressed",self.qrcode_compressedimage2_callback,10 ,callback_group=self.img_cb_group)

        self.topic_qrcode_result_sub = self.create_subscription(String,"qrcode_result_topic",self.qrcode_result_callback,10 ,callback_group=self.topic_qrcode_cb_group)
        # self.topic_qrcode_image_sub =self.create_subscription(Image,"/image/image_qrcode",self.qrcode_image_callback,10 ,callback_group=self.img_cb_group)
            # def qrcode_image_callback(self, msg):
            #     cv_qrimage = self.bridge.imgmsg_to_cv2(msg,desired_encoding="rgb8")
            #     self.qrcode_image.emit(cv_qrimage)

        self.topic_uart4_sub_MCU2 = self.create_subscription(String, 'uart_reader4_data_topic', self.MCU2_callback,10)

        self.talk_client  = self.create_client(ControlService, 'talk_service')

    def MCU2_callback(self, msg: String):
        self.MCU2msg = msg
        self.get_logger().info(f'MCU2 send back: {msg.data}')

    def qrcode_result_callback(self, msg: String):
        self.get_logger().info(f'qrcode_result_callback: {msg.data}')
        json_decoded = json.loads(msg.data)
        self.qrcode_result_dict[json_decoded['label']] = json_decoded['qrcode']
        self.qrcode_result.emit(f"货架位置: {json_decoded['label']},  对应的QR码: {json_decoded['qrcode']}")

    def position_callback(self, msg: T265Data): # topic_t265_sub的回调函数，接收T265Data消息并更新位置信息
        info = f"X:{msg.pos_x+0.0:+6.3f}m, Y:{msg.pos_y+0.0:+6.3f}m, Z:{msg.pos_z+0.0:+6.3f}m, C:{msg.confidence}" #H:{msg.tof_z+0.0:+6.3f}"
        self.get_logger().debug(info)
        self.pos = msg
        self.position.emit(info, msg.pos_x, msg.pos_y, msg.pos_z, msg.confidence)

    def send_talk(self, cmd:String):
        if rclpy.ok() and self.talk_client.service_is_ready()==False:
            err_msg = f"发送 {cmd} 失败: ROS2 服务 [ControlService] 未启动或超时"
            self.get_logger().error(err_msg)
            return # ！！！非常重要：必须 return，不要往下走 call_async
        # 1️⃣ 先创建 future  # . 只有服务就
        request = ControlService.Request()
        request.req = cmd
        future = self.talk_client.call_async(request)
        future.add_done_callback(lambda fut: self.talk_future_done(fut, cmd))
        self.get_logger().info(f"发送 {cmd} 成功")
    
    def talk_future_done(self, future, talk):
        try:
            response = future.result()  # 會 raise 如果有 exception
            info_str = f"{talk} 响应成功 → {response.echo}"   
            self.get_logger().info(info_str)
        except Exception as e:
            err_msg = f"{talk} 响应失败: {str(e)}"
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

    def qrcode_callback(self, msg:String):
        qrcode = msg.data
        # if self.pos is not None:
        #     if self.pos.pos_x > 1.35 :
        #         if qrcode not in self.qr_set:
        #             self.qr_set.add(qrcode)
        #             self.qr_order.append(qrcode)
        self.get_logger().info(f"qrcode 识别到QR码: {qrcode}")
        self.qrcode.emit(qrcode, self.qr_order)
    def qrcode2_callback(self, msg:String):
        qrcode = msg.data
        self.get_logger().info(f"qrcode2 识别到QR码: {qrcode}")
        self.qrcode2.emit(qrcode, self.qr_order2)
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