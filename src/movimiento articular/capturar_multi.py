import rclpy
from rclpy.node import Node
import csv
from sensor_msgs.msg import JointState
from datetime import datetime

class JointLogger(Node):
    def __init__(self):
        super().__init__('joint_logger')

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10
        )

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file = open(f'joint_data_{now}.csv', mode='w', newline='')
        self.writer = csv.writer(self.csv_file)

        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        headers = ['timestamp_sec']
        for joint in self.joint_names:
            headers += [f'{joint}_pos', f'{joint}_vel', f'{joint}_eff']
        self.writer.writerow(headers)

    def listener_callback(self, msg):
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        data_row = [timestamp]

        joint_data = {name: (0.0, 0.0, 0.0) for name in self.joint_names}
        for i, name in enumerate(msg.name):
            if name in self.joint_names:
                pos = msg.position[i] if i < len(msg.position) else 0.0
                vel = msg.velocity[i] if i < len(msg.velocity) else 0.0
                eff = msg.effort[i] if i < len(msg.effort) else 0.0
                joint_data[name] = (pos, vel, eff)

        for joint in self.joint_names:
            data_row.extend(joint_data[joint])

        self.writer.writerow(data_row)
        self.get_logger().info(f'Datos guardados para las articulaciones: {self.joint_names}')

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

