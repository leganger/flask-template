#!/usr/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

# Example of how to do stuff and send server generated events to clients.
def do_stuff(input_string, input_int):
    print(input_string, input_int)
    # Here we can do stuff
    for char in input_string:

        output_string = ""
        while len(output_string) < int(input_int):
            output_string += char

        # Here we send messages to clients while we do stuff.
        socketio.sleep(1)
        socketio.emit('server_message',
                      {'data': output_string},
                      namespace='')
    return socketio.emit("server_message", {"data": "Finished doing stuff!"})

@socketio.on('input', namespace='')
def input_submitted(message):
    emit('server_message', {'data': 'Doing stuff...'})
    do_stuff(message["string"], message["int"])

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == '__main__':
    socketio.run(app, debug=True)