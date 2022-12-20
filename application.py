from imports import *
from instrument_references import *
from automatic_mode import *

class Application:

    def __init__(self):
        self.instrument_ref = InstrumentReferences()
        self.device_gui_mode = True
        self.automatic_mode = False
        self.auto = AutomaticMode()

    def run(self):
        imgui.begin("Mode", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        self.automatic_mode = imgui.checkbox("Automatic mode", self.automatic_mode)[1]

        if imgui.button("save devices"):
            db = shelve.open("device_init")
            for d in self.instrument_ref.list_of_all_devices:
                if d.status == Device.Status.OK:
                    device : Device
                    device = d
                    db[device.name] = device.initialisation_string
            db.close()

        if imgui.button("recall devices"):
            db = shelve.open("device_init")
            for k in db.keys():
                for d in self.instrument_ref.list_of_all_devices:
                    if d.status == Device.Status.NOTCONNECTED:
                        device : Device
                        device = d
                        if device.name == k:
                            temp = db[k]
                            if temp != None:
                                if temp != '':
                                    device.initialise(temp)
                                else:
                                    device.initialise()
                            print("Initialised: " + str(k))
            db.close()

        if imgui.button("save configuration"):
            db = shelve.open("device_config")
            for d in self.instrument_ref.list_of_all_devices:
                if d.status == Device.Status.OK:
                    device : Device
                    device = d
                    db[device.name] = device.get_configuration()
            db.close()

        if imgui.button("recall configuration"):
            db = shelve.open("device_config")
            for k in db.keys():
                for d in self.instrument_ref.list_of_all_devices:
                    if d.status == Device.Status.OK:
                        device : Device
                        device = d
                        if device.name == k:
                            temp = db[k]
                            if temp != None:
                                try:
                                    device.set_configuration(*temp)
                                except:
                                    device.set_configuration(temp)
                            print("Found: " + str(k))
            db.close()

        device = self.instrument_ref.gui_camera
        imgui.begin(str(device.name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        device.gui_initialise()
        imgui.separator()
        device.gui_configure()
        imgui.separator()
        device.gui_manual_control()
        imgui.separator()
        device.gui_status()
        imgui.end()

        if self.automatic_mode:
             self.auto.run(self.instrument_ref)
        else:
            self.device_based_gui()
        imgui.end()

    def device_based_gui(self):
        for d in self.instrument_ref.list_of_all_guis:
            device : DeviceGui
            device = d
            imgui.begin(str(d.name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            device.gui_initialise()
            imgui.separator()
            device.gui_configure()
            imgui.separator()
            device.gui_manual_control()
            imgui.separator()
            device.gui_status()
            imgui.end()
        pass

