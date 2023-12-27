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

    if request.method == 'POST':
        # Get the uploaded file from the form.
        uploaded_file = request.files['file']

        # Make the API request and obtain the JSON response.
        url = 'https://app.nanonets.com/api/v2/OCR/Model/f8f086b3-7480-4e2b-bef7-0e5e8bd08479/LabelUrls/?async=false'
        headers = {'accept': 'application/x-www-form-urlencoded'}
        files = {'file': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)}
        auth = requests.auth.HTTPBasicAuth('4e121e69-8f9e-11ee-8a1f-4a1e4b95b6ce', '')

        apiResponse = requests.post(url, headers=headers, auth=auth, files=files)
        # print("API Response:", apiResponse.text)
        
        # Get json raw object responsed from Nanonet.
        apiResponseJson = apiResponse.json()
        print("API Response JSON:", apiResponseJson)

        # Filter to get only table cells from json object.
        filteredJson = apiResponseJson.get("result", [])[0].get("prediction", [])

    # # Testing with sample response first before api response.
    # with open('data/sampleResponse.json', 'r') as file:
    #     sampleResponseJson = json.load(file)
    # filteredJson = sampleResponseJson.get("result", [])[0].get("prediction", [])

    # call buildReport function from model class to build report if the data is present.
    if filteredJson is not None:
        report = buildReport(filteredJson)

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
