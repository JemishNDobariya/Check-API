import requests
from difflib import SequenceMatcher
from flask import Flask, jsonify, render_template

def fetch_data(api_url):
    data = []
    page = 1
    while True:
        response = requests.get(api_url, params={'page': page})
        if response.status_code != 200:
            break
        json_data = response.json()
        if not json_data:
            break
        data.extend(json_data)
        page += 1
    return data

def get_citations(response_text, sources):
    citations = []
    for source in sources:
        if 'context' in source:
            if SequenceMatcher(None, response_text, source['context']).ratio() > 0.7:  # Threshold for match
                citations.append(source)
    return citations

def process_data(data):
    results = []
    for entry in data:
        response_text = entry['response_text']
        sources = entry['sources']
        citations = get_citations(response_text, sources)
        results.append({'response_text': response_text, 'citations': citations})
    return results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_citations', methods=['GET'])
def get_citations_route():
    api_url = 'https://devapi.beyondchats.com/api/get_message_with_sources'
    data = fetch_data(api_url)
    results = process_data(data)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
