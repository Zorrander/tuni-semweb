from flask import Blueprint, render_template,request, jsonify
from rdflib.term import Literal
from . import utils, model

bp = Blueprint('endpoint', __name__)

@bp.route('/endpoint')
def endpoint():
    print "received request"
    q=request.json['query']
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_list = []
    for x in res:
        res_list.append()
    return jsonify({"result" : res_list})


@bp.route('/endpoint/skills')
def endpoint_skills():
    """Retrieves skills available in the knowledge base.

    Retrieves recursively the sub classes of cogrobtut:Skill.

    Returns
    -------
    Json[List[str]]
        The list of skills.
    """
    q = """
        SELECT ?localName
        WHERE { ?entity rdfs:subClassOf* cogrobtut:Skill .
	    bind( strafter(str(?entity), "#") as ?localName) .
        }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return jsonify({"result" : individuals})



@bp.route('/endpoint/step/<path:command_name>')
def endpoint_step_info(command_name):
    """Retrieve information available for a given skill.

    Retrieve the skill activated by the command sent as argument, list its steps,
    and for each one of them gets all information available.

    Parameters
    ----------
    command_name : str
            An utterance.

    Returns
    -------
    Json[List[Dict(predicate:object)]]
        The list of (predicate, object).
    """
    q = """
        SELECT ?s ?p ?o
        WHERE {
        ?u cogrobtut:isInvokedBy cogrobtut:""" + command_name + """;
           cogrobtut:activates ?skill .
        ?skill cogrobtut:hasStep ?step .
        ?step ?prop ?val .
        bind( strafter(str(?step), "#") as ?s) .
        bind( strafter(str(?prop), "#") as ?p) .
        bind( strafter(str(?val), "#") as ?o) . }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    res = {}
    for row in res_rows:
        if row[0] in res:
            res[row[0]].update({row[1]:row[2]})
        else:
            res[row[0]] = {row[1]:row[2]}
    print "server found {}".format(res)
    return jsonify(res)

@bp.route('/endpoint/steps/<path:skill>')
def endpoint_steps(skill):
    q = """
        SELECT ?o
        WHERE {
        cogrobtut:""" + skill + """ cogrobtut:hasStep ?val ;
        bind( strafter(str(?val), "#") as ?o) . }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    print individuals
    return jsonify({"result" : individuals})

@bp.route('/endpoint/task/<path:step>')
def task_from_step(step):
    q = """
    SELECT ?action ?first ?second
    WHERE {
    OPTIONAL{cogrobtut:""" + step + """ cogrobtut:hasAction ?o0. }
    OPTIONAL{cogrobtut:""" + step + """ cogrobtut:doesFirst ?o1;
                                        cogrobtut:doesThen ?o2. }
    BIND( strafter(str(?o0), "#") as ?action) .
    BIND( strafter(str(?o1), "#") as ?first) .
    BIND( strafter(str(?o2), "#") as ?second) .
    }"""
    return jsonify({"result" : utils.process_sparql_result(q)})


@bp.route('/endpoint/first/task/<path:step>')
def first_task_from_step(step):
    q = """ SELECT ?action
    WHERE { OPTIONAL{cogrobtut:""" + step + """ cogrobtut:consistsIn ?o0. }
    BIND( strafter(str(?o0), "#") as ?action) . }"""
    return jsonify({"result" : utils.process_sparql_result(q)})

@bp.route('/endpoint/utterances/<path:command>')
def endpoint_utterances(command):
    q = """
        SELECT ?localName
        WHERE { ?entity rdfs:subClassOf cogrobtut:Utterance ;
                                 cogrobtut:isInvokedBy ?slot.
                ?slot cogrobtut:hasValue """ + "'" + command + "'" + """.
                bind( strafter(str(?slot), "#") as ?localName).
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})


@bp.route('/endpoint/next_slot/<path:slot>')
def endpoint_next_slot(slot):
    q = """
        SELECT ?localName ?value
        WHERE { cogrobtut:""" + slot + """ cogrobtut:isFollowedBy ?obj .
        BIND( strafter(str(?obj), "#") as ?localName) .
        OPTIONAL { ?obj cogrobtut:hasValue ?value . } }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    res = {}
    for row in res_rows:
        res["name"] = row[0]
        if len(row)==1:
            res["value"] = ""
        else:
            res["value"] = row[1]
    print "server found {}".format(res)
    return jsonify(res)

@bp.route('/endpoint/preconditions/<path:action>')
def preconditions_from_action(action):
    q = """
        SELECT ?precondition
        WHERE {
        OPTIONAL{cogrobtut:""" + action + """ cogrobtut:hasPreCondition ?obj. }
        BIND( strafter(str(?obj), "#") as ?precondition) .
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})

@bp.route('/endpoint/location/<path:entity>')
def location_of(entity):
    q = """
        SELECT ?x ?y ?z
        WHERE {
            OPTIONAL{
            ?entity rdf:type cogrobtut:""" + entity + """ ;
                    cogrobtut:hasLocation ?loc.
            ?loc cogrobtut:x ?x;
                 cogrobtut:y ?y;
                 cogrobtut:z ?z. }
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})

@bp.route('/endpoint/description/<path:entity>')
def description(entity):
    q = """
        SELECT ?com
        WHERE {
            OPTIONAL {
                cogrobtut:""" + entity + """ rdf:type ?class .
                ?class rdfs:comment ?com .
                }
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})


@bp.route('/endpoint/width/<path:entity>')
def width_of(entity):
    q = """
        SELECT ?w
        WHERE {
            OPTIONAL{
            ?entity rdf:type cogrobtut:""" + entity + """ ;
                    cogrobtut:hasWidth ?loc.
            ?loc cogrobtut:value ?w. }
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})

@bp.route('/endpoint/attributes/<path:attribute>')
def attribute_known(attribute):
    q = """
        SELECT ?x
        WHERE {
            OPTIONAL{
            ?entity rdfs:subClassOf* cogrobtut:""" + attribute + """ .
            }
            BIND( strafter(str(?entity), "#") as ?x) .
        }
    """
    return jsonify({"result" : utils.process_sparql_result(q)})
