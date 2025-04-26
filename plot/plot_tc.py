import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import sys
import os

# DATADIR = "C:/Users/Maccor/Documents/USB-TC/"
DATADIR = "~/Documents/git/py-MCC-USB-TC/"
# TC_CORR_CONSTS = [2.666, 2.598, 2.409, 2.138, 3.268, 3.271, 3.077, 3.242]
TC_CORR_CONSTS = [0, 0, 0, 0, 0, 0, 0, 0]


def get_tc_data(thermocouples: list, date_range: tuple):
    for tc in thermocouples:
        if tc not in range(8):
            # Todo, this and th exception above should probbly be changed with assertations..
            raise Exception(f"Thermocouple channel must be 0-7, you tried {tc_channel}.")
        
    # Find which days to get TC data for
    start_dt, end_dt = date_range
    delta = 60*60*24 # seconds in a day
    filenames = []
    while start_dt <= end_dt + delta: # Adding another day here to get the edge condition.
        filenames.append(datetime.datetime.fromtimestamp(start_dt).strftime("%Y-%m-%d")+".csv")
        start_dt += delta
    start_dt -= delta*len(filenames) #Restore original datetime

    dfs = []
    for fn in filenames:
        filepath = os.path.join(DATADIR, fn)
        try:
            dfs.append(pd.read_csv(filepath, names = ["time", "ch00", "ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"]))
        except FileNotFoundError:
            continue

    tc_df = pd.concat(dfs, ignore_index=True)
    # tc_df.rename(columns={'time': 't', f'ch{tc_channel:02g}': 'T1'}, inplace=True)

    tc_df = tc_df[['time', *[f'ch{tc:02g}' for tc in thermocouples]]]
    # Adjust time due to inaccurate system time
    # tc_df['t'] = tc_df['t'] + 639.0 + 3600*2

    # Correct measurements
    tc_df[[f'ch{tc:02g}' for tc in thermocouples]] -= [TC_CORR_CONSTS[tc] for tc in thermocouples]

    # Filter out everything not in the wanted timespan
    tc_df = tc_df.loc[(tc_df["time"] >= start_dt) & (tc_df["time"] <= end_dt)]

    # Make prettier
    tc_df.reset_index(inplace=True, drop=True)

    return tc_df

def plot(df, temp_unit="C", dateformat='%Y-%m-%d %H:%M:%S'):
    # Plot each column against the chosen column



    x_column = "time"
    df[x_column] = pd.to_datetime(df[x_column], unit='s')
    plt.figure()
    for column in df.columns:
        if column != x_column:
            match temp_unit:
                case "C":
                    df[column] -= 273.1
                case "K":
                    pass
            plt.plot(df[x_column], df[column], label=column)
    # Format the x-axis to show dates                                              
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(dateformat))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()  # Rotate date labels
    plt.title(f'channels {[col for col in df.columns[1:]]}')
    plt.xlabel("Time")
    plt.ylabel(f"Temperature, T [�{temp_unit}]")
    plt.ylim((0, 100))
    plt.legend()
    # plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = get_tc_data([0, 1, 2, 3, 4, 5, 6, 7], [datetime.datetime.timestamp(datetime.datetime.now()-datetime.timedelta(days=1)), datetime.datetime.timestamp(datetime.datetime.now())])
    plot(df, dateformat='%Y-%m-%d %H %M')