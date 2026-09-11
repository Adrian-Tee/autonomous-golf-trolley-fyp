import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_path = get_package_share_directory('mobile_robot_navigation')
    slam_config = os.path.join(pkg_path, 'config', 'slam_toolbox.yaml')

    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[
                slam_config,
                {'use_sim_time': True}
            ],
            arguments=['--ros-args', '--log-level', 'info'],
            output='screen'
        ),
    ])
