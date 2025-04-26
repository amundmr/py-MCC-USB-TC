import uldaq as ul
from uldaq import InterfaceType, TempScale
from uldaq import DaqDeviceInfo

from lib import *

import time

class DeviceConnection:
    def __init__(self):
        self.set_up()

    def __del__(self):
        self.device.release()

    def set_up(self):
        devices = ul.get_daq_device_inventory(InterfaceType.USB)

        if not devices:
            raise Exception('Error: No USB DAQ devices found')

        device = devices[0]
        self.device = ul.DaqDevice(device)
        self.device.connect()
        self.ai_device = self.device.get_ai_device()
        device_descriptor = self.device.get_descriptor()
        print(f"Connected to device {device_descriptor.product_name}, product id: {device_descriptor.product_id}, SN: {device_descriptor._unique_id}")

        daq_dev_info = self.device.get_info()

        ai_info = self.ai_device.get_info()
        if not ai_info.get_num_chans_by_type(2) == CHANNELS_TOTAL:
            raise Exception(f"Could not get {CHANNELS_TOTAL} temp channels from device.")

        time.sleep(2) # Required for the device to finish setting up.

    def measure_temps(self):
        # Get the value from the device (optional parameters omitted)
        # Performance: ~0.065s with 4 channels
        temps = []
        for channel in range(CHANNELS_TOTAL):
            try:
                value = self.ai_device.t_in(channel, TempScale.KELVIN)
            except ul.ULException as e:
                if e.error_code == 85:
                    # Temperature input has open connection
                    # Don't bother shouting about
                    value = 0
                else:
                    print(f"UL Error encountered on channel {channel}. Returning value 0.")
                    print(e)
                    value = 0

            temps.append(value)
        return temps



if __name__ == "__main__":
    deviceconnection = DeviceConnection()
    try:
        curr_time = time.time()
        print(f"Starting data logging every {MEASUREMENT_INTERVAL}s.")
        while True:
            if time.time() - curr_time > MEASUREMENT_INTERVAL:
                curr_time = time.time()
                temps = deviceconnection.measure_temps()
                save_data(temps)

    except KeyboardInterrupt:
        print("Stopping temp logging and releasing device.")
        del deviceconnection
        
