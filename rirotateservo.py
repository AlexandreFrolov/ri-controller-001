import sys
import time
import platform
from ctypes import *

class RiRotateServo:
    def __init__(self, controller):
        self.controller = controller
        self.errTextC = create_string_buffer(1000)
        self.state = c_int()
        self.rservo = c_int()

    def err_msg(self):
        return(self.errTextC.raw.decode())

    def add(self, servo_type, channel):
        self.controller.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.controller.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        errCode = self.controller.lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive_rotate".encode(), servo_type.encode(), self.rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.controller.lib.RI_SDK_LinkServodriveToController(self.rservo, self.controller.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.err_msg()}")        

    def add_custom_servo(self, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, channel):
        self.controller.lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
        self.controller.lib.RI_SDK_exec_RServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        self.controller.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        rservo = c_int()

        errCode = self.controller.lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive_rotate".encode(), rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateDeviceComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.controller.lib.RI_SDK_exec_RServoDrive_CustomDeviceInit(rservo, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RServoDrive_CustomDeviceInit failed with error code {errCode}: {self.err_msg()}")

        errCode = self.controller.lib.RI_SDK_LinkServodriveToController(rservo, self.controller.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.err_msg()}")   

        self.rservo = rservo
        return rservo

    def rotate_by_pulse(self, dt):
        self.controller.lib.RI_SDK_exec_RServoDrive_RotateByPulse.argtypes = [c_int, c_int, c_bool, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RServoDrive_RotateByPulse(self.rservo, dt, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RServoDrive_RotateByPulse failed with error code {errCode}: {self.err_msg()}")

    def stop_rservo(self):
        self.controller.lib.RI_SDK_exec_RServoDrive_Stop.argtypes = [c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RServoDrive_Stop(self.rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RServoDrive_Stop failed with error code {errCode}: {self.err_msg()}")

    def cleanup_servo(self):
        self.controller.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_DestroyComponent(self.rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {self.err_msg()}")


