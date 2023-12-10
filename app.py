import os
import pandas as pd
import seaborn as sns
import streamlit as st
from windrose import windrose
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np


@st.cache_data
def read_file_and_detect_format(file_path):

    if file_path is not None:
        file_extension = os.path.splitext(file_upload.name)[1].lower()

        if file_extension == '.xlsx':
            uploaded_df = pd.read_excel(file_path)
            headers_list = uploaded_df.columns.tolist()
            print("File format: Excel (.xlsx)")
            return uploaded_df, headers_list
        elif file_extension == '.csv':
            uploaded_df = pd.read_csv(file_path, parse_dates=["dateandtime"])
            headers_list = uploaded_df.columns.tolist()
            print("File format: CSV (.csv)")
            return uploaded_df, headers_list
        elif file_extension == '.txt':
            uploaded_df = pd.read_csv(file_path, delimiter=' ')
            headers_list = uploaded_df.columns.tolist()
            print("File format: Text (.txt)")
            return uploaded_df, headers_list
        else:
            # Handle unsupported file formats or other actions as needed
            print("Unsupported file format")
            return None, None
    return None, None


# @st.cache_data
# def load_default_data():
    # default_df = pd.read_csv("wind_generation_data.csv")
    # return default_df.copy()


# Streamlit framework

st.title("Wind Generation Analysis Tool")

file_upload = st.sidebar.file_uploader("Upload CSV File", type=["csv", "xlsx", "txt"],
                                       help='Only supported file formats are CSV, Excel and Text')
df, header = read_file_and_detect_format(file_upload)

#  st.sidebar.write("or")

# load_default_data_button = st.button("Try out with sample data 👈🏻")

# if load_default_data_button:
    # st.session_state.df = load_default_data()
    # st.sidebar.success("Loaded default data successfully!")


