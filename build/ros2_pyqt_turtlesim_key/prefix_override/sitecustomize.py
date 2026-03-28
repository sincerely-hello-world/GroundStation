import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/focal/Desktop/2024_GroundStation/install/ros2_pyqt_turtlesim_key'
