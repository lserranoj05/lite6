import rclpy
from rclpy.node import Node
import csv
import time
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from datetime import datetime

class JointLogger(Node):
    def __init__(self):
        super().__init__('joint3_logger')

        # Suscribirse al topic donde se publican los JointStates
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10
        )

        # Crear archivo CSV
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file = open(f'joint3_data_{now}.csv', mode='w', newline='')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(['timestamp_sec', 'position', 'velocity', 'effort'])  # Encabezados

    def listener_callback(self, msg):
        if 'joint3' in msg.name:
            idx = msg.name.index('joint3')

            timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            position = msg.position[idx]
            velocity = msg.velocity[idx]
            effort = msg.effort[idx]

            self.writer.writerow([timestamp, position, velocity, effort])
            self.get_logger().info(f'Guardado joint3 -> Pos: {position}, Vel: {velocity}, Eff: {effort}')

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def enviar_comando_inicial(node):
    publisher = node.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

    msg = JointTrajectory()
    msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

    point = JointTrajectoryPoint()
    point.positions = [0.0, 0.0, 3.14, 0.0, 0.0, 0.0]
    point.time_from_start.sec = 2
    point.time_from_start.nanosec = 0

    msg.points.append(point)

    # Publicar mensaje
    node.get_logger().info('Enviando comando inicial al robot...')
    publisher.publish(msg)
    # Esperar 2 segundos
    #time.sleep(3.0)


def capturar(args=None):
    rclpy.init(args=args)
    node = JointLogger()

    # Enviar comando inicial antes de comenzar a capturar
    enviar_comando_inicial(node)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Finalizando...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    capturar()

