from flask import Flask
from flask import request

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