from flask import Blueprint, render_template, request, jsonify
from . import utils

bp = Blueprint('views', __name__)

@bp.route('/')
def index():
    q = """
        SELECT ?localName
        WHERE { ?entity rdfs:subClassOf cogrobtut:Skill .
	    bind( strafter(str(?entity), "#") as ?localName) .
        }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return render_template('interface/index.html', result = individuals)

@bp.route('/skills')
def skills():
    q = """
        SELECT ?localName
        WHERE { ?entity rdfs:subClassOf cogrobtut:Skill .
	    bind( strafter(str(?entity), "#") as ?localName) .
        }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return render_template('interface/skills.html', query=q, result = individuals)

@bp.route('/dictionary', methods=['GET'])
def dictionary():
    q = """
        SELECT ?localName
        WHERE { ?entity rdfs:subClassOf cogrobtut:Utterance .
        bind( strafter(str(?entity), "#") as ?localName) .
        }
    """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return render_template('interface/dictionary.html', result = individuals)

@bp.route('/query')
def query():
    return render_template('interface/query.html')

@bp.route('/query', methods=['POST'])
def sparql():
    q = request.form['query']
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_rows = [x for x in res]
    individuals=[]
    for row in res_rows:
        for elem in row:
            individuals.append(elem)
    return render_template('interface/query.html', query=q, result = individuals)
