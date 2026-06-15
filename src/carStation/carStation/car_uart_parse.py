import serial
import time
import re
import json,math
from typing import Tuple
 
import math
from typing import Tuple

def encode_aim(x: float, y: float, deg: float, label='N',status='NO') -> str:
    """生成JSON字符串"""
    data = {"x": x, "y": y, "deg": deg,"label":label,"status":status}
    return json.dumps(data)

def decode_aim(json_str: str) -> tuple:
    """解析JSON字符串,返回(x, y, deg, label, status)"""
    data = json.loads(json_str)
    return data["x"], data["y"], data["deg"], data["label"], data["status"]

def encode_status(label:str,status='NO'):
    data = {"label":label,"status":status}
    return json.dumps(data)
def decode_status(json_str: str) -> tuple:
    """解析JSON字符串,返回(label, status)"""
    data = json.loads(json_str)
    return data["label"], data["status"]




class car_aim:
    def __init__(self, x=0.0, y=0.0, deg=0.0, yaw =0.0, flag=True, label='N',status='NO',):
        '''
        flag=True :初始化参数填 deg角度
        flag=False:初始化参数填 yaw弧度
        '''
        self.x = x
        self.y = y
        self.label = label
        self.status = status
 
        if flag ==  True:
            self.deg = deg  # 角度值（度）
            self.yaw = math.radians(deg)  # 弧度值
            # 可选：将弧度规范化到 [-pi, pi) 范围
            self.yaw = math.remainder(self.yaw, 2 * math.pi)
        else:       
            self.yaw = math.remainder(yaw, 2 * math.pi)
            self.deg = self.yaw * 180 / math.pi
    def __repr__(self):
        return f"label:{self.label} (x={self.x}, y={self.y}, deg={self.deg})"

def compute_rotation_cmd(current_yaw: float, target_yaw: float,
                        max_angular: float = 1.5,
                        min_angular: float = 0.8,
                        tolerance_yaw: float = 0.07,
                        kp: float = 0.9):
    """
    改进的旋转控制函数
    """
    import math
    
    # 使用math.remainder确保角度差在[-π, π]范围内
    yaw_error = math.remainder(target_yaw - current_yaw, 2 * math.pi)
    
    # 强制将 yaw_error 设为正的 math.pi，确保机器人坚定地向一个方向旋转，不再抽搐 # 仅仅单向移动时！
    if abs(abs(yaw_error) - math.pi) < 0.06:  # 0.05 弧度约等于 2.8 度
        yaw_error = math.pi

    # 添加死区控制，避免在目标附近震荡
    if abs(yaw_error) < tolerance_yaw:
        print("yaw ok")
        return 0.0, True
    
    # 使用PID控制器的思想，但简化为比例控制
    angular_vel = kp * yaw_error
    
    # 限制角速度
    angular_vel = max(-max_angular, min(angular_vel, max_angular))
    
    # 当角速度很小时，确保不低于最小值（但方向正确）
    if abs(angular_vel) < min_angular and abs(yaw_error) > tolerance_yaw:
        angular_vel = min_angular if angular_vel > 0 else -min_angular
    
    # 检查是否到达目标
    reached = abs(yaw_error) <= tolerance_yaw
    print(f"{angular_vel:.2f}{reached}")
    return angular_vel, reached

def is_target_front(current_x, current_y, current_yaw, target_x, target_y):
    """
    判断目标点是否在机器人车头前方（前方180度范围内）
    
    返回值:
    True  -> 目标点在车头前方
    False -> 目标点在车头后方
    """
    # 1. 计算目标点相对于机器人的位置差（世界坐标系）
    dx = target_x - current_x
    dy = target_y - current_y
    
    # 2. 坐标变换：将目标点转换到机器人的“本体坐标系”
    # 也就是把机器人的朝向 current_yaw 当作 0度，计算目标点的相对坐标
    # target_x_local 代表目标点在机器人“前后方向”上的距离
    target_x_local = dx * math.cos(current_yaw) + dy * math.sin(current_yaw)
    
    # 3. 判断：如果局部X坐标大于0，说明在车头前方；小于0则在后方
    if target_x_local > -0.1 : return True
    return False

 
