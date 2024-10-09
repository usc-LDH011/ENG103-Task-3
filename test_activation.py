from flask import Flask, render_template, request
import sensor  # Import the sensor code

app = Flask(__name__)

system_active = False  # State of the system

@app.route('/')
def index():
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
        dist = sensor.measure_distance()
        return f"Distance: {dist} cm"
    else:
        return "System is inactive"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
