import requests
from flask import Flask
import os

app = Flask(__name__)

def get_counter(endpoint):
    resp = requests.get(endpoint)
    return resp.text

def update_counter(endpoint):
    resp = requests.post(endpoint)
    return resp.text

@app.route('/')
def index_handler():
    counter_service_url = os.environ.get('COUNTER_SERVICE_URL')
    counter_service_endpoint = counter_service_url+"/api/counter"
    counter = get_counter(counter_service_endpoint)
    update_counter(counter_service_endpoint)
    output = "app-version=v1, page-counter=" + str(counter)
    return output

if __name__ == '__main__':
    app.run()