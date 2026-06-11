import json,re, threading
from typing import List, Optional

# pX1 = 0.4
# pX2 = pX1 + 3.5
# pX3 = 
# pX4 = 
# pX5 = 



class myPoint:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.7, 
                 label: str = 'none', qrcode: str = 'none', 
                 label2: str = 'none', qrcode2: str = 'none'):
        self.x = x      # 单位：米
        self.y = y
        self.z = z
        self.label = label
        self.qrcode = qrcode
        self.label2 = label2
        self.qrcode2 = qrcode2

    @classmethod
    def from_dict(cls, data: dict) -> "myPoint":
        """直接从 JSON 解析出的字典生成 Point 对象"""
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.7),
            label=data.get("label", "none"),
            qrcode=data.get("qrcode", "none"),
            label2=data.get("label2", "none"),
            qrcode2=data.get("qrcode2", "none")
        )
    def __repr__(self):
        return f"label:{self.label} (x={self.x}, y={self.y})"

# 航迹点坐标，原点为飞机出发位置
my_paths_point = [
    {"x": 0.00 , "y": 0.00, "z": 1.20, "label": "TakeOff", "qrcode": "",},

    {"x": 0.40 ,     "y": 0.40, "z": 1.20, "label": "A1", "qrcode": "",},
    {"x": 0.40 ,     "y": 0.4+2.4, "z": 1.20, "label": "B1", "qrcode": "",},
    {"x": 0.40+3.5 , "y": 0.4+2.4, "z": 1.20, "label": "F1", "qrcode": "",},

    {"x": 0.40+3.5 , "y": 0.4+2.0, "z": 1.20, "label": "F2", "qrcode": "",},
    {"x": 0.40+0.3 , "y": 0.4+2.0, "z": 1.20, "label": "B2", "qrcode": "",},
    {"x": 0.40+0.3 , "y": 0.4+0.5, "z": 1.20, "label": "A2", "qrcode": "",},

    {"x": 0.40+0.9 ,     "y": 0.4+1.0, "z": 1.20, "label": "G1", "qrcode": "",},
    {"x": 0.40+0.9+2.6 , "y": 0.4+1.0, "z": 1.20, "label": "E1", "qrcode": "",},
    {"x": 0.40+0.9+2.6 , "y": 0.2    , "z": 1.20, "label": "E2", "qrcode": "",},
    {"x": 0.40+0.9+2.1 , "y": 0.3    , "z": 1.20, "label": "E3", "qrcode": "",},
    {"x": 0.40+0.9+2.1 , "y": 0.3+0.8, "z": 1.20, "label": "E4", "qrcode": "",},

    {"x": 0.40+0.9 ,     "y": 0.4+0.5, "z": 1.20, "label": "G2", "qrcode": "",},

    {"x": -0.1 ,         "y": -0.1,    "z": 1.20,  "label": "LandPos", "qrcode": "",},
]
# # 假设 raw_data 是你之前生成的 Python list[dict]
points = [myPoint.from_dict(item) for item in my_paths_point]


def check_pos_region(x, y):
    """
    判断坐标点 (x, y) 属于哪个预定义的矩形区域。
    飞机里程计输出的坐标点，是飞机的当前位置。
    
    参数:
        x, y: 坐标点的数值。
        regions: 字典，键为区域名称（如 'A'），值为该区域的矩形对角点坐标元组。
                 格式: { 'A': ((x1, y1), (x2, y2)), ... }
                 对角点可以是任意顺序（左上-右下 或 左下-右上等）。
    
    返回:
        包含区域名称的字符串，如果不在任何区域内则返回 None。
    
    示例:
        regions = {
            'A': ((0, 0), (10, 10)),
            'B': ((10, 0), (20, 10))
        }
        print(check_region(5, 5))  # 输出 'A'
    """
    x= x+0.4 # 添加起飞位置相对于地图原点偏移
    y= y+0.4

    regions = {
            'A': ((0.3, 0.8), (1.7, 2.3)),
            'B': ((0.3, 2.3), (2.0, 3.8)),
            'C': ((1.7, 2.3), (3.4, 0.8)),
            'D': ((3.4, 2.3), (2.0, 3.8)),

            'E': ((3.4, 2.3), (4.8, 0)),
            'F': ((3.4, 2.3), (4.8, 3.8)),
    }
    for name, (p1, p2) in regions.items():
        # 解析矩形的 x 和 y 范围（自动处理对角点的任意顺序）
        x_min, x_max = sorted([p1[0], p2[0]])
        y_min, y_max = sorted([p1[1], p2[1]])
        
        # 判断点是否在矩形内（边界算在内）
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return name
    return None

