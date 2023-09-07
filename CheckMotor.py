import time
import RPi.GPIO as GPIO

MOTOR_RIGHT_ENABLE = 33
MOTOR_RIGHT_PIN1 = 15
MOTOR_RIGHT_PIN2 = 13
MOTOR_LEFT_ENABLE = 32
MOTOR_LEFT_PIN3 = 16
MOTOR_LEFT_PIN4 = 18
PWM_CONTROL_RIGHT = None
PWM_CONTROL_LEFT = None

TURN_TIME = 0.25

SPEED = 50


def moveRightMotorForward():
    GPIO.output(MOTOR_RIGHT_ENABLE, SPEED)
    GPIO.output(MOTOR_RIGHT_PIN1, 1)
    GPIO.output(MOTOR_RIGHT_PIN2, 0)


def moveRightMotorBackward():
    GPIO.output(MOTOR_RIGHT_ENABLE, SPEED)
    GPIO.output(MOTOR_RIGHT_PIN1, 0)
    GPIO.output(MOTOR_RIGHT_PIN2, 1)


def moveLeftMotorForward():
    GPIO.output(MOTOR_LEFT_ENABLE, SPEED)
    GPIO.output(MOTOR_LEFT_PIN3, 1)
    GPIO.output(MOTOR_LEFT_PIN4, 0)


def moveLeftMotorBackward():
    GPIO.output(MOTOR_LEFT_ENABLE, SPEED)
    GPIO.output(MOTOR_LEFT_PIN3, 0)
    GPIO.output(MOTOR_LEFT_PIN4, 1)


def stay_put():
    GPIO.output(MOTOR_LEFT_ENABLE, 0)
    GPIO.output(MOTOR_LEFT_PIN3, 0)
    GPIO.output(MOTOR_LEFT_PIN4, 0)
    GPIO.output(MOTOR_RIGHT_ENABLE, 0)
    GPIO.output(MOTOR_RIGHT_PIN1, 0)
    GPIO.output(MOTOR_RIGHT_PIN2, 0)


def setupMotorIO():
    global PWM_CONTROL_LEFT
    global PWM_CONTROL_RIGHT
    GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN2, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_ENABLE, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN3, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN4, GPIO.OUT)
    PWM_CONTROL_RIGHT = GPIO.PWM(MOTOR_RIGHT_ENABLE, 100)  # Initial Freq 1
    PWM_CONTROL_LEFT = GPIO.PWM(MOTOR_LEFT_ENABLE, 100)  # Initial Freq 1
    PWM_CONTROL_LEFT.start(SPEED)
    PWM_CONTROL_RIGHT.start(SPEED)


def setupIO():
    GPIO.setmode(GPIO.BOARD)
    setupMotorIO()


def front():
    moveLeftMotorForward()
    moveRightMotorForward()
    print("Move Front")


def back():
    moveLeftMotorBackward()
    moveRightMotorBackward()
    print("Move Back")


def left():
    moveRightMotorForward()
    moveLeftMotorBackward()
    time.sleep(TURN_TIME)
    stay_put()
    print("Move Left")


def right():
    moveRightMotorBackward()
    moveLeftMotorForward()
    time.sleep(TURN_TIME)
    stay_put()
    print("Turn right")


def changeSpeed(upOrDown):
    global SPEED
    if (upOrDown == 'u'):
        SPEED = SPEED + 25
        if (SPEED > 100):
            SPEED = 100
    else:
        SPEED = SPEED - 25
        if (SPEED < 0):
            SPEED = 0
    print(SPEED)
    PWM_CONTROL_LEFT.ChangeDutyCycle(SPEED)
    PWM_CONTROL_RIGHT.ChangeDutyCycle(SPEED)

def testMotorSpeeds():
    for i in range(10):
        print(i)
        PWM_CONTROL_LEFT.ChangeDutyCycle(i*10)
        PWM_CONTROL_RIGHT.ChangeDutyCycle(i*10)
        front()
        time.sleep(1)
        stay_put()  

print("Starting program")
setupIO()
try:
    stay_put()
    while True:
        # stay_put()
        decision = input("front(f) / back(b) / left(l) / right(r) / speedUp(u) / speedDown(d) / testSpeed(t) - ")
        if (decision == 'f'):
            front()
        elif (decision == 'b'):
            back()
        elif (decision == 'l'):
            left()
        elif (decision == 'r'):
            right()
        elif (decision == 'd'):
            changeSpeed('d')
        elif (decision == 'u'):
            changeSpeed('u')
        elif (decision == 't'):
            testMotorSpeeds()
        else:
            GPIO.cleanup()
            exit()
        time.sleep(1)  # Sleep for 1 second

except KeyboardInterrupt:
    GPIO.cleanup()
