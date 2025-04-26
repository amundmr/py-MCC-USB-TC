import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

fig, ax = plt.subplots()
ax.set(
    title="Gorenje BOP7556AX Temperature vs setpoint with heating period",
    ylabel = r'Measured Temperature [$^\circ$C]',
    xlabel = r'Setpoint Temperature [$^\circ$C]',
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


data = np.array([
    [50, 38, 55, 60],
    [70, 52, 60, 25],
    [100, 71, 80, 14],
    [150, 106, 115, 9],
    [200, 138, 147, 7],
    [250, 171, 182, 6],
])
ax.fill_between(data.T[0], data.T[1], data.T[2], label="Temperature range", alpha=0.5)

ax2 = ax.twinx()
ax2.scatter(data.T[0], data.T[3], color="tab:orange", label="Heating period")
ax2.set_ylabel("Period [minutes]")


# Get handles and labels from both axes
handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Combine them
handles = handles1 + handles2
labels = labels1 + labels2

# Then make the legend
ax.legend(handles, labels, loc='upper center')  # You can change loc if you want

plt.draw()
plt.savefig("analysis_all_temps.png", dpi=600, bbox_inches="tight")
plt.show()
