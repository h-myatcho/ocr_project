from flask import Flask, render_template, request
import requests
import json

from models.report import Table, Row, Cell, Report, buildReport

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    filteredJson = None
    apiResponseJson = None
    report = None
    # arrayVar = []

    if request.method == 'POST':
        # Get the uploaded file from the form.
        uploaded_file = request.files['file']

        # Make the API request and obtain the JSON response.
        url = 'your-model-url-here'
        headers = {'accept': 'application/x-www-form-urlencoded'}
        files = {'file': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)}
        auth = requests.auth.HTTPBasicAuth('your-nanonets-api-key-here', '')

        apiResponse = requests.post(url, headers=headers, auth=auth, files=files)
        
        # Get json raw object responsed from Nanonet.
        apiResponseJson = apiResponse.json()

        # Filter to get only table cells from json object.
        pages = apiResponseJson.get("result", [])
        filteredJson = [page.get("prediction", []) for page in pages]
    

    # # Testing with sample response first before api response.
    # with open('data/sampleResponse.json', 'r') as file:
    #     sampleResponseJson = json.load(file)
    # filteredJson = sampleResponseJson.get("result", [])[0].get("prediction", [])

    # call buildReport function from model class to build report if the data is present.
    if filteredJson is not None:
        report = buildReport(filteredJson)

    # # To get dataOutput
    # with open('onePage.txt', 'w') as f:
    #     json_string = json.dumps(filteredJson)
    #     f.write(json_string)

    reportJson = json.dumps(report, default=lambda o: o.__dict__, indent=2)

    return render_template('index.html', response_text=reportJson)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port='5001')