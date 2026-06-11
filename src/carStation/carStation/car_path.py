import os,sys
# 自动获取当前文件所在目录的上一级目录，并强行加入 Python 的搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from carStation.car_uart_parse import car_aim
 

d1_y = 0.60
d2_y = 0.40+1.5
d3_y = 0.40+1.5+1.4

l1_x = 0.25-1.44
l2_x = 0.25
l3_x = 0.25+1.57
l4_x = 0.25+1.5+0.8

path_C = ["init", "init_1", "node1", "node2","node3","node4","back1", "back2", "over"]
# path_

# 加载航点
car_route_data = [
    {"x": +0.00, "y": 0.00,  "deg": 0,  "label": "init"   }, # 必须有的初始状态
    {"x": +l2_x, "y": 0.00,  "deg": 0,      "label": "init1" },
    {"x": +0.00, "y": 0.00,  "deg": 0,     "label": "node0" }, 
    {"x": +l2_x, "y": d1_y,  "deg": 0,     "label": "node1" }, 
    {"x": +l2_x, "y": d2_y,  "deg": 0,     "label": "node2" },
    {"x": +l3_x, "y": d2_y,  "deg": 0,     "label": "node3" }, 
    {"x": +l3_x, "y": d1_y,  "deg": 0,     "label": "node4" }, 
    {"x": +l2_x+0.4, "y": d2_y,  "deg": 0,     "label": "node5" }, 
    {"x": +l1_x,     "y": d2_y,  "deg": 0,     "label": "node6" }, 
    {"x": +l2_x+0.3, "y": d3_y,  "deg": 0,     "label": "node7" }, 
    {"x": +l1_x, "y": d1_y,  "deg": 0,     "label": "node8" }, 
    {"x": +l1_x, "y": d3_y,  "deg": 0,     "label": "node9" }, 
    {"x": +l3_x, "y": d3_y,  "deg": 0,     "label": "node10" }, 
    {"x": +l4_x, "y": d3_y,  "deg": 0,     "label": "node11" }, 
    {"x": +l4_x, "y": d2_y,  "deg": 0,     "label": "node12" },
    {"x": +l4_x, "y": 0.00,  "deg": 0,     "label": "node13" },
    {"x": +l3_x, "y": 0.00,  "deg": 0,     "label": "node14" },
    {"x": +0.00, "y": d1_y,  "deg": 0,     "label": "node15" },
    {"x": -0.30, "y": -0.30,  "deg": 0,     "label": "node00" },



    # # # 旋转测试
    {"x": +0.0, "y": 0.00,  "deg": 0,  "label": "init"   }, # 必须有的初始状态
    {"x": +0.8, "y": 0.0, "deg": "0",    "label":"init_1"},
    {"x": +0.8, "y": 0.8, "deg": "90",    "label":"1"},
    {"x": -0.0, "y": 0.8, "deg": "180",    "label":"2"},
    {"x": +0.0, "y": 0.0, "deg": "90",    "label":"3"},
    {"x": -0.0, "y": 0.0, "deg": "0",    "label":"4"},
 
]

# A函数：根据单个标签，返回对应的 car_aim 对象
def pick_aim_by_label(car_route_data, find_label):
    # 在 car_route_data 中遍历，找到 label 匹配的那一条数据
    target_data = next((d for d in car_route_data if d["label"] == find_label), None)
    
    # 如果没有找到对应的标签，打印提示并返回 None
    if target_data is None:
        print(f"警告：未找到标签为 '{find_label}' 的航点！")
        return None
        
    # 将找到的字典数据转换为 car_aim 对象并返回
    return car_aim(
        x=target_data["x"], 
        y=target_data["y"], 
        deg=float(target_data["deg"]),
        label=str(target_data["label"])
    )

# B函数：根据标签的顺序列表，返回 car_aim 对象的列表
def find_labels_list(find_labels:list):
    car_aim_list = []
    # 按照 find_labels 列表的顺序，依次调用 A 函数
    for label in find_labels:
        aim_obj = pick_aim_by_label(car_route_data, label)
        # 只有当 A 函数成功返回对象时（即找到了标签），才加入列表
        if aim_obj is not None:
            car_aim_list.append(aim_obj)
    return car_aim_list
def find_car_paths(fire_list:list):
    labels = ["init", "init1", "node1"]
    if 'A' in fire_list:
        labels.extend(["node8","node6"])
    labels.append("node2")

    if 'B' in fire_list:
        labels.extend(["node5","node7","node9","node7","node10"])
    if 'D' in  fire_list:
        if 'B' not in fire_list:
            labels.extend(["node5","node7","node10"])
    labels.append("node3")
    

    if 'F' in fire_list:
        if 'B' not in fire_list and 'D' not in  fire_list:
            labels.pop()
            labels.extend(["node5","node7","node11","node10","node3","node12"])
        else: 
            labels.pop()
            labels.extend(["node11","node10","node3","node12"])
            
    labels.append("node3")

    if 'C' in fire_list and "node10" in fire_list:
        labels.extend(["node5","node3"])
    labels.append("node4")


    if 'E' in fire_list:
        labels.pop()
        labels.extend(["node14","node13","node14"])
        if 'C' in fire_list:
            labels.append("node4")
 
    labels.extend(["node15","node00"])

    if 'test' in fire_list :
        labels = ["init", "init_1", "1","2","3","4"]
        # return final_paths

    final_paths= find_labels_list(labels)


    print(f"待查找火源路线{fire_list}")
    print(f"{'索引':<5} {'标签':<8} {'X坐标':>8} {'Y坐标':>8} {'角度(deg)':>8}")
    print("-" * 50) # 打印一条分割线，让视觉更清晰
    for i, wp in enumerate(final_paths):
        # {:<4} 表示左对齐占4位（索引）
        # {:<12} 表示左对齐占12位（标签，防止标签长短不一导致错位）
        # {:>10.2f} 表示右对齐占10位，保留2位小数的浮点数（坐标和角度）
        print(f"{i:<5} {wp.label:<8} {wp.x:>8.2f} {wp.y:>8.2f} {wp.deg:>8.1f}")


    return final_paths
 
# 所有节点坐标
node_paths = [car_aim(x=d["x"], 
                     y=d["y"], 
                     deg=float(d["deg"]),
                    label=str(d["label"]),
                               ) 
             for d in car_route_data]
# 最终小车航轨
car_paths =  None




if __name__ == "__main__":
    # final_paths = find_car_paths(["D", "F","E"]) #find_labels_list( my_labels)
    final_paths = find_car_paths(["test"]) #find_labels_list( my_labels)
    print(len(final_paths))
 