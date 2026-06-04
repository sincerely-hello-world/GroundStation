#----------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def crop_center_with_offset(frame, crop_size, offset_x=0, offset_y=0):
    """
    从 frame 中裁剪一个 crop_size x crop_size 的区域，
    裁剪中心默认为图像中心，可通过 offset_x / offset_y 偏移（像素）。
    
    参数:
        frame (np.ndarray): 输入图像 (H, W, C)
        crop_size (int): 裁剪区域的宽高（正方形）
        offset_x (int): 相对于中心点的水平偏移（正：向右，负：向左）
        offset_y (int): 相对于中心点的垂直偏移（正：向下，负：向上）
    
    返回:
        cropped (np.ndarray): 裁剪后的图像，若原图小于 crop_size，则自动缩小裁剪区域（不放大）
                            若无法裁剪（如 crop_size <= 0），返回原图或空数组。
    """
    if crop_size <= 0:
        raise ValueError("crop_size 必须为正整数")
    
    h, w = frame.shape[:2]
    
    # 实际可用的最大裁剪尺寸（不能超过原图）
    actual_crop = min(crop_size, w, h)
    
    # 原始中心点
    center_x = w // 2
    center_y = h // 2

    # 应用偏移后的目标中心
    target_cx = center_x + offset_x
    target_cy = center_y + offset_y

    # 计算裁剪边界（以目标中心为中心）
    half = actual_crop // 2
    left = target_cx - half
    right = left + actual_crop
    top = target_cy - half
    bottom = top + actual_crop

    # 边界校正：确保 [left, right) 和 [top, bottom) 在 [0, w) 和 [0, h) 范围内
    if left < 0:
        left = 0
        right = actual_crop
    if right > w:
        right = w
        left = w - actual_crop
    if top < 0:
        top = 0
        bottom = actual_crop
    if bottom > h:
        bottom = h
        top = h - actual_crop
    cropped = frame[top:bottom, left:right]
    return cropped


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from sensor_msgs.msg import Image,CompressedImage

import cv2
from cv_bridge import CvBridge
import numpy as np
from pyzbar.pyzbar import decode,ZBarSymbol

