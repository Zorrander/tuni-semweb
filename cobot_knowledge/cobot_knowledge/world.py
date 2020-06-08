import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from pathlib import Path
from cobowl.world import DigitalWorld
from cobot_msgs.msg import Task, Method
from cobot_msgs.srv import Select, Describe, Ask, Update, CreateInstance, GenerateInstanceName, Export, ReadTasks, ReadMethods

RESOURCE_PATH = get_package_share_directory('cobot_knowledge')

class RosKnowledge(Node):

    def __init__(self):
        super().__init__('world')
        self.world = DigitalWorld(base=str(Path(RESOURCE_PATH)/'handover.owl'))

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
                        self.world.apply_effects(primitive)
                    else:
                        print("Error")
            self.world.dismiss_command()
        except Exception as e:
            print("Dispatching Error: {} ".format(e))
            #new_plan = self.world.create_plan(world, [e.primitive])
            #self.run(new_plan, goal_state)

def main(args=None):
    rclpy.init(args=args)

    node = RosKnowledge()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
