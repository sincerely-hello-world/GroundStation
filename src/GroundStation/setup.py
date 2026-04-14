from setuptools import setup
import os
from glob import glob

package_name = 'GroundStation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ← 关键：添加这一行，让 param 目录被安装
        (os.path.join('share', package_name, 'imgs'), glob('imgs/img_*.png')),
        (os.path.join('share', package_name, 'param'), glob('param/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='focal',
    maintainer_email='focal@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'myMain = GroundStation.myMain:main',
            'navNode = GroundStation.navNode:main',
            'testNode = GroundStation.testNode:main'
        ],
    },
)
