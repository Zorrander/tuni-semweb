from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import utils

bp = Blueprint('skills', __name__)

@bp.route('/skills/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('interface/skill_create.html')
    elif request.method == 'POST':
        new_skill = utils.create_graph(request)
        file_name = utils.path_database+request.form['skill_name']+".owl"
        new_skill.serialize(file_name, format="application/rdf+xml")
        utils.reload_kb()
        return redirect(url_for('views.skills'))

@bp.route('/skills/read/<path:name>')
def read(name):
    q = """
        SELECT ?pred ?obj
        WHERE { cogrobtut:""" + name + """ ?p ?o
        bind( strafter(str(?p), "#") as ?pred)
        bind( strafter(str(?o), "#") as ?obj) . }
        """
    res = utils.kb.query(q, initNs=utils.namespaces)
    res_list = [x for x in res]
    return render_template('interface/skill_info.html', skill=name, result = res_list)

@bp.route('/skills/update/<path:name>')
def update(name):
    return render_template('interface/skill_update.html', skill=name)

@bp.route('/skills/delete/<path:name>')
def delete(name):
    utils.remove(name)
    return redirect(url_for('views.skills'))