from std_srvs.srv import Trigger
def detect_color_blob(frame):
    """
    识别画面中特定黄白色块，并返回其相对于画面中心的偏移量
    """
    # 1. 获取画面尺寸并计算中心点
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2

    # 2. 颜色转换：OpenCV 默认是 BGR，先转为 RGB，再转为 HSV
    # (你给的阈值是 RGB 格式，所以先转回 RGB 方便理解，实际处理用 HSV)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 3. 定义颜色阈值
    # 目标颜色：RGB (255, 240, 100) 到 (255, 255, 255) -> 属于明亮的黄白色
    
    # 在 HSV 空间中：
    # H (色相): 黄色大约在 20-30 之间
    # S (饱和度): 你的颜色下限饱和度较低 (240/255 ≈ 0.94)，上限为纯白(0)
    # V (明度): 你的颜色非常亮，下限 100/255 ≈ 0.39，上限 255
    lower_hsv = np.array([20, 100, 100])  # 稍微放宽了饱和度下限，防止漏检
    upper_hsv = np.array([35, 255, 255])  # 涵盖到浅黄色/白色区域

    # 4. 创建掩膜（Mask），提取符合颜色的区域
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # 5. 图像降噪处理（腐蚀与膨胀），去掉细小的噪点
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 6. 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_objects = []

    if contours:
        # 找到面积最大的那个色块
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        # 过滤掉太小的噪点（比如面积小于 500 像素的就忽略）
        if area > 500:
            # 计算色块的中心点 (矩形的中心)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                blob_cx = int(M["m10"] / M["m00"])
                blob_cy = int(M["m01"] / M["m00"])

                # 计算相对于摄像头画面中心的偏移量
                offset_x = blob_cx - center_x
                offset_y = blob_cy - center_y

                detected_objects.append({
                    "color_name": "Yellow-White",
                    "offset_x": offset_x,
                    "offset_y": offset_y,
                    "center_point": (blob_cx, blob_cy)
                })

                # --- 调试可视化 (可选) ---
                # 在画面上画出识别到的色块轮廓和中心点
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (blob_cx, blob_cy), 5, (0, 0, 255), -1)
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1) # 画面中心
                cv2.putText(frame, f"Offset X: {offset_x}, Y: {offset_y}", 
                            (blob_cx + 10, blob_cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    return frame, detected_objects
class camNode(Node):
    def __init__(self,name='camNode'):
        super().__init__(name)
        self.crop_size = 480 # 截取摄像头中心区域
        self.camIndex = 0    # 摄像头编号
        self.camWidth = 1280 # 请求的分辨率
        self.camHeight = 720

        self.client_led1_trigger = self.create_client(Trigger,"led1_trigger")
 
        # 发布
        self.topic_publisher_qrcode = self.create_publisher(String, 'qrcode_data_topic', 10)
        

        # 创建 cv_bridge 实例 
        self.bridge = CvBridge()

        # 打开USB摄像头（索引0，根据实际情况调整）
        self.cap = self.open_camera_with_resolution(self.camIndex, self.camWidth, self.camHeight)
        if not self.cap.isOpened():
            self.get_logger().error("无法打开摄像头")
            raise RuntimeError("摄像头打开失败")
        # ─────────────── 关键：在初始化时读取一次分辨率 ───────────────
        # 获取摄像头属性（注意：width 是 CAP_PROP_FRAME_WIDTH，height 是 CAP_PROP_FRAME_HEIGHT）
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 打印到 ROS 日志（推荐）
        
        self.get_logger().info("摄像头节点已启动，按 Ctrl+C 退出")
        self.get_logger().info(f"摄像头初始化分辨率：{width} × {height}")
        self.get_logger().info(f"real摄像头裁剪中心后大小 {self.crop_size}*{self.crop_size}")

        # 创建定时器（相当于ROS的循环频率）
        # 这里每秒检测30帧（约33ms一次）
        self.qr_timer = self.create_timer(0.033, self.cam_timer_callback)

    def open_camera_with_resolution(self,index:int, width:int, height:int):
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            raise RuntimeError("无法打开摄像头")

        # 设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # 读取实际值（很多摄像头不会严格按照你设置的来）
        real_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        real_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.get_logger().info(f"real摄像头 {index} 分辨率：请求 {width}x{height} → 实际 {real_w}x{real_h}")
        return cap 

    def cam_timer_callback(self):
        ret, frame = self.cap.read()
        
        frame = crop_center_with_offset(frame, self.crop_size,0,0)
        if not ret:
            self.get_logger().error("无法读取帧")
            return
        frame, detected_objects = detect_color_blob(frame)
        # self.get_logger().info(f"检测黄色灯光块")

        try:
            # 发布消息
            msg = String()
            msg.data = '1'
            self.topic_publisher_qrcode.publish(msg)
            self.client_led1_trigger.call_async(Trigger.Request())

        except Exception as e:
            self.get_logger().warn(f"摄像头任务失败: {e}")

        # decode_img = None
        # try:
        #     # # 最常用编码："bgr8"（因为 cv2 默认是 BGR 通道顺序）
        #     # ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        #     # # 加上时间戳和 frame_id（强烈推荐，rviz 需要）
        #     # ros_image_msg.header.stamp = self.get_clock().now().to_msg()
        #     # ros_image_msg.header.frame_id = "image_qrcode"   # 可改成你的坐标系名
        #     # self.topic_publisher_qrimage.publish(ros_image_msg)

        #     ros_compressed_image_msg = CompressedImage()
        #     success,encoded_image = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, 43])
        #     ros_compressed_image_msg.data= np.array(encoded_image).tobytes()
        #     # if success: # cv2 m
        #     #     # 编码成功才执行解码逻辑
        #     #     nparr = np.frombuffer(ros_compressed_image_msg.data, np.uint8)
        #     #     decode_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        #     # bridge m
        #     # ros_compressed_image_msg = self.bridge.cv2_to_compressed_imgmsg(frame, 'jpg') 

        #     ros_compressed_image_msg.header.stamp=self.get_clock().now().to_msg()
        #     ros_compressed_image_msg.header.frame_id = "compressedimage_qrcode"   # 可改成你的坐标系名
        #     ros_compressed_image_msg.format='jpeg'
            
        #     self.topic_publisher_qrcompressedimage.publish(ros_compressed_image_msg)

        # except Exception as e:
        #     self.get_logger().error(f"image 转换失败: {e}")

        # # ─────────────── 本地调试显示（可选） ───────────────
        # decode_img=self.bridge.compressed_imgmsg_to_cv2(ros_compressed_image_msg)
        # cv2.imshow('USB Camera with QR Detection', decode_img)

        # decode_img=self.bridge.imgmsg_to_cv2(ros_image_msg)
        # cv2.imshow('USB Camera with QR Detection', decode_img)
        cv2.imshow('USB Camera vedio', frame)
        cv2.waitKey(1) # ← 关键！1ms 就够了，不会明显卡顿  # 必须有！否则窗口不刷新

    def destroy_node(self):
        # 释放资源
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    try:
        node = camNode()
        # 推荐使用spin方式（阻塞式，自动处理回调）
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        # 清理
        if 'node' in locals():
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

