import copy
import asyncio
from pathlib import Path

import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

from cobowl.world import DigitalWorld
from semantic_htn.planner import Planner

from cobot_msgs.msg import Command
from cobot_msgs.srv import ReachCartesianPose, Grasp, MoveGripper

RESOURCE_PATH = get_package_share_directory('cobot_knowledge')

class RosPlanner(Node):

    def __init__(self):
        super().__init__('planner')
        self.world = DigitalWorld(base=str(Path(RESOURCE_PATH)/'handover.owl'))
        self.world.add_object("peg")
        self.world.add_object("box")
        self.world.add_object("separator")
        self.planner = Planner(self.world)
        self.move_to = self.create_client(ReachCartesianPose, '/go_to_cartesian_goal')
        self.grasp = self.create_client(Grasp, '/grasp')
        self.release = self.create_client(MoveGripper, '/move_gripper')
        self.sub = self.create_subscription(Command, '/plan_request', self.send_command, 10)


    def add_object(self, name):
        self.world.add_objects(name)

    def send_command(self, msg):
        action = msg.action.lower()
        targets = [x.lower() for x in msg.targets]
        self.get_logger().info('Received: "%s" - "%s"' % (action, targets))
        self.world.send_command(action, targets)
        self.create_plan()

    def create_plan(self):
        plan = self.planner.create_plan(self.world)
        self.get_logger().info('Created plan: "%s"' % plan)
        self.run(plan)

    #def run(self, plan):
    #    self.planner.run(self.world, plan)

    def run(self, plan, goal_state = False):
        try:
            self.get_logger().info('Running plan...')
            original_plan = copy.copy(plan)
            for task in plan:
                self.get_logger().info('- "%s" ' % task)
            #while plan and not world.check_state(goal_state):
            while original_plan:
                primitive = original_plan.pop(0)
                if primitive.is_a[0].name == "State":
                    pass
                    #goal_state = primitive
                    #plan.extend(self.inverse_planning(primitive))
                else:
                    if self.world.are_preconditions_met(primitive):
                        self.get_logger().info('Do  "%s"' % primitive)
                        self.perform(primitive)
                    else:
                        print("Error")
            self.world.dismiss_command()
        except Exception as e:
            print("Dispatching Error: {} ".format(e))
            #new_plan = self.world.create_plan(world, [e.primitive])
            #self.run(new_plan, goal_state)

    def perform(self, primitive):
        operator = self._get_operator(primitive.is_a[0].name, primitive)
        operator()

    def _get_operator(self, primitive_type, primitive):
        if primitive_type == "IdleTask":
            return self._use_idle_operator()
        elif primitive_type == "ResetTask":
            self.onto.panda.isWaitingForSomething = True
            return self._use_reset_operator()
        elif primitive_type == "StopTask":
            self.onto.panda.isWaitingForSomething = True
            return self._use_stop_operator()
        elif primitive_type == "LiftingTask":
            return self._use_move_operator(primitive.has_place_goal)
        elif primitive_type == "DropingTask":
            return self._use_move_operator(primitive.has_place_goal)
        elif primitive_type == "WaitForTask":
            self.world.onto.panda.isWaitingForSomething = True
            return self._use_idle_operator()
        elif primitive_type == "GraspTask":
            self.world.onto.panda.isHoldingSomething = True
            return self._use_close_operator(primitive.actsOn)
        elif primitive_type == "ReachTask":
            self.world.onto.panda.isCapableOfReaching = True
            return self._use_move_operator(primitive.actsOn)
        elif primitive_type == "InsertingTask":
            self.world.onto.panda.isAligned = False
            return self._use_move_operator(primitive.actsOn)
        elif primitive_type == "ReleaseTask":
            self.world.onto.panda.isHoldingSomething = False
            return self._use_open_operator()
            if self.world.onto.panda.isWaitingForSomething:
                self.world.onto.panda.isWaitingForSomething = False
        elif primitive_type == "TranslationTask":
            return self._use_move_operator(primitive.has_place_goal)
        elif primitive_type == "AligningTask":
            self.world.onto.panda.isAligned = True
            return self._use_move_operator(primitive.has_place_goal)
        else:
            raise ValueError(type)

    def _use_move_operator(self, target):
        def move_to():
            req = ReachCartesianPose.Request()
            print("_use_move_operator {}...".format(target))
            req.type = 0 if target.name == "storage" else 1  # else target.name = "handover"
            # TODO:retrieve from KB
            print(req)
            self.move_to.call_async(req)
            print("plan moving on")
        return move_to

    def _use_close_operator(self, target):
        def grasp():
            req = Grasp.Request()
            req.width = 2.0  # [cm]
            req.force = 50.0  # [N]
            print("Grasping {}...".format(target))
            self.grasp.call_async(req)
        return grasp

    def _use_open_operator(self):
        def release():
            req = MoveGripper.Request()
            req.width = 8.0
            self.release.call_async(req)
        return release

    def _use_idle_operator(self):
        def wait():
            print("Waiting...")
        return wait

    def _use_stop_operator(self):
        def stop():
            print("Stopping...")
        return stop

    def _use_reset_operator(self):
        def reset():
            print("Reseting...")
        return reset


def main(args=None):
    rclpy.init(args=args)

    node = RosPlanner()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
