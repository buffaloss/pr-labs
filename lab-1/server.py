from flask import Flask, request


# Create the application instance
app = Flask(__name__)


# Create a URL route in our application for "/ok"
@app.route('/ok')
def ok():
    return {
        'message1': 'we',
        'message2': 'are',
        'message3': 'here'
    }


# Create a URL route in our application for "/lol"
@app.route('/lol')
def lol():
    return 'looooooool'


# Create a URL route in our application for "/convo"
# accept POST requests too
@app.route('/convo', methods=['GET', 'POST'])
def convo():
    if request.method == 'GET':
        return {
            'message': 'Please send me some data.'
        }
    elif request.method == 'POST':
        payload = request.json
        print(payload)
        return {
            'message': 'The data has been received.'
        }


# Start the server
app.run()