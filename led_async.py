import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from riled import RiLed

def print_led_state(led):
    color = led.get_color()
    print(f"Led color: : {str(color['red'].value)}, {str(color['green'].value)}, {str(color['blue'].value)}")
    print(f"Led state: : {str(led.get_state().value)}")

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(True))
        print(f"Controller Model: {controller.model_name}")
        controller.init()

        led = RiLed(controller)
        print(f"LED Model: {led.model_name}")

        led.add(14, 15, 13)
        print_led_state(led)

        led.pulse(255, 0, 0, 1500)
        time.sleep(0.3) 
        print_led_state(led)
        time.sleep(1) 

        led.pulse(0, 255, 0, 1500)
        time.sleep(0.3) 
        print_led_state(led)
        time.sleep(1) 

        led.pulse(0, 0, 255, 1500)
        time.sleep(0.3) 
        print_led_state(led)
        time.sleep(1) 

        led.stop()
        led.cleanup()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)