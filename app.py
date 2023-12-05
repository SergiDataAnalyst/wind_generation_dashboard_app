import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mysql.connector import Error
import mysql.connector
from windrose import WindroseAxes
import matplotlib.cm as cm
import numpy as np

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


def create_mysql_table(connection, table_name, df):
    try:
        cursor = connection.cursor()

        # Drop the table if it exists
        cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

        # Create the table
        cursor.execute("CREATE TABLE {} ({})".format(table_name, ', '.join(['{} TEXT'.format(col) for col in df.columns])))

        # Insert data into the table
        for _, row in df.iterrows():
            cursor.execute("INSERT INTO {} VALUES ({})".format(table_name, ', '.join(['"{}"'.format(val) for val in row])))

        # Commit the changes
        connection.commit()

        st.success("Table {} created successfully.".format(table_name))
    except Error as e:
        st.error("Error: {}".format(e))


# MySQL connection parameters
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "wegindieschweiz"
mysql_port = '3306'
mysql_database = "wind_database"


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

elif selected_tab == "Wind Rose":
    st.subheader("Impact of Wind Direction on Power Output")
    st.text(f"Investigate how variations in wind direction affect power generation. "
            f"Certain wind directions may be more favorable or challenging for power production.")

    ws = np.random.random(500) * 6
    wd = np.random.random(500) * 360

    # Create a WindroseAxes plot with a dark background
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#282c34')
    ax.set_facecolor("black")  # Set dark background color

    # Create a 2D histogram
    H, xedges, yedges = np.histogram2d(wd, ws, bins=(np.arange(0, 361, 10), np.arange(0, 8, 1)))

    # Plot the wind rose using contourf with a different color palette (YlOrBr)
    ax.contourf(xedges[:-1], yedges[:-1], H.T, cmap=cm.YlOrBr)

    # Set legend with white color
    legend = ax.legend(title='Legend', fontsize='xx-large')
    legend.get_title().set_color("white")  # Set title color

    # Set labels and ticks color to white
    ax.set_yticklabels([''] * len(ax.get_yticklabels()), color='white', fontsize='x-large')
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], color='white', fontsize='x-large')

    # Display the plot in Streamlit
    st.pyplot(fig)






# Optionally, display the DataFrame
if st.checkbox("Show DataFrame"):
    st.subheader("Wind Generation Data")
    st.dataframe(df)

# Button to connect to MySQL and create a table
if st.sidebar.button("Connect to SQL"):
    try:
        # Create a MySQL connection
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            port=mysql_port,
            database=mysql_database
        )
        if connection.is_connected():
            st.success(f"Connected to MySQL Server: {mysql_host}")

            # Load CSV data
            uploaded_df, _, _, _ = process_uploaded_file(file_upload)

            # Create a MySQL table
            create_mysql_table(connection, "your_table_name", uploaded_df)

        # Close the MySQL connection
        if connection.is_connected():
            connection.close()
            st.success("MySQL connection closed.")
    except Error as e:
        st.error(f"Error: {e}")




