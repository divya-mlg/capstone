import requests
from flask import Flask
import os
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(
TracerProvider(
        resource=Resource.create({SERVICE_NAME: "capstone-frontend"})
    )
)
tracer = trace.get_tracer(__name__)

# create a JaegerExporter
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    collector_endpoint='http://jaegertracing:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)
app = Flask(__name__)

def get_counter(endpoint):
    resp = requests.get(endpoint, timeout=5)
    return resp.text

def update_counter(endpoint):
    resp = requests.post(endpoint, timeout=5)
    return resp.text

@app.route('/')
def index_handler():
    counter_service_url = os.environ.get('COUNTER_SERVICE_URL')
    counter_service_endpoint = counter_service_url+"/api/counter"
    with tracer.start_as_current_span("hello_world") as span:
        counter = get_counter(counter_service_endpoint)
        update_counter(counter_service_endpoint)
        output = "Hello, you are visior number " + str(counter)
        output = "app-version=v2, page-counter=" + str(counter) + ", new-features=tracing"
        span.set_attribute("counter", counter)
        span.set_attribute("app-version", "v2")
        return output

if __name__ == '__main__':
    app.run()