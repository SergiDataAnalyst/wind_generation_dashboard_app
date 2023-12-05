import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

file_path = 'wind_generation_data.csv'
df = pd.read_csv(file_path)
header = df.columns.tolist()

wind_speed_column = header[2]
power_output_column = header[1]

correlation_coefficient = df[wind_speed_column].corr(df[power_output_column])

sns.set_palette("viridis")

sns.set_style("darkgrid")

plt.figure(figsize=(12, 8))
sns.regplot(x=wind_speed_column, y=power_output_column, data=df, scatter_kws={'alpha': 0.5, 'color': '#35B778'})
plt.title(f'Correlation between Wind Speed and Power Output\nCorrelation Coefficient: {correlation_coefficient:.2f}', fontsize=16)
plt.xlabel('Wind Speed (m/s)', fontsize=14)
plt.ylabel('Power Output (kW)', fontsize=14)

# Display the plot
plt.show()

