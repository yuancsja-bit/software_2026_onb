import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import Joy

class Translator(Node): 

    def __init__(self):
        super().__init__('translator') #calls __init__ function of inherited class (Node). What should the name be?
        self.subscription = self.create_subscription( #declares that this node can publish messages 
            Joy, #message type
            'joy', #actual topic name?
            self.listener_callback, #runs when a message is received
            10 #queue size
        )
        self.subscription #not entirely sure why this is needed for subscription but not publisher

        self.publisher_ = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds',10) #what is the topic name???

    def listener_callback(self,msg): 
        #print(msg)
        twist_msg = self.joy_to_twiststamped(msg)
        self.publisher_.publish(twist_msg)

    def joy_to_twiststamped(self,msg: Joy) -> Twist: #translator function
        translated = TwistStamped()

        if len(msg.axes) > 0: #gets joy input
            x_move = msg.axes[0]
            z_move = msg.axes[1]

            translated.twist.linear.x = x_move
            translated.twist.linear.z = z_move
        if len(msg.buttons) > 0:
            a_button = msg.buttons[0]
            b_button = msg.buttons[1]
            x_button = msg.buttons[2]
            y_button = msg.buttons[3]
        
        
        if y_button == 1 and last_y_input == 0:
            translated.twist.linear.y = 0.7

        if x_button > 0:
            translated.twist.angular.x = 0.7
        if b_button > 0:
            translated.twist.angular.y = 0.7
        if a_button > 0:
            translated.twist.angular.z = 0.7
        
        translated.header.stamp = self.get_clock().now().to_msg()

        #print(translated)
        return translated
        

def main(args=None):
    #print("about to initialize")
    rclpy.init(args=args) #no idea what this does beyond that it's mandatory
    #print("initialized")
    translator = Translator()
    #print("node created")
    rclpy.spin(translator)

    translator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__': #only runs main() when it's run directly, and not if it's being imported for its modules
    main()