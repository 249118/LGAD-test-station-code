from ctypes import *
import os
import sys
import platform
import netifaces
import getpass
import keyboard
import time
from devices.linear_stage import *
from devices.hv_supply import *
from devices.laser_power_meter import *
from devices.oscilloscope import *
from devices.camera import *
from devices.digital_multi_meter import *
from devices.lv_supply import *
from devices.laser_power_controler import *
from devices.temperature_controler import *

from device_gui.gui_linear_stage import *
from device_gui.gui_oscilloscope import *
from device_gui.gui_hv_supply import *
from device_gui.gui_camera import *
from device_gui.gui_laser_power_meter import *
from device_gui.gui_digital_multi_meter import *
from device_gui.gui_lv_supply import *
from device_gui.gui_laser_power_controler import *
from device_gui.gui_temperature_controler import *

from sweep import Sweep

class InstrumentReferences:
    def __init__(self):
        #references to linear stage objects
        self.x_axis_stage = LinearStage("X")
        self.y_axis_stage = LinearStage("Y")
        self.z_axis_stage = LinearStage("Z")
        self.atten_axis_stage = LinearStage("Attenuator")
        #reference to HV supply object
        self.hv_supply = HVSupply()
        #reference to LV supply object
        self.lv_supply = LVSupply()
        #reference to oscilloscope
        self.oscilloscope = Oscilloscope()
        #reference to camera
        self.camera = Camera()
        self.gui_camera = GuiCamera(self.camera)
        #reference to laser power meter object
        #self.laser_power_meter = LaserPowerMeter()
        #reference to DMM
        self.digital_multi_meter = DigitalMultiMeter()

        #self.laser_power_controler = LaserPowerControler(self.laser_power_meter, self.atten_axis_stage)
        self.temperature_controler = TemperatureControler(self.digital_multi_meter, self.lv_supply)

        self.list_of_all_devices = []
        self.list_of_all_devices.append(self.x_axis_stage)
        self.list_of_all_devices.append(self.y_axis_stage)
        self.list_of_all_devices.append(self.z_axis_stage)
        self.list_of_all_devices.append(self.atten_axis_stage)
        self.list_of_all_devices.append(self.hv_supply)
        self.list_of_all_devices.append(self.lv_supply)
        self.list_of_all_devices.append(self.oscilloscope)
        self.list_of_all_devices.append(self.camera)
        #self.list_of_all_devices.append(self.laser_power_meter)
        self.list_of_all_devices.append(self.digital_multi_meter)
        #self.list_of_all_devices.append(self.laser_power_controler)
        self.list_of_all_devices.append(self.temperature_controler)

        self.list_of_all_guis = []
        self.list_of_all_guis.append(GuiLinearStage(self.x_axis_stage))
        self.list_of_all_guis.append(GuiLinearStage(self.y_axis_stage))
        self.list_of_all_guis.append(GuiLinearStage(self.z_axis_stage))
        self.list_of_all_guis.append(GuiLinearStage(self.atten_axis_stage))
        self.list_of_all_guis.append(GuiHVPSU(self.hv_supply))
        self.list_of_all_guis.append(GuiLVPSU(self.lv_supply))
        self.list_of_all_guis.append(GuiOscilloscope(self.oscilloscope))
        #self.list_of_all_guis.append(GuiCamera(self.camera)) 
        #self.list_of_all_guis.append(GuiLaserPowerMeter(self.laser_power_meter))
        self.list_of_all_guis.append(GuiDigitalMultiMeter(self.digital_multi_meter))
        #self.list_of_all_guis.append(GuiLaserPowerControler(self.laser_power_controler))
        self.list_of_all_guis.append(GuiTemperatureControler(self.temperature_controler))
        
        self.sweep_controlers = []
        self.sweep_controlers.append(Sweep(self.x_axis_stage))
        self.sweep_controlers.append(Sweep(self.y_axis_stage))
        self.sweep_controlers.append(Sweep(self.z_axis_stage))
        self.sweep_controlers.append(Sweep(self.hv_supply))
        #self.sweep_controlers.append(Sweep(self.laser_power_controler))
        self.sweep_controlers.append(Sweep(self.temperature_controler))
        #self.sweep_controlers.append(Sweep(self.laser_power_controler))
        #self.sweep_controlers.append(Sweep(self.temperature_controler))