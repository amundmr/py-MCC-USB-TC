# Common functions for all OS'es
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

