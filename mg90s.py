
import sys
import time
from ctypes import *
from ricontroller import RiController
from riservo import RiServo

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(False))
        print(f"Controller Model: {controller.model_name}")
        
        controller.init()

        servo_1 = RiServo(controller)
        servo_1.add("mg90s", 0)

        print("\nMG90S поворот в крайние положения")

        servo_1.rotate(0, 200) # 2320 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 229

        servo_1.rotate(1, 200) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 0

        servo_1.set_middle() # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 114

        print("\nMG90S управление через длительность импульсов")

        servo_1.turn_by_pulse(2650) # 2550 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 229 (custom 207)

        servo_1.turn_by_pulse(365) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 0
        
        servo_1.turn_by_pulse(1500) # 1430 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 114 (custom 103)
        

        print("\nMG90S Минимальный шаг")

        servo_1.set_middle() # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 114


        servo_1.rotate_min_step(1, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        servo_1.rotate_min_step(0, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        print("\nMG90S управление через Duty")

        servo_1.turn_by_duty(75)
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        servo_1.turn_by_duty(300)
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        servo_1.turn_by_duty(540)
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle()))
     
        print("\nMG90S поворот на заданный угол")

        servo_1.set_middle() # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(servo_1.get_angle())) # угол 114

        servo_1.turn_by_angle(90, 200)
        time.sleep(1) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        servo_1.turn_by_angle(-90, 300)
        time.sleep(1) 
        print("servo_1 angle: " + str(servo_1.get_angle()))

        servo_1.cleanup_servo()
        controller.cleanup()

    except Exception as e:
        print("Class RiApi Error:", str(e))
        sys.exit(2)
