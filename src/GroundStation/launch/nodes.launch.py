from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart
def generate_launch_description():
    pkg = get_package_share_directory('GroundStation')   # 你的 package 名
    navNode_param_yaml = os.path.join(pkg, 'param', 'navNode.yaml')   # 推荐把 param 放到包的 param/ 目录

    # 定义所有节点
    node_GroundStation=Node(
        package='GroundStation',
        executable='myMain',
    )

    node_FlyControl=Node(
        package='GroundStation',
        executable='navNode',
        parameters=[ navNode_param_yaml ]
    )

    navTestNode = Node(
        package='GroundStation',
        executable='testNode',
        parameters=[ navNode_param_yaml ]
    )

    node_CarControl=Node(
        package='carStation',
        executable='carNode',
    )

    # 3. 使用 TimerAction 包裹节点 
    node_FlyControl_delay = TimerAction(
        period=3.0,                     # 延迟3秒
        actions=[node_FlyControl]       # 延迟执行的动作
    )
    node_CarControl_delay = TimerAction(
        period=3.0,                     # 延迟3秒
        actions=[node_CarControl]       # 延迟执行的动作
    )

    # 4. 注册事件处理器：当节点A启动完成后，启动定时器
    reg_FlyControl = RegisterEventHandler(
        OnProcessStart(
            target_action=node_GroundStation,
            on_start=[node_FlyControl_delay]  # 节点A启动完成后，开始计时4秒
        )
    )
    # reg_CarControl = RegisterEventHandler(
    #     OnProcessStart(
    #         target_action=node_FlyControl_delay,
    #         on_start=[node_CarControl_delay]  # 节点A启动完成后，开始计时4秒
    #     )
    # )
    
    return LaunchDescription([
        node_GroundStation,
        reg_FlyControl,
        # reg_CarControl
    ])
# node_CarControl_delay4s