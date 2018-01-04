from tacx_speed import *

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit
from flask import Markup

import time

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
socketio = SocketIO(app)

thread = None

def background_thread():
    while True:
        data = update()

        socketio.emit('message', data)
        time.sleep(1)

@socketio.on('connect')
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


@socketio.on('changeResistance')
def change_Resistance(changeResistance):
    global resistance_level
    resistance_level = int(changeResistance.strip()[-2:])
    print("Resistance lever should be at:", resistance_level)


@app.route('/', methods= ['GET'])
def serve():

    # data = update()

    return render_template('index.html')


def update():

    speed = getSpeed()

    power = calcPower(speed, resistance_level)
    heartrate = 60

    return {'speed': speed, 'power': power, 'heartrate': heartrate, 'tire_circumference': tire_circumference, 'resistance_level': resistance_level}

if __name__ == '__main__':
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=countRPM, bouncetime=100)

    socketio.run(app, host='0.0.0.0', port=80, debug=True)
    #socketio.run(app)

