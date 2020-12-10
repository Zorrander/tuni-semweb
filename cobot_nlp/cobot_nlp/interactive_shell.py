import rclpy
from rclpy.node import Node
from cobot_msgs.msg import Command
from cmd import Cmd

class Listener(Node, Cmd):

    prompt = '(panda) '
    intro = 'Type help or ? to list commands.\n'

    def __init__(self):
        Node.__init__(self, 'interactive_shell')
        Cmd.__init__(self)
        self.pub = self.create_publisher(Command, 'plan_request', 10)

    def do_command(self, arg):
        args = self.parse(arg)
        if len(args) == 2:
            self.get_logger().info('I heard: [%s]' % msg.data)
            # test = self.nlp.run(msg.data)
            test = msg.data.split(' ')
            cmd = Command()
            cmd.action= test[0]
            cmd.targets = [test[1]]
            self.pub.publish(cmd)

    def do_bye(self, arg):
        '''Stop'''
        return True

def main(args=None):
    rclpy.init()

    node = Listener()

    while rclpy.ok():
        rclpy.spin_once(node)
        node.cmdloop()

    # rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
