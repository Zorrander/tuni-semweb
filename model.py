from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, Namespace, RDFS
from rdflib.extras.describer import Describer

COGROBTUT = Namespace("http://cognitive.robotics.tut#")

class Concept(object):
    def __init__(self, name, mother_class, kb):
        self.name = name
        self.kb = kb
        self.g = Graph(kb.store, COGROBTUT[name])
        self.g.bind('cogrobtut', COGROBTUT)
        d = Describer(self.g, about=COGROBTUT[self.name])
        d.rel(RDFS.subClassOf, COGROBTUT[mother_class])

    def to_rdf(self):
        return self.g

class Utterance(Concept):
    def __init__(self, name, action, target, related_skill, kb):
        super(Utterance, self).__init__(name, "Utterance", kb)
        self.related_skill = related_skill
        self.action = action
        self.target = target

    def to_rdf(self):
        d = Describer(self.g, about=COGROBTUT["FrankaDictionary"])
        with d.rel(COGROBTUT.hasEntry, COGROBTUT[self.name]):
            d.rel(COGROBTUT.activates, COGROBTUT[self.related_skill])
            with d.rel(COGROBTUT.isInvokedBy, COGROBTUT[self.action+"_Slot"]):
                d.rel(RDFS.subClassOf, COGROBTUT.Slot)
                d.rel(COGROBTUT.hasValue, Literal(self.action))
            with d.rel(COGROBTUT.isFollowedBy, COGROBTUT[self.target+"_Slot"]):
                d.rel(RDFS.subClassOf, COGROBTUT.Slot)
                d.rel(COGROBTUT.hasValue, Literal(self.target))
        return self.g

class Action(object):
    index = 0

    def __init__(self, name):
        self.uri = COGROBTUT[name + "_Action" + str(Action.index)]
        Action.index+=1

class Task(object):
    index = 0

    def __init__(self, name = ""):
        if name:
            self.uri = COGROBTUT[name + "_Task" + str(Task.index)]
        else:
            self.uri = COGROBTUT["Task_" + str(Task.index)]
        Task.index+=1


class Skill(object):
    def __init__(self, name, utterances, steps, tasks, kb):
        self.name = name
        self.utterances = utterances
        self.steps = steps
        self.tasks = tasks
        self.kb = kb
        self.g = Graph(kb.store, COGROBTUT[name])
        self.g.bind('cogrobtut', COGROBTUT)

    def to_rdf(self):
        self.dictionary_to_rdf()
        d = Describer(self.g, about=COGROBTUT[self.name])
        d.rel(RDFS.subClassOf, COGROBTUT.Skill)
        previous_state = None
        for step in self.tasks.keys():
            print "CONSIDERING STEP {}".format(step)
            with d.rel(COGROBTUT.hasStep, COGROBTUT[step]):
                d.rel(RDFS.subClassOf, COGROBTUT.Step)
                if previous_state:
                    d.rel(COGROBTUT.isDoneAfter, COGROBTUT[previous_state])
                first_node = Describer(self.g, about=Task().uri)
                d.rel(COGROBTUT.consistsIn, first_node._current())
                self.tasks_to_rdf(self.tasks[step], first_node)
            previous_state = step
        return self.g

    def dictionary_to_rdf(self):
        d = Describer(self.g, about=COGROBTUT["FrankaDictionary"])
        d.rel(RDFS.subClassOf, COGROBTUT.Dictionary)
        print "keys utterances {}".format(self.utterances.keys())
        for utterance in self.utterances.keys():
            print "utterance {}".format(self.utterances[utterance])
            with d.rel(COGROBTUT.hasEntry, COGROBTUT[utterance]):
                d.rel(COGROBTUT.activates, COGROBTUT[self.name])
                d.rel(RDFS.subClassOf, COGROBTUT.Utterance)
                with d.rel(COGROBTUT.isInvokedBy, COGROBTUT[self.utterances[utterance][0]+"_Slot"]):
                    d.rel(RDFS.subClassOf, COGROBTUT.Slot)
                    d.rel(COGROBTUT.hasValue, Literal(self.utterances[utterance][0]))
                with d.rel(COGROBTUT.isFollowedBy, COGROBTUT[self.utterances[utterance][1]+"_Slot"]):
                    d.rel(RDFS.subClassOf, COGROBTUT.Slot)
                    d.rel(COGROBTUT.hasValue, Literal(self.utterances[utterance][1]))

    def tasks_to_rdf(self, tasks, parent_node):
        parent_node.rel(RDFS.subClassOf, COGROBTUT.Task)
        if len(tasks) == 1:
            d = Describer(self.g, about=Action(tasks[min(tasks.keys())]).uri)
            d.rel(RDFS.subClassOf, COGROBTUT.Action)
            parent_node.rel(COGROBTUT.hasAction, d._current())
        else:
            with parent_node.rel(COGROBTUT.doesFirst, Action(tasks[min(tasks.keys())]).uri):
                parent_node.rel(RDFS.subClassOf, COGROBTUT.Action)
            copy = dict(tasks)
            del copy[min(copy.keys())]
            right_node = Describer(self.g, about=Task().uri)
            parent_node.rel(COGROBTUT.doesThen, right_node._current())
            self.tasks_to_rdf(copy, right_node)

def get(symbols):
    if (len(symbols)==3):
        d = {}
        d["operator"]=symbols[0]
        d["action"]=symbols[1]
        d["targetA"]=symbols[2]
        return d
    else:
        print "expected 3 symbols but got {} instead".format(len(symbols))

def assemble(symbols):
    if (len(symbols)==4):
        d = {}
        d["operator"]=symbols[0]
        d["action"]=symbols[1]
        d["targetA"]=symbols[2]
        d["targetB"]=symbols[3]
        return d
    else:
        print "expected 4 symbols but got {} instead".format(len(symbols))

def move(symbols):
    if (len(symbols)==4):
        d = {}
        d["operator"]=symbols[0]
        d["action"]=symbols[1]
        d["targetA"]=symbols[2]
        d["targetB"]=symbols[3]
        return d
    else:
        print "expected 4 symbols but got {} instead".format(len(symbols))

set_instructions = { 'get' : get,
            'assemble' : assemble,
            'move' : move
        }
def parse_instruction(instruction):
    # Get the function from switcher dictionary
    symbols = instruction.split(" ")
    symbols.pop(0)
    print symbols
    action = set_instructions.get(symbols[1], "nothing")
    # Execute the function
    return action(symbols)
