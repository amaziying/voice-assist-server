import json

from flask import Flask, request, jsonify, render_template
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

from triage_manager import enqueue, get_active_requests, get_closed_requests, pickup_request, close_request

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

def create_app():
    app = CustomFlask(__name__)

    return app

app = create_app()

# Connect to IBM Watson
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-17',
    username='632402de-fa93-4f20-ab17-0b8b8ccad28e',
    password='VQdbAVLmc1sI')

watson_cache = {}

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/api/requests', methods=['POST'])
def open_request():
    data = request.get_json()
    text = data['transcription']
    patient_id = data['patient_id']

    if text not in watson_cache:
        watson_cache[text] = natural_language_understanding.analyze(
            text=text,
            features=[features.Keywords(), features.Sentiment()])

    enqueue(patient_id, text, watson_cache[text])
    return jsonify({'result': watson_cache[text]})

@app.route('/api/requests', methods=['GET'])
def list_requests():
    finder = request.args.get('finder')
    result = []

    if finder == 'active':
        result = get_active_requests()
    elif finder == 'closed':
        result = get_closed_requests()

    return jsonify({'result': result})


@app.route('/api/pickup_request', methods=['POST'])
def pickup():
    data = request.get_json()
    request_id = data['request_id']

    pickup_request(request_id)

    return jsonify({})

@app.route('/api/close_request', methods=['POST'])
def close():
    data = request.get_json()
    request_id = data['request_id']

    close_request(request_id)

    return jsonify({})
