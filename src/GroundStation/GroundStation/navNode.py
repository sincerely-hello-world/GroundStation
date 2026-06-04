
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rcl_interfaces.msg import SetParametersResult
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.parameter import Parameter
from std_srvs.srv import Empty,Trigger
from std_msgs.msg import String
# 自定义消息和服务的数据类型
from uav_car_interfaces.msg import T265Data
from uav_car_interfaces.srv import ControlService

from dataclasses import dataclass

from GroundStation.myFunction import *
import json,re, threading
from typing import List, Optional



class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.7, label: str = 'none',qrcode: str = 'none',label2: str = 'none', qrcode2: str = 'none', color: str = 'none'):
        self.x = x      # 单位：米
        self.y = y
        self.z = z
        self.label = label
        self.qrcode = qrcode
        self.label2 = label2
        self.qrcode2 = qrcode2
        self.color = color

@dataclass(frozen=True)  # frozen=True 开启只读模式
class myStatus:
    TAKEOFF :str = 'Takeoff'
    TAKEOFF_WAIT :str = 'Takeoff_wait'
    LAND :str = 'Land'
    SetAim :str = 'SetAim'
    WaitAim :str = 'WaitAim'
    ArriveAim :str = 'ArriveAim'
    Delay :str = 'Delay'
    End :str = 'End' # 运行结束
    

