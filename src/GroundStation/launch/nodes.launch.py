from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os
def generate_launch_description():
    pkg = get_package_share_directory('GroundStation')   # 你的 package 名
    navNode_param_yaml = os.path.join(pkg, 'param', 'navNode.yaml')   # 推荐把 param 放到包的 param/ 目录

    # 定义所有节点
    
    return LaunchDescription([
        Node(
            package='GroundStation',
            executable='myMain',
        ),
        Node(
            package='GroundStation',
            executable='navNode',
            parameters=[ navNode_param_yaml ]
        ),
        # Node(
        #     package='GroundStation',
        #     executable='testNode',
        #     parameters=[ navNode_param_yaml ]
        # ),
    ])