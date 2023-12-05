from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Assuming you have the necessary data loaded into a DataFrame called 'df'
# You can replace this with your actual data loading logic


ws = np.random.random(500) * 6
wd = np.random.random(500) * 360

# Example data loading (replace this with your actual data loading logic)
ax = WindroseAxes.from_ax()
ax.set_facecolor("black")  # Set dark background color

ax.contourf(wd, ws, bins=np.arange(0, 8, 1), cmap=cm.YlOrBr)

legend = ax.legend(title='Legend', fontsize='xx-large')
legend.get_title().set_color("white")  # Set title color

# Set labels and ticks color to white
ax.set_yticklabels([''] * len(ax.get_yticklabels()), color='white', fontsize='x-large')
ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], color='white', fontsize='x-large')

# Display the plot
plt.show()
