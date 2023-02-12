from flask import Flask, abort
from flask import request
import redis
import os

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