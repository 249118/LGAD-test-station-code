from imports import *
from instrument_references import *
from devices.oscilloscope import *
from sweep import *


class AutomaticMode():
    def __init__(self) -> None:
        self.worker = None
        self.pause = False
        self.stop = False

        self.show_matrix = False

        self.number_of_all_points = 0
        self.matrix = []

        self.current_line = ""
        self.line_lock = Lock()

        self.current_status=""
        self.status_lock = Lock()

        self.current_progress = (0,1)
        self.progress_lock = Lock()


    def worker_thread(self, number_of_points, list_of_sweeps : List[Sweep] ,oscilloscope : Device):

        with self.progress_lock:
            self.current_progress = (0, number_of_points)

        #check if all devices are in ok state, otherwise return
        if oscilloscope.status != Device.Status.OK:
            self.current_status = "Not all devices are ready"
            return False

        for sweep in list_of_sweeps:
            s : Sweep
            s = sweep
            if s.device_reference.status != Device.Status.OK:
                with self.status_lock:
                        self.current_status = "Not all devices are ready"
                return False

        #create file for measurment data
        try:
            p = pathlib.Path("output/")
            p.mkdir(exist_ok=True)
            date = datetime.datetime.now()
            measurment_folder = "measurment_" + date.strftime("%d.%m.%y_%H.%M.%S")
            folder = pathlib.Path("output/" + measurment_folder + "/")
            folder.mkdir(exist_ok=False)
            file_path = folder / "measurment.csv"
        except:
            with self.status_lock:
                self.current_status = "Could not create measurment file"
            return False

        with file_path.open("a") as f:
            f.write("software ver: V3.0"+"\n")
            f.write("no of points:"+str(number_of_points)+"\n")
            temp = ""
            for sweep in list_of_sweeps:
                s : Sweep
                s = sweep
                temp += "[" + s.device_reference.name + ":" + s.device_reference.get_units() + "],"

            temp+= str("[" + oscilloscope.name + ":" + oscilloscope.get_units()+"],")
            f.write(temp+"\n")
                
        #start measurment
        for p in range(number_of_points):
            data_line = ""

            #Set all devices to the desired value
            for sweep in list_of_sweeps:
                s : Sweep
                s = sweep
                sweep.device_reference.set_sweep_value(sweep.calc(p))
                sleep(0.1)
                wait = True
                while wait:
                    wait = not sweep.device_reference.is_value_set()
                    with self.status_lock:
                        self.current_status = "Waiting for: " + str(sweep.device_reference.name)
                        sleep(0.1)
                
            for sweep in list_of_sweeps:
                data_line += str(sweep.device_reference.get_sweep_value()) + ","

            with self.line_lock:
                self.current_line = data_line
            data_line += str(oscilloscope.get_values()) + "\n"

            #Make sure devices did not fault before continiuing
            if oscilloscope.status != Device.Status.OK:
                with self.status_lock:
                    self.current_status = "Not all devices are ready"
                self.pause = True

            with self.progress_lock:
                self.current_progress = (self.current_progress[0]+1,number_of_points)

            for sweep in list_of_sweeps:
                if sweep.device_reference.status != Device.Status.OK:
                    with self.status_lock:
                        self.current_status = "Device reported fault: " + str(sweep.device_reference.name)
                    self.pause = True

            with file_path.open("a") as f:
                f.write(data_line)

            while self.pause:
                pass
            
            if self.stop:
                return False
            
        return True


        
    def run(self, instrument_ref: InstrumentReferences):
        imgui.begin("Automatic mode", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.separator()
        imgui.text("XYZ sweep configurations")

        #Sort what devices were initialised
        available_sweep_devices = []
        for sweep in instrument_ref.sweep_controlers:
            s : Sweep
            s = sweep
            if s.device_reference.status == Device.Status.OK:
                available_sweep_devices.append(s)

        #Show sweep gui
        for sweep in available_sweep_devices:
            s : Sweep
            s = sweep
            s.gui_sweep()
            imgui.separator()

        self.number_of_all_points=1
        enabled_sweep_devices = []
        for sweep in available_sweep_devices:
            s : Sweep
            s = sweep
            if s.enabled:
                enabled_sweep_devices.append(s)
                s.divisor = self.number_of_all_points
                self.number_of_all_points*=s.points


        imgui.text("Number of all data points: " + str(self.number_of_all_points))

        #Generate matrix
        imgui.separator()
        self.show_matrix = imgui.checkbox("Show generated matrix", self.show_matrix)[1]
        if self.show_matrix:
            unit_line = "no"
            for sweep in enabled_sweep_devices:
                    s : Sweep
                    s = sweep
                    unit_line += "," + s.device_reference.units
            imgui.text(unit_line)
            for i in range(self.number_of_all_points):
                line = str(i)
                for sweep in enabled_sweep_devices:
                    s : Sweep
                    s = sweep
                    output = s.calc(i)
                    line += "," + str(output)
                imgui.text(line)

        imgui.separator()
        
        if self.line_lock.acquire(False):
            imgui.text(str(self.current_line))
            self.line_lock.release()

        imgui.separator()
        imgui.text("Automatic mode control")
        if imgui.button("Start"):
            self.pause = False
            self.stop = False
            self.worker = Thread(target=self.worker_thread, daemon=False, args=([self.number_of_all_points, enabled_sweep_devices ,instrument_ref.oscilloscope])) 
            self.worker.start()

        if imgui.button("Pause"):
            if self.pause:
                self.pause = False
            else:
                self.pause = True
        imgui.text("Pause: " + str(self.pause))

        if imgui.button("Stop"):
            self.stop = True

        imgui.separator()
        imgui.text("Experiment status: ")
        imgui.same_line()
        if self.worker is None:
            imgui.text("Not initialised")
        elif self.worker.is_alive():
            imgui.text("Working")
        else:
            imgui.text("End")
        with self.progress_lock:
            imgui.text(str(self.current_progress[0]) + " out of: " + str(self.current_progress[1]) + " completed")
        imgui.separator()
        with self.status_lock:
            imgui.text(str(self.current_status))

        imgui.separator()
        imgui.end()

    

        