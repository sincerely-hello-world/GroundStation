import sys,math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsRectItem, QGraphicsSimpleTextItem,QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor, QImage, QFont, QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
 

class DroneMapWidget(QGraphicsView):
    """
    无人机实时轨迹地图子窗口控件
    功能：加载背景地图，实时绘制飞行轨迹与当前位置，支持坐标映射与界面缩放
    """
    # 定义信号，用于接收外部传入的无人机实时经纬度或平面坐标 (x, y)
    update_position_signal = pyqtSignal(float, float)
    
    
    def __init__(self, map_image_path=None, parent=None, mapX=4.8, mapY=4.0, title="无人机航迹地图"):
        super().__init__(parent)
        self.mapX = mapX
        self.mapY = mapY
        self.title = title
        self.now_x = 0
        self.now_y = 0
        self.last_x = 0 # 上一次传入的真实xy坐标值
        self.last_y = 0
        # 存储所有航迹点
        self.track_points = []
        self.pathlength = 0
        # 保存原始图片
        self.original_pixmap = None
        self.init_ui(map_image_path)

    def init_ui(self, map_image_path):
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. 初始化图形视图框架 (直接使用 QGraphicsView 自身)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # 设置视图属性
        self.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿
        self.setRenderHint(QPainter.SmoothPixmapTransform)  # 平滑图片变换
        
        # 关闭滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 背景框和文字，初始时不可见
        self.coord_bg = QGraphicsRectItem()
        self.coord_bg.setBrush(QBrush(QColor(0, 0, 0, 150)))
        self.coord_bg.setPen(QPen(Qt.NoPen))
        self.coord_bg.setZValue(100) # 确保在最上层
        self.scene.addItem(self.coord_bg)

        # 5. 初始化右下角悬浮 HUD 区域
        self.hud_label = QLabel(self)
        # 使用 QSS 设置淡黑色半透明背景、白色字体、圆角和内边距
        self.hud_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);  /* 最后一项 150 是透明度(0-255) */
                color: white;                         /* 白色字体 */
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;                   /* 圆角 */
                padding: 8px;                         /* 内边距 */
            }
        """)
        # 初始化文本
        self.update_hud_display(0, 0, 0,self.title)

        # 设置大小策略，让控件可以自由扩展
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


        # 2. 加载并缩放背景地图
        if map_image_path:
            pixmap = QPixmap(map_image_path)
            if not pixmap.isNull():
                # 保存原始图片
                self.original_pixmap = pixmap
                
                # 初始时缩放到当前控件大小
                current_size = self.size()
                if current_size.width() > 0 and current_size.height() > 0:
                    scaled_pixmap = pixmap.scaled(
                        current_size.width(), 
                        current_size.height(),
                        Qt.IgnoreAspectRatio,  # 完全拉伸填充
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap = pixmap
                
                self.background_item = QGraphicsPixmapItem(scaled_pixmap)
                self.scene.addItem(self.background_item)
                
                # 设置场景的范围与当前控件大小一致
                self.scene.setSceneRect(0, 0, current_size.width(), current_size.height())
        
        # 3. 初始化无人机图标（用红色圆点代替）
        self.drone_icon = QGraphicsEllipseItem(-8, -8, 16, 16)
        self.drone_icon.setBrush(QColor(255, 0, 0))
        self.drone_icon.setPen(QPen(Qt.white, 2))
        self.scene.addItem(self.drone_icon)
        self.drone_icon.setVisible(False)  # 收到第一个坐标前隐藏

        # 4. 初始化飞行轨迹线 (使用 QPainterPath 高效绘制连续路径)
        self.flight_path = QPainterPath() # 绘图坐标轨迹
        self.path_item = QGraphicsPathItem(self.flight_path)
        self.path_item.setPen(QPen(QColor(0, 150, 255), 3))  # 蓝色轨迹线
        self.scene.addItem(self.path_item)

        self.view_width = self.size().width()
        self.view_height = self.size().height()
        # 绑定信号与槽
        self.update_position_signal.connect(self._update_drone_state)


    def update_hud_display(self, x_val, y_val, path_len, title=None):
        if hasattr(self, 'hud_label'):
            """更新右下角 HUD 的数据显示"""
            # 格式化字符串，.2f 保留两位小数
            if title is None:
                text = f"当前位置(x:{x_val:3.2f}, y:{y_val:3.2f})\n当前里程: {path_len:3.2f}\n单位:米"
            else:
                text = f"{title}\n当前位置(x:{x_val:3.2f}, y:{y_val:3.2f})\n当前里程: {path_len:3.2f}\n单位:米"
            self.hud_label.setText(text)
            
            # 必须调用 adjustSize 让标签根据新文本自适应宽高
            self.hud_label.adjustSize()
            
            # 重新计算并移动位置，防止文本变长后溢出边界
            margin = 15
            x = self.width() - self.hud_label.width() - margin
            y = self.height() - self.hud_label.height() - margin
            self.hud_label.move(x, y)
    def resizeEvent(self, event):
        """关键：每次窗口大小改变时，拉伸图片填满整个控件"""
        super().resizeEvent(event)
        self.view_width = self.size().width()
        self.view_height = self.size().height()
        # 确保 hud_label 已经初始化
        # self.update_hud_display( self.now_x, self.now_y, self.pathlength,self.title)
        if hasattr(self, 'hud_label'):
            margin = 15  # 距离右边和下边的边距
            # 计算右下角坐标
            x = self.width() - self.hud_label.width() - margin
            y = self.height() - self.hud_label.height() - margin
            self.hud_label.move(x, y)
            self.update_hud_display( self.now_x, self.now_y, self.pathlength,self.title)
 

        if hasattr(self, 'original_pixmap') and self.original_pixmap and not self.original_pixmap.isNull():
            # 获取当前控件大小
            widget_size = self.size()
            if widget_size.width() > 0 and widget_size.height() > 0:
                # 直接将图片拉伸到控件大小（完全填充）
                scaled_pixmap = self.original_pixmap.scaled(
                    widget_size.width(), 
                    widget_size.height(),
                    Qt.IgnoreAspectRatio,  # 忽略比例，完全拉伸
                    Qt.SmoothTransformation
                )
                
                # 更新图片
                if hasattr(self, 'background_item'):
                    self.background_item.setPixmap(scaled_pixmap)
                    
                    # 更新场景范围
                    self.scene.setSceneRect(0, 0, widget_size.width(), widget_size.height())
                    
                    # 🔥 关键：坐标需要重新映射（如果已有轨迹和无人机）
                    self._remap_coordinates()
    
    def _remap_coordinates(self):
        """当窗口大小改变时，重新映射所有坐标点"""
        if not hasattr(self, 'track_points') or not self.track_points:
            return
        
        # 获取旧的大小（需要保存）
        if not hasattr(self, 'old_size'):
            self.old_size = self.size()
            return
        
        old_width = self.old_size.width()
        old_height = self.old_size.height()
        new_width = self.size().width()
        new_height = self.size().height()
        
        if old_width == 0 or old_height == 0:
            self.old_size = self.size()
            return
        
        # 计算缩放比例
        scale_x = new_width / old_width
        scale_y = new_height / old_height
        
        # 重新映射航迹点
        new_track_points = []
        for x, y in self.track_points:
            new_x = x * scale_x
            new_y = y * scale_y
            new_track_points.append((new_x, new_y))
        
        self.track_points = new_track_points
        
        # 重新绘制轨迹线
        self.flight_path = QPainterPath()
        # self.flight_path.clear()
        if self.track_points:
            self.flight_path.moveTo(self.track_points[0][0], self.track_points[0][1])
            for x, y in self.track_points[1:]:
                self.flight_path.lineTo(x, y)
        self.path_item.setPath(self.flight_path)
        
        # 重新定位无人机
        if self.drone_icon.isVisible() and len(self.track_points) > 0:
            last_x, last_y = self.track_points[-1]
            self.drone_icon.setPos(last_x, last_y)
        
        # 保存当前大小用于下次缩放
        self.old_size = self.size()
    
    def _update_drone_state(self, x, y):
        """内部槽函数：根据真实世界坐标更新 UI"""
        # 获取当前视图大小
        self.view_width = self.size().width()
        self.view_height = self.size().height()
        # print("view_width:", view_width, "view_height:", view_height)
        
        # 假设传入的坐标范围是 0-1000，需要映射到视图大小
        # 根据你的实际需求修改这个映射逻辑
        self.now_x = max(0.0, min(x, self.mapX))
        self.now_y = max(0.0, min(y, self.mapY))
        

        scene_x = (self.now_x / self.mapX) * self.view_width
        scene_y = self.view_height - (self.now_y / self.mapY) * self.view_height
        
        # 记录航迹点
        self.track_points.append((scene_x, scene_y))
        
        # 更新无人机当前位置
        self.drone_icon.setPos(scene_x, scene_y)
        self.drone_icon.setVisible(True)

        # 实时更新轨迹线
        if self.flight_path.elementCount() == 0 or len(self.track_points) < 1: # 小巧思：self.flight_path.isEmpty(): 这里为什么一直返回True？因为self.flight_path只含有moveTo() 或是空的路径，都会被isEmpty()判断为空，QT官方有解释
            self.flight_path.moveTo(scene_x, scene_y)
            self.pathlength = 0
        else:
            self.flight_path.lineTo(scene_x, scene_y)
            pathtemp = math.sqrt((x - self.last_x) ** 2 + (y - self.last_y) ** 2)
            if pathtemp > 0.007:
                self.pathlength += pathtemp
            # self.pathlength += math.sqrt((x - self.last_x) ** 2 + (y - self.last_y) ** 2)
        self.path_item.setPath(self.flight_path)

        self.last_x = self.now_x
        self.last_y = self.now_y
        self.update_hud_display( self.now_x, self.now_y,self.pathlength, self.title)

        # # 可选：添加航迹点标记（小圆点）
        # track_point = QGraphicsEllipseItem(scene_x-2, scene_y-2, 4, 4)
        # track_point.setPen(QPen(QColor(0, 200, 0), 5))
        # self.scene.addItem(track_point)
        
        # # 1秒后自动删除小圆点，避免过多图形项
        # # QTimer.singleShot(1000, lambda: self.scene.removeItem(track_point))

        # # 检查是否已经有背景图片（意味着场景已准备好）
        # if hasattr(self, 'background_item'):
        #     self._remap_coordinates()
    def update_position(self, x, y):
        """对外暴露的接口：供外部线程或定时器调用"""
        self.update_position_signal.emit(x, y)

    def clear_trajectory(self):
        """清空当前的飞行轨迹"""
        self.flight_path = QPainterPath() # 避免脏数据
        self.path_item.setPath(self.flight_path) # 【重要】：即使路径清空了，也要显式更新 path_item，确保视图刷新
        self.track_points = []  # 同时清空存储点的列表
        self.pathlength = 0 # 重置长度
        # 重新创建无人机图标
        self.drone_icon.setVisible(False)
    
    def stopUpdate(self):
        self.update_position_signal.disconnect()
    def startUpdate(self):
        self.update_position_signal.connect(self._update_drone_state)

    def pathLength(self):
        """获取当前路径长度/实际长度 米"""
        return self.pathlength

    # def add_track_point(self, x, y):
    #     """添加单个航迹点"""
    #     view_width = self.size().width()
    #     view_height = self.size().height()
        
    #     scene_x = (x / self.mapX) * view_width
    #     scene_y = (y / self.mapY) * view_height
        
    #     track_point = QGraphicsEllipseItem(scene_x-2, scene_y-2, 4, 4)
    #     track_point.setBrush(QColor(0, 255, 0))
    #     track_point.setPen(QPen(QColor(0, 200, 0), 2))
    #     self.scene.addItem(track_point)
        
    #     if self.flight_path.isEmpty():
    #         self.flight_path.moveTo(scene_x, scene_y)
    #     else:
    #         self.flight_path.lineTo(scene_x, scene_y)
        
    #     self.track_points.append((scene_x, scene_y))
    #     self.path_item.setPath(self.flight_path)

# ------------------- 简单的自测运行代码 -------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 实例化子窗口
    drone_window = DroneMapWidget(map_image_path="/home/focal/Desktop/2024_GroundStation/src/GroundStation/imgs/2023map.png")
    drone_window.setWindowTitle("无人机实时轨迹监控")
    drone_window.resize(1000, 700)
    drone_window.show()
    drone_window.stopUpdate()
    drone_window.clear_trajectory()

    drone_window.update_position(0.0, 0.5)
    drone_window.startUpdate()
    # 模拟实时数据流
    simulated_x = 0.0
    simulated_y = 0.5
    cnt = 20
    import random
    def mock_data_stream():
            global simulated_x, simulated_y, cnt
            # 每次移动 0.01~0.15m
            simulated_x += random.uniform(-0.05, 0.15)
            simulated_y += random.uniform(-0.05, 0.15)

            # 边界限制
            simulated_x = max(0.0, min(4.8, simulated_x))
            simulated_y = max(0.0, min(4.0, simulated_y))

            drone_window.update_position(simulated_x, simulated_y)
            
            cnt -= 1
            if cnt <= 0:
                drone_window.stopUpdate()
                timer.stop()  # 停止定时器
                drone_window.update_position(simulated_x, simulated_y)
                print("测试完成")
                print(f"总里程{drone_window.pathLength():.2f}米")

    timer = QTimer()
    timer.timeout.connect(mock_data_stream)
    timer.start(100)

    timer2 = QTimer()
    timer2.timeout.connect(lambda: drone_window.update_position(        0.8,        0.8,    ))
    timer2.start(101)

    # drone_window.update_position(        0.8,        0.8,    )
    # drone_window.clear_trajectory()
    # drone_window.update_position(        0.0,        2.4,    )
    # drone_window.startUpdate()
    # drone_window.update_position(        3.6,        3.6,    )
    

    sys.exit(app.exec_())