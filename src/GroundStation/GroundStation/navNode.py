
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
    TAKEOFF :str = 'Takeoff'
    TAKEOFF_WAIT :str = 'Takeoff_wait'
    LAND :str = 'Land'
    SetAim :str = 'SetAim'
    WaitAim :str = 'WaitAim'
    ArriveAim :str = 'ArriveAim'
    Delay :str = 'Delay'
    End :str = 'End' # 运行结束
    

# @dataclass(frozen=True)  # frozen=True 开启只读模式
# class myTask:
#     SCAN_ALL :str = 'Scan_all'
#     # FIND_LAEBL :str = 'Find_label'


class navNode(Node):
    mcu_arrive = False
    pos_arrive = False
    pos = T265Data()
    
    aim = Point() # 路径目标点
    find_label = '' # 要搜寻的标签位置

    状态 = myStatus()
    status = ''
    task = ''

    img_cb_group =MutuallyExclusiveCallbackGroup()
    topic_cb_group =MutuallyExclusiveCallbackGroup()
    topic_t265_cb_group=MutuallyExclusiveCallbackGroup()
    topic_qrcode_cb_group=MutuallyExclusiveCallbackGroup()
    def __init__(self, name = 'navNode'):
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
        # self.get_logger().info(f'{self.paths[0].x}, {self.paths[0].y}, {self.paths[0].z}')
        self.add_on_set_parameters_callback(self.param_callback)



        #----------------------
        self.talk2ui_server  = self.create_service(ControlService, 'talk_service', self.talk_callback)
        self.client_command = self.create_client(ControlService,"command_service")
        
        self.topic_t265_sub = self.create_subscription(T265Data,"t265_data_topic", self.position_callback, 10,callback_group=self.topic_t265_cb_group)
        self.topic_uart4_sub_MCU2 = self.create_subscription(String, 'uart_reader4_data_topic', self.MCU2_callback,10)

        self.topic_qrcode_sub = self.create_subscription(String,"qrcode_data_topic",self.qrcode_callback,10 ,callback_group=self.topic_qrcode_cb_group)
        self.topic_qrcode2_sub = self.create_subscription(String,"qrcode2_data_topic",self.qrcode2_callback,10 ,callback_group=self.topic_qrcode_cb_group)  

        self.scan_all_timer = None 
        self.find_label_timer = None 

        self.delay_timer = None
        self.path_index = 0
        self.delay_ok = False
        self.get_logger().info('上位机导航节点启动成功')

    def talk_callback(self, request, response):
        self.task = request.req
        self.get_logger().info(f"收到来自UI的请求：{request.req}")
        if self.task == 'scan_all' and  self.scan_all_timer is None:
            if self.scan_all_timer is None:
                self.status = self.状态.TAKEOFF
                self.path_index = 0
                self.scan_all_timer = self.create_timer(0.1, self.scan_all_timer_callback)
        
        self.get_logger().warning(f'任务开始执行{self.task}' )
    
    
    def send_aim(self, aim:Point):
        self.send_command(TGformat(head='G',x=aim.x,y=aim.y,z=aim.z,end=''))
    def scan_all_timer_callback(self):#todo: 扫描所有二维码
        if self.status == self.状态.TAKEOFF:
            self.get_logger().info(f"状态1：{self.status}--[{self.aim.label}]")
            self.send_command('takeoff')
            self.status = self.状态.TAKEOFF_WAIT

        elif self.status == self.状态.TAKEOFF_WAIT:
            self.get_logger().info(f"状态2：{self.status}--[{self.aim.label}]")
            if self.check_arrive_aim():
                self.status = self.状态.SetAim

        elif self.status == self.状态.SetAim:
            self.get_logger().info(f"状态3：{self.status}--[{self.aim.label}]")
            if self.path_index == len(self.paths)-1: # MAX index + 1 = len !!!, 最后一点为降落点，但用降落指令
                self.aim = self.paths[-1]
                self.send_command('normalLand')
                self.status = self.状态.LAND
            else:
                self.aim = self.paths[self.path_index]
                self.send_aim(self.aim)
                self.path_index += 1
                self.status = self.状态.WaitAim

        elif self.status == self.状态.WaitAim:  
            self.get_logger().info(f"状态4：{self.status}--[{self.aim.label}]")
            if self.check_arrive_aim():
                self.status = self.状态.ArriveAim

        elif self.status == self.状态.ArriveAim:
            self.get_logger().info(f"状态5：{self.status}--[{self.aim.label}]")
            if len(self.aim.laebl) == 2:
                self.status = self.状态.Delay
            else:
                self.status = self.状态.SetAim

        elif self.status == self.状态.Delay:
            self.get_logger().info(f"状态6：{self.status}--[{self.aim.label}]")
            if self.delay_ok == True:
                self.delay_ok = False
                if self.delay_timer:
                    self.delay_timer.cancel()  # 确保定时器只执行一次
                self.status = self.状态.SetAim
            else:
                if self.delay_timer is None or self.delay_timer.is_canceled():
                    self.delay_timer = self.create_timer(2.0, self.delay_ok_callback)
        elif self.status == self.状态.LAND:
            self.get_logger().info(f"状态7：{self.status}--[降落开始]")
            if self.check_arrive_aim():
                self.status = self.状态.End

        elif self.status == self.状态.End:
            self.get_logger().info(f"状态8：{self.status}--[任务结束]")
            self.scan_all_timer.cancel()
            self.scan_all_timer = None

    def find_label_timer_callback(self):#todo: 寻找指定位置的二维码
        self.send_command('normalLand')
        pass

    def delay_ok_callback(self):
        self.delay_ok = True
    def check_arrive_aim(self):
        if  self.pos_arrive or self.mcu_arrive:
            self.get_logger().info(f"已到目标点")
            return True
        else:
            self.get_logger().info(f"未到目标点")
            self.mcu_arrive = False
            return False

    def qrcode_callback(self, msg:String):
        self.qrcode = msg.data
    def qrcode2_callback(self, msg:String):
        self.qrcode2 = msg.data
    def position_callback(self, msg: T265Data): # topic_t265_sub的回调函数，接收T265Data消息并更新位置信息
        # info = f"X:{msg.pos_x+0.0:+6.3f}m, Y:{msg.pos_y+0.0:+6.3f}m, Z:{msg.pos_z+0.0:+6.3f}m, C:{msg.confidence}, H:{msg.tof_z+0.0:+6.3f}m"
        # self.get_logger().info(info)
        self.pos = msg
        within_tolerance = (
            max( # 切比雪夫距离（也叫最大值距离、L∞ 范数）就是取三个轴差值的最大值。
                abs(self.pos.pos_x - self.aim.x),
                abs(self.pos.pos_y - self.aim.y),
                abs(self.pos.pos_z - self.aim.z)
            ) < 0.05
        )
        self.pos_arrive = within_tolerance

    def set_aim(self, aim:Point):
        cmd= TGformat(head='G',x=aim.x,y=aim.y,z=aim.z,end='')
        self.send_command(cmd)

    def MCU2_callback(self, msg: String):
        self.MCU2msg = msg
        self.get_logger().info(f'MCU2 send back: {msg.data}')
        if self.MCU2msg.data == "Gdone*":
            self.mcu_arrive = True
        elif self.MCU2msg.data == "Gdoing*":
            self.mcu_arrive = False
        else:
            self.mcu_arrive = False
    def send_command(self, cmd:String):
        if rclpy.ok() and self.client_command.wait_for_service(timeout_sec = 0.1)==False:
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
            response = future.result()  # 會 raise 如果有 exception
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
            if param.name == 'paths_scan_all':
                self.paths_scan_all_str = param.value
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
                # self.get_logger().info(f'{self.paths[0].x}, {self.paths[0].y}, {self.paths[0].z}')
            else:
                self.get_logger().warn(f'unexpected parameter: {param.name}')
        return SetParametersResult(successful=True)
def main(args=None):
    rclpy.init(args=args)
    try:
        node = navNode()
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