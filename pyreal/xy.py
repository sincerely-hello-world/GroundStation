
class ObstaclePoint:
    """障碍物坐标点"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ObstacleManager:
    def __init__(self, distance_threshold=0.10):
        self.obstacle_list = []  # 存储 ObstaclePoint 对象列表
        self.distance_threshold = distance_threshold
    
    def add_obstacle(self, x, y):
        """添加障碍物坐标到列表"""
        self.obstacle_list.append(ObstaclePoint(x, y))
    
    def is_similar_coordinate(self, x, y):
        """
        检查坐标是否与列表中任一坐标相似（切比雪夫距离 <= threshold）
        返回: True 表示相似，False 表示不相似
        """
        if  len(self.obstacle_list) == 0:
            return False  # 列表为空，直接返回 False
        for obs in self.obstacle_list:
            # 计算切比雪夫距离：max(|x1-x2|, |y1-y2|)
            chebyshev_distance = max(abs(obs.x - x), abs(obs.y - y))
            if chebyshev_distance <= self.distance_threshold:
                return True
        return False
    
    def clear_list(self):
        """清空列表"""
        self.obstacle_list.clear()


# 创建管理器
manager = ObstacleManager(distance_threshold=0.10)

# # 添加一些障碍物位置
# manager.add_obstacle(1.0, 2.0)
# manager.add_obstacle(3.5, 4.5)
# manager.add_obstacle(0.8, 1.2)

# 检查坐标是否相似
print(manager.is_similar_coordinate(1.05, 2.03))  # True (距离很小)
print(manager.is_similar_coordinate(1.5, 2.5))    # False (距离超过0.10)
print(manager.is_similar_coordinate(0.85, 1.15))  # True (在阈值内)