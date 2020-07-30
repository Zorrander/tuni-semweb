import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from cobowl.robot import CollaborativeRobotInterface

from cobot_msgs.msg import Command
from cobot_msgs.srv import ReachCartesianPose, Grasp, MoveGripper

class RealCollaborativeRobot(Node, CollaborativeRobotInterface):

    def __init__(self, knowledge_base_path):
        Node.__init__(self, 'real_robot')
        CollaborativeRobotInterface.__init__(self, knowledge_base_path)
        self.world.add_object("peg")
        self.move_to = self.create_client(ReachCartesianPose, '/go_to_cartesian_goal')
        self.grasp = self.create_client(Grasp, '/grasp')
        self.release = self.create_client(MoveGripper, '/move_gripper')
        self.sub = self.create_subscription(Command, '/plan_request', self.send_command, 10)

    def move_operator(self, target):
        def move_to():
            req = ReachCartesianPose.Request()
            print("_use_move_operator {}...".format(target))
            req.type = 0 if target[0].name == "storage" else 1  # else target.name = "handover"
            # TODO:retrieve from KB
            print(req)
            self.move_to.call_async(req)
            print("plan moving on")
        return move_to

    def close_operator(self, target):
        def grasp():
            req = Grasp.Request()
            req.width = 2.0  # [cm]
            req.force = 50.0  # [N]
            print("Grasping {}...".format(target))
            self.grasp.call_async(req)
        return grasp

    def open_operator(self):
        def release():
            req = MoveGripper.Request()
            req.width = 8.0
            self.release.call_async(req)
        return release

    def idle_operator(self):
        def wait():
            print("Waiting...")
        return wait

    def stop_operator(self):
        def stop():
            print("Stopping...")
        return stop

    def reset_operator(self):
        def reset():
            print("Reseting...")
        return reset


def main(args=None):
    rclpy.init(args=args)
    RESOURCE_PATH = get_package_share_directory('cobot_knowledge')
    kb_path = Path(RESOURCE_PATH)/'handover.owl')
    node = RealCollaborativeRobot()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
