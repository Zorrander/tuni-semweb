import os
import time
import rclpy
from rclpy.node import Node
import speech_recognition as sr

from std_msgs.msg import Empty
from std_srvs.srv import Trigger
from geometry_msgs.msg import Point

from semrob.robot import robot
from semrob.world import world

from cobot_msgs.msg import Command
from cobot_msgs.srv import ReachCartesianPose, Grasp, MoveGripper, NamedTarget, ReachJointPose

from cobot_sem.ros_world import DigitalWorldInterface

class RealCollaborativeRobot(Node, robot.CollaborativeRobotInterface):

    def __init__(self):
        Node.__init__(self, 'real_robot')

        self.declare_parameter('world_file')
        param_str = self.get_parameter('world_file')
        world_interface = DigitalWorldInterface(str(param_str.value))

        robot.CollaborativeRobotInterface.__init__(self, world_interface)

        self.target_reached_pub = self.create_publisher(Empty, '/target_reached', 10)
        self.object_released_pub = self.create_publisher(Empty, '/object_released', 10)
        self.joint_move_to = self.create_client(ReachJointPose, '/go_to_joint_space_goal')

        self.human_ready_sub = self.create_subscription(Empty, '/human_ready', self.human_ready, 10)
        self.sub = self.create_subscription(Command, '/plan_request', self.process_command, 10)

        self.cartesian_move_to = self.create_client(ReachCartesianPose, '/go_to_cartesian_goal')
        self.grasp = self.create_client(Grasp, '/grasp')
        self.reach_named_target = self.create_client(NamedTarget, '/move_to')
        self.release = self.create_client(MoveGripper, '/move_gripper')
        self.reset = self.create_client(Trigger, '/reset')
        self.idle = self.create_client(Trigger, '/idle')
        self.communicate = self.create_client(Trigger, '/communicate')

    def human_ready(self, empty_msg):
        self.world.onto.agent.isReady = True

    def process_command(self, command_msg):
        print("Received command: ", command_msg)
        action = command_msg.action.lower()
        target = [x.lower() for x in command_msg.targets] if command_msg.targets else []
        self.world.send_command(action, target)

    def move_operator(self, target):
        self.is_waiting = False
        print("_use_move_operator {}...".format(target))
        self.world.onto.agent.isReady = False
        # req.position.layout.dim[0] = 7
        req = NamedTarget.Request()
        req.name = target
        res = self.reach_named_target.call_async(req)
        while not res.done():
            time.sleep(0.1)
        self.release_planner()

    def close_operator(self, target):
        self.is_waiting = False
        req = Grasp.Request()
        print(target)
        print(target.has_width)
        req.width = float(target.has_width) if target.has_width else 0.002  # [cm]
        req.force = 100.0  # [N]
        print("Grasping {}...".format(target))
        res = self.grasp.call_async(req)
        while not res.done():
            time.sleep(0.1)
        self.release_planner()

    def open_operator(self, target):
        self.is_waiting = False
        # msg = Empty()
        # self.object_released_pub.publish(msg)
        req = MoveGripper.Request()
        req.width = 2.5
        res = self.release.call_async(req)
        while not res.done():
            time.sleep(0.1)
        # return release
        self.release_planner()

    def communication_operator(self):
        print("Real robot is communication_operator...")
        if not self.is_waiting:
            msg = Empty()
            self.target_reached_pub.publish(msg)
            self.is_waiting = True
        req = Trigger.Request()
        res = self.communicate.call_async(req)
        while not res.done():
            time.sleep(0.1)
        self.release_planner()

    def idle_operator(self):
        print("Real robot is waiting...")
        req = Trigger.Request()
        res = self.idle.call_async(req)
        while not res.done():
            time.sleep(0.1)
        self.release_planner()
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
    rclpy.spin(robot)

    robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
