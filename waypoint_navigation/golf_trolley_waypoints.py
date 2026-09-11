#!/usr/bin/env python3

import math
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


# ============================================================
# GPS-TO-MAP REFERENCE POINT
#
# These GPS and AMCL values were measured at the same trolley
# position.
# ============================================================

REFERENCE_LATITUDE = 3.1390272923535383
REFERENCE_LONGITUDE = 101.68698546731835

REFERENCE_MAP_X = 0.064805878453927
REFERENCE_MAP_Y = -0.0052072616703259765

# WGS84 Earth radius in metres
EARTH_RADIUS = 6378137.0


# ============================================================
# GPS WAYPOINTS
#
# Format:
# (latitude, longitude)
#
# These coordinates correspond to your original four RViz
# map waypoints.
# ============================================================

GPS_WAYPOINTS = [
    (3.139026984267732, 101.687053646174945),
    (3.139054143473240, 101.687126190805799),
    (3.139025944003433, 101.687180009146516),
    (3.139024946941456, 101.687201155244622),
]


def gps_to_map(
    latitude: float,
    longitude: float,
) -> tuple[float, float]:
    """
    Convert a GPS latitude and longitude into Nav2 map x and y.

    Gazebo ENU convention:
      East  = positive map x
      North = positive map y
    """

    reference_latitude_rad = math.radians(REFERENCE_LATITUDE)

    latitude_difference_rad = math.radians(
        latitude - REFERENCE_LATITUDE
    )

    longitude_difference_rad = math.radians(
        longitude - REFERENCE_LONGITUDE
    )

    east_displacement = (
        EARTH_RADIUS
        * math.cos(reference_latitude_rad)
        * longitude_difference_rad
    )

    north_displacement = (
        EARTH_RADIUS
        * latitude_difference_rad
    )

    map_x = REFERENCE_MAP_X + east_displacement
    map_y = REFERENCE_MAP_Y + north_displacement

    return map_x, map_y


def calculate_yaw(
    map_waypoints: list[tuple[float, float]],
    index: int,
) -> float:
    """Point every waypoint toward the next waypoint."""

    if index < len(map_waypoints) - 1:
        current_x, current_y = map_waypoints[index]
        next_x, next_y = map_waypoints[index + 1]

    else:
        # Final waypoint follows the direction of the previous segment.
        current_x, current_y = map_waypoints[index - 1]
        next_x, next_y = map_waypoints[index]

    return math.atan2(
        next_y - current_y,
        next_x - current_x,
    )


def create_pose(
    navigator: BasicNavigator,
    map_x: float,
    map_y: float,
    yaw: float,
) -> PoseStamped:
    """Create one Nav2 PoseStamped waypoint in the map frame."""

    pose = PoseStamped()

    pose.header.frame_id = "map"
    pose.header.stamp = navigator.get_clock().now().to_msg()

    pose.pose.position.x = map_x
    pose.pose.position.y = map_y
    pose.pose.position.z = 0.0

    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)

    return pose


def main() -> None:
    rclpy.init()
    navigator = BasicNavigator()

    try:
        print("Waiting for Nav2 and AMCL...")
        navigator.waitUntilNav2Active()

        map_waypoints = []

        print("\nGPS-to-map conversion:")

        # Convert every GPS waypoint into a map coordinate.
        for index, (latitude, longitude) in enumerate(GPS_WAYPOINTS):
            map_x, map_y = gps_to_map(latitude, longitude)

            map_waypoints.append((map_x, map_y))

            print(
                f"Waypoint {index + 1}: "
                f"latitude={latitude:.12f}, "
                f"longitude={longitude:.12f} "
                f"-> map x={map_x:.3f}, y={map_y:.3f}"
            )

        poses = []

        # Create Nav2 PoseStamped messages.
        for index, (map_x, map_y) in enumerate(map_waypoints):
            yaw = calculate_yaw(map_waypoints, index)

            pose = create_pose(
                navigator=navigator,
                map_x=map_x,
                map_y=map_y,
                yaw=yaw,
            )

            poses.append(pose)

            print(
                f"Waypoint {index + 1} orientation: "
                f"yaw={yaw:.3f} rad"
            )

        print(
            f"\nSending {len(poses)} GPS-derived waypoints to Nav2..."
        )

        navigator.followWaypoints(poses)

        previous_waypoint = -1

        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()

            if feedback is not None:
                current_waypoint = getattr(
                    feedback,
                    "current_waypoint",
                    None,
                )

                if (
                    current_waypoint is not None
                    and current_waypoint != previous_waypoint
                ):
                    print(
                        f"Travelling to waypoint "
                        f"{current_waypoint + 1}/{len(poses)}"
                    )

                    previous_waypoint = current_waypoint

            time.sleep(0.5)

        result = navigator.getResult()

        if result == TaskResult.SUCCEEDED:
            print("SUCCESS: All GPS waypoints completed.")

        elif result == TaskResult.CANCELED:
            print("CANCELED: GPS waypoint mission was cancelled.")

        elif result == TaskResult.FAILED:
            print("FAILED: Nav2 could not complete the GPS mission.")

        else:
            print(f"Mission ended with result: {result}")

    except KeyboardInterrupt:
        print("\nCancelling GPS waypoint mission...")
        navigator.cancelTask()

    except Exception as error:
        print(f"ERROR: {error}")

    finally:
        navigator.destroyNode()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
