import RPi.GPIO as GPIO
import time
def main ():
    BT1 = 14
    BT2 = 4
    BT3 = 3
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global S
    s = sg90()
    anglepulseBT1 = 10
    anglepulseBT2 = 50
    anglepulseBT3 = 120
    print("tat ca da san sang")
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("quay 10 angle")
            anglepulseBT1 = controlservo(s, anglepulseBT1)
        if GPIO.input(BT2) == GPIO.LOW:
            print("quay 50 angle")
            anglepulseBT2 = controlservo(s, anglepulseBT2)
        if GPIO.input(BT3) == GPIO.LOW:
            print("quay 120 angle")
            anglepulseBT3 = controlservo(s, anglepulseBT3)
def controlservo(s, anglepulseBT):
    current = s.currentdirection()
    if current >= 180 or current <=0:
        anglepulseBT = -anglepulseBT
    rotato = anglepulseBT + current
    rotato = 180 if rotato >= 180 else 0 if rotato <= 0 else rotato
    s.setdirection(rotato, 40)
    time.sleep(0.5)
    return anglepulseBT
class sg90:
    def __init__(self):
        self.pin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)
        self.direction = 90
    def cleanup(self):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()
    def currentdirection(self):
        return self.direction
    def _henkan(self, value):
        return round(0.056 * value + 2.0)
    def setdirection(self, direction, speed):
        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction
try:
    main()
except KeyboardInterrupt:
    S.cleanup()
