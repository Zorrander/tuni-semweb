from rdflib import ConjunctiveGraph, Namespace, Graph
import re
import model
import os

namespaces = dict(rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"),
    cogrobtut=Namespace(model.COGROBTUT),
    dash=Namespace("http://datashapes.org/dash#"),
    shema=Namespace("http://schema.org/"),
    sh=Namespace("http://www.w3.org/ns/shacl#"),
    xsd=Namespace("http://www.w3.org/2001/XMLSchema#"),
    )

#path_database = "/home/admin-franka/franka-web-app/flaskr/static/owl/franka_robolab/"
path_database = "/home/anglerau/GitLab/flask-app/flaskr/static/owl/franka_robolab/"
file_extension = ".owl"
kb = ConjunctiveGraph()
list_parsed_files = []
for f in os.listdir(path_database):
    if f.endswith(file_extension):
        list_parsed_files.append(f)
        with open(path_database+f) as onto:
            new_context = Graph(kb.store, f)
            new_context.parse(onto)

def reload_kb():
    for f in os.listdir(path_database):
        if not (f in list_parsed_files):
            with open(path_database+f) as onto:
                new_context = Graph(kb.store, f)
                new_context.parse(onto)

def build_set_utterances(utterances):
    print "build_set_utterances gets : {}".format(utterances)
    u_index = 0
    s_index = 0
    tmp = utterances
    res = {}
    while tmp:
        found_next = False
        for i in utterances.keys():
            print "considering key : {}".format(i)
            if (i == "utterance"+str(u_index)+"-slot"+str(s_index)): #Found a slot for current utterance
                if (s_index == 0):
                    res["utterance"+str(u_index)] = [utterances[i]]
                else:
                    res["utterance"+str(u_index)].append(utterances[i])
                tmp.pop(i)
                found_next = True
        if found_next:
            s_index+=1
        else:
            s_index=0
            u_index+=1

    print "build_set_utterances returns : {}".format(res)
    return res

def create_graph(request):
    print request.form
    name = request.form['skill_name']
    utterances = {key: request.form[key] for key in request.form.keys() if (key.startswith("utterance"))}
    utterances = build_set_utterances(utterances)
    steps = [request.form[key] for key in request.form.keys() if (key.startswith("step"))]
    tasks = {}
    for s in steps:
        tasks[s] = {}
    for key1 in request.form.keys():
        print "key1:{}".format(key1)
        for key2 in steps:
            print "key2:{}".format(key2)
            if key1.startswith(key2):
                index = key1[-1:]
                print "Index : {}".format(index)
                tasks[key2].update({index : request.form[key1]})

    print "Name : {}".format(name)
    print "Utterances : {}".format(utterances)
    print "Steps : {}".format(steps)
    skill = model.Skill(name, utterances, steps, tasks, kb)
    return skill.to_rdf()

def remove(f):
    filename=f+file_extension
    if not (filename in os.listdir(path_database)):
        pass
    else:
        os.remove(path_database+filename)
        list_parsed_files.remove(filename)
        kb.remove_context(filename)

def process_sparql_result(query):
    res = kb.query(query, initNs=namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return individuals

def print_context():
    print "Contexts"
    for c in kb.contexts():
        print c
        for i in c:
            print i
