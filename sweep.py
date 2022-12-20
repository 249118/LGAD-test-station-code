from imports import *
from devices.device import *

class Sweep():
                def __init__(self, device_reference : Device):
                    self.device_reference = device_reference
                    self.divisor = 1
                    self.modulo = 0
                    self.multiplication = 1

                    self.points = 2
                    self.minimum = 0
                    self.maximum = 0
                    self.delta = 0

                    self.enabled = False
                    self.array = []

                def gui_sweep(self):
                    #display sweep configuration window, check if all values are within proper limits
                    if self.device_reference.status == Device.Status.OK:
                        name = self.device_reference.name
                        imgui.text(name + " sweep configuration")
                        minimum, maximum = self.device_reference.get_limits()
                        changed, (self.minimum, self.maximum) = imgui.slider_int2("Sweep range: " + str(name), self.minimum, self.maximum, minimum, maximum)
                        self.minimum = np.clip(self.minimum, minimum, maximum)
                        self.maximum = np.clip(self.maximum, minimum, maximum)
                        changed, temp = imgui.input_int("Sweep points: " + str(name), self.points, 1, 10, imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                        if temp >= 2:
                            self.points = temp
                        self.enabled = imgui.checkbox(name + " enabled", self.enabled)[1]
                        imgui.checkbox("Is possible? ", self.is_possible())
                        self.delta = (self.maximum - self.minimum)/(self.points-1)
                        self.modulo = self.points

                def calc(self, i):
                    #calculate value of the device based on internal variables and given point
                    if not self.is_possible():
                        return i
                    else:
                        sequence_val = (math.floor(i/self.divisor))%self.modulo
                        real_val = sequence_val*self.delta + self.minimum
                        return real_val

                def is_possible(self):
                    if self.minimum >= self.maximum:
                        return False
                    if self.points <= 1:
                        return False
                    return True
