import cv2
import RPi.GPIO as GPIO
import time


def main():
    BT1 = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(-1)
    print("Capture da ok")
    while True:
        ret, frame = capture.read()
# Frame duoc tra ve la dang ma tran; numpy.array print(type(frame))
# Chieu dai va chieu rong la co cua ma tran; print(frame.shape)
        if GPIO.input(BT1) == GPIO.LOW:
            while True:
                cv2.imshow("Anh chup camera", frame)
                cv2.waitKey()
                cv2.destroyWindow("Anh chup camera")
                break


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(namewindow)
