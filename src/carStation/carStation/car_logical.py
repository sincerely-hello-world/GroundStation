import os,sys
# 自动获取当前文件所在目录的上一级目录，并强行加入 Python 的搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time,math,re
from carStation.car_uart_parse import *
from carStation.car_path import car_route_data,pick_aim_by_label, find_car_paths

# class Fire(x,y,z):
#     pass


class CarLogicalNode(Node):
    def __init__(self):
        super().__init__('CarLogic')

 
        self.aimIndex = 0
        self.aim = pick_aim_by_label(car_route_data,"init")
        self.pathsLen = None # len(self.car_paths)
        self.car_paths = None
        self.fireList = []
        
        self.carTaskOK = False
        self.recvOKFlag = False

        # 订阅
        # self.create_subscription(String,'car/obstacle',self.obstacle_callback,10)
        self.create_subscription(String,'car/pos/status',self.status_callback,10)
        self.create_subscription(String,'fire/area',self.fire_callback,10)

        # 发布
        self.car_control_pub = self.create_publisher(String, 'car/driver/control', 10)
        self.log_topic_pub = self.create_publisher(String,"log_topic",10 )
        self.send_log_json(label='消防车',info='消防车控制节点启动成功')

    # def obstacle_callback(self,msg:String):
    #     pass

    def send_log_json(self, label:str, info:str):
        self.get_logger().info(f"{label}:{info}")
        json_dumps = json.dumps({'label':label,'info':info})
        self.log_topic_pub.publish(String(data=json_dumps))


    def fire_callback(self,msg:String):
        fireInfo = msg.data
        # 判断 fire 本身就是 A/B/C/D/E/F 中的一个
        if fireInfo in ('A', 'B', 'C', 'D', 'E', 'F') and fireInfo not in self.fireList and self.recvOKFlag == False:
            self.fireList.append(fireInfo)
            self.send_log_json(label='消防车',info=f"收到火源:{fireInfo}")
        elif fireInfo == "fireListEnd" :
            if len(self.fireList) == 0:
                self.send_log_json(label='消防车',info=f"没有任何火源信息")
                self.recvOKFlag = False
            else:
                self.send_log_json(label='消防车',info=f"去灭火{','.join(self.fireList)}")
                self.send_log_json(label='car',info='start')
                self.car_paths = find_car_paths(list(self.fireList))
                self.pathsLen = len(self.car_paths)
                self.recvOKFlag = True
        elif fireInfo == 'test':
            self.send_log_json(label='消防车',info=f"测试{'test'}")
            self.send_log_json(label='car',info='start')
            self.car_paths = find_car_paths(['test'])
            self.pathsLen = len(self.car_paths)
            self.recvOKFlag = True
        elif fireInfo == 'reset':
            self.car_paths = None
            self.fireList = []
            self.carTaskOK = False
            self.recvOKFlag = False
            self.aim = pick_aim_by_label(car_route_data,"init")
            pass


    def status_callback(self, msg: String):
        if self.pathsLen == 0:
            return
        if self.recvOKFlag == True and self.carTaskOK == False:
            json_str = msg.data
            label,status = decode_status(json_str)
            self.aim.status = status
            if label == self.aim.label:
                if self.carTaskOK == False and self.aim.status == 'OK' :
                    self.send_log_json(label='消防车',info=f'{self.aim.label}区域巡逻完毕')
                    self.aimIndex  = 1 + self.aimIndex # 上一个任务完成，开始下一个
                    if self.aimIndex == self.pathsLen : # 巡逻完毕，也防止列表越界！
                        self.carTaskOK = True
                        self.car_control_pub.publish(String(data='stopCar'))
                        self.send_log_json(label='消防车',info='灭火任务执行完毕')  
                        return
                    self.aim = self.car_paths[self.aimIndex]
                    self.send_log_json(label='消防车',info=f'正在前往{self.aim.label}巡逻')     
                    self.pub_car_aim()
                

    def pub_car_aim(self):
        msg = String()
        msg.data = encode_aim(x=self.aim.x, y=self.aim.y, deg=self.aim.deg, label=self.aim.label,status=self.aim.status)
        self.car_control_pub.publish(msg)
        self.get_logger().info(f'发布控制: {self.aim}')


if __name__ == '__main__':
    rclpy.init()
    test_node = CarLogicalNode()
    try:
        rclpy.spin(test_node)
    except KeyboardInterrupt:
        pass
    finally:
        test_node.destroy_node()
        rclpy.shutdown()

# if __name__ == '__main__':

#     fireList = []
#     fireList.append('区域A')
#     fireList.append('区域B')
#     fireList.append('区域C')

#     result = ','.join(fireList)
#     print(result)
    # 输出：区域A,区域B,区域C  ✅ 严格按照 append 顺序
 
