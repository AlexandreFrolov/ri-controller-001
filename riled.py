import sys
import time
import platform
from ctypes import *

class RiLed:
    def __init__(self, controller):
        self.controller = controller
        self.model_name = "ky016"
        self.errTextC = create_string_buffer(1000)
        self.state = c_int()
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

    def get_state(self):
        self.controller.lib.RI_SDK_exec_RGB_LED_GetState.argtypes = [c_int, POINTER(c_int), c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_GetState(self.led, self.state, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_GetState failed with error code {errCode}: {self.err_msg()}")
        return self.state

    def get_color(self):
        self.controller.lib.RI_SDK_exec_RGB_LED_GetColor.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), c_char_p]
        red = c_int()
        green = c_int()
        blue = c_int()
        led_color = {
         'red': red,
         'green': green,
         'blue': blue
        }
        errCode = self.controller.lib.RI_SDK_exec_RGB_LED_GetColor(self.led, red, green, blue, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_RGB_LED_GetColor failed with error code {errCode}: {self.err_msg()}")
        led_color['red'] = red
        led_color['green'] = green
        led_color['blue'] = blue
        return led_color
