import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command

def generate_launch_description():

    pkg_gazebo = get_package_share_directory('mobile_robot_gazebo')
    pkg_description = get_package_share_directory('mobile_robot_description')

    world_file = os.path.join(pkg_gazebo, 'worlds', 'golf_training.world')
    xacro_file = os.path.join(pkg_description, 'urdf', 'golf_trolley.urdf.xacro')

    robot_desc = Command(['xacro ', xacro_file])

    return LaunchDescription([

        # Start Gazebo with your world
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_file],
            output='screen'
        ),

        # Publish robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc,
                        'use_sim_time': True}],
            output='screen'
        ),

        # Spawn robot into Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'golf_trolley',
                '-topic', 'robot_description',
                '-x', '1.5',
                '-y', '3.5',
                '-z', '0.25',
                '-Y', '1.5708'
            ],
            output='screen'
        ),
    ])
