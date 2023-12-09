from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd


# Assuming you have the necessary data loaded into a DataFrame called 'df'
# You can replace this with your actual data loading logic

df = pd.read_csv("wind_generation_data.csv")
header = df.columns.tolist()
print(header)
ws = df[header[2]]
wd = df[header[4]]

print("wind speeds:", ws)
print("Wind directions", wd)

column_data = ws.dropna().astype(float)
top_ws_range = ws.quantile(0.9)
plt.figure(figsize=(8, 2))

ax = WindroseAxes.from_ax()
ax.set_facecolor("grey")  # Set dark background color

ax.contourf(wd, ws, bins=np.arange(0, top_ws_range, 2), cmap=cm.viridis)

legend = ax.legend(title='Legend', fontsize='xx-large')
legend.get_title().set_color("white")  # Set title color

# Set labels and ticks color to white
ax.set_yticklabels([''] * len(ax.get_yticklabels()), color='white', fontsize='x-large')
ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], color='white', fontsize='x-large')

# Display the plot
plt.show()