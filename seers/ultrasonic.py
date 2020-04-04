import time
from RPi import GPIO

SPEED_OF_SOUND = 34300 # in cm/s

def find_next_node():
    """
    Uses the ultrasonic sensor to get the distance to the next sensor node.
    Assumes the PKIIPS standard ultrasonic schematic is being used and 
    the sensor is pointed directly at the next node.

    return: distance to the next sensor node, in cm
    rtype: int
    """

    # Pins
    TRIGGER = 18
    ECHO = 24

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIGGER, True)
    time.sleep(0.00001) # recommended wait for ultrasonic to go out
    GPIO.output(TRIGGER, False)

    start = end = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()
    
    while GPIO.input(ECHO) == 1:
        end = time.time()
    
    elapsed = end - start
    return (elapsed * SPEED_OF_SOUND) / 2