def compute_pose_to_pose_command(current_x: float, current_y: float, current_yaw: float,
                                 target_x: float, target_y: float, target_yaw: float,
                                 # 运动参数
                                 max_linear: float = 0.18,
                                 min_linear: float = 0.05,
                                 max_angular: float = 1.2,
                                 min_angular: float = 0.85,
                                 # 控制阈值
                                 angle_to_target_thresh: float = 0.05,   # 朝向目标点的角度容差(rad)
                                 dist_to_target_thresh: float = 0.05,    # 离目标点距离容差(m)
                                 yaw_to_target_thresh: float = 0.04,    # 最终朝向容差(rad)
                                 kp_angular: float = 0.9,
                                 kp_linear: float = 0.5,
                                 turn_flag = False,
                                 ) -> Tuple[float, float, bool]:
    """
    分阶段逼近目标点（x, y, yaw）
    返回: (linear_vel, angular_vel, task_complete)
    """
    current_yaw = math.remainder(current_yaw, 2 * math.pi)
    is_target_in_front = is_target_front(current_x, current_y, current_yaw, target_x, target_y)

    # 1. 计算相对位置（目标在当前机器人坐标系下的坐标）
    dx = target_x - current_x
    dy = target_y - current_y
    distance = max(abs(dx), abs(dy))
    # 最终偏航误差
    final_yaw_error = math.remainder(target_yaw - current_yaw, 2 * math.pi)

    # 目标点相对于机器人的朝向角
    if distance < dist_to_target_thresh+0.12: # 如果要使用后退方案。 问题：目标点附近会前后剧烈震荡！
        # print("🎯 位置已到达！抛弃位置修正，全力修正最终朝向...")
        # 近距离：直接使用当前朝向和目标朝向的偏角
        angle_to_target = target_yaw
        angle_error = final_yaw_error
    else:
        # 远距离：使用目标点坐标向量！
        angle_to_target = math.atan2(dy, dx)
        angle_error = abs(math.remainder(angle_to_target - current_yaw, 2 * math.pi))
        # if is_target_in_front == False : # 不在前方，目标角度+pi # 如果要使用后退方案。
        #     angle_to_target = angle_to_target + math.pi
    angle_to_target = math.atan2(dy, dx)
    angle_error = abs(math.remainder(angle_to_target - current_yaw, 2 * math.pi))
     
 

    # print(f"当前角度{math.degrees(current_yaw):.2f}°,目标角度{math.degrees(target_yaw):.2f}°,实际{math.degrees(angle_to_target):.2f},误差{math.degrees(angle_error):.2f}°,")
    # print(f"当前位置{current_x:.2f},{current_y:.2f},目标位置{target_x:.2f},{target_y:.2f}")

    # 2. 判断任务完成
    if distance <= dist_to_target_thresh and abs(final_yaw_error) < yaw_to_target_thresh+0.05:
        # print("00000,任务完成！")
        return 0.0, 0.0, True
    

    # 3. 分阶段决策
    # ---------- 阶段2:直线移动（接近目标点） ----------
    if distance > dist_to_target_thresh:
        if 1:#is_target_in_front:
            # 前方:前向移动 + 动态微调朝向 (允许边走边修偏)
            linear_vel = kp_linear * distance
            linear_vel = max(min_linear, min(linear_vel, max_linear))
            
            # 微调角速度（持续跟踪目标点）
            cmd_w, _ = compute_rotation_cmd(current_yaw, angle_to_target,
                                            max_angular=max_angular, min_angular=min_angular,
                                            tolerance_yaw=0.03, kp=kp_angular) # tolerance让其持续微调
            print(f"222222,阶段2:前向移动,边走边微调{linear_vel:.2f},{cmd_w:.2f}")
            if angle_error > angle_to_target_thresh and distance > dist_to_target_thresh + 0.15:
                # 【新增判断逻辑】角度偏差过大，强制线速度为 0，只进行原地旋转纠偏
                linear_vel = 0.0
                print(f"前进，暂停移动，原地纠偏中{linear_vel:.2f},{cmd_w:.2f}...")
            return linear_vel, cmd_w*1.2, False
            
        else:
            # 后方:倒车移动 + 动态微调朝向
            linear_vel = -kp_linear * distance
            linear_vel = max(-max_linear, min(linear_vel, -min_linear))
            
            target_angle_for_back = -math.remainder(angle_to_target , 2 * math.pi)
            cmd_w, _ = compute_rotation_cmd(current_yaw, angle_to_target,
                                            max_angular=max_angular, min_angular=min_angular,
                                            tolerance_yaw=0.03, kp=kp_angular)
            print("333333,阶段2:后向倒车,边退边微调 ")
            if angle_error > angle_to_target_thresh and distance > 0.10:
                # 【新增判断逻辑】角度偏差过大，强制线速度为 0，只进行原地旋转纠偏
                linear_vel = 0.0
                print(f"后退，暂停移动，原地纠偏中...")
            return linear_vel-0.05, cmd_w, False
    # ---------- 阶段3:最终朝向精调 ----------
    # (此部分保持你的原逻辑不变)
    # elif distance <  dist_to_target_thresh :
    else:
        # cmd_w, reached_yaw = compute_rotation_cmd(current_yaw, target_yaw,
        #                                           max_angular=max_angular, min_angular=min_angular,
        #                                           tolerance_yaw=yaw_to_target_thresh,
        #                                           kp=kp_angular)
        # if reached_yaw:
        #     print("22222,任务完成！(包含最终朝向)")
        #     return 0.0, 0.0, True
        # else:
        #     print("44444,阶段3:到达位置,最终朝向精调")
        #     return 0.0, cmd_w, False
        return 0.0, 0.0, True

    
    # fallback（正常情况下不会到这里）
    print("555555,fallback:默认停止")
    return 0.0, 0.0, True


