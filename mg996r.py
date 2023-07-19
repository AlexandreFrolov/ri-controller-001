import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from rirotateservo import RiRotateServo

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(True))
        print(f"Controller Model: {controller.model_name}")
        
        controller.init()

        rservo = RiRotateServo(controller)

        rservo.add("mg996r", 0)
#        rservo.stop_rservo()

        print(1050)
        rservo.rotate_by_pulse(1050)
        time.sleep(3) 

        print(2100)
        rservo.rotate_by_pulse(2100)
        time.sleep(3) 

        print(1570)
        rservo.rotate_by_pulse(1570)
        time.sleep(3) 

        rservo.cleanup_servo()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)