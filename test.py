import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt



# Assuming you have the necessary data loaded into a DataFrame called 'df'
# You can replace this with your actual data loading logic

# Example data loading (replace this with your actual data loading logic)
df = pd.read_csv('wind_generation_data.csv')

headers = df.columns.tolist()

# Convert 'Date_Time' column to datetime type
df['Date_Time'] = pd.to_datetime(df['Dateandtime'], format='%d %m %Y %H:%M')

# Extract the season from the 'Date_Time' column
df['Season'] = df['Date_Time'].dt.month % 12 // 3 + 1

# Map season numbers to season names
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
df['Season'] = df['Season'].map(season_mapping)

# Group by season and calculate the average power generation
average_power_by_season = df.groupby('Season')['LV_ActivePower_kW'].mean().reset_index()

# Set the color palette
sns.set_palette("viridis")

# Set a dark background style for a modern look
sns.set_style("darkgrid")

# Create a bar plot to depict seasonal variations
st.subheader("Seasonal Variations in Power Generation")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Season', y='LV_ActivePower_kW', data=average_power_by_season, ax=ax)
plt.title("Average Power Generation by Season")
plt.xlabel("Season")
plt.ylabel("Average Power Generation (kW)")
st.pyplot(fig)
