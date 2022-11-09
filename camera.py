from time import sleep
from picamera import PiCamera
from pyzbar.pyzbar import decode
import numpy as np
import requests
import I2C_LCD_driver

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
existingLocks = {1:17,2:18, 3:19}
for i,pin in existingLocks.items():
    GPIO.setup(pin , GPIO.OUT)


lcd = I2C_LCD_driver.lcd()

def send_post(qrCode, url):
	obj = {'qrCode': qrCode}
	x = requests.post(url, json = obj)
	#print(x.text)
	return x

def unlock(changepin):
    changePin = int(changepin) #cast changepin to an int
    if changePin in existingLocks:
        print("ON")
        pin = existingLocks[changePin]
        GPIO.output( pin , 0)
        sleep(0.5)
        GPIO.output(pin,1)


addr = "https://pharmabox-git-jjw-clean-creation-endpoints-pharmaboxfydp.vercel.app/api/lockerboxes/validateqr"


camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 24
#camera.start_preview()
prev_qr =  ""
lcd.lcd_display_string("Scan QR Code",1,1)
while True:
	sleep(0.5)
	output = np.empty((240,320,3), dtype=np.uint8)
	camera.capture(output, 'rgb')
	res = decode(output)
	if res != []:
		data = res[0].data.decode('utf-8')
		if prev_qr == data:
			continue
		prev_qr = data
		print(data)
		lcd.lcd_clear()
		lcd.lcd_display_string("Code Scanned",1,1)
		result = send_post(data,addr)
		if result.status_code == 200:
			res = result.json()
			#print(res)
			lockerBox = res['updatedLockerBox']['label']
			lcd.lcd_display_string(f"Open Locker: {lockerBox}",2,1)
			unlock(lockerBox)
		elif result.status_code >= 400:
			lcd.lcd_display_string("Bad Request",2,1)
		sleep(3)
		lcd.lcd_clear()
		lcd.lcd_display_string("Scan QR Code",1,1)
	#print(res)
#camera.stop_preview()
