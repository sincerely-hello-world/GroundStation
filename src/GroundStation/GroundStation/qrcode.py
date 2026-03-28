# import cv2
# from pyzbar.pyzbar import decode

# # 打开USB摄像头（0表示默认摄像头，根据实际情况可能需要调整索引）
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("无法打开摄像头")
#     exit()

# print("按 'q' 键退出程序")

# while True:
#     # 读取一帧画面
#     ret, frame = cap.read()
#     if not ret:
#         print("无法读取帧")
#         break

#     # 对当前帧进行QR码识别
#     decoded_objects = decode(frame)
#     for obj in decoded_objects:
#         # 打印识别到的QR码数据
#         print("QR码类型:", obj.type)
#         print("QR码数据:", obj.data.decode('utf-8'))
        
#         # 在帧上绘制矩形框（可选，用于可视化）
#         pts = obj.polygon
#         if len(pts) > 4:
#             hull = cv2.convexHull(np.array([point for point in pts], dtype=np.float32))
#             hull = list(map(tuple, np.squeeze(hull)))
#         else:
#             hull = pts
#         n = len(hull)
#         for j in range(0, n):
#             cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

#     # 显示当前帧
#     cv2.imshow('USB Camera with QR Detection', frame)

#     # 按 'q' 键退出循环
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 释放资源
# cap.release()
# cv2.destroyAllWindows()


#----------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from sensor_msgs.msg import Image,CompressedImage

import cv2
from cv_bridge import CvBridge
import numpy as np
from pyzbar.pyzbar import decode

class QRCodeDetectorNode(Node):
    def __init__(self,name='qrcode'):
        super().__init__(name)

        # QoS 设置（可选，ROS2更强调QoS）
        # qos = QoSProfile(
        #     depth=10,
        #     reliability=ReliabilityPolicy.RELIABLE,
        #     history=HistoryPolicy.KEEP_LAST
        # )

        
        # 创建图像QRimage 发布者（话题名可自定义，例如 /camera/image_annotated）
        self.topic_publisher_qrimage = self.create_publisher(
            Image,
            '/image/image_qrcode',   # ← 推荐命名：带处理结果的图像
            10
        )
 
        self.topic_publisher_qrcompressedimage = self.create_publisher(
            CompressedImage,
            '/image/image_qrcode/compressed',   # ← 推荐命名：带处理结果的图像
            10
        )
        # 创建 cv_bridge 实例（只需创建一次）
        self.bridge = CvBridge()

        # 创建发布者 QRcode 发布者（保持不变）
        self.topic_publisher_qrcode = self.create_publisher(String, 'qrcode_data_topic', 10)

        # 打开USB摄像头（索引0，根据实际情况调整）
        self.cap = self.open_camera_with_resolution()
        if not self.cap.isOpened():
            self.get_logger().error("无法打开摄像头")
            raise RuntimeError("摄像头打开失败")
        # ─────────────── 关键：在初始化时读取一次分辨率 ───────────────
        # 获取摄像头属性（注意：width 是 CAP_PROP_FRAME_WIDTH，height 是 CAP_PROP_FRAME_HEIGHT）
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 打印到 ROS 日志（推荐）
        self.get_logger().info(f"摄像头初始化分辨率：{width} × {height}")
        self.get_logger().info("QR码检测节点已启动，按 Ctrl+C 退出")

        # 创建定时器（相当于ROS的循环频率）
        # 这里每秒检测30帧（约33ms一次）
        self.qr_timer = self.create_timer(0.033, self.qr_timer_callback)

    def open_camera_with_resolution(self,index=0, width=1280, height=720):
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

    def qr_timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("无法读取帧")
            return

        # QR码检测
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            try:
                qrdata = obj.data.decode('utf-8')
                self.get_logger().info(f"QRCODE NODE 识别到QR码: {qrdata}")

                # 发布消息
                msg = String()
                msg.data = qrdata
                self.topic_publisher_qrcode.publish(msg)

                # 在帧上绘制矩形框（可选，用于可视化）
                pts = obj.polygon
                if len(pts) > 4:
                    hull = cv2.convexHull(np.array([point for point in pts], dtype=np.float32))
                    hull = list(map(tuple, np.squeeze(hull)))
                else:
                    hull = pts
                n = len(hull)
                for j in range(0, n):
                    cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)
            except Exception as e:
                self.get_logger().warn(f"QR码解码失败: {e}")

        decode_img = None
        try:
            # # 最常用编码："bgr8"（因为 cv2 默认是 BGR 通道顺序）
            # ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            # # 加上时间戳和 frame_id（强烈推荐，rviz 需要）
            # ros_image_msg.header.stamp = self.get_clock().now().to_msg()
            # ros_image_msg.header.frame_id = "image_qrcode"   # 可改成你的坐标系名
            # self.topic_publisher_qrimage.publish(ros_image_msg)

            ros_compressed_image_msg = CompressedImage()
            success,encoded_image = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, 65])
            ros_compressed_image_msg.data= np.array(encoded_image).tobytes()
            # if success: # cv2 m
            #     # 编码成功才执行解码逻辑
            #     nparr = np.frombuffer(ros_compressed_image_msg.data, np.uint8)
            #     decode_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # bridge m
            # ros_compressed_image_msg = self.bridge.cv2_to_compressed_imgmsg(frame, 'jpg') 

            ros_compressed_image_msg.header.stamp=self.get_clock().now().to_msg()
            ros_compressed_image_msg.header.frame_id = "compressedimage_qrcode"   # 可改成你的坐标系名
            ros_compressed_image_msg.format='jpeg'
            
            self.topic_publisher_qrcompressedimage.publish(ros_compressed_image_msg)

        except Exception as e:
            self.get_logger().error(f"image 转换失败: {e}")

        # ─────────────── 本地调试显示（可选） ───────────────
        # decode_img=self.bridge.compressed_imgmsg_to_cv2(ros_compressed_image_msg)
        # cv2.imshow('USB Camera with QR Detection', decode_img)

        # decode_img=self.bridge.imgmsg_to_cv2(ros_image_msg)
        # cv2.imshow('USB Camera with QR Detection', decode_img)
        
        # cv2.waitKey(1) # ← 关键！1ms 就够了，不会明显卡顿  # 必须有！否则窗口不刷新

    def destroy_node(self):
        # 释放资源
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    try:
        node = QRCodeDetectorNode()
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

