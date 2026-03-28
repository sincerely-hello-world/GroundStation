from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 定义所有节点
    return LaunchDescription([
        Node(
            package='GroundStation',
            executable='logical',
        ),
        # Node(
        #     package='GroundStation',
        #     executable='qrcode',
        # ),
    ])