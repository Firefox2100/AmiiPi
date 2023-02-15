import RPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from luma.core.virtual import terminal
from PIL import ImageFont

stick_up = 6
stick_down = 19
stick_left = 5
stick_right = 26
stick_press = 13
key1 = 21
key2 = 20
key3 = 16

spi_device = 0
spi_port = 0
rotation = 2

font_path = "../assets/ProggyTiny.ttf"
font_size = 16


def gpio_config():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(stick_up,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(stick_down,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(stick_left,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(stick_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(stick_press, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key1,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3,        GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(stick_up,     GPIO.RISING)
    GPIO.add_event_detect(stick_down,   GPIO.RISING)
    GPIO.add_event_detect(stick_left,   GPIO.RISING)
    GPIO.add_event_detect(stick_right,  GPIO.RISING)
    GPIO.add_event_detect(stick_press,  GPIO.RISING)
    GPIO.add_event_detect(key1,         GPIO.RISING)
    GPIO.add_event_detect(key2,         GPIO.RISING)
    GPIO.add_event_detect(key3,         GPIO.RISING)


def get_terminal() -> terminal:
    serial = spi(device=spi_device, port=spi_port)
    device = sh1106(serial, rotate=rotation)

    font = ImageFont.truetype(font_path, font_size)
    term = terminal(device, font)

    return term
