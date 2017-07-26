from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
from watson_developer_cloud import VisualRecognitionV3 as vr
import atexit
import cf_deployment_tracker
import os
import json

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/results", methods=['POST'])
def recognise_image():
    result_items = list()
    x = vr(api_key='', version='2017-07-25')
    imgurl = request.form['imgurl']
    # print imgurl
    img = x.classify(images_url=imgurl)
    print img
    classes = img['images'][0]['classifiers'][0]['classes']
    custom_classes = img['custom_classes']
    images_processed = img['images_processed']
    if img['images'][0]['source_url']:
        source_url = img['images'][0]['source_url']
    else:
        source_url = ''
    if img['images'][0]['resolved_url']:
        resolved_url = img['images'][0]['resolved_url']
    else:
        resolved_url = ''
    complete_response = json.dumps(img, sort_keys = True, indent = 4, separators = (',', ': '))
    return render_template('show_results.html', json_resp=classes, custom_classes=custom_classes, 
        images_processed=images_processed, source_url=source_url, resolved_url=resolved_url, complete_response=complete_response)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
