import matplotlib.pyplot as plt
import pandas as pd
import datetime

# The correction constants are most easily gotten by attaching all probes to the same thermo-joint
# together with a calibrated thermometer and looking at the differences between the measurement and the real temp
CORR_CONSTS = [2.666, 2.598, 2.409, 2.138, 3.268, 3.271, 3.077, 3.242]

fig, ax = plt.subplots()
ax.set(
    title="Temperatures in Celsius",
    ylabel = r'Temperature [$^\circ$C]',
    xlabel = 'Time',
     # ylim = (2.5,5),
    # xlim = (0, 150),
    # xticks = (np.arange(0, 150), step=20)),
    # yticks = (np.arange(3, 5, step=0.2)),
    )
fig.tight_layout()

# Insert the filenames of the data you'd like to plot
fns = [
       "2024-03-25.csv",
       "2024-03-26.csv",
       "2024-03-27.csv",
       ]

dfs = []
for fn in fns:
    dfs.append(pd.read_csv(fn, names = ["time", "ch00", "ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"]))

df = pd.concat(dfs, ignore_index=True)
df["time"] = df["time"].apply(datetime.datetime.fromtimestamp)

# Correct the probe's deviation from reference
def correct_temps(correction_coefficients, df):
    for ch in range(8):
        df[f"ch0{ch}"] -= correction_coefficients[ch]
correct_temps(CORR_CONSTS, df)

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

# Define custom start time: YYYY, MM, DD, HH, SS
start_time = nearest(df["time"], datetime.datetime(2024, 2, 14, 9, 56))

cmap = plt.get_cmap("tab10")
for ch in range(8):
    ax.plot(df["time"], df[f"ch0{ch}"]-273.15, color=cmap(ch), label = f"Channel {ch}")

plt.legend()
plt.draw()
plt.show()
