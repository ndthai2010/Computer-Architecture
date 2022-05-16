import time
import Adafruit_Nokia_LCD as LCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main():
	SCLK = 23
	DIN = 27
	DC = 17
	RST = 15
	CS = 18
	global disp
	disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
	disp.begin(contrast=60)
	disp.clear()
	disp.display()
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
	draw.ellipse((2, 2, 22, 22), outline=0, fill=255)
	draw.rectangle((24, 2, 44, 22), outline=0, fill=255)
	draw.polygon([(46, 22), (56, 2), (66, 22)], outline=0, fill=255)
	draw.line((68, 22, 81, 2), fill=0)
	draw.line((68, 2, 81, 22), fill=0)
	font = ImageFont.load_default()
	draw.text((8, 30), 'Hi', font=font)
	disp.image(image)
	disp.display()
	while True:
		time.sleep(2)
try:
	main()
except KeyboardInterrupt:
	disp.clear()