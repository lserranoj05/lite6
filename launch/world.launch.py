### FICHERO LAUNCH DE LA ESCENA ###
# Inicia Gazebo con la escena indicada
# Sincroniza el reloj de Gazebo con el reloj de ROS2
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    package_path = get_package_share_directory('lite6')
    
    #Nombres de fihceros posibles: 
    #'inclinado.sdf' = plano inclinado; 
    #'base_world_mesa.sdf' = con mesa; 
    #'base_world.sdf' = vacio; 
    #'base_world_pista.sdf' = pista horizontal
    
    escena = 'base_world_mesa.sdf'

    world_file_path = os.path.join(package_path, 'worlds', escena) 
    
    

    return LaunchDescription([
        # Arranca Gazebo con el mundo especificado
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', '-v', '4', world_file_path],
            output='screen'
        ),
        
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
            output='screen'
        ),
    ])

