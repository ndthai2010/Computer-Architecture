import RPi.GPIO as GPIO
from config import Config
import time
import Adafruit_Nokia_LCD as LCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    BT1 = 14
    DIR = 19
    PWD = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2
    PWD1 = GPIO.PWM(DIR, 100)
    PWD2 = GPIO.PWM(PWD, 100)
    PWD1.start(0)
    PWD2.start(0)
    currentPWD1 = 10
    currentPWD2 = 10
    print("Chuan bi hoan tat ok")
    while True:
        SCLK = 23
        DIN = 27
        DC = 17
        RST = 15
        CS = 18
        global disp
        if GPIO.input(BT1) == GPIO.LOW:
            print("press BT1")
            PWD2.ChangeDutyCycle(0)
            time.sleep(1)
            upPWD = 10
            currentPWD1 = (currentPWD1 + upPWD) if currentPWD1 < 100 else 100
            disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
            disp.begin(contrast=60)
            disp.clear()
            disp.display()
            image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
            draw = ImageDraw.Draw(image)
            draw.rectangle(
                (0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
            font = ImageFont.load_default()
            draw.text((8, 30), str(currentPWD1), font=font)
            disp.image(image)
            disp.display()
            handleDutyCycle(PWD1, currentPWD1, currentPWD2)
            print("Toc do hien tai: " + str(currentPWD1) + " theo chieu thuan")
            currentPWD2 = 0
            time.sleep(0.5)


def handleDutyCycle(PWD, currentPWD, currentPWDpre):
    print(currentPWDpre)
    if currentPWD > 100 or currentPWD < 0:
        print("khong the tang hay giam toc nua")
        return
    elif currentPWDpre != 0:
        time.sleep(1)
    PWD.ChangeDutyCycle(currentPWD)


try:
    main()
except KeyboardInterrupt:
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()