class navNode(Node):
    pos = T265Data()
    aim = Point() # 当前路径点

    state_lock = threading.Lock()

    状态 = myStatus()
 

    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
    topic_cb_group=MutuallyExclusiveCallbackGroup()

    shutdown_requested = False
    def __init__(self, name = 'navNode'):
        super().__init__(node_name=name)
        # parameters
        self.declare_parameter('test', '')
        self.declare_parameter('paths_scan_all', '')    
         
        self.test = self.get_parameter('test').value
        self.paths_scan_all_str = self.get_parameter('paths_scan_all').value

        if self.paths_scan_all_str is not None:
            self.path_scan_all_json = json.loads(self.paths_scan_all_str)
            self.path_scan_all: List[Point] = [
                Point(
                    x=float(p['x']),
                    y=float(p['y']),
                    z=float(p['z']),
                    label=str(p['label']),
                    qrcode=str(p['qrcode']),
                    label2=str(p['label2']),
                    qrcode2=str(p['qrcode2']),
                )
                for p in self.path_scan_all_json
            ]
            self.get_logger().info(f'path_scan_all: {self.paths_scan_all_str}')
            
        self.add_on_set_parameters_callback(self.param_callback)

        #----------------------
        # 服务
        self.talk2ui_server  = self.create_service(ControlService, 'talk_service', self.talk_callback) # 和地面站交流

        self.client_command = self.create_client(ControlService,"command_service") # 给飞机串口-飞控MCU的端口发指令
        self.client_led1_trigger = self.create_client(Trigger,"led1_trigger")
        self.client_led2_trigger = self.create_client(Trigger,"led2_trigger")
        # 订阅话题
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.position_callback, 10,callback_group=self.topic_t265_cb_group)
        self.topic_uart4_sub_MCU2 = self.create_subscription(String, 'uart_reader4_data_topic', self.MCU2_callback,10)
        self.topic_qrcode_sub = self.create_subscription(String,"qrcode_data_topic",self.qrcode_callback,10 ,callback_group=self.topic_cb_group)
        self.topic_fly_camera_sub = self.create_subscription(String, 'fly/camera/data', self.fly_camera_callback, 10,  callback_group=self.topic_cb_group)
        # 发布话题
        self.log_topic_pub = self.create_publisher(String,"log_topic",10 ,callback_group=self.topic_cb_group)
        self.fire_topic_pub = self.create_publisher(String,"fire/area",10 ,callback_group=self.topic_cb_group)
        self.topic_flyServo_pub = self.create_publisher(String,'fly/servo10',10,callback_group=self.topic_cb_group)
        

        self.task = None
        
        self.paths = None
        self.path_index = 0

        self.status = self.状态.TAKEOFF
        self.task_timer = None 

        self.delay_timer = None
        self.delay_ok = False

        self.mcu_arrive = False
        self.pos_arrive = False

        self.scan_label = None # 要搜寻的标签位置
        self.get_logger().info('上位机导航节点启动成功')


        import time
        time.sleep(2)
        self.send_log_json(label='无人机',info='地面站控制节点启动成功')

        # self.fire_topic_pub.publish(String(data='A'))
        # self.fire_topic_pub.publish(String(data='B'))
        # self.fire_topic_pub.publish(String(data='C'))
        # self.fire_topic_pub.publish(String(data='D'))
        # time.sleep(0.1)
        # self.fire_topic_pub.publish(String(data='over'))


    def clear_fly_status(self):
        self.task = None
        
        self.paths = None
        self.path_index = 0

        self.status = self.状态.TAKEOFF
        self.task_timer = None 

        self.delay_timer = None
        self.delay_ok = False

        self.mcu_arrive = False
        self.pos_arrive = False

        
        
    def talk_callback(self, request, response):
        self.task = request.req
        self.get_logger().info(f"收到来自UI的请求：{self.task}")
        if self.task == 'shutdown-navNode':
            self.get_logger().info(f'关闭该节点运行：{self.task}')
            self.status = self.状态.End
            self.clear_fly_status()
            self.send_command('land') #紧急降落
            self.shutdown_requested = True
            response.echo =f'task is shutdown'
        elif self.task_timer is not None:
            response.echo =f'task is running'
        elif self.task == 'scan_all' and  self.task_timer is None:
            self.get_logger().info(f'全部航点扫描任务：{self.task}')
            self.clear_fly_status()
            self.paths = self.path_scan_all
            if self.paths is None:
                self.get_logger().error(f'未找到合适路径{self.task}')
            else:
                self.task_timer = self.create_timer(0.1, self.task_timer_callback,callback_group=self.topic_cb_group)
        else:
            self.get_logger().error(f'nav收到未定义的任务{self.task}' )
            response.echo =f'undefined task'
        return response

    def send_aim(self, aim:Point):
        self.send_command(TGformat(head='G',x=aim.x,y=aim.y,z=aim.z,end=''))
    def task_timer_callback(self):#todo:  状态机任务控制
        if self.status == self.状态.TAKEOFF:
            with self.state_lock:
                self.path_index = 0
                self.aim = self.paths[self.path_index]
            self.get_logger().info(f"状态1：{self.status}--[{self.aim.label}{self.aim.qrcode}]]")
            self.send_command('takeoff')
            self.send_log_json(label='fly',info='start')
            self.status = self.状态.TAKEOFF_WAIT

        elif self.status == self.状态.TAKEOFF_WAIT:
            self.get_logger().info(f"状态2：{self.status}--[{self.aim.label}{self.aim.qrcode}]]")
            if self.check_arrive_aim():
                self.status = self.状态.SetAim

        elif self.status == self.状态.SetAim:
            if self.path_index == len(self.paths)-1: # MAX index + 1 = len !!!, 最后一点为降落点，但用降落指令
                with self.state_lock:
                    self.aim = self.paths[-1]
                self.send_aim(self.aim)
                self.status = self.状态.LAND
            else:
                with self.state_lock:
                    self.aim = self.paths[self.path_index]
                    self.get_logger().info(f"状态3：{self.status}--[{self.aim.label}{self.aim.qrcode}]")
                    self.path_index += 1
                self.send_aim(self.aim)
                self.status = self.状态.WaitAim

        elif self.status == self.状态.WaitAim:  
            self.get_logger().info(f"状态4：{self.status}--[{self.aim.label}{self.aim.qrcode}]]")
            if self.check_arrive_aim():
                self.status = self.状态.ArriveAim

        elif self.status == self.状态.ArriveAim:
            self.get_logger().info(f"状态5：{self.status}--[{self.aim.label}{self.aim.qrcode}]]")
            if len(self.aim.label) == 2 : # 进入delay状态
                self.status = self.状态.Delay
                self.delay_ok = False
            else:
                self.status = self.状态.SetAim

        elif self.status == self.状态.Delay:
            self.get_logger().info(f"状态6：{self.status}--[{self.aim.label}{self.aim.qrcode}]]")

            if self.delay_ok == True:
                self.delay_ok = False # 重置 在这里延迟结束，可以发送整理到的二维码
                self.status = self.状态.SetAim
            else:
                if self.delay_timer is None or self.delay_timer.is_canceled():
                    self.delay_timer = self.create_timer(1.0, self.delay_timer_callback,callback_group=self.topic_cb_group)
                pass
        elif self.status == self.状态.LAND:
            self.get_logger().info(f"状态7：{self.status}--[准备降落]")
            if self.check_arrive_aim():
                self.get_logger().info(f"状态7：{self.status}--[到达降落点，降落]")
                self.send_command('normalLand')
                self.status = self.状态.End

        elif self.status == self.状态.End:
            self.get_logger().info(f"状态8：{self.status}--[任务结束]")
            self.task_timer.cancel()
            self.send_log_json(label='fly',info='over')
            self.task_timer = None

    def qrcode_callback(self, msg:String): # 来自飞机摄像机的数据
        return
        self.qrcode = msg.data
        self.client_led1_trigger.call_async(Trigger.Request())
        if self.pos_arrive:
            self.get_logger().info(f"二维码识别器:{self.qrcode}")
    def fly_camera_callback(self, msg: String):
        pass
    def delay_timer_callback(self): 
        '''延时完成的回调： 发送识别结果'''
        self.send_log_json(f"无人机",f"{self.aim.label}航点完成")# 当前识别到qr】码【{self.aim.qrcode}】
        self.get_logger().info(f"无人机{self.aim.label}航点完成")
        self.delay_ok = True
        self.delay_timer.cancel()  # 确保定时器只执行一次
        self.delay_timer = None
    def check_arrive_aim(self):
        info_str = f"当前状态：[{self.status}],点位标签[label:{self.aim.label},qr:{self.aim.qrcode}],到达?:[MCU:{self.mcu_arrive}]-[POS:{self.pos_arrive}]"
        aim_str = f"目标位置：({self.aim.x:.2f}, {self.aim.y:.2f}, {self.aim.z:.2f})-{self.aim.label}"
        pos_str = f"当前位置：({self.pos.pos_x:.2f}, {self.pos.pos_y:.2f}, {self.pos.pos_z:.2f})"

        self.pos_arrive=self.is_pos_arrive()
        # self.get_logger().info(f"{info_str}")
        if  self.pos_arrive or self.mcu_arrive:
            return True
        else:
            return False    
    def send_log_json(self, label:str, info:str):
        json_str = json.dumps({'label':label,'info':info})
        self.log_topic_pub.publish(String(data=json_str))
        self.get_logger().info(f"飞机向地面站发送数据------:{json_str}")

    
    def is_pos_arrive(self):
        within_tolerance = (
            max( # 切比雪夫距离：取三个轴差值的最大值。
                abs(self.pos.pos_x - self.aim.x),
                abs(self.pos.pos_y - self.aim.y),
                abs(self.pos.pos_z - self.aim.z)
            ) < 0.055 # cm厘米三维距离
        )
        self.pos_arrive = within_tolerance
        return within_tolerance
    def position_callback(self, msg: T265Data): # topic_t265_sub的回调函数，接收T265Data消息并更新位置信息
        self.pos = msg
    def MCU2_callback(self, msg: String):
        self.MCU2msg = msg
        self.get_logger().info(f'MCU2 send back: {msg.data}')
        if self.MCU2msg.data == "Gdone*":
            self.mcu_arrive = True
            # self.get_logger().info(f"mcu:已到目标点-[{self.aim.label}]")
        elif self.MCU2msg.data == "Gdoing*":
            self.mcu_arrive = False
        else:
            self.mcu_arrive = False
    def send_command(self, cmd:String):
        if rclpy.ok() and  self.client_command.service_is_ready()==False:
            err_msg = f"发送 {cmd} 失败: ROS2 服务 [ControlService] 未启动或超时"
            self.get_logger().error(err_msg)
            return # ！！！非常重要：必须 return，不要往下走 call_async
        # 1️⃣ 先创建 future  # . 只有服务就绪了，才执行后续发送逻辑
        request = ControlService.Request()
        request.req = cmd
        future = self.client_command.call_async(request)
        future.add_done_callback(lambda fut: self.command_future_done(fut, cmd))
        
    def command_future_done(self, future, original_cmd):
        try:
            response = future.result()  # 会 raise 如果有 exception
            info_str = f"{original_cmd} 发送成功 → {response.echo}"   
            self.get_logger().info(info_str)
        except Exception as e:
            err_msg = f"{original_cmd} 发送失敗: {str(e)}"
            self.cmd_result.emit(False, err_msg)
            self.get_logger().error(err_msg)
    def param_callback(self, params):
        self.get_logger().info(f"param_callback: {params}")
        for param in params:
            if param.name == 'test':
                self.test = param.value
                self.get_logger().info(f'test: {self.test}')
            else:
                self.get_logger().warn(f'unexpected parameter: {param.name}')
        return SetParametersResult(successful=True)

    def find_point_by_label(self,paths: List[Point], label: str) -> Optional[Point]:
        """
        根据 label 查找 Point，支持精确匹配，未找到时返回 None
        """
        if not paths or not label:
            return None
        label = str(label).strip()
        for p in paths:
            if str(p.label).strip() == label :
                self.get_logger().info(f"Found point with label: [{p.label}],{p.x, p.y, p.z}")
                return p
        return None

    def find_points_by_labels(self,paths: List[Point], labels: List[str]) -> Optional [List[Point]]:
        """
        根据多个 label，返回对应的 Point 列表（按 labels 的顺序排列）
        
        参数:
            paths: List[Point]      - 所有路径点的完整列表
            labels: List[str]       - 想要的 label 列表（支持唯一label）
            
        返回:
            List[Point]             - 按输入 labels 顺序排列的 Point 列表（找不到的 label 会返回 None,整体返回 None）
        """
        if not paths or not labels:
            return []
        result: List[Point] = []
        for label in labels:
            point = self.find_point_by_label(paths, label)
            if point is not None:
                result.append(point)
            else:
                self.get_logger().error(f"出错了: Label '{label}' 不在预设的路径列表内！")
                return None
        return result
def main(args=None):
    rclpy.init(args=args)
    try:
        node = navNode()
        # 使用 executor 更灵活（可替换为 MultiThreadedExecutor）
        executor = MultiThreadedExecutor(num_threads = 2)
        executor.add_node(node)
        try:
            # executor.spin()
            while rclpy.ok() and not node.shutdown_requested:
                executor.spin_once(timeout_sec=0.1)   # 关键：改用 spin_once + 循环检查标志
        # except SystemExit as e:               # ← 捕获服务中抛出的异常
        #     node.get_logger().info(f"收到 SystemExit: {e}，正在关闭节点...")
        except KeyboardInterrupt:
            pass  # 正常退出，不打印 traceback
    finally:
        if node is not None:
            executor.shutdown()
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
   
if __name__ == '__main__':
    main()

        # self.paths = self.path_scan_all
        # self.scan_label = 'A6'
        # self.paths = self.find_points_by_labels(self.path_scan_all, ['TakeOff',self.scan_label,'LeftSideA','LandPos'])
        # self.task_timer = self.create_timer(0.1, self.task_timer_callback)
        # self.get_logger().warning(f'任务开始执行{self.task}' )

 