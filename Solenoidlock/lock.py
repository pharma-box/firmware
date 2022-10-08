from flask import Flask, render_template, request, redirect, url_for, make_response
import time
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
existingLocks = {1:17,2:18, 3:19}
for i,pin in existingLocks.items():
    GPIO.setup(pin , GPIO.OUT)
app = Flask(__name__) #set up flask server
#when the root IP is selected, return index.html page
@app.route('/')
def index():
    return render_template('index.html')
#recieve which pin to change from the button press on index.html
#each button returns a number that triggers a command in this function
#
#Uses methods from motors.py to send commands to the GPIO to operate the motors
@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin) #cast changepin to an int
    if changePin in existingLocks:
        print("ON")
        pin = existingLocks[changePin]
        GPIO.output( pin , 0)
        sleep(0.5)
        GPIO.output(pin,1)
    response = make_response(redirect(url_for('index')))
    return(response)
app.run(debug=True, host='0.0.0.0', port=8000)
