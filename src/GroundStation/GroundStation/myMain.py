import sys,threading
 
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QDialog,QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QObject,QTimer,Qt,QThread

from GroundStation.myUI import *
from GroundStation.myFunction import *

from GroundStation.bridgeNode import *

class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0, confidence=0):
        self.x = x
        self.y = y
        self.z = z
        self.confidence = confidence

class UIController(QMainWindow, Ui_MainWindow):   # UIController类同时继承了QMainWindow和Ui_MainWindow，负责管理主窗口的UI和ROS2节点
    pos = Point()
    def __init__(self, name="无人机地面站GroundStation"):
        super().__init__()
        if not rclpy.ok():
            rclpy.init()
        self.setupUi(self)
        self.setWindowTitle(name)

        self.subdialog1 = subDialog1() # 创建子窗口1类的实例
        self.bridge_node = ROS2_bridgeNode("Ground") # 创建ROS2节点类的实例，节点名称为"Ground" # 主窗口持有 ros2 node的实例，方便在主窗口中调用ROS2节点的方法


        self.LED_blink_timer = QTimer()
        self.LED_blink_timer.timeout.connect(self.LED_blink_timer_callback)
        self.LED_stop_timer = QTimer()
        self.LED_stop_timer.setSingleShot(True)      # 单次触发
        self.LED_stop_timer.timeout.connect(self.LED_stop_timer_callback)
        self.LED_toggle = False





        # self.label_qrcode_image.setScaledContents(True)          # ← 关键！让图片自动缩放填充 label
        # self.label_qrcode_image.setAlignment(Qt.AlignCenter)     # 可选：居中
        self.lineEdit_status.setText("等待无人机上线")
        self.pushButton_takeoff.setEnabled(False)

        # ✅ 在这里连接：主界面的按钮 → 子窗口的 show
        # self.pushButton_openDialog1.clicked.connect(self.subdialog1.show)
        self.pushButton_takeoff.clicked.connect(lambda: self.bridge_node.send_command("takeoff"))
        self.pushButton_land.clicked.connect(lambda: self.bridge_node.send_command("land"))
        self.pushButton_runtask.clicked.connect(lambda: self.bridge_node.send_talk("scan_all"))
        self.pushButton.clicked.connect(self.takeoff_confirm)
        self.pushButton_search.clicked.connect(self.search_qrcode) # todo 搜索功能

        
        
        # ✅ 在这里连接：subDialog1界面的按钮 → ROS2节点的方法    手动遥控器界面 
        self.actionHand.triggered.connect(self.subdialog1.show)
        self.subdialog1.pushButton_stopland.clicked.connect(lambda: self.bridge_node.send_command("land"))
        self.subdialog1.pushButton_forward.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x+0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_back.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x-0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_left.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y+0.2, self.pos.z,'')))
        self.subdialog1.pushButton_right.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y-0.2, self.pos.z,'')))
        self.subdialog1.pushButton_hover.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_down.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z-0.13,'')))
        self.subdialog1.pushButton_up.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z+0.13,'')))

        self.showMaximized()
 

        # ✅ 在这里连接： ROS2发来的信号
        self.bridge_node.qrcode.connect(self.update_qrcode)
        self.bridge_node.qrcode_image.connect(self.update_qrcode_image)
        self.bridge_node.qrcode2.connect(self.update_qrcode2)
        self.bridge_node.qrcode2_image.connect(self.update_qrcode2_image)

        self.bridge_node.cmd_result.connect(self.info_cmd_result)
        self.bridge_node.position.connect(self.update_pos)

        self.bridge_node.qrcode_result.connect(self.showQRresult) # todo 监听二维码结果
        self.bridge_node.qrcode_result.connect(self.LED_trigger,) # todo 监听二维码结果

        self.ros2_thread = QThread()
        self.ros2_thread = threading.Thread(target=start_ros2Node_spin, args=([self.bridge_node],),daemon=True,name="ROS2_Bridge_Spin_Thread")
        self.ros2_thread.start()

    def LED_trigger(self):
        print("触发LED闪烁（可重复触发重置）")
        self.LED_blink_timer.setInterval(200)
        self.LED_blink_timer.start()
        self.LED_stop_timer.start(1700) # 1500毫秒后停止
    def LED_blink_timer_callback(self):
        self.LED_toggle = not self.LED_toggle
        if self.LED_toggle:
            self.pushButton_LED.setStyleSheet("background-color: gray; color: rgb(0, 0, 0);")
        else:
            self.pushButton_LED.setStyleSheet("background-color: green;  color: rgb(0, 0, 0);")
    def LED_stop_timer_callback(self):
        self.LED_blink_timer.stop()
        self.pushButton_LED.setStyleSheet("background-color: gray; color: rgb(0, 0, 0);")


    def takeoff_confirm(self):
        if self.confidence > 0 and self.confidence < 3:
            QMessageBox.warning(self,'起飞确认',"请初始化惯性导航仪")
            self.lineEdit_status.setText("已成功连接无人机，等待起飞确认")
        elif self.confidence == 3:
            QMessageBox.information(self,'起飞确认',"无人机就绪，允许起飞")
            self.lineEdit_status.setText("无人机就绪，允许起飞")
            self.pushButton_takeoff.setEnabled(True)
        else:
            QMessageBox.warning(self,'起飞确认',"请等待无人机初始化")        
    def update_pos(self, info, x,y,z,confidence):
        self.lineEdit_pos.setText(info)
        self.subdialog1.lineEdit_pos.setText(info)
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z
        self.confidence = confidence
        

    def info_cmd_result(self, success:bool, info:str):
        self.bridge_node.get_logger().error('fail')
        if not success:
            QMessageBox.warning(self,'ros2指令发送失败',info)
        # else:
        #     QMessageBox.information(self,title='ros2指令发送成功',text=info)
    
    def search_qrcode(self):
        search = self.lineEdit_search.text()
        result = self.bridge_node.qrcode_result_dict.get(search, f"查询失败，未找到{search}位置的QR码")
        self.bridge_node.get_logger().info(f'查询到{search}位置放的二维码是:{result}')
        self.lineEdit_search_result.setText(result)
    def showQRresult(self,data:str):
        self.textEdit_qrresult.append(data)
        # 自动滚动到底部
        scrollbar = self.textEdit_qrresult.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_qrcode(self,qrcode:str,qrcode_order:list):
        self.lineEdit_qrcode.setText(qrcode)
    def update_qrcode2(self,qrcode:str,qrcode_order:list):
        self.lineEdit_qrcode2.setText(qrcode)
    
        
    def update_qrcode_image(self, cv_img):
        if cv_img is None:
            return
        # 做一次 copy （雖然 emit 後通常已經是新的物件）
        arr = cv_img
        height, width, channels = arr.shape
        bytes_per_line = channels * width
        qimage = QImage(
            arr.data, width, height, bytes_per_line,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(qimage)
        # 可選：縮放到 label 大小，保持比例
        pixmap = pixmap.scaled(
            self.label_qrcode_image.width(),
            self.label_qrcode_image.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_qrcode_image.setPixmap(pixmap)
    def update_qrcode2_image(self, cv_img):
        if cv_img is None:
            return
        # 做一次 copy （雖然 emit 後通常已經是新的物件）
        arr = cv_img
        height, width, channels = arr.shape
        bytes_per_line = channels * width
        qimage = QImage(
            arr.data, width, height, bytes_per_line,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(qimage)
        # 可選：縮放到 label 大小，保持比例
        pixmap = pixmap.scaled(
            self.label_qrcode_image.width(),
            self.label_qrcode_image.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_qrcode2_image.setPixmap(pixmap)
    def updatePosition(self, strings: str):
        self.lineEdit_pos.setText(strings)

    def closeEvent(self, event):
        if self.subdialog1.isVisible():
            self.subdialog1.close() # 关闭子窗口
        self.bridge_node.send_talk('shutdown-navNode')
        self.ros2_thread.join(timeout=0.5)  # 最多等2秒
        event.accept()

class subDialog1(QDialog ,Ui_subDialog1):
    def __init__(self,name="地面站-手动控制对话框"):
        super().__init__()
        self.setupUi(self)  # 初始化运行B窗口类下的 setupUi 函数
        self.setWindowTitle(name)
        # self.pushButton_closeDialog.clicked.connect(self.close) #窗口2 中的关闭按钮

def main():
  
    app = QApplication(sys.argv)
    uiC = UIController()

    uiC.show()

    exit_code = app.exec_() # 进入Qt事件循环，等待用户操作，直到窗口关闭后退出循环
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
    
 

# ————————————————
# 版权声明：本文为CSDN博主「leangfu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u014041346/article/details/83684106