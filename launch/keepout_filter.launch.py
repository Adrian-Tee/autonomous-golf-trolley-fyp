from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    params_file = "/home/adriantee/ros2_ws/src/mobile_robot_navigation/config/nav2_params.yaml"
    keepout_mask = "/home/adriantee/ros2_ws/maps/keepout_mask.yaml"

    return LaunchDescription([

        Node(
            package="nav2_map_server",
            executable="map_server",
            name="keepout_filter_mask_server",
            output="screen",
            parameters=[
                params_file,
                {"yaml_filename": keepout_mask}
            ],
        ),

        Node(
            package="nav2_map_server",
            executable="costmap_filter_info_server",
            name="keepout_costmap_filter_info_server",
            output="screen",
            parameters=[params_file],
        ),

        Node(
            package="nav2_lifecycle_manager",
            executable="lifecycle_manager",
            name="lifecycle_manager_keepout_zone",
            output="screen",
            parameters=[
                {
                    "use_sim_time": True,
                    "autostart": True,
                    "node_names": [
                        "keepout_filter_mask_server",
                        "keepout_costmap_filter_info_server"
                    ]
                }
            ],
        ),
    ])
