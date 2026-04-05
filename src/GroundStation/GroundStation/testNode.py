
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rcl_interfaces.msg import SetParametersResult
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.parameter import Parameter
from std_srvs.srv import Empty
from std_msgs.msg import String
# 自定义消息和服务的数据类型
from uav_car_interfaces.msg import T265Data
from uav_car_interfaces.srv import ControlService

from dataclasses import dataclass

from GroundStation.myFunction import *
import json
import os
from typing import List


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.7, label: str = '',qrcode: str = ''):
        self.x = x      # 单位：米
        self.y = y
        self.z = z
        self.label = label
        self.qrcode = qrcode

@dataclass(frozen=True)  # frozen=True 开启只读模式
class myStatus:
    INIT :str = 'INIT'
    SEND :str = 'SEND'
    DELAY :str = 'DELAY'
    END :str = 'END'
 

class testNode(Node):

    pos = T265Data()
    aim = Point() # 路径目标点

    状态 = myStatus()
    status = ''


    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
    topic_qrcode_cb_group=MutuallyExclusiveCallbackGroup()
    def __init__(self, name = 'testNode'):
        super().__init__(node_name=name)
        # parameters
        self.declare_parameter('test', '')
        self.declare_parameter('paths_scan_all', '')    
         
        self.test = self.get_parameter('test').value
        self.paths_scan_all_str = self.get_parameter('paths_scan_all').value

        if self.paths_scan_all_str is not None:
            self.path_scan_all_json = json.loads(self.paths_scan_all_str)
            self.paths: List[Point] = [
                Point(
                    x=float(p['x']),
                    y=float(p['y']),
                    z=float(p['z']),
                    label=str(p['label']),
                    qrcode=str(p['qrcode']),
                )
                for p in self.path_scan_all_json
            ]
            self.get_logger().info(f'paths: {self.paths_scan_all_str}')
        #----------------------

        
        self.topic_t265_pub = self.create_publisher(T265Data,"t265_data_topic", 10,callback_group=self.topic_t265_cb_group)
        self.topic_uart4_pub_MCU2 = self.create_publisher(String, 'uart_reader4_data_topic',10)

        self.topic_qrcode_pub = self.create_publisher(String,"qrcode_data_topic",10 ,callback_group=self.topic_qrcode_cb_group)
        self.topic_qrcode2_pub = self.create_publisher(String,"qrcode2_data_topic",10 ,callback_group=self.topic_qrcode_cb_group)  

        self.get_logger().info('测试节点启动成功')
        self.status = self.状态.INIT
        self.delay_timer = None
        self.path_index = 0
        self.main_timer = self.create_timer(0.1, self.timer_to_publish)

    def timer_to_publish(self):
        self.pos.pos_x = self.aim.x
        self.pos.pos_y = self.aim.y
        self.pos.pos_z = self.aim.z
        self.pos.confidence = 3
        self.topic_t265_pub.publish(self.pos)
        # self.topic_uart4_pub_MCU2.publish(String(data='Gdone*'))
        self.topic_qrcode_pub.publish(String(data='testQRcode'))
        self.topic_qrcode2_pub.publish(String(data='testQRcode'))

        if self.status == self.状态.INIT:
            self.get_logger().info(f"测试点：{self.status}--[{self.aim.label}]")
            self.status = self.状态.SEND
        if self.status == self.状态.SEND:
            self.get_logger().info(f"测试点：{self.status}--[{self.aim.label}]")
            if self.path_index == len(self.paths):
                self.status = self.状态.END
            else:
                self.aim = self.paths[self.path_index]
                self.path_index += 1
                self.status = self.状态.DELAY
        if self.status == self.状态.DELAY:
            self.get_logger().info(f"测试点：{self.status}--[{self.aim.label}]")
            if self.delay_timer is None or self.delay_timer.is_canceled():
                self.delay_timer = self.create_timer(4.0, self.delay_ok_callback)
        if self.status == self.状态.END:
            self.get_logger().info(f"测试点：{self.status}--[{self.aim.label}]")
            self.main_timer.cancel()
            rclpy.shutdown()
    def delay_ok_callback(self):
        self.get_logger().info(f"测试点：{self.status}--[{self.aim.label}]")
        self.status = self.状态.SEND
        self.delay_timer.cancel()
        self.delay_timer = None
def main(args=None):
    rclpy.init(args=args)
    try:
        node = testNode()
        # 使用 executor 更灵活（可替换为 MultiThreadedExecutor）
        executor = MultiThreadedExecutor(num_threads = 2)
        executor.add_node(node)
        try:
            executor.spin()
        except KeyboardInterrupt:
            pass  # 正常退出，不打印 traceback
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    
if __name__ == '__main__':
    main()