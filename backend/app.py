from flask import Flask
from flask import request
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

counter_val = 1

def get_counter():
    global counter_val
    return str(counter_val)

def increment_counter():
    global counter_val
    counter_val = counter_val + 1
    return str(counter_val)
    
@app.route('/api/counter', methods=["GET", "POST"])
def counter():
    if request.method == "GET":
        return get_counter()
    else:
        return increment_counter()

    return counter_val

if __name__ == '__main__':
    app.run()