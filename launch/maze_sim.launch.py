import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg_maze_nav = get_package_share_directory('maze_navigation')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    robot_sdf = os.path.join(
        pkg_turtlebot3_gazebo,
        'models',
        'turtlebot3_burger',
        'model.sdf'
    )

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='simple_maze.world',
        description='World file inside maze_navigation/worlds'
    )
    spawn_x_arg = DeclareLaunchArgument('spawn_x', default_value='0.5')
    spawn_y_arg = DeclareLaunchArgument('spawn_y', default_value='0.5')

    world = LaunchConfiguration('world')
    spawn_x = LaunchConfiguration('spawn_x')
    spawn_y = LaunchConfiguration('spawn_y')

    world_path = PathJoinSubstitution([pkg_maze_nav, 'worlds', world])

    gz_sim_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r ', world_path]
        }.items()
    )

    start_robot_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', robot_sdf,
            '-name', 'turtlebot3_burger',
            '-x', spawn_x,
            '-y', spawn_y,
            '-z', '0.01',
        ],
        output='screen'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/cmd_vel@geometry_msgs/msg/TwistStamped]gz.msgs.Twist',
        ],
        output='screen'
    )

    

    return LaunchDescription([
        world_arg,
        spawn_x_arg,
        spawn_y_arg,
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),
        gz_sim_cmd,
        start_robot_spawner_cmd,
        start_gazebo_ros_bridge_cmd,
    ])
