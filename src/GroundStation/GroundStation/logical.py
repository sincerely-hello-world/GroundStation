import sys,threading
 
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QDialog,QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QObject,QTimer,Qt

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
        self.setupUi(self)
        self.setWindowTitle(name)

        self.subdialog1 = subDialog1() # 创建子窗口1类的实例
        self.showdialog = showDialog()

        if not rclpy.ok():
            rclpy.init()
        self.ros_node = ROS2_bridgeNode("Ground") # 创建ROS2节点类的实例，节点名称为"Ground" # 主窗口持有 ros2 node的实例，方便在主窗口中调用ROS2节点的方法

        # self.label_qrcode_image.setScaledContents(True)          # ← 关键！让图片自动缩放填充 label
        # self.label_qrcode_image.setAlignment(Qt.AlignCenter)     # 可选：居中
        self.lineEdit_status.setText("等待无人机上线")
        self.pushButton_takeoff.setEnabled(False)

        # ✅ 在这里连接：主界面的按钮 → 子窗口的 show
        # self.pushButton_openDialog1.clicked.connect(self.subdialog1.show)
        self.pushButton_takeoff.clicked.connect(lambda: self.ros_node.send_command("takeoff"))
        self.pushButton_land.clicked.connect(lambda: self.ros_node.send_command("land"))

        self.pushButton_runtask.clicked.connect(self.showdialog.show)#("@L03[+1234-7774+8651|+2345-8888+9999|+0001-0002+0003|]"))
        self.pushButton.clicked.connect(self.takeoff_confirm)
        
        self.actionHand.triggered.connect(self.subdialog1.show)
        
        # ✅ 在这里连接：subDialog1界面的按钮 → ROS2节点的方法    手动遥控器界面 
        self.subdialog1.pushButton_stopland.clicked.connect(lambda: self.ros_node.send_command("land"))
        self.subdialog1.pushButton_forward.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x+0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_back.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x-0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_left.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x, self.pos.y+0.2, self.pos.z,'')))
        self.subdialog1.pushButton_right.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x, self.pos.y-0.2, self.pos.z,'')))
        self.subdialog1.pushButton_hover.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_down.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x, self.pos.y, self.pos.z-0.13,'')))
        self.subdialog1.pushButton_up.clicked.connect(lambda: self.ros_node.send_command(TGformat('G',self.pos.x, self.pos.y, self.pos.z+0.13,'')))


        # ✅ 在这里连接：subDialog2界面的按钮 → ROS2节点的方法
        self.showdialog.pushButton_ok.clicked.connect(self.close_temp)

        # 固定二维码显示区域，避免图片刷新时 label 自发拉伸变化大小
        ## self.label_qrcode_image.setFixedSize(800, 800)
        ## self.label_qrcode_image.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # self.label_qrcode_image.setScaledContents(True)
        # self.label_qrcode_image.setAlignment(Qt.AlignCenter)
        self.showMaximized()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_qrcode_image)
        # self.timer.start(30)  # 约33fps

        # ✅ 在这里连接： ROS2发来的信号
        self.ros_node.qrcode.connect(self.update_qrcode)
        self.ros_node.qrcode_image.connect(self.update_qrcode_image)
        self.ros_node.cmd_result.connect(self.info_cmd_result)
        self.ros_node.position.connect(self.update_pos)

        self.ros2_thread = threading.Thread(target=start_bridgeNode_spin, args=(self.ros_node,),daemon=True)
        self.ros2_thread.start()
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
    def close_temp(self):
        self.showdialog.hide()
        QMessageBox.information(self,'参数设置',"参数设置成功")
        
    def update_pos(self, info, x,y,z,confidence):
        self.lineEdit_pos.setText(info)
        self.subdialog1.lineEdit_pos.setText(info)
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z
        self.confidence = confidence
        

    def info_cmd_result(self, success:bool, info:str):
        self.ros_node.get_logger().error('fail')
        if not success:
            QMessageBox.warning(self,'ros2指令发送失败',info)
        # else:
        #     QMessageBox.information(self,title='ros2指令发送成功',text=info)
        
    def update_qrcode(self,qrcode:str,qrcode_order:list):
        if qrcode_order:
            lines = [f"{i+1}. {item}" for i, item in enumerate(qrcode_order)]
            text = "\n".join(lines)
            self.plainTextEdit_qrcode_order.setPlainText(text)
        self.lineEdit_qrcode.setText(qrcode)
        
    
        
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

    def updatePosition(self, strings: str):
        self.lineEdit_pos.setText(strings)

    def closeEvent(self, event):
        if self.subdialog1.isVisible():
            self.subdialog1.close() # 关闭子窗口
        self.ros2_thread.join(timeout=0.5)  # 最多等2秒
        event.accept()

class subDialog1(QDialog ,Ui_subDialog1):
    def __init__(self,name="地面站-手动控制对话框"):
        super().__init__()
        self.setupUi(self)  # 初始化运行B窗口类下的 setupUi 函数
        self.setWindowTitle(name)
        # self.pushButton_closeDialog.clicked.connect(self.close) #窗口2 中的关闭按钮

class showDialog(QDialog ,Ui_showDialog):
    def __init__(self,name="参数设置对话框"):
        super().__init__()
        self.setupUi(self)  # 初始化运行B窗口类下的 setupUi 函数
        self.setWindowTitle(name)
        self.pushButton_cannel.clicked.connect(self.close)

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