def my_ser_write(ser, command):
    ser.write(command.encode())
    time.sleep(0.2)  # 确保命令发送完成

def my_init_car_parameters(my_ser, baudrate=115200):
    
    # my_ser_write(my_ser, "$upload:1,0,0#")  # 请求上报编码器数据 Request to report encoder data
    my_ser_write(my_ser, "$upload:0,0,0#") # 不上报编码器数据,减少串口负担
    my_ser_write(my_ser, "$mtype:2#")  # 配置电机类型 Configure motor type
    my_ser_write(my_ser, "$mphase:20#")  # 配置减速比 Configure the reduction ratio
    my_ser_write(my_ser, "$mline:13#")  # 配置磁环线 Configure the magnetic ring wire
    my_ser_write(my_ser, "$wdiameter:46.60#")  # 配置轮子直径 Configure the wheel diameter
    my_ser_write(my_ser, "$deadzone:2100#")  # 配置电机死区 Configure the motor dead zone # 1700~2400合适
    # my_ser_write(my_ser, "$MPID:1.15,0.06,0.5#")  # 配置PID参数 Configure PID parameters

def my_control_speed(my_ser, m1, m2, m3, m4):
    my_ser_write(my_ser, "$spd:{},{},{},{}#".format(m1, m2, m3, m4))

def parse_int_data(frame):
    frame = frame.strip()  # 去掉两端的空格或换行符
    if frame.startswith("$MAll:") and frame.endswith("#"):
        content = frame[6:-1]
        try:
            # 1. 解析为整数列表
            nums = [int(x) for x in content.split(',')]
            
            # 2. 符号反转:第1个(索引0) 和 第4个(索引3)
            if len(nums) >= 4:
                nums[1] = -nums[1]
                nums[2] = -nums[2]
            return nums
        except (ValueError, IndexError):
            return None
    return None

