import os,sys
# 自动获取当前文件所在目录的上一级目录，并强行加入 Python 的搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


import rclpy
from rclpy.node import Node
import serial,time
import threading
from std_msgs.msg import String  #  ROS2 uart串口 接收发送的话题，均使用 msg/String
from rclpy.executors import MultiThreadedExecutor

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

from carStation.car_uart_parse import *
from carStation.car_diff_drive import best_effort_qos



def sanitize_string(s: str, replacement: str = '*') -> str:
    """
    将字符串中所有控制字符（包括 \x00）、非打印字符替换为 replacement。
    """
    # 方法1：只保留可打印 ASCII（32~126），其余替换为 *
    cleaned = ''.join(
        c if 32 <= ord(c) <= 126 else replacement
        for c in s
    )
    return cleaned

velocity_calc = VelocityCalculator()

class UartClass(Node):
    def __init__(self,
                 node_name='uartx_node', # 替换为实际节点名称，如 'uart3_node' 或 'uart4_node'
                 serial_port='/dev/ttySx',  # 替换为实际串口设备，如 /dev/ttyS3 或 /dev/ttyS4
                 baudrate=57600,
                 send_topic_name='uart_senderx_data_topic',            # 发送端订阅的 topic 名
                 recv_topic_name='uart_readerx_data_topic',            # 接收端发布的 topic 名
                 debug_send=True,
                 debug_recv=True,
                 ):
        super().__init__(node_name)
        self.ser = None  # 串口对象，初始为 None，表示未连接
        self.serial_port = serial_port
        self.baudrate = baudrate
 
        self.debug_send = debug_send
        self.debug_recv = debug_recv

        # 创建退出控制事件
        self.shutdown_event = threading.Event()
        self.latest_data_lock = threading.RLock()  # 使用RLock更安全
        
        self.create_timer(0.8, self.serial_timer_callback) # 定时器，负责自动重连和状态监控

        # === 发送部分 ===
        self.send_topic_name =   send_topic_name
        self.sub_send = self.create_subscription(
            String, topic=self.send_topic_name, callback=self.send_uart_data, qos_profile=best_effort_qos
        )
        self.get_logger().info(f'{self.get_name()}串口 {serial_port},已订阅发送主题: {self.send_topic_name}')

        # === 接收部分 ===
        self.recv_topic_name = recv_topic_name
        self.pub_recv = self.create_publisher(String, self.recv_topic_name, 10)
        self.get_logger().info(f'{self.get_name()}串口 {serial_port},将发布接收数据到主题: {self.recv_topic_name}')
        self.create_timer(0.020, self.timer_publish_received_data) # 定时器，定期发布接收到的数据

        # 启动接收线程
        self.recv_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.recv_thread.start()

        self.log_topic_pub = self.create_publisher(String,"log_topic",10 )
        self.send_log_json(label='消防车',info='串口节点启动成功')

 
    def serial_timer_callback(self):
        """定时器回调函数：负责自动重连、状态监控和数据收发"""
        # 1. 如果串口未打开，尝试建立连接
        if self.ser is None:
            try:
                self.get_logger().info(f'🔌 正在尝试连接串口设备 [{self.serial_port}]...')
                self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=0.02)
                
                # 连接成功，执行初始化操作
                self.get_logger().info('✅ 成功连接！小车CAR驱动板已就绪。')
                my_init_car_parameters(self.ser)
                time.sleep(0.2) # 等待参数设置生效
                my_control_speed(self.ser, 0, 0, 0, 0) 
                self.send_log_json(label='消防车',info='串口通信链接成功')
                
            except (serial.SerialException, OSError) as e:
                # 连接失败（设备未插入或权限不足），等待下次定时器触发再试
                self.get_logger().warn(f'⏳ 小车CAR驱动板未就绪，等待设备插入... ({e})')
                self.send_log_json(label='消防车',info='串口驱动板断开/失败')
                return  # 直接返回，不执行后面的收发逻辑

        # 2. 串口已打开，尝试进行正常的读取/发送操作
        try:
            self.ser.write("".encode('utf-8'))   # 访问属性以触发可能的异常（如设备被拔掉）
        except (serial.SerialException, OSError, ValueError) as e:
            # 3. 运行中设备被拔掉或发生 I/O 错误
            self.get_logger().error(f'⚠️ 串口通信异常，设备可能已断开: {e}')
            if self.ser or self.ser.is_open:
                try:
                    self.ser.close()
                except:
                    pass
            self.ser = None  # 重置串口对象，触发下次回调的重连逻辑

    def send_log_json(self, label:str, info:str):
        self.get_logger().info(f"{label}:{info}")
        json_dumps = json.dumps({'label':label,'info':info})
        self.log_topic_pub.publish(String(data=json_dumps))

    def send_uart_data(self, msg: String):
        """回调：当有数据要通过串口发送时"""
        if self.ser is None:
            return self.get_logger().warn(f'⚠️ 无法发送数据，小车串口未连接-fn: send_uart_data')
        try:
            send_content = msg.data #.strip()
            # hex_with_0x = ''.join(f'0x{b:02x}' for b in send_content.encode())
            if not send_content:
                self.get_logger().warn(f'空字符串，未发送任何数据')
                return
 
            if self.debug_send: # 打印发送的十六进制字符串和对应的 ASCII 字符 要发送数据hex为{hex_with_0x}
                self.get_logger().info(f"要发送数据为{send_content} success")
 
            if self.ser.is_open: 
                sent = self.ser.write(send_content.encode('utf-8'))
                if sent != len(send_content):
                    self.get_logger().warn(f'发送错误：仅发送了 {sent}/{len(send_content)} 字节 error')
        except ValueError as e:
            self.get_logger().error(f'无效的消息内容: "{msg.data}" - {e}')
        except Exception as e:
            self.get_logger().error(f'fn: send_uart_data 发送失败: {e}')
            self.ser = None


    def read_serial(self):
        """后台线程：持续读取串口数据并解析帧"""
        while rclpy.ok() and  self.shutdown_event.is_set() is not True and self.ser is not None:
            try:
                data = self.ser.readline().strip()  # 读取一行数据并去除两端空白
                if data is not None:
                    # 先尝试解码，遇到非法 UTF-8 用 * 替代（但 \x00 不会触发这里）
                    decoded = data.decode('utf-8', errors='replace')
                    # 再把 decode 后的字符串中所有不可见字符（含 \x00）替换为 *
                    rec_line = sanitize_string(decoded, '*')
                    msg = String()
                    msg.data = rec_line
                    with self.latest_data_lock:
                        self.latest_data = msg.data
                    if self.debug_recv:
                        self.get_logger().info(f"接收到帧: {rec_line}")
            except Exception as e:
                self.get_logger().error(f'读取串口数据失败: {e}')
                return  # 退出线程
            

    def timer_publish_received_data(self):
        """定时器回调：发布最新接收到的数据"""
        with self.latest_data_lock:
            if hasattr(self, 'latest_data') :
                if  self.latest_data.startswith("$MAll:") and self.latest_data.endswith("#"):
                    msg = String()
                    msg.data = self.latest_data
                    self.pub_recv.publish(msg)

    # def destroy_node(self):
    #     self.shutdown_event.set()  # 通知线程退出
    #     if hasattr(self, 'recv_thread') and self.recv_thread.is_alive():
    #         self.recv_thread.join(timeout=1.0)  # 等待线程结束，避免资源泄漏
    #     super().destroy_node()



