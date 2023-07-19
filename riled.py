import sys
import time
import platform
from ctypes import *
from ricontroller import RiController
import traceback

class RiLed:
    def __init__(self, controller):
        self.controller = controller
        self.model_name = "RoboIntellect LED"
        self.errTextC = create_string_buffer(1000)
        self.led = c_int()

    def err_msg(self):
        return(self.errTextC.raw.decode())

    def add(self, r, g, b):
        self.controller.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.controller.lib.RI_SDK_LinkLedToController.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), self.led, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {self.err_msg()}")
        errCode = self.controller.lib.RI_SDK_LinkLedToController(self.led, self.controller.pwm, r, g, b, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkLedToController failed with error code {errCode}: {self.err_msg()}")

    def stop(self):
        self.controller.lib.RI_SDK_exec_RGB_LED_Stop.argtypes = [c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_Stop(self.led, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_Stop failed with error code {errCode}: {self.err_msg()}")

    def cleanup(self):
        self.controller.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_DestroyComponent(self.led, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {self.err_msg()}")

    def pulse(self, r, g, b, duration):
        self.controller.lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_SinglePulse(self.led, r, g, b, duration, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_SinglePulse failed with error code {errCode}: {self.err_msg()}")

    def pulse_pause(self, r, g, b, duration, pause, limit):
        self.controller.lib.RI_SDK_exec_RGB_LED_FlashingWithPause.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_FlashingWithPause(self.led, r, g, b, duration, pause, limit, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_FlashingWithPause failed with error code {errCode}: {self.err_msg()}")

    def pulse_frequency(self, r, g, b, frequency, limit):
        self.controller.lib.RI_SDK_exec_RGB_LED_FlashingWithFrequency.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_FlashingWithFrequency(self.led, r, g, b, frequency, limit, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_FlashingWithFrequency failed with error code {errCode}: {self.err_msg()}")

    def flicker(self, r, g, b, duration, limit):
        self.controller.lib.RI_SDK_exec_RGB_LED_Flicker.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_Flicker(self.led, r, g, b, duration, limit, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_Flicker failed with error code {errCode}: {self.err_msg()}")
