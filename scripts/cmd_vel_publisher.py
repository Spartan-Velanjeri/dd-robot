#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import yaml
from ament_index_python.packages import get_package_share_directory
class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/diff_drive_base_controller/cmd_vel_unstamped', 10)
        self.get_logger().info('Cmd Vel Publisher has been started.')

        # Load commands from the YAML file
        self.commands = []
        package_name = 'dd_robot'
        cmd_vel_yaml = os.path.join(get_package_share_directory(package_name), 'config', 'commands.yaml')
        with open(cmd_vel_yaml, 'r') as file:
            self.commands = yaml.safe_load(file)

        # Create a timer to publish commands cyclically
        self.current_command_idx = 0
        self.timer = self.create_timer(1.0, self.publish_cmd)  # Change the period if needed

    def publish_cmd(self):
        msg = Twist()
        cmd = self.commands[self.current_command_idx]
        msg.linear.x = cmd['linear_x']
        msg.angular.z = cmd['angular_z']
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published cmd_vel: linear_x={msg.linear.x}, angular_z={msg.angular.z}')

        # Move to the next command
        self.current_command_idx = (self.current_command_idx + 1) % len(self.commands)

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_publisher = CmdVelPublisher()
    rclpy.spin(cmd_vel_publisher)
    cmd_vel_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
