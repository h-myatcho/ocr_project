from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None

    if request.method == 'POST':
        # Get the uploaded file from the form
        uploaded_file = request.files['file']

        # Make the API request and obtain the JSON response
        url = 'https://app.nanonets.com/api/v2/OCR/Model/4b02ca67-557a-4cd3-af8e-a19dcc58898c/LabelUrls/?async=false'
        headers = {'accept': 'application/x-www-form-urlencoded'}
        files = {'file': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)}
        auth = requests.auth.HTTPBasicAuth('dba71e7c-7d8b-11ee-998f-7efeff8449b1', '')
        
        response = requests.post(url, headers=headers, auth=auth, files=files)
        response_json = response.json()
        response_text = json.dumps(response_json, indent=2)

    return render_template('index.html', response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True, port='5001')

