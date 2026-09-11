from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                # ROS -> Gazebo control
                '/cmd_vel_nav@geometry_msgs/msg/Twist]gz.msgs.Twist',

                # Gazebo -> ROS odometry / sensors
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
                
                # Gazebo -> ROS GPS
                '/gps/fix@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',
                # Gazebo -> ROS joint states
                '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',

                # Gazebo -> ROS LiDAR
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',

                # Gazebo -> ROS RGB-D camera
                '/rgbd_camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
                '/rgbd_camera/depth_image@sensor_msgs/msg/Image[gz.msgs.Image',

                # Gazebo -> ROS TF
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                '/tf_static@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',

                # Gazebo -> ROS clock
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            ],
            output='screen'
        ),
    ])
