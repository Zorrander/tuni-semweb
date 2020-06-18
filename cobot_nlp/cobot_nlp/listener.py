import rclpy
from rclpy.node import Node
from .nlp import NLP
from std_msgs.msg import String
from cobot_msgs.msg import Command

class Listener(Node):

    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(String, 'command', self.chatter_callback, 10)
        self.pub = self.create_publisher(Command, 'plan_request', 10)
        self.nlp = NLP()

    def chatter_callback(self, msg):
        self.get_logger().info('I heard: [%s]' % msg.data)
        test = self.nlp.run(msg.data)
        print("Result processing")
        print(test)
        if test:
            cmd = Command()
            cmd.action=test[0]
            cmd.targets = test[1]
            self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
