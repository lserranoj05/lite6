### FICHERO LAUNCH DEL ROBOT ###
# Incluye el modelo del robot en la simulacion de Gazebo
# Lanza ROS2 Control
# Lanza los nodos que publican informacion de su estado
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    
    # Nombre del paquete
    pkg_path = get_package_share_directory('lite6')

    # Ruta del archivo URDF
    urdf_file_path = os.path.join(pkg_path, 'urdf','lite6.urdf')
    
     # Leer el contenido del URDF
    with open(urdf_file_path, 'r') as urdf_file:
        robot_desc = urdf_file.read()

    # Definir la descripción del robot
    robot_description = {'robot_description': robot_desc}
    
    node_robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description, {'use_sim_time': use_sim_time}]
    )
    
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-string', robot_desc,
            '-x', '0.0', #0.0 normal; -3 rampa; 9 pista
            '-y', '0.9',
            '-z', '0.20', # 0.50 tumbado; 0.0 de pie; 9 rampa
            '-R', '1.5708', # 1.5708 tumbado; 0.0 de pie
            '-P', '0.0',
            '-Y', '0.0',
            '-name', 'lite6_robot',
            '-allow_renaming', 'false'
        ],
    )
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager", "/controller_manager"],
    )
    
    robot_controller_spawner = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

        
    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
        output='screen'
    )
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster",
                   "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([ 
    # Cuando gz_spawn_entity termina, lanza joint_state_broadcaster_spawner
    RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        ),
        
        # Cuando joint_state_broadcaster_spawner termine, lanza robot_controller_spawner
    RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[robot_controller_spawner],
        )
    ),
    gz_spawn_entity,
    node_robot_state_publisher,   
    bridge,
    ])
