import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mysql.connector import Error


# Load data from CSV


def process_uploaded_file(file_upload):
    if file_upload is not None:
        df = pd.read_csv(file_upload)
        header = df.columns.tolist()
        wind_speed_column = header[2]
        power_output_column = header[1]
        theoretical_power_column = header[3]
        return df, wind_speed_column, power_output_column, theoretical_power_column
    else:
        print("Please upload a CSV file.")


# Set the page title
st.title("Wind Generation Analysis App")


# Create tabs
tabs = ["Correlation Analysis", "Power Comparison", "Wind Rose"]
selected_tab = st.sidebar.selectbox("Select Task", tabs)

file_upload = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# Load the data if the file is uploaded
if file_upload is not None:
    df = pd.read_csv(file_upload)
    header = df.columns.tolist()
    wind_speed_column = header[2]
    power_output_column = header[1]
    theoretical_power_column = header[3]
else:
    st.warning("Please upload a CSV file")

# Task 1: Correlation Analysis
if selected_tab == "Correlation Analysis":
    # Calculate correlation coefficient
    correlation_coefficient = df[wind_speed_column].corr(df[power_output_column])

    # Set a beautiful color palette
    sns.set_palette("viridis")

    # Set a dark background style for a more modern look
    sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

    # Plot correlation between wind speed and power output
    st.subheader("Correlation between Wind Speed and Power Output")
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#282c34')
    sns.regplot(x=wind_speed_column, y=power_output_column, data=df, scatter_kws={'alpha': 0.5, 'color': '#35B778'}, ax=ax)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title(f'Correlation Coefficient: {correlation_coefficient:.2f}', fontsize=16, color='white')
    plt.xlabel('Wind Speed (m/s)', fontsize=14, color='white')
    plt.ylabel('Power Output (kW)', fontsize=14, color='white')
    st.pyplot(fig)

# Task 2: Power Comparison
elif selected_tab == "Power Comparison":
    # Extract relevant columns
    wind_speed_column = header[2]
    actual_power_column = header[1]
    theoretical_power_column = header[3]

    # Set a beautiful color palette
    sns.set_palette("viridis")

    # Set a dark background style for a more modern look
    sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

    # Plot power comparison between actual and theoretical
    st.subheader("Power Comparison between Actual and Theoretical")
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#282c34')
    sns.scatterplot(x=wind_speed_column, y=actual_power_column, data=df, label='Actual Power Output', alpha=0.5, ax=ax)
    sns.lineplot(x=wind_speed_column, y=theoretical_power_column, data=df, label='Theoretical Power Curve', color='orange', ax=ax)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title('Comparison between Actual Power Output and Theoretical Power Curve', fontsize=16, color='white')
    plt.xlabel('Wind Speed (m/s)', fontsize=14, color='white')
    plt.ylabel('Power Output (kW)', fontsize=14, color='white')
    plt.legend()
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color("white")

    st.pyplot(fig)