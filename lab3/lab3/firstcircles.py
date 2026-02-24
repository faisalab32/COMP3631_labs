import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal


class FirstCircles(Node):
    def __init__(self):
        super().__init__('firstcircle')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz 

    def do_circles(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s
        desired_velocity.angular.z = 0.2 # clockwise with 0.2 Rad/s // I thinin making circle Radius = 1 as mentioned in notes 

        for _ in range(100):  # Stop for a brief moment
            self.publisher.publish(desired_velocity)
            self.rate.sleep()
    
    def stop(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.0  # Send zero velocity to stop the robot
        self.publisher.publish(desired_velocity)


def main():
    def signal_handler(sig, frame):
        first_circle.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    first_circle = FirstCircles()

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=rclpy.spin, args=(first_circle,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            first_circle.do_circles()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()


