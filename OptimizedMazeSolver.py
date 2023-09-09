import time
import RPi.GPIO as GPIO

# Define GPIO pins
SENSOR_PINS = [36, 23, 21, 19]
MOTOR_RIGHT_ENABLE1 = 33
MOTOR_RIGHT_PIN1 = 15
MOTOR_RIGHT_PIN2 = 13
MOTOR_LEFT_ENABLE2 = 32
MOTOR_LEFT_PIN3 = 16
MOTOR_LEFT_PIN4 = 18

# Define constants
SPEED_HIGH = 50
SPEED_LOW = 40
ADJUSTING_TIME_DELAY = 0.03
SLEEP_TIME_DELAY = 0.03
INIT_TURN_TIME = 0.06
STEPS_FOR_HOME = 6

# Define sensor labels
SENSOR_LABELS = ["One", "Two", "Three", "Four"]

# Initialize GPIO
def setup_GPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_RIGHT_ENABLE1, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN2, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_ENABLE2, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN3, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN4, GPIO.OUT)

# Initialize PWM
def setup_PWM():
    PWM_CONTROL_RIGHT = GPIO.PWM(MOTOR_RIGHT_ENABLE1, 70)
    PWM_CONTROL_LEFT = GPIO.PWM(MOTOR_LEFT_ENABLE2, 70)
    PWM_CONTROL_LEFT.start(SPEED_HIGH)
    PWM_CONTROL_RIGHT.start(SPEED_HIGH)
    return PWM_CONTROL_LEFT, PWM_CONTROL_RIGHT

# Initialize sensors
def setup_sensors():
    for pin in SENSOR_PINS:
        GPIO.setup(pin, GPIO.IN)

# Motor control functions
def move_motor(enable_pin, pin1, pin2, forward):
    GPIO.output(enable_pin, 1)
    GPIO.output(pin1, forward)
    GPIO.output(pin2, not forward)

def stop_motors():
    GPIO.output(MOTOR_LEFT_ENABLE2, 0)
    GPIO.output(MOTOR_RIGHT_ENABLE1, 0)
    time.sleep(SLEEP_TIME_DELAY)

# Speed control functions
def set_speed(pwm_control, speed):
    pwm_control.ChangeDutyCycle(speed)

# Sensor functions
def read_sensors():
    return {label: GPIO.input(pin) for label, pin in zip(SENSOR_LABELS, SENSOR_PINS)}

# Movement functions
def move_forward():
    move_motor(MOTOR_RIGHT_ENABLE1, MOTOR_RIGHT_PIN1, MOTOR_RIGHT_PIN2, forward=True)
    move_motor(MOTOR_LEFT_ENABLE2, MOTOR_LEFT_PIN3, MOTOR_LEFT_PIN4, forward=True)

def adjust_right(steps=1):
    for _ in range(steps):
        move_motor(MOTOR_RIGHT_ENABLE1, MOTOR_RIGHT_PIN1, MOTOR_RIGHT_PIN2, forward=False)
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()

def adjust_left(steps=1):
    for _ in range(steps):
        move_motor(MOTOR_LEFT_ENABLE2, MOTOR_LEFT_PIN3, MOTOR_LEFT_PIN4, forward=False)
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()

def turn_left():
    set_speed(PWM_CONTROL_LEFT, SPEED_LOW)
    set_speed(PWM_CONTROL_RIGHT, SPEED_LOW)
    while not read_sensors()["One"]:
        move_forward()
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()
    while not (read_sensors()["Two"] or read_sensors()["Three"]):
        move_forward()
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()
    set_speed(PWM_CONTROL_LEFT, SPEED_HIGH)
    set_speed(PWM_CONTROL_RIGHT, SPEED_HIGH)

def turn_right():
    set_speed(PWM_CONTROL_LEFT, SPEED_LOW)
    set_speed(PWM_CONTROL_RIGHT, SPEED_LOW)
    while not read_sensors()["Four"]:
        move_forward()
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()
    while not (read_sensors()["Two"] or read_sensors()["Three"]):
        move_forward()
        time.sleep(SLEEP_TIME_DELAY)
        stop_motors()
    set_speed(PWM_CONTROL_LEFT, SPEED_HIGH)
    set_speed(PWM_CONTROL_RIGHT, SPEED_HIGH)

def turn_around():
    turn_right()

def decide_action():
    sensor_val = read_sensors()
    if sensor_val["Two"] == 0 and sensor_val["Three"] == 1:
        return "adjust_right"
    elif sensor_val["Two"] == 1 and sensor_val["Three"] == 0:
        return "adjust_left"
    elif sensor_val["One"] == 0 and sensor_val["Two"] == 0 and sensor_val["Three"] == 0 and sensor_val["Four"] == 1:
        return "dead_end"
    else:
        return "straight"

def act():
    decision = decide_action()
    if decision == "straight":
        move_forward()
    elif decision == "adjust_left":
        adjust_left()
    elif decision == "adjust_right":
        adjust_right()
    elif decision == "dead_end":
        turn_around()
    else:
        print("Unmapped")
        stop_motors()

if __name__ == "__main__":
    setup_GPIO()
    PWM_CONTROL_LEFT, PWM_CONTROL_RIGHT = setup_PWM()
    setup_sensors()
    try:
        while True:
            act()
    except KeyboardInterrupt:
        GPIO.cleanup()
