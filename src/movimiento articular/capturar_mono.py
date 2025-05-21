import rclpy
from rclpy.node import Node
import csv
from sensor_msgs.msg import JointState
from datetime import datetime

class JointLogger(Node):
    def __init__(self):
        super().__init__('joint3_logger')

        # Suscribirse al topic donde se publican los JointStates
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',  # <-- Cambia esto por el nombre real del tópico
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

def capturar(args=None):
    rclpy.init(args=args)
    node = JointLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Finalizando...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    capturar()

