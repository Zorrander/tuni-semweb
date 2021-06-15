import os
import time
import rclpy
from rclpy.node import Node
import speech_recognition as sr

from std_msgs.msg import Empty
from geometry_msgs.msg import Point

from semrob.robot import robot
from semrob.world import world
from cobot_msgs.msg import Command


class DigitalWorldInterface(world.DigitalWorld):
    def __init__(self, world_file):
        world.DigitalWorld.__init__(self, world_file)
        #self.robot_name = self.create_client(RobotName, '/robot_name')
        #self.subscription = self.create_subscription(
        #    Point,
        #    'target_pose',
        #    self.camera_callback,
        #    10)
        # self.sub = self.create_subscription(Command, '/plan_request', self.process_command, 10)

        # self.target_reached_sub = self.create_subscription(Empty, '/object_released', self.object_released, 10)




    def sphinx_callback(self, recognizer, audio):
        # recognize speech using Sphinx
        try:
            print("Think")
            # print("Sphinx thinks you said " + recognizer.recognize_sphinx(audio, grammar=path.join(path.dirname(path.realpath(__file__)), 'counting.gram')))
            cmd = recognizer.recognize_sphinx(audio, keyword_entries=[("give", 1.0), ("reach", 1.0), ("grasp", 1.0), ("release", 1.0), ("peg", 1.0)])
            bow = cmd.strip().split(' ')
            print(bow)
            if len(bow) == 3:
                print("Sphinx thinks you said [{} - {}]".format(bow[2], bow[0]))
                self.run(command=(bow[2], bow[0]))

        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        print("Say something")

    def start_listening(self):
        r = sr.Recognizer()
        m = sr.Microphone(device_index=8)
        with m as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("say something!")
            audio = r.listen(m)
            self.sphinx_callback(r, audio)

    def object_released(self, empty_msg):
        self.dismiss_command()

    def get_robot_name(self):
        req = RobotName.Request()
        print("get_robot_name...")
        res = self.robot_name.call(req)
        print(res.name)

    def camera_callback(self, msg):
        self.onto.box1.update_pose(msg.x, msg.y, msg.z)
