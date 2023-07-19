import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from riled import RiLed

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(True))
        print(f"Model: {controller.model_name}")
        controller.init()

        led = RiLed(controller)
        print(f"Model: {led.model_name}")



        led.add(14, 15, 13)

        print("Led state: " + str(led.get_state()))

        led.pulse(255, 0, 0, 1500)
        time.sleep(1) 
        led.pulse(0, 255, 0, 1500)
        time.sleep(1) 
        led.pulse(0, 0, 255, 1500)
        time.sleep(1) 

        print("Led state: " + str(led.get_state()))

        color = led.get_color()

        print("Led color: ")
        print(color)

        led.flicker(255, 0, 0, 500, 5)
        led.flicker(0, 255, 0, 500, 5)
        led.flicker(0, 0, 255, 500, 5)

        led.pulse(255, 0, 0, 500)
        led.pulse(0, 255, 0, 500)
        led.pulse(0, 0, 255, 500)


        led.pulse_pause(255, 0, 0, 1000, 200, 3)
        led.pulse_pause(0, 255, 0, 1000, 200, 3)
        led.pulse_pause(0, 0, 255, 1000, 200, 3)

        led.pulse_frequency(255, 0, 0, 10, 10)
        led.pulse_frequency(0, 255, 0, 20, 10)
        led.pulse_frequency(0, 0, 255, 30, 10)

        time.sleep(1) 

        led.stop()
        led.cleanup()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)