from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the sonic sensor
TRIG = 23
ECHO = 24

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# System state (active/inactive)
system_active = False

def measure_distance():
    # Ensure the TRIG pin is low
    GPIO.output(TRIG, False)
    time.sleep(2)  # Let the sensor settle

    # Trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    # Measure the time for the ECHO pin to go high
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the duration and distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound: 34300 cm/s / 2
    distance = round(distance, 2)

    return distance

@app.route('/')
def index():
    # Render the control page with the current system state
    return render_template('index.html', system_active=system_active)

@app.route('/control', methods=['POST'])
def control():
    global system_active
    action = request.form['action']

    if action == 'Activate':
        system_active = True
    elif action == 'Deactivate':
        system_active = False

    return render_template('index.html', system_active=system_active)

@app.route('/distance')
def distance():
    if system_active:
        dist = measure_distance()
        return f"Distance: {dist} cm"
    else:
        return "System is inactive"

@app.route('/cleanup')
def cleanup():
    GPIO.cleanup()
    return "GPIO cleaned up!"

if __name__ == '__main__':
    try:
        # Start the Flask web server
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        # Clean up GPIO pins on exit
        GPIO.cleanup()

