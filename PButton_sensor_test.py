from gpiozero import DistanceSensor
from time import sleep, strftime
from flask import Flask, render_template, request, jsonify
from gpiozero.pins.pigpio import PiGPIOFactory
import threading

app = Flask(__name__)
factory = PiGPIOFactory()
sensor = DistanceSensor(echo=17, trigger=4, max_distance=2, pin_factory=factory)

active = False
log_messages = []

# Background thread to constantly check the sensor when active
def sensor_check_thread():
    while True:
        if active and sensor.distance < 0.5:  # Adjust the threshold as needed
            log_message("Sensor triggered: Object detected.")
        sleep(0.3)  # Adjust the sleep time as needed

# Function to log messages with timestamps
def log_message(message):
    log_messages.append(f"{message} - {strftime('%Y-%m-%d %H:%M:%S')}")
    print(message)  # For debugging on console

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle', methods=['POST'])
def toggle():
    global active
    active = not active
    status = "activated" if active else "deactivated"
    log_message(f"System {status}")
    return render_templatef('index.html')

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(logs=log_messages)

# Start the sensor checking thread
sensor_thread = threading.Thread(target=sensor_check_thread, daemon=True)
sensor_thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
