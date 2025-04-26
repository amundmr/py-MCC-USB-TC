from mcculw import ul
from mcculw.enums import InterfaceType, TempScale
from mcculw.device_info import DaqDeviceInfo

from lib import *

import time

def set_up():
    ul.ignore_instacal() #This allows us to not auto-load instacal configs, so we can create our own object
    devices = ul.get_daq_device_inventory(InterfaceType.USB)

    if not devices:
        raise Exception('Error: No USB DAQ devices found')

    device = devices[0]
    ul.create_daq_device(BOARD_NUM, device)

    print(f"Connected to device {device}, product id: {device.product_id}, SN: {device._unique_id}")

    daq_dev_info = DaqDeviceInfo(BOARD_NUM)

    ai_info = daq_dev_info.get_ai_info()
    if not ai_info.num_temp_chans == CHANNELS_TOTAL:
        raise Exception(f"Could not get {CHANNELS_TOTAL} temp channels from device.")

    time.sleep(2) # Required for the device to finish setting up.

def measure_temps():
    # Get the value from the device (optional parameters omitted)
    # Performance: ~0.065s with 4 channels
    temps = []
    for channel in range(CHANNELS_TOTAL):
        try:
            value = ul.t_in(BOARD_NUM, channel, TempScale.KELVIN)
        except ul.ULError as e:
            print(f"UL Error encountered on channel {channel}. Returning value 0.")
            print(e)
            value = 0

        temps.append(value)
    return temps



if __name__ == "__main__":
    set_up()
    try:
        curr_time = time.time()
        print(f"Starting data logging every {MEASUREMENT_INTERVAL}s.")
        while True:
            if time.time() - curr_time > MEASUREMENT_INTERVAL:
                curr_time = time.time()
                temps = measure_temps()
                save_data(temps)

    except KeyboardInterrupt:
        print("Stopping temp logging and releasing device.")
        ul.release_daq_device(BOARD_NUM)
