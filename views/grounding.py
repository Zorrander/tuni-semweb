from flask import Blueprint, render_template,request, jsonify
from . import utils, model

bp = Blueprint('grounding', __name__)

@bp.route('/endpoint/ground/subclass/<path:new_class>/<path:mother_class>')
def ground_subclass(name, mother_class):
    concept = model.Concept(name, mother_class, utils.kb).to_rdf()
    file_name = utils.path_database+name+".owl"
    concept.serialize(file_name, format="application/rdf+xml")
    utils.reload_kb()

@bp.route('/endpoint/relate/skill/<path:new_skill_action>/<path:new_skill_target>/<path:related_skill_action>/<path:related_skill_target>')
def ground_utterance(new_skill_action, new_skill_target, related_skill_action, related_skill_target):
    q = """
         SELECT ?localName
         WHERE { ?utterance cogrobtut:activates ?entity .
         ?utterance cogrobtut:isInvokedBy ?slot1 .
         ?utterance cogrobtut:isFollowedBy ?slot2 .
         ?slot1 cogrobtut:hasValue """ + "'" + related_skill_action + "'" + """.
         ?slot2 cogrobtut:hasValue """ + "'" + related_skill_target + "'" + """ .
         bind( strafter(str(?entity), "#") as ?localName) . }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    concept = model.Utterance(new_skill_action+new_skill_target, new_skill_action, new_skill_target, individuals[0], utils.kb).to_rdf()
    file_name = utils.path_database+new_skill+".owl"
    concept.serialize(file_name, format="application/rdf+xml")
    utils.reload_kb()
