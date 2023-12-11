from flask import Flask, request

app = Flask(__name__)
correct_sequences = ['1234', '6789', 'ABCD', 'QAZW']

@app.route('/update_sequences', methods=['POST'])
def update_sequences():
    global correct_sequences
    data = request.json
    correct_sequences = data['sequences']
    return 'Sequences updated', 200

if __name__ == '__main__':
    app.run(port=5000)
