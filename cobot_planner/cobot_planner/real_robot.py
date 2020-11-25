import rclpy
import os
from threading import Thread
import time
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from semrob.robot import robot
from semrob.world import world
from geometry_msgs.msg import Point

from cobot_msgs.msg import Command
from cobot_msgs.srv import ReachCartesianPose, Grasp, MoveGripper, NamedTarget, RobotName
from std_msgs.msg import Empty
from std_srvs.srv import Trigger

# from kb_manager.manager import Manager

class DigitalWorldInterface(Node, world.DigitalWorld):
    def __init__(self):
        Node.__init__(self, 'world_interface')
        world.DigitalWorld.__init__(self)
        time.sleep(3)
        self.robot_name = self.create_client(RobotName, '/robot_name')
        self.subscription = self.create_subscription(
            Point,
            'target_pose',
            self.camera_callback,
            10)

    def get_robot_name(self):
        req = RobotName.Request()
        print("get_robot_name...")
        res = self.robot_name.call(req)
        print(res.name)

    def camera_callback(self, msg):
        self.onto.box1.update_pose(msg.x, msg.y, msg.z)

class RealCollaborativeRobot(Node, robot.CollaborativeRobotInterface):

    def __init__(self):
        Node.__init__(self, 'real_robot')

        world_interface = DigitalWorldInterface()
        spin_thread = Thread(target=rclpy.spin, args=(world_interface,))
        spin_thread.start()

        robot.CollaborativeRobotInterface.__init__(self, world_interface)
        self.target_reached_pub = self.create_publisher(Empty, '/target_reached', 10)
        self.move_to = self.create_client(ReachCartesianPose, '/go_to_cartesian_goal')
        self.grasp = self.create_client(Grasp, '/grasp')
        self.reach_named_target = self.create_client(NamedTarget, '/move_to')
        self.release = self.create_client(MoveGripper, '/move_gripper')
        self.reset = self.create_client(Trigger, '/reset')
        self.sub = self.create_subscription(Command, '/plan_request', self.run, 10)
        ### TODO: remove test objects
        # self.world.add_object("peg")  # Manually create an object or testing purposes
        #self.gui = Manager(self.world)
        #self.world.attach(self.gui)
        #self.gui.start()
        time.sleep(2)
        print("ROBOT RUNNING")

    def say_hello(self):
        pass

    def create_plan(self):
        return self.planner.create_plan()

    def run(self, plan):
        for action in self.planner.run(plan):
            self.perform(action)

    def prompt_welcome(self, commands):
        print()
        print("PANDA PLATFORM INTERFACE")
        print("========================")
        print()
        print("To command the robot use one of the following trigger words:")
        for cmd in commands:
            print("- {}".format(cmd))

    def introduce_itself(self, commands):
        pass

    def pre_notify(self, task):
        print("About to perform {}".format(task))

    def post_notify(self, task):
        print("{} completed".format(task))

    def send_command(self, command_msg):
        print("Received command: ", command_msg)
        action = command_msg.action
        target = command_msg.targets
        return self.world.send_command(action, target)

    def move_operator(self, target):
        print("_use_move_operator {}...".format(target))
        if target.name == "storage":
            req = ReachCartesianPose.Request()
            req.point.x = self.world.onto.storage.x
            req.point.y = self.world.onto.storage.y
            req.point.z = self.world.onto.storage.z
            self.move_to.call_async(req)
        elif target.name == "handover":
            req = ReachCartesianPose.Request()
            req.point.x = self.world.onto.handover.x
            req.point.y = self.world.onto.handover.y
            req.point.z = self.world.onto.handover.z
            self.move_to.call_async(req)
        elif target.name == "init_pose":
            req = NamedTarget.Request()
            req.name = 'ready'
            self.reach_named_target.call_async(req)
        else:
            print("PROBLEM")
        # return move_to

    def close_operator(self, target):
        req = Grasp.Request()
        req.width = 3.0  # [cm]
        req.force = 100.0  # [N]
        print("Grasping {}...".format(target))
        self.grasp.call_async(req)
        # return grasp

    def open_operator(self, target):
        req = MoveGripper.Request()
        req.width = 8.0
        self.release.call_async(req)
        # return release

    def communication_operator(self):
        print("Real robot is communication_operator...")
        msg = Empty()
        self.target_reached_pub.publish(msg)

    def idle_operator(self):
        print("Real robot is waiting...")
        # return wait

    def stop_operator(self):
        def stop():
            print("Stopping...")
        return stop

    def reset_operator(self):
        def reset():
            pass
        return reset

    def handle_anchoring_error(self, object):
        print("REACH FINAL STAGE OF ERROR")
        print("COULD NOT ANCHOR", object)

    def handle_grounding_error(self, object):
        print("COULD NOT GROUND", object)

def main(args=None):
    rclpy.init(args=args)

    robot = RealCollaborativeRobot()

    while rclpy.ok():
        plan = robot.create_plan()
        robot.run(plan)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
