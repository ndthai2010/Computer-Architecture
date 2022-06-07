import RPi.GPIO as GPIO
import Adafruit_Nokia_LCD as LCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

def main() :
    BT1 = 14
    SCLK = 23
    DIN = 27
    DC = 17
    RST = 15
    CS = 18
    BL = 22
    
    currentAngle = 0
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global s 
    s = sg90()
    
    anglepulseBT1 = 15
    
    global disp
    
    disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
    
    disp.begin(contrast=60)
    disp.clear()
    disp.display()
    
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, LCD.LCDWIDTH - 1, LCD.LCDHEIGHT - 1 ), outline = 0, fill = 255)
    font = ImageFont.load_default()
    draw.text((7, 8), "Welcome ", font = font)
    disp.image(image)
    disp.display()

    
    print("Init complete")
    while True: 
        if GPIO.input(BT1) == GPIO.LOW:
            print("rotate 5 angle")
            anglepulseBT1 = controlservo(s, anglepulseBT1)
            currentAngle +=5
            if currentAngle >= 180:
                currentAngle = 0
            disp.clear()
            disp.display()
            image_wait = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
            draw = ImageDraw.Draw(image_wait)
            draw.rectangle((0, 0, LCD.LCDWIDTH - 1, LCD.LCDHEIGHT - 1 ), outline = 0, fill = 255)
            draw.text((7, 8), "Rotate 5 angle ", font = font)
            draw.text((7, 25), str(currentAngle), font = font)
            disp.image(image_wait)
            disp.display()
            
def controlservo(s, anglepulseBT):
    current = s.currentdirection()
    if current > 180 or current <= 0:
        anglepulseBT = - anglepulseBT
    rotato = anglepulseBT + current
    if rotato > 180:
        rotato = 0
    elif rotato < 0:
        rotato = 0
    s.setdirection(rotato, 40)
    time.sleep(0.5)
    currentAngle = rotato
    return anglepulseBT

class sg90(object):
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
        return round(0.056*value +2.0)
    
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
    s.cleanup()