#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    fastlio_config_file = LaunchConfiguration("fastlio_config_file")

    description_pkg = FindPackageShare("blueboat_cirtesu_description")
    fastlio_pkg = FindPackageShare("fast_lio")
    localizer_pkg = FindPackageShare("localizer")

    default_fastlio_config = PathJoinSubstitution(
        [fastlio_pkg, "config", "mid360.yaml"]
    )

    localizer_config = PathJoinSubstitution(
        [localizer_pkg, "config", "localizer.yaml"]
    )

    robot_description = Command(
        [
            "xacro ",
            PathJoinSubstitution([description_pkg, "urdf", "blueboat_enu.xacro"]),
        ]
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    fast_lio_node = Node(
        package="fastlio2",
        namespace="fastlio2",
        executable="lio_node",
        name="lio_node",
        output="screen",
        parameters=[
            fastlio_config_file,
            {"use_sim_time": use_sim_time},
        ],
    )

    localizer_node = Node(
        package="localizer",
        executable="localizer_node",
        namespace="localizer",
        name="localizer_node",
        output="screen",
        parameters=[
            {
                "config_path": localizer_config,
            }
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
            ),
            DeclareLaunchArgument(
                "fastlio_config_file",
                default_value=default_fastlio_config,
            ),
            robot_state_publisher_node,
            fast_lio_node,
            localizer_node,
        ]
    )