import pandas as pd
import seaborn as sns
import streamlit as st
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np


#  Uploads csv_file and works with it as a df, returns the df and some of the header columns
def process_uploaded_file(csv_file):
    if csv_file is not None:
        uploaded_df = pd.read_csv(csv_file)
        headers_list = uploaded_df.columns.tolist()

        return uploaded_df, headers_list

    else:
        return None, None


# Streamlit framework
# Page title
st.title("Wind Generation Analysis Tool")
# Tabs
# File uploaded
file_upload = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
df, header = process_uploaded_file(file_upload)


# Load the data if the csv file is uploaded
if df is not None:
    st.write("A sample of your data")
    st.dataframe(df.head())

    st.write("Select the columns to match your data")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        wind_speed_column = st.selectbox("Wind Speed", (None,) + tuple(df.columns))

    with col2:
        power_output_column = st.selectbox("Power Output", (None,) + tuple(df.columns))

    with col3:
        theoretical_power_column = st.selectbox("Theoretical Power Curve", (None,) + tuple(df.columns))

    with col4:
        wind_direction_column = st.selectbox("Wind Direction", (None,) + tuple(df.columns))

    if wind_speed_column and power_output_column and theoretical_power_column and wind_direction_column is not None:

        tabs = ["Correlation Analysis", "Power Comparison", "Wind Rose"]
        selected_tab = st.sidebar.selectbox("Select Task", tabs)

        if selected_tab == "Correlation Analysis":
            bar = st.progress(50)
            bar.progress(100)
            st.subheader("Correlation between Wind Speed and Power Output")
            correlation_coefficient = df[wind_speed_column].corr(df[power_output_column])
            sns.set_palette("viridis")
            sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('#282c34')
            sns.regplot(x=wind_speed_column, y=power_output_column,
                        data=df, scatter_kws={'alpha': 0.5, 'color': '#35B778'}, ax=ax)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            plt.title(f'Correlation Coefficient: {correlation_coefficient:.2f}', fontsize=16, color='white')
            plt.xlabel('Wind Speed (m/s)', fontsize=14, color='white')
            plt.ylabel('Power Output (kW)', fontsize=14, color='white')
            st.pyplot(fig)

        # Tab 2: Power Comparison
        elif selected_tab == "Power Comparison":
            with st.spinner('Computing...'):

                # Set a beautiful color palette
                sns.set_palette("viridis")

                # Set a dark background style for a more modern look
                sns.set_style("darkgrid", {"axes.facecolor": "#282c34"})

                # Plot power comparison between actual and theoretical
                st.subheader("Power Comparison between Actual and Theoretical")
                fig, ax = plt.subplots(figsize=(12, 8))
                fig.patch.set_facecolor('#282c34')
                sns.scatterplot(x=wind_speed_column, y=power_output_column, data=df, label='Actual Power Output', alpha=0.5,
                                ax=ax)
                sns.lineplot(x=wind_speed_column, y=theoretical_power_column, data=df,
                             label='Theoretical Power Curve', color='orange', ax=ax)

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
            st.success('Done!')

        elif selected_tab == "Wind Rose":

            df = pd.read_csv("wind_generation_data.csv")
            header = df.columns.tolist()
            print(header)
            ws = df[header[2]]
            wd = df[header[4]]

            column_data = ws.dropna().astype(float)
            top_ws_range = ws.quantile(0.9)
            fig, ax = plt.subplots(figsize=(4, 2), subplot_kw=dict(projection="windrose"))

            fig.patch.set_facecolor('#282c34')
            # Plot the wind rose
            ax.contourf(wd, ws, bins=np.arange(0, top_ws_range, 2), cmap=cm.viridis)

            # Customize legend
            legend = ax.legend(title='Legend', fontsize='xx-small', loc='upper right',
                               bbox_to_anchor=(1.5, 0.3, 0.5, 0.5), borderaxespad=-0.1, labelcolor='white')
            legend.get_title().set_color("white")  # Set title color

            # Set labels and ticks color to white
            ax.set_yticklabels([''] * len(ax.get_yticklabels()), color='white', fontsize='x-large')
            ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], color='white', fontsize='x-large')

            # Set titles color to white
            ax.set_title("Wind Rose Plot", color='white', fontsize='xx-small')

            # Display the plot with a dark background using st.pyplot()
            st.pyplot(fig)

    else:
        st.write("Please, match your data to the columns")

    # Tab 1: Correlation Analysis

else:
    st.warning("Please upload a CSV file")