# Load the data if the csv file is uploaded
if df is not None:
    st.write("A sample of your data")
    st.dataframe(df.head())

    st.write("Select the columns to match your data")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        wind_speed_column = st.selectbox("Wind Speed", (None,) + tuple(df.columns))

    with col2:
        power_output_column = st.selectbox("Power Output", (None,) + tuple(df.columns))

    with col3:
        theoretical_power_column = st.selectbox("Theoretical Power", (None,) + tuple(df.columns))

    with col4:
        wind_direction_column = st.selectbox("Wind Direction", (None,) + tuple(df.columns))

    with col5:
        date_column = st.selectbox("Date", (None,) + tuple(df.columns))

    if all(column is not None for column in [wind_speed_column, power_output_column, theoretical_power_column,
                                             wind_direction_column, date_column]):
        # Your code here

        tabs = ["Correlation Analysis", "Power Comparison", "Wind Rose", "Wasted Power", "Outlier Detection"]
        selected_tab = st.sidebar.selectbox("Select Task", tabs)
        sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

        if selected_tab == "Correlation Analysis":

            st.subheader("Correlation between Wind Speed and Power Output")
            correlation_coefficient = df[wind_speed_column].corr(df[power_output_column])

            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('#282c34')  # darker plot background
            sns.scatterplot(data=df, x=wind_speed_column, y=power_output_column, color='#32bb95', alpha=0.6)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            plt.title(f'Correlation Coefficient: {correlation_coefficient:.2f}', fontsize=16, color='white')
            plt.xlabel('Wind Speed (m/s)', fontsize=14, color='white')
            plt.ylabel('Power Output (kW)', fontsize=14, color='white')
            sns.lineplot(data=df, x=wind_speed_column, y=theoretical_power_column, color='#9332bb')  # red plotline
            st.pyplot(fig)

        # Tab 2: Power Comparison
        elif selected_tab == "Power Comparison":
            with st.spinner('Computing...'):

                st.subheader("Power Comparison between Actual and Theoretical")

                df['distance'] = np.nan

                for index, row in df.iterrows():
                    x_scatter = row[wind_speed_column]
                    y_scatter = row[power_output_column]

                    # Find the corresponding y-coordinate on the line plot (theoretical power curve)
                    x_line = df[wind_speed_column]
                    y_line = df[theoretical_power_column]

                    # Calculate the Euclidean distance
                    distance = np.sqrt((x_line - x_scatter) ** 2 + (y_line - y_scatter) ** 2)

                    # Assign the minimum distance to the 'distance' column
                    df.at[index, 'distance'] = distance.min()

                # Set a dark background style for a more modern look
                sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

                fig, ax = plt.subplots(figsize=(12, 8))
                fig.patch.set_facecolor('#282c34')
                sns.scatterplot(x=wind_speed_column, y=power_output_column, data=df,
                                label='Actual Power Output', alpha=0.5, ax=ax)
                sns.lineplot(x=wind_speed_column, y=theoretical_power_column, data=df,
                             label='Theoretical Power Curve', color='orange', ax=ax)

                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                plt.title('Comparison between Actual Power Output and Theoretical Power Curve',
                          fontsize=16, color='white')
                plt.xlabel('Wind Speed (m/s)', fontsize=14, color='white')
                plt.ylabel('Power Output (kW)', fontsize=14, color='white')
                plt.legend()
                legend = ax.legend()
                for text in legend.get_texts():
                    text.set_color("white")

                st.pyplot(fig)
            st.success('Done!')

        elif selected_tab == "Wind Rose":

            ws = df[wind_speed_column]
            wd = df[wind_direction_column]
            ws = ws.dropna().astype(float)
            top_ws_range = ws.quantile(0.9)
            fig, ax = plt.subplots(figsize=(4, 2), subplot_kw=dict(projection="windrose"))

            fig.patch.set_facecolor('#282c34')
            # Plot the wind rose
            ax.contourf(wd, ws, bins=np.arange(0, top_ws_range, 2), cmap=cm.viridis)

            # Customize legend
            legend = ax.legend(title='wind speed m/s', fontsize='xx-small', loc='upper right',
                               bbox_to_anchor=(1.5, 0.3, 0.5, 0.5), borderaxespad=-0.1, labelcolor='white')
            legend.get_title().set_color("white")  # Set title color

            # Set labels and ticks color to white
            ax.set_yticklabels([''] * len(ax.get_yticklabels()), color='white', fontsize='x-large')
            ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], color='white', fontsize='x-large')

            # Set titles color to white
            ax.set_title("Wind Rose Plot", color='white', fontsize='xx-small')

            # Display the plot with a dark background using st.pyplot()
            st.pyplot(fig)

        elif selected_tab == "Wasted Power":

            df2 = df.set_index(pd.DatetimeIndex(df[date_column])).drop(date_column, axis=1)
            df_resampled = df2.resample('M').mean()  # Add formula details to transform to kWh

            fig, ax = plt.subplots(figsize=(12, 8))  # Use dark background
            fig.patch.set_facecolor('#282c34')  # dark countour!

            # Bar chart for theoretical power with transparency
            sns.barplot(x=df_resampled.index,
                        y=df_resampled[theoretical_power_column], data=df_resampled,
                        color='#ffff11', label='Theoretical Power', alpha=1)
            sns.barplot(x=df_resampled.index, y=df_resampled[power_output_column], data=df_resampled,
                        color='#3ae3b4', label='Active Power', alpha=0.9)

            # Formatting
            plt.title('Comparison of Active Power and Theoretical Power', color='white',
                      size=16)  # Set title color and size

            plt.ylabel('Power (kW)', color='white', size=16)  # Set y-axis label color and size
            plt.xticks(rotation=45, color='white', size=14)  # Set x-axis tick color and size
            plt.yticks(color='white', size=15)  # Set y-axis tick color and size
            plt.legend(fontsize=12, labelcolor='white')  # Set legend font size
            plt.tight_layout()

            plt.grid(False)  # Turn off grid lines
            total_wasted_power = df_resampled[theoretical_power_column].sum() - df_resampled[power_output_column].sum()
            st.write("Total Wasted Power is:", total_wasted_power)

            # Show the plot
            st.pyplot(fig)

        elif selected_tab == "Outlier Detection":

            fig, ax = plt.subplots(figsize=(12, 8))  # Use dark background
            fig.patch.set_facecolor('#282c34')  # dark countour!

            # Define a color palette for better distinction
            palette = "Set3"
            print(header)

            for i, each in enumerate(header[1:], 1):
                plt.subplot(1, 4, i)
                sns.boxplot(data=df, y=each, palette=palette)

                # Customize the plot
                plt.title(each, fontsize=14)
                plt.xlabel('')
                plt.ylabel(each.replace('_', ' ').title(), fontsize=12, color='white')
                plt.xticks(fontsize=10, color='white')
                plt.yticks(fontsize=10, color='white')

            # Adjust layout
            st.pyplot(fig)

    else:
        st.write("Please, match your data to the columns")

    # Tab 1: Correlation Analysis

else:
    st.warning("Upload your data...")
    print(df)








