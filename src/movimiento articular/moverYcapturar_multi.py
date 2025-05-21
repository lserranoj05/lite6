import rclpy
from rclpy.node import Node
import csv
import time
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from datetime import datetime

class JointLogger(Node):
    def __init__(self):
        super().__init__('joint_logger')
        self.done = False

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

        self.capture_active = False
        self.goal_positions = None
        self.epsilon = 0.001  # Tolerancia para considerar alcanzado el objetivo

    def set_goal_positions(self, positions):
        self.goal_positions = positions
        self.capture_active = True
        self.get_logger().info('Inicio de captura de datos de articulaciones.')

    def listener_callback(self, msg):
        if not self.capture_active or self.goal_positions is None:
            return

        joint_indices = {name: i for i, name in enumerate(msg.name)}
        if not all(joint in joint_indices for joint in self.joint_names):
            return

        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        data_row = [timestamp]

        current_positions = []
        for joint in self.joint_names:
            idx = joint_indices[joint]
            pos = msg.position[idx]
            vel = msg.velocity[idx] if idx < len(msg.velocity) else 0.0
            eff = msg.effort[idx] if idx < len(msg.effort) else 0.0
            current_positions.append(pos)
            data_row.extend([pos, vel, eff])

        self.writer.writerow(data_row)

        if all(abs(p - g) < self.epsilon for p, g in zip(current_positions, self.goal_positions)):
            self.get_logger().info('Posición objetivo alcanzada. Finalizando captura.')
            #rclpy.shutdown()
            self.done = True

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def enviar_comando_inicial(node):
    publisher = node.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

    msg = JointTrajectory()
    msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

    goal_positions = [0.0, 0.0, 3.14, 0.0, 0.0, 0.0]

    point = JointTrajectoryPoint()
    point.positions = goal_positions
    point.time_from_start.sec = 2
    point.time_from_start.nanosec = 0

    msg.points.append(point)

    node.get_logger().info('Enviando comando inicial al robot...')
    publisher.publish(msg)

    time.sleep(1.0)
    node.set_goal_positions(goal_positions)

def capturar(args=None):
    rclpy.init(args=args)
    node = JointLogger()

    enviar_comando_inicial(node)

    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        node.get_logger().info('Finalizando manualmente...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    capturar()

