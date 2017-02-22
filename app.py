import json
from flask import Flask, request, jsonify
from watson_developer_cloud import AlchemyLanguageV1

app = Flask('Voice assist app')
alchemy_language = AlchemyLanguageV1(api_key='cddea2ac5896fad34230018d6b70ec134c26ceeb')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/request', methods=['POST'])
def request_handler():
	data = request.get_json()
	text = data['transcription']

	response = alchemy_language.keywords(text=text)
	keywords = map(lambda x: x['text'], response['keywords'])

	if len(keywords) > 0:
		sentiment = alchemy_language.targeted_sentiment(text=text,
				                                        targets=keywords,
				                                        language='english')
		result = sentiment['results']
	else:
		result = []

	return jsonify({'result': result})




