import sys
import time
import platform
from ctypes import *
import traceback

class RiController:
    def __init__(self, is_async: c_bool):
        self.model_name = "RoboIntellect controller 001"
        self.platform = platform.system()
        try:
            if self.platform == "Windows":
                self.lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")
            if self.platform == "Linux":
                self.lib = cdll.LoadLibrary("/usr/local/robohand_remote_control/librisdk.so")
        except OSError as e:
            raise Exception("Failed to load: " + str(e))
        self.errTextC = create_string_buffer(1000)
        self.i2c = c_int()
        self.pwm = c_int()
        self.is_async = is_async

    def err_msg(self):
        return(self.errTextC.raw.decode())

    def async_on(self):
        self.is_async = c_bool(True)         

    def async_off(self):
        self.is_async = c_bool(False)         

    def init(self):
        self.lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_CreateBasic.argtypes = [POINTER(c_int), c_char_p]
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]
        descriptor = c_int()

        errCode = self.lib.RI_SDK_InitSDK(1, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_InitSDK failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_CreateBasic(descriptor, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateBasic failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), self.pwm, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), self.i2c, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_LinkPWMToController(self.pwm, self.i2c, c_uint8(0x40), self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkPWMToController failed with error code {errCode}: {self.err_msg()}")

    def cleanup(self):
        self.lib.RI_SDK_sigmod_PWM_ResetAll.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]
        errCode = self.lib.RI_SDK_sigmod_PWM_ResetAll(self.pwm, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_sigmod_PWM_ResetAll failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_DestroyComponent(self.i2c, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.lib.RI_SDK_DestroySDK(True, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_DestroySDK failed with error code {errCode}: {self.err_msg()}")
