from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origin='*')

# Initialize an empty dictionary to store messages
message_storage = {}

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('message')
def handle_message(message):
    print (f'Message Received: {message}')
    # Store the message in the dictionary with the current timestamp as the key
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_storage[timestamp] = message
    
    # Print all messages from the message_storage
    print("All Messages:")
    for time, msg in message_storage.items():
        print(f"{time}: {msg}")
    
    socketio.emit('message', message)  # Broadcast the message to all clients

@app.route("/chat")
def home():
    return render_template('base.html')

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        print(name)
        return render_template('base.html', username=name)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
