import matplotlib.pyplot as plt
import pandas as pd
import datetime

# The correction constants are most easily gotten by attaching all probes to the same thermo-joint
# together with a calibrated thermometer and looking at the differences between the measurement and the real temp
CORR_CONSTS = [0]*8 #[2.666, 2.598, 2.409, 2.138, 3.268, 3.271, 3.077, 3.242]

fig, ax = plt.subplots()
ax.set(
    title="Oven temperature",
    ylabel = r'Temperature [$^\circ$C]',
    xlabel = 'Time',
     # ylim = (2.5,5),
    # xlim = (0, 150),
    # xticks = (np.arange(0, 150), step=20)),
    # yticks = (np.arange(3, 5, step=0.2)),
    )
ax.tick_params(
    axis='both',      # apply to both x and y axis
    direction='in',   # ticks pointing inwards
    top=True,         # show ticks on top
    right=True        # show ticks on right
)
fig.tight_layout()

# Insert the filenames of the data you'd like to plot
fns = [
       "2025-04-26.csv",
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
# df = df[(df["time"]>datetime.datetime(2025, 4, 26, 9, 40)) & (df["time"]<datetime.datetime(2025, 4, 26, 12, 18))]
df = df[(df["time"]>datetime.datetime(2025, 4, 26, 12, 19))] # From start of 100C temp
df = df[(df["time"]>datetime.datetime(2025, 4, 26, 15, 20))] # From start of filament in oven

cmap = plt.get_cmap("tab10")
# for ch in range(1):
    # ax.plot(df["time"], df[f"ch0{ch}"]-273.15, color=cmap(ch), label = f"Channel {ch}")
# ax.axhline(70, linestyle="dashdot", color="gray", label=r"70$^\circ$C")
# ax.axhline(50, linestyle="dashed", color="gray", label=r"50$^\circ$C")
ax.plot(df["time"], df[f"ch00"]-273.15, label="Oven temperature")

ax.annotate(
    r'Setpoint at 100$^\circ$C',                    # No text
    xy=(datetime.datetime(2025, 4, 26, 13, 6), 76),
    xytext=(datetime.datetime(2025, 4, 26, 13, 26), 76),      # Start point
    arrowprops=dict(
        arrowstyle='->',   # Double-headed arrow
        color='black',
        lw=2               # Line width
    )
)
ax.annotate(
    r'Setpoint at 150$^\circ$C',                    # No text
    xy=(datetime.datetime(2025, 4, 26, 13, 44), 110),
    xytext=(datetime.datetime(2025, 4, 26, 14, 4), 110),      # Start point
    arrowprops=dict(
        arrowstyle='->',   # Double-headed arrow
        color='black',
        lw=2               # Line width
    )
)
ax.annotate(
    r'Setpoint at 200$^\circ$C',                    # No text
    xy=(datetime.datetime(2025, 4, 26, 13, 42), 143),
    xytext=(datetime.datetime(2025, 4, 26, 12, 52), 143),      # Start point
    arrowprops=dict(
        arrowstyle='->',   # Double-headed arrow
        color='black',
        lw=2               # Line width
    )
)
ax.annotate(
    r'Setpoint at 250$^\circ$C',                    # No text
    xy=(datetime.datetime(2025, 4, 26, 14, 13), 177),
    xytext=(datetime.datetime(2025, 4, 26, 13, 23), 177),      # Start point
    arrowprops=dict(
        arrowstyle='->',   # Double-headed arrow
        color='black',
        lw=2               # Line width
    )
)

plt.legend()
plt.draw()
# plt.savefig("oventemp_graph_100_150_200_250.png", dpi=600)
plt.show()