def get_dis_left_right(data):
    nums = parse_int_data(data)
    if nums is not None:
        # left_distance = (nums[0]+nums[2])/2
        # right_distance = (nums[1]+nums[3])/2
        # left_distance =  nums[2] 
        # right_distance = nums[3] 
        left_distance =  nums[0] 
        right_distance = nums[1] 
        return left_distance, right_distance
    return 0, 0

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster

class VelocityCalculator:
    def __init__(self, wheel_radius_mm=46.5, wheel_track_mm=130, mm_PER_TICK=0.13912764571428574):
        self.METERS_PER_TICK = mm_PER_TICK / 1000.0
        self.wheel_track = wheel_track_mm / 1000.0

        self.last_linear_velocity = 0.0
        self.last_angular_velocity = 0.0
        
        self.last_left_encoder = None
        self.last_right_encoder = None
        self.last_time = None

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
 
        # 滤波系数
        self.alpha = 0.8 

    def update(self, left_encoder, right_encoder):
        current_time = time.time()
        
        if self.last_left_encoder is None:
            self.last_left_encoder = left_encoder
            self.last_right_encoder = right_encoder
            self.last_time = current_time
            return 0.0, 0.0,self.x, self.y, self.theta

        dt = current_time - self.last_time
        if dt <= 0: return self.last_linear_velocity, self.last_angular_velocity

        # 1. 计算位移
        d_left = (left_encoder - self.last_left_encoder) * self.METERS_PER_TICK 
        d_right = (right_encoder - self.last_right_encoder) * self.METERS_PER_TICK * 0.999 # 经验修正右轮略快问题

        # 2. 异常跳变检查 (如编码器重启或溢出)
        if abs(d_left) > 0.5 or abs(d_right) > 0.5:
            # 重置缓存,跳过本次计算
            self.last_left_encoder, self.last_right_encoder = left_encoder, right_encoder
            self.last_time = current_time
            return 0.0, 0.0,self.x, self.y, self.theta

        # 3. 计算原始速度 单位均为米
        raw_dis = (d_left + d_right) / 2.0              # 平均位移
        raw_v = raw_dis /  dt                           # 线速度
        raw_θ = (d_right - d_left) / self.wheel_track   # 角位移
        raw_w = raw_θ /   dt                            # 角速度
        import math

        avg_theta = self.theta #+ (raw_θ / 2.0)
        raw_dx = math.cos(avg_theta) * raw_dis
        raw_dy = math.sin(avg_theta) * raw_dis

        
        self.x += raw_dis * math.cos(avg_theta)
        self.y += raw_dis * math.sin(avg_theta)
        self.theta += raw_θ
        # 归一化角度到[-π, π]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

 
        self.last_linear_velocity = raw_v
        self.last_angular_velocity = raw_w

        # 5. 更新状态
        self.last_left_encoder, self.last_right_encoder = left_encoder, right_encoder
        self.last_time = current_time

        return raw_v, raw_w, self.x, self.y, self.theta

    def set_speed(self, linear_vel, angular_vel):

        # 轮距,单位米 
        # 轮速,单位米/秒
        # 速度控制算法（如PID）可以在这里实现
        self.left_vel = linear_vel - (angular_vel * self.wheel_track / 2.0)
        self.right_vel = linear_vel + (angular_vel * self.wheel_track / 2.0)
        return self.left_vel, self.right_vel
    
        # v_x = msg.linear.x      # 线速度  0~1m/s
        # omega = msg.angular.z   # 角速度  0~1rad/s
        # L = 0.13 # 轮距,单位米
        # v_left = v_x - (omega * L / 2)
        # v_right = v_x + (omega * L / 2)

#   每个脉冲的行程  (3.141592*46.5)/1050/1000 =  0.13912764571428574 mm
