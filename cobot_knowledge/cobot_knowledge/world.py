import rclpy
from pathlib import Path
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

from semrob.world import world
from cobot_msgs.msg import Task, Method
from cobot_msgs.srv import Select, Describe, Ask, Update, CreateInstance, GenerateInstanceName, Export, ReadTasks, ReadMethods, RobotName

RESOURCE_PATH = get_package_share_directory('cobot_knowledge')

class RosKnowledge(Node):

    def __init__(self):
        super().__init__('world')
        self.world = world.DigitalWorld("sem-htn.owl")

        self.robot_name_srv = self.create_service(RobotName, '/robot_name', self.robot_name)

        self.add_data_srv = self.create_service(Ask, 'add_data', self.add_data)
        self.test_data_srv = self.create_service(Update,'test_data', self.test_data)
        self.read_data_srv = self.create_service( Select, 'select_data',self.read_data)
        self.remove_data_srv = self.create_service(Ask,     'remove_data',self.remove_data)
        self.select_data_srv = self.create_service( Describe,  'read_data', self.select_data)

        self.read_tasks = self.create_service(ReadTasks,     'read_tasks',self.read_tasks)
        self.read_methods = self.create_service( ReadMethods,  'read_methods', self.read_methods)

        self.create_instance_srv = self.create_service(CreateInstance, 'create_instance', self.create_instance)
        self.generate_instance_uri_srv = self.create_service(GenerateInstanceName, 'generate_instance_uri', self.generate_instance_uri)

        self.export_srv = self.create_service(Export, 'export_onto', self.export)


    def robot_name(self, request, response):
        print("Search robot")
        robot = self.world.onto.search_one(type = self.world.onto.Robot)
        response.name = robot.name
        print(response)
        return response

    def read_tasks(self, request, response):
        tasks = self.world.onto.search(is_a = self.world.onto.Task)
        print(tasks)
        response.tasks = list()
        for x in tasks:
            task = Task()
            task.name = x.name
            response.tasks.append(task)
        return response

    def read_methods(self, request, response):
        methods = self.world.onto.search(is_a = self.world.onto.Method)
        response.methods = [Method(x.name) for x in methods]
        return response

    def add_data(self, request, response):
        trpl = request.update_triple
        response.success = True  # TODO: call owlready
        return response

    def remove_data(self, request, response):
        trpl = request.update_triple
        response.success = True  # TODO: call owlready
        return response

    def select_data(self, request, response):
        sel = request.where
        result = self.world.select_data(sel)
        print(result)
        response.match = True  # TODO: call owlready
        return response

    def read_data(self, request, response):
        descr = request.where
        response.rdf_description = True  # TODO: call owlready
        return response

    def test_data(self, request, response):
        test = request.triple
        response.veracity = True  # TODO: call owlready
        return response

    def create_instance(self, request, response):
        pass

    def generate_instance_uri(self, request, response):
        pass

    def export(self, request, response):
        self.world.onto.save(file = request.filename, format = "rdfxml")
        response.success = True
        response.message = "Ontology saved"
        return(response)

    def add_object(self, name):
        self.world.add_objects(name)

    def send_command(self, msg):
        action = msg.action
        targets = msg.targets
        self.get_logger().info('Received: "%s" - "%s"' % (action, targets))
        self.world.send_command(action, targets)
        self.create_plan()


def main(args=None):
    rclpy.init(args=args)

    node = RosKnowledge()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
