from mcculw import ul
from mcculw.enums import InterfaceType, TempScale
from mcculw.device_info import DaqDeviceInfo
import time
import csv
from datetime import date
import os

BOARD_NUM = 0
CHANNELS_TOTAL = 8 # Do not change this unless you want to adapt your data reader too.
MEASUREMENT_INTERVAL = 1 # Seconds

"""
8 channels, measurement_interval of 1s data usage:
test: after 30 min of data acq, the file size is: 294 912 bytes
1 hour: 0.59MB
1 day:  14.16 MB
1 month:439 MB
1 year: 5 266 MB (yes, 5.3GB)
"""


def set_up():
    ul.ignore_instacal() #This allows us to not auto-load instacal configs, so we can create our own object
    devices = ul.get_daq_device_inventory(InterfaceType.USB)

    if not devices:
        raise Exception('Error: No DAQ devices found')

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

def save_data(temp_list):

    if not len(temp_list) == CHANNELS_TOTAL:
        raise Exception(f"Temp list doesn't contain exactly {CHANNELS_TOTAL} values! There is something fishy.")

    datestr = date.today()

    if not os.path.isfile(f"{datestr}.csv"):
        with open(f"{datestr}.csv", "w") as f:
            pass
    else:
        with open(f"{datestr}.csv", "a", newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([time.time(), *temp_list])


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
