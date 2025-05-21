import rclpy
from rclpy.node import Node
import time
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class MoveCommander(Node):
    def __init__(self):
        super().__init__('move_commander')
        self.publisher = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

    def send_movement_command(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

        point = JointTrajectoryPoint()
        point.positions = [0.0, 0.0, 3.14, 0.0, 0.0, 0.0] # Rads
        point.time_from_start.sec = 2
        point.time_from_start.nanosec = 0

        msg.points.append(point)

        self.get_logger().info('Enviando comando de movimiento...')
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveCommander()

    # Esperar un pequeño momento para asegurarse de que el publisher está listo
    time.sleep(1.0)

    node.send_movement_command()

    # Esperar 2 segundos después de enviar
    time.sleep(3.0)

    node.get_logger().info('Comando enviado. Cerrando nodo...')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