import math
from typing import List

# 1. 定义全局变量，用于存储已检测到的 fire 目标点


def is_repeat_fire_aim(x: float, y: float,fireAimList: List[myPoint] = [], threshold: float = 0.5) -> bool:
    """
    判断当前点位是否在已添加的 fireAimList 周围（仅计算 XY 平面）
    
    :param x: 当前点的 X 坐标 (米)
    :param y: 当前点的 Y 坐标 (米)
    :param threshold: 判定为“周围”的距离阈值，默认 0.5 米
    :return: 如果在任意已知目标的 threshold m 范围内返回 True，否则返回 False
    """
    for point in fireAimList:
        # 只计算 XY 平面的欧几里得距离
        distance = math.sqrt((x - point.x) ** 2 + (y - point.y) ** 2)
        
        # 只要有一个点在阈值范围内，就立即返回 True
        if distance < threshold:
            return True
            
    # 遍历完所有点都没有在范围内的，返回 False
    return False

# # ================= 测试用例 =================
# if __name__ == "__main__":
#     fireAimList: List[myPoint] = []
#     # 模拟往全局列表中加点
#     fireAimList.append(myPoint(x=5.0, y=5.0, label="fire_1"))
#     fireAimList.append(myPoint(x=10.0, y=2.0, label="fire_2"))

#     # 测试 1: 距离 (5.0, 5.0) 只有 0.5m，应该返回 True
#     print(is_repeat_fire_aim(5.3, 5.1,fireAimList))  # 输出: True

#     # 测试 2: 距离最近的点超过 1.0m，应该返回 False
#     print(is_repeat_fire_aim(6.5, 6.5,fireAimList))  # 输出: False

#     # 测试 3: 刚好在 1.0m 边界上，应该返回 True
#     print(is_repeat_fire_aim(11.0, 2.0,fireAimList)) # 输出: True

#     # 测试 4: 列表为空时的表现
#     fireAimList.clear()
#     print(is_repeat_fire_aim(5.0, 5.0,fireAimList))  # 输出: False

 
# ================= 使用示例 =================
if __name__ == "__main__":


    # 测试几个点
    test_points = [(0.5, 0.5), (0.5, 3.2)]
    
    # for x, y in test_points:
    #     region = check_pos_region(x, y)
    #     print(f"点 ({x}, {y}) 位于区域: {region if region else '无'}")
    point_fire = points[0:1]
    for point in points:
        # print(point)
        # print(point.label, check_pos_region(point.x, point.y))
        print(point.label, is_repeat_fire_aim(point.x,point.y,point_fire))
 



 
# def find_point_by_label(self,paths: List[Point], label: str) -> Optional[Point]:
#     """
#     根据 label 查找 Point，支持精确匹配，未找到时返回 None
#     """
#     if not paths or not label:
#         return None
#     label = str(label).strip()
#     for p in paths:
#         if str(p.label).strip() == label :
#             self.get_logger().info(f"Found point with label: [{p.label}],{p.x, p.y, p.z}")
#             return p
#     return None

# def find_points_by_labels(self,paths: List[Point], labels: List[str]) -> Optional [List[Point]]:
#     """
#     根据多个 label，返回对应的 Point 列表（按 labels 的顺序排列）
    
#     参数:
#         paths: List[Point]      - 所有路径点的完整列表
#         labels: List[str]       - 想要的 label 列表（支持唯一label）
        
#     返回:
#         List[Point]             - 按输入 labels 顺序排列的 Point 列表（找不到的 label 会返回 None,整体返回 None）
#     """
#     if not paths or not labels:
#         return []
#     result: List[Point] = []
#     for label in labels:
#         point = self.find_point_by_label(paths, label)
#         if point is not None:
#             result.append(point)
#         else:
#             self.get_logger().error(f"出错了: Label '{label}' 不在预设的路径列表内！")
#             return None
#     return result