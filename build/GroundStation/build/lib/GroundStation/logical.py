import sys
 
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QDialog
from PyQt5.QtCore import pyqtSignal, QObject

from Ui_main import Ui_MainWindow
from Ui_subDialog1 import Ui_Dialog

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

# 自定义消息和服务的数据类型
from uav_car_interfaces.msg import T265Data
from uav_car_interfaces.srv import ControlService

import threading

class ROS2NodeClass(Node):
    def __init__(self,name):
        super().__init__(name)
        QObject.__init__(self)
        Node.__init__(self, 'ground_station_node')
        self.get_logger().info("ros2 node launch success:%s!" % name)

        self.pos = T265Data()
        self.client_command = self.create_client(ControlService,"command_service",10)
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.position_callback)

    def position_callback(self, msg: T265Data):
        self.pos = msg
        self.get_logger().info(
                    f't265 confidence:[{self.pos.confidence:1d}], '
                    f'pos(x:{self.pos.pos_x:+6.3f}m, y:{self.pos.pos_y:+6.3f}m), '
                    f'h[{self.pos.pos_z:+6.3f}m]')
        
    def send_command(self, cmd):
        while rclpy.ok() and self.client_command.wait_for_service(timeout_sec = 1.0)==False:
            self.get_logger().info(f"Wait for the command server online....")
        
        request = ControlService.Request()
        request.req = cmd
        self.client_command.call_async(request).add_done_callback(self.command_callback)

    def command_callback(self, future):
        response = future.result()
        self.get_logger().info(f"G command response: {response.echo}")


class MyMainUI(QMainWindow,Ui_MainWindow): #继承主窗口函数的类, 继承编写的主函数
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化运行A窗口类下的 setupUi 函数
        self.setWindowTitle("无人机地面站")
        self.SubDialog1 = SubDialog1()
        self.pushButton_openDialog1.clicked.connect(self.SubDialog1.show)

class SubDialog1(QDialog ,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化运行B窗口类下的 setupUi 函数
        self.setWindowTitle("地面站-手动控制对话框")
        self.pushButton_closeDialog.clicked.connect(self.close) #窗口2 中的关闭按钮


def main():
    app = QApplication(sys.argv)
    mui = MyMainUI()
 
    # mui.pushButton_openDialog1.clicked.connect(D1.show) #窗口1的打开窗口按钮
    
    mui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
 

# ————————————————
# 版权声明：本文为CSDN博主「leangfu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u014041346/article/details/83684106