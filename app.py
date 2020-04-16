from __future__ import print_function

import os
import sys
import argparse
import json
from jena_reasoning.owl import Knowledge
from flask import Flask, Blueprint, render_template, jsonify, request


APP = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '/static/models')

print("Upload folder: " + UPLOAD_FOLDER)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
INDEX PAGE
'''
@APP.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=UPLOAD_FOLDER, filename=filename)
################################################################################

'''
ADD KNOWLEDGE
'''

@APP.route('/ontologies')
def knowledge_base():
    return render_template('semantics/knowledge_base.html')

@APP.route('/ontologies/<path:name>')
def read(name):
    data = robot.read_skill(name)
    return render_template('semantics/skill_info.html', skill=name, result=data)

@APP.route('/ontologies/query', methods=('GET', 'POST'))
def sparql():
    if request.method == 'POST':
        query = request.form['query']
        data = robot.process(query)
        print (data)
        return render_template('semantics/query.html', query_result=data)
    return render_template('semantics/query.html')

################################################################################

'''
TESTING THE SPEECH INTERFACE
'''

@APP.route('/convo/')
def render_conversation():
    return render_template('nlp/conversation.html')

################################################################################


'''
VISUALIZING THE CAMERA FEEDBACK
'''

@APP.route('/camera/')
def camera():
    return render_template('video/camera.html')

################################################################################


'''
PLANNING SCENE
'''

@APP.route('/plan')
def plan():
    return render_template('planning/plan.html')

################################################################################


'''
VIRTUAL ASSEMBLER
'''
@APP.route('/assembler')
def assembler():
    return render_template('virtual_assembler/dashboard.html')

@APP.route('/threejs')
def threejs():
    return render_template('virtual_assembler/robot.html')

################################################################################

@APP.route('/new_assembly', methods = ['POST'])
def learn_new_skill():
    reasoner = Knowledge()
    req_data = request.get_json()
    #print(req_data['input'])
    #jsdata = request.form['input'
    #for x in req_data:
    print("Object : {} ".format(req_data), file=sys.stderr)
    #reasoner.add_object(req_data)
    return jsonify(req_data)

################################################################################

APP.add_url_rule('/', endpoint='index')

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Panda TUNI webAPP")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    if ARGS.debug:
        print("Running in debug mode")
        APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        APP.run(host='0.0.0.0', port=PORT, debug=False)
