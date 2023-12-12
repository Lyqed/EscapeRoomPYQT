from flask import Flask, request, jsonify, render_template
from queue import Queue

app = Flask(__name__)
command_queue = Queue()

@app.route('/update_sequence', methods=['POST'])
def update_sequence():
    data = request.json
    command_queue.put(('update', data))
    return jsonify({"status": "success"})

@app.route('/reset', methods=['POST'])
def reset():
    command_queue.put(('reset', None))
    return jsonify({"status": "success"})

@app.route('/')
def index():
    return render_template(r'index.html')


@app.route('/get_commands', methods=['GET'])
def get_commands():
    commands = []
    while not command_queue.empty():
        commands.append(command_queue.get())
    return jsonify(commands)

def run_server():
    app.run(debug=True, use_reloader=False)

def get_command_queue():
    return command_queue

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