def main(args=None):
    rclpy.init(args=args)

    # 创建两个串口读取节点
    car_uart_node = UartClass( # uart3 发送 t265数据给 MCU的Uart7
        node_name='CAR_UART',
        serial_port='/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0',
        baudrate=115200,
        send_topic_name='car/driver/cmd_topic',
        recv_topic_name='car/driver/recv_topic',

        debug_send=False,  
        debug_recv=False,
    )
    # 使用多线程执行器，让节点并发运行
    executor = MultiThreadedExecutor(num_threads=5)
    executor.add_node(car_uart_node)

    from carStation.car_odom import CarOdomPublisher
    car_odom_node = CarOdomPublisher() # 发布小车里程计信息
    executor.add_node(car_odom_node)

    from carStation.car_diff_drive import DiffDriveController
    diff_drive_node = DiffDriveController() # 订阅 car/driver/cmd_topic 话题，控制小车运动
    executor.add_node(diff_drive_node)

    from carStation.car_tof import CarToFPublisher
    car_tof_node = CarToFPublisher() # 发布ToF传感器数据
    executor.add_node(car_tof_node)

    from carStation.car_logical import CarLogicalNode
    car_logic_node = CarLogicalNode() # 发布ToF传感器数据
    executor.add_node(car_logic_node)

    try:
        # 阻塞运行，直到 Ctrl+C
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        # 清理资源
        time.sleep(0.2) # 确保命令发送完成
        car_uart_node.destroy_node()
        car_odom_node.destroy_node()
        diff_drive_node.destroy_node()
        car_tof_node.destroy_node()
        car_logic_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()



