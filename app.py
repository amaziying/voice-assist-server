import json
from flask import Flask, request, jsonify
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

app = Flask('Voice assist app')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-17',
    username='632402de-fa93-4f20-ab17-0b8b8ccad28e',
    password='VQdbAVLmc1sI')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/request', methods=['POST'])
def request_handler():
    data = request.get_json()
    text = data['transcription']

    result = natural_language_understanding.analyze(
        text=text,
        features=[features.Keywords(), features.Sentiment()])

    return jsonify({'result': result})
