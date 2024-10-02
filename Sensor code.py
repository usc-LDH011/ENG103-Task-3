from gpiozero import DistanceSensor
from time import sleep
from flask import Flask, render_template, request, jsonify
from gpiozero.pins.pigpio import PiGPIOFactory

app = Flask(__name__)
factory = PiGPIOFactory()
sensor = DistanceSensor(echo=17, trigger=4, max_distance=2, pin_factory=factory)

active = False
log_messages = []

@app.route('/')
def index():
    return render_template('WebControlPanel.html')

@app.route('/toggle', methods=['POST'])
def toggle():
    global active
    active = not active
    status = "activated" if active else "deactivated"
    log_message(f"System {status}")
    return "", 204

@app.route('/sensor_check', methods=['POST'])
def sensor_check():
    if active and sensor.distance < 0.5:  # Adjust the threshold as needed
        log_message("Sensor triggered: Object detected.")
    return "", 204

def log_message(message):
    log_messages.append(f"{message} - {time.strftime('%Y-%m-%d %H:%M:%S')}")


@app.route('/get_logs')
def get_logs():
    return "\n".join(log_messages)

if __name__ == "__main__":
    try:
        while True:
            sleep(0.3)  # Adjust as needed
            sensor_check()  # Check the sensor status
    except KeyboardInterrupt:
        pass
