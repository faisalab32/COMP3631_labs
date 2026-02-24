import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal


class FirstSquare(Node):
    def __init__(self):
        super().__init__('firstsquare')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz 
        
#--------------------------------------------------------------------------------------------------------------
    
    def walk_forward(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s

        for _ in range(30):  # Stop for a brief moment
            self.publisher.publish(desired_velocity)
            self.rate.sleep()

    def turn_right(self):
        desired_velocity = Twist()
        desired_velocity.angular.z = -0.5197 
        for _ in range(30):  # Stop for a brief moment
            self.publisher.publish(desired_velocity)
            self.rate.sleep()

#--------------------------------------------------------------------------------------------------------------

    def stop(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.0  # Send zero velocity to stop the robot
        self.publisher.publish(desired_velocity)

def main():
    def signal_handler(sig, frame):
        first_square.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    first_square = FirstSquare()

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=rclpy.spin, args=(first_square,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            first_square.walk_forward() # would be something like "move forward // rightangleturn // moveforward"
            first_square.turn_right() #first line done 
            first_square.walk_forward() 
            first_square.turn_right() # second line done 
            first_square.walk_forward() 
            first_square.turn_right() # third line done 
            first_square.walk_forward() 
            first_square.turn_right() # 4th line done 
            first_square.walk_forward() 
            first_square.turn_right()
            
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()


