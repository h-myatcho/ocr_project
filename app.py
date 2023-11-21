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

        # Get json raw object responsed from Nanonet
        response_json = response.json()

        # Filter to get only cells from json object
        filteredJson = response_json.get("result", [])[0].get("prediction", [])[0].get("cells", [])

        # Initiate the final json object
        finalJson = {'table': {'rows': []}}
        row = []
        rowNumber = 0
        finalJson['table']['rows'].append(row)

        # loop and fetch only necessary data from cell list and rebuild the final json
        for cell in filteredJson:

            if (cell['row']) - 1 > rowNumber:
                rowNumber += 1
                rebuildCell = {
                    'text': cell['text'],
                }

                row = [rebuildCell]
                finalJson['table']['rows'].append(row)

            else:
                rebuildCell = {
                    'text': cell['text']
                }
                finalJson['table']['rows'][rowNumber].append(rebuildCell)

        print(finalJson)
        response_text = json.dumps(finalJson, indent=2)

    # response_text = json.dumps(json_data, indent=2)
    return render_template('index.html', response_text=response_text)


if __name__ == '__main__':
    app.run(debug=True, port='5001')
