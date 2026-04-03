
#!/bin/bash
## 启动脚本start.sh

 
# 获取当前脚本所在目录的绝对路径（处理软链接等情况更健壮）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo '脚本所在目录: '$SCRIPT_DIR

## 获取上一层目录并赋值给一个变量
#PARENT_DIR=$(dirname "$SCRIPT_DIR") ## 父目录获取
#echo '脚本所在目录的父目录: '$PARENT_DIR

export ROS_LOG_DIR=$SCRIPT_DIR/run_log
echo '日志输出目录: '$ROS_LOG_DIR

echo 'ros2项目构建时所在目录: '$SCRIPT_DIR
# ( cd $SCRIPT_DIR &&  colcon build --symlink-install )
# 初始化
echo 'ros2项目初始化bash所在路径: '$SCRIPT_DIR/install/setup.bash
source $SCRIPT_DIR/install/setup.bash # ros2项目启动bash所在路径

 
 
ros2 launch GroundStation nodes.launch.py
# # 启动项目
# echo 'ros2项目启动python所在路径: '$SCRIPT_DIR/GroundStation/install/GroundStation/share/GroundStation/launch/
# echo 'ros2项目启动python源码所在路径: '$SCRIPT_DIR/GroundStation/src/GroundStation/launch/
# ros2 launch GroundStation uav_car_drone.launch.py


# ros2 pkg create  my_interfaces     --build-type ament_cmake --dependencies rosidl_default_generators builtin_interfaces
# ros2 pkg create  GroundStation      --build-type ament_python --dependencies rclpy  my_interfaces
 
 
