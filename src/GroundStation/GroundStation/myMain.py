import sys,threading
 
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QDialog,QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QObject,QTimer,Qt,QThread

from GroundStation.myUI import *
from GroundStation.myFunction import *

from GroundStation.bridgeNode import *


from ament_index_python.packages import get_package_share_directory
import os

 
def get_image_path(img_name: str) -> str:
    """获取安装后的图片绝对路径"""
    pkg_share = get_package_share_directory('GroundStation')   # 你的包名
    return os.path.join(pkg_share, 'imgs', img_name)

class Point: # 飞机的座标点
    def __init__(self, x=0.0, y=0.0, z=0.0, confidence=0):
        self.x = x
        self.y = y
        self.z = z
        self.confidence = confidence

class UIController(QMainWindow, Ui_MainWindow):   # UIController类同时继承了QMainWindow和Ui_MainWindow，负责管理主窗口的UI和ROS2节点
    pos = Point()
    flyTask = None

    def __init__(self, name="无人机地面站GroundStation"):
        super().__init__()
        if not rclpy.ok():
            rclpy.init()
        self.setupUi(self)
        self.setWindowTitle(name)

        self.bridge_node = ROS2_bridgeNode("Ground") # 创建ROS2节点类的实例，节点名称为"Ground" # 主窗口持有 ros2 node的实例，方便在主窗口中调用ROS2节点的方法


        self.pushButton_takeoff.setEnabled(False)
        self.LED_blink_timer = QTimer()
        self.LED_blink_timer.timeout.connect(self.LED_blink_timer_callback)
        self.LED_stop_timer = QTimer()
        self.LED_stop_timer.setSingleShot(True)      # 单次触发
        self.LED_stop_timer.timeout.connect(self.LED_stop_timer_callback)
        self.LED_toggle = False
        self.lineEdit_status.setText("等待无人机上线")
        

        # ✅ 在这里连接：subDialog1界面的按钮 → ROS2节点的方法    飞机手动遥控器界面 
        # self.actionHand.triggered.connect(self.subdialog1.show)
        self.subdialog1 = subDialog1() # 创建子窗口1类的实例
        self.subdialog1.pushButton_fly.clicked.connect(lambda: self.bridge_node.send_command("takeoff"))
        self.subdialog1.pushButton_flyagain.clicked.connect(lambda: self.bridge_node.send_command("takeoff"))
        self.subdialog1.pushButton_stopland.clicked.connect(lambda: self.bridge_node.send_command("land"))
        self.subdialog1.pushButton_landnormal.clicked.connect(lambda: self.bridge_node.send_command("normalland"))
        self.subdialog1.pushButton_forward.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x+0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_back.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x-0.2, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_left.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y+0.2, self.pos.z,'')))
        self.subdialog1.pushButton_right.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y-0.2, self.pos.z,'')))
        self.subdialog1.pushButton_hover.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z,'')))
        self.subdialog1.pushButton_down.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z-0.13,'')))
        self.subdialog1.pushButton_up.clicked.connect(lambda: self.bridge_node.send_command(TGformat('H',self.pos.x, self.pos.y, self.pos.z+0.13,'')))
        self.subdialog1.checkBox.setChecked(True) 
        self.subdialog1.checkBox.stateChanged.connect(self.on_servo_state_changed)
        
        # ✅ 在这里连接：subDialog2界面的按钮 → ROS2节点的方法    消防车手控界面
        self.subdialog2 = subDialog2()
        self.subdialog2.pushButton_runTask.clicked.connect(self.carTaskSet)
        self.subdialog2.pushButton_setTask.clicked.connect(self.carTaskSet)
        self.subdialog2.pushButton_stop.clicked.connect(self.carTaskSet)
        self.subdialog2.pushButton_unlock.clicked.connect(self.carTaskSet)


        # ✅ 在这里连接：主界面的按钮
        # self.pushButton_takeoff.clicked.connect(lambda: self.bridge_node.send_command("takeoff"))
        self.pushButton_land.clicked.connect(lambda: self.bridge_node.send_command("land"))
        
        self.pushButton.clicked.connect(self.takeoff_confirm)
        self.pushButton_reset_task.clicked.connect(lambda: self.Set_Task('reset'))
        self.pushButton_scanall.clicked.connect(lambda: self.Set_Task('scan_all'))
        self.pushButton_runtask.clicked.connect(self.Fly_RunTask)

        # ✅ 在这里连接：tab界面的按钮   子窗体界面的画面 
        self.flyMap =  DroneMapWidget(map_image_path=get_image_path('2023map.png'),title="无人机航迹监控")
        self.carMap =  DroneMapWidget(map_image_path=get_image_path('2023map.png'),title="消防车路径监控")



        # ✅ 在这里连接：tab界面的按钮   子窗体界面的画面 
        self.tabWidget.removeTab(0)         # 删除Designer里的"其他"页面 样板空页面
        self.tabWidget.addTab(self.subdialog1, "无人机手控")
        self.tabWidget.addTab(self.subdialog2, "消防车手控")
        self.tabWidget.addTab(self.flyMap, "无人机航迹图")
        self.tabWidget.addTab(self.carMap, "消防车路径图")
        self.tabWidget.setCurrentIndex(2)  # 索引从0开始


        # ✅ 在这里连接： ROS2发来的信号
        self.ros2_thread = QThread()
        self.ros2_thread = threading.Thread(target=start_ros2Node_spin, args=([self.bridge_node],),daemon=True,name="ROS2_Bridge_Spin_Thread")
        self.ros2_thread.start()
        
        self.bridge_node.qrcode.connect(self.update_qrcode)
        self.bridge_node.cmd_result.connect(self.info_cmd_result)
        self.bridge_node.log_signal.connect(self.showLoggerCallback) # 监听状态信息显示
        self.bridge_node.log_signal.connect(self.LED_trigger)  
        self.bridge_node.log_signal.connect(self.DroneStatus)

        self.bridge_node.flyOdom.connect(self.updateFlyPos)
        self.bridge_node.carOdom.connect(self.updateCarPos)

        # ✅  初始化结束# ✅  初始化结束# ✅  初始化结束
    def carTaskSet(self):
        """统一处理消防车控制事件"""
        sender = self.sender()
        sender_name = sender.objectName()
               
        if sender_name == "pushButton_unlock":
            self.bridge_node.car_control_pub.publish(String(data="unlockCar"))
            QtWidgets.QMessageBox.warning(self, "提示", "正在让小车暂停运动")
 
        if sender_name == "pushButton_stop":
            self.bridge_node.car_control_pub.publish(String(data="stopCar"))
            QtWidgets.QMessageBox.warning(self, "提示", "正在让小车停下运动")
 
        if sender_name in ("pushButton_runTask", "pushButton_setTask"):
            # 用列表推导式收集被勾选的任务
            checked_tasks = [
                task for task, checkbox in [
                    ("A", self.subdialog2.checkBoxA),
                    ("B", self.subdialog2.checkBoxB),
                    ("C", self.subdialog2.checkBoxC),
                    ("D", self.subdialog2.checkBoxD),
                    ("E", self.subdialog2.checkBoxE),
                    ("F", self.subdialog2.checkBoxF),
                ] if checkbox.isChecked()
            ]
            if not checked_tasks:
                QtWidgets.QMessageBox.warning(self, "提示", "请先勾选小车要执行的任务")
                return
            if sender_name == "pushButton_setTask":
                QtWidgets.QMessageBox.information(self, "提示", f"小车设置了任务{checked_tasks}")
                return
            
            QtWidgets.QMessageBox.information(self, "提示", f"小车执行任务{checked_tasks}")
            for task in checked_tasks:
                self.bridge_node.car_fireArea_pub.publish(String(data=task))
            self.bridge_node.car_fireArea_pub.publish(String(data='fireListEnd'))
        

    def Set_Task(self, task:str):
        if task == 'scan_all':
            self.lineEdit_task.setText("无人机:巡航灭火点任务") # 重要，起始信号
            self.flyTask = 'scan_all'
        elif task == 'reset':
            self.bridge_node.send_talk(task)
            self.lineEdit_task.setText('任务重置了，重新设置任务')
    def Fly_RunTask(self):
        if "scan_all" == self.flyTask: # and self.pushButton_takeoff.text() == "可以起飞":
            self.bridge_node.send_talk(self.flyTask)
            self.flyTask = 'scan_all_running'
        elif "scan_all_running" == self.flyTask:
            QMessageBox.warning(self,'警告',"已经启动巡航任务了，请勿重复执行")
        else:
            self.flyTask = None
            QMessageBox.warning(self,'警告',"请设置正确的任务")

    def takeoff_confirm(self):
        if self.pos.confidence < 3 and self.pos.z > 0 :
            QMessageBox.warning(self,'起飞确认',"请初始化惯性导航仪")
            self.lineEdit_status.setText("已成功连接无人机，等待起飞确认")
        elif self.pos.confidence == 3:
            QMessageBox.information(self,'起飞确认',"无人机就绪，允许起飞")
            self.lineEdit_status.setText("无人机就绪，允许起飞")
            self.pushButton_takeoff.setEnabled(False)
            self.pushButton_takeoff.setText("可以起飞")
            self.pushButton_takeoff.setStyleSheet("background-color: green; color: rgb(0, 0, 0);")
        else:
            QMessageBox.warning(self,'起飞确认',"请等待无人机初始化")        


        

    def info_cmd_result(self, success:bool, info:str):
        self.bridge_node.get_logger().error(f'控制指令信息：{info}')
        if not success:
            QMessageBox.warning(self,'警告',info)
        # else:
        #     QMessageBox.information(self,title='ros2指令发送成功',text=info)
    
    def on_servo_state_changed(self, state):
        """处理舵机状态变化的槽函数"""
        if self.subdialog1.checkBox.isChecked():
            self.bridge_node.topic_flyServo_pub.publish(String(data="lock"))
            self.bridge_node.get_logger().info("手动发送指令：锁定舵机，抓住")
            self.bridge_node.log_signal.emit("手动：锁定舵机，抓住")
        else:
            self.bridge_node.topic_flyServo_pub.publish(String(data="unlock"))
            self.bridge_node.get_logger().info("手动发送指令：张开舵机，投放")
            self.bridge_node.log_signal.emit("手动：张开舵机，投放")
    def DroneStatus(self,log:str):
        if "无人机巡航结束" in log:
            self.flyMap.stopUpdate()
            self.bridge_node.get_logger().info("停止更新无人机地图")
            self.bridge_node.log_signal.emit("停止更新无人机地图")
        elif "无人机巡航开始" in log:
            self.flyMap.stopUpdate()
            self.flyMap.clear_trajectory()
            self.flyMap.startUpdate()
            self.bridge_node.get_logger().info("重新更新无人机地图")
            self.bridge_node.log_signal.emit("重新更新无人机地图")
        elif "消防车灭火结束" in log:
            self.carMap.stopUpdate()
            self.bridge_node.get_logger().info("停止更新消防车地图")
            self.bridge_node.log_signal.emit("停止更新消防车地图")
        elif "消防车灭火开始" in log:
            self.carMap.stopUpdate()
            self.carMap.clear_trajectory()
            self.carMap.startUpdate()
            self.bridge_node.get_logger().info("重新更新消防车地图")
            self.bridge_node.log_signal.emit("重新更新消防车地图")
    def updateCarPos(self, x, y):
        self.carMap.update_position(x+1.4, y+0.3)
 
    def updateFlyPos(self, info, x,y,z,confidence):
        self.lineEdit_pos.setText(info)
        self.subdialog1.lineEdit_pos.setText(info)
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z
        self.pos.confidence = confidence
        self.flyMap.update_position(x+0.3,y+0.3)
    def showLoggerCallback(self,data:str):
        self.textEdit_qrresult.append(data)
        # 自动滚动到底部
        scrollbar = self.textEdit_qrresult.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_qrcode(self,qrcode:str):
        self.lineEdit_qrcode.setText(qrcode)
 

    def closeEvent(self, event):
        if self.subdialog1.isVisible():
            self.subdialog1.close() # 关闭子窗口
        self.bridge_node.send_talk('shutdown-navNode') # 停止navNode节点 无人机控制节点
        self.bridge_node.car_control_pub.publish(String(data="stopCar")) # 停止小车控制，让车停下来即可
        self.ros2_thread.join(timeout=0.5)  # 最多等0.5秒
        event.accept()
    def showEvent(self, event):
        # 窗口显示出来后，再加载图片 → 图片就是高清的！
        # 立即固定窗口大小（放在图片更新之后）
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry()
        self.resize(avail.width(), avail.height())
        # self.update_label_img(self.label_qrcode_image, get_image_path('img_map.png'))
        super().showEvent(event)  
        pass
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

    def update_label_img(self, qt_label:object, img_path:str ):
        if img_path is not None:
            # 从文件路径加载（最常用、最推荐）
            pixmap = QPixmap(img_path)
            if pixmap.isNull():
                self.bridge_node.get_logger().warning(f"警告：无法加载图像 {img_path}")
                return
        # 可選：縮放到 label 大小，保持比例
        pixmap = pixmap.scaled(
            qt_label.width(),
            qt_label.height(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        qt_label.setPixmap(pixmap)



## 多重继承 自窗口类 和 窗口类
class subDialog1(QWidget ,Ui_subDialog1):
    def __init__(self,name="地面站-手动控制对话框"):
        super().__init__()
        self.setupUi(self)  # 初始化运行B窗口类下的 setupUi 函数
        self.setWindowTitle(name)
        # self.pushButton_closeDialog.clicked.connect(self.close) #窗口2 中的关闭按钮

class subDialog2(QWidget ,Ui_carControl):
    def __init__(self,name="小车控制窗口"):
        super().__init__()
        self.setupUi(self)  # 运行B窗口类下的 setupUi 函数
        self.setWindowTitle(name)

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
