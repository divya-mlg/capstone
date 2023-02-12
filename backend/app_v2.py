from flask import Flask, abort
from flask import request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import redis
import os

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

# connect to a redis instance and initialize index_counter
red = redis.Redis.from_url(os.environ.get('REDIS_FROM_URL'))
print(red.ping())
red.set("index_counter", 1)

def get_counter():
    counter_val = red.get("index_counter")
    return counter_val.decode('utf-8')


def increment_counter():
    counter_val = int(red.get("index_counter"))
    counter_val = counter_val + 1
    red.set("index_counter", counter_val)
    return str(counter_val)
    
@app.route('/api/counter', methods=["GET", "POST"])
def counter():
    if request.method == "GET":
        return get_counter()
    elif request.method == "POST":
        return increment_counter()

    abort(405)

if __name__ == '__main__':
    app.run()