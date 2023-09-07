import time
import RPi.GPIO as GPIO

# Declare GPIO pins
SENSOR_1 = 19
SENSOR_2 = 21
SENSOR_3 = 23
SENSOR_4 = 36


def setupSensorIO():
    GPIO.setup(SENSOR_1, GPIO.IN)
    GPIO.setup(SENSOR_2, GPIO.IN)
    GPIO.setup(SENSOR_3, GPIO.IN)
    GPIO.setup(SENSOR_4, GPIO.IN)


def setupIO():
    GPIO.setmode(GPIO.BOARD)
    setupSensorIO()


S1 = "One"
S2 = "Two"
S3 = "Three"
S4 = "Four"


def getSensorReadings():
    return {
        S1: GPIO.input(SENSOR_1),
        S2: GPIO.input(SENSOR_2),
        S3: GPIO.input(SENSOR_3),
        S4: GPIO.input(SENSOR_4),
    }


def printSensorReadings(sensorVal):
    print(S1 + ": " + str(sensorVal[S1]) + " " + S2 + ": " + str(sensorVal[S2]) + " " + S3 + ": " + str(sensorVal[S3]) +
          " " + S4 + ": " + str(sensorVal[S4]))


print("Starting Program")
setupIO()
storedVal = {}
try:
    while True:
        currentVal = getSensorReadings()
        if (storedVal != currentVal):
            printSensorReadings(currentVal)
            storedVal = currentVal
        time.sleep(0.01)  # Sleep for 10 milliseconds

except KeyboardInterrupt:
    GPIO.cleanup()
