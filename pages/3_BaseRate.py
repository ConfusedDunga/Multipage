import streamlit as st
import pandas as pd
import plotly.express as px
from st_pages import Page, Section, show_pages, add_page_title
add_page_title()

def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

def calculate_metrics(data):
    latest_month_index = data['Fiscal Year'].idxmax()
    latest_inflation = data.loc[latest_month_index, 'Base Rate']

    previous_month_index = latest_month_index - 1
    previous_month_inflation = data.loc[previous_month_index, 'Base Rate']

    previous_year_same_month_index = latest_month_index - 12
    previous_year_same_month_inflation = data.loc[previous_year_same_month_index, 'Base Rate']

    return latest_inflation, previous_month_inflation, previous_year_same_month_inflation

def display_metrics(latest_inflation, previous_month_inflation, previous_year_same_month_inflation, latest_month):
    col1, col2, col3 = st.columns(3)
    col1.metric(f"{latest_month} Base Rate", f"{latest_inflation*100:.2f}%", help=f"Latest available {latest_month}'s base rate")
    col2.metric("Change from Previous Month", f"{(latest_inflation - previous_month_inflation) * 100:.2f}%", help="Change from the previous month")
    col3.metric("Change from Previous Year (Same Month)", f"{(latest_inflation - previous_year_same_month_inflation) * 100:.2f}%", help="Change from the previous year, same month")

def main():
    # Load data
    file_path = "NRB_Data.xlsx"
    sheet_name = "BaseRate"
    df = load_data(file_path, sheet_name)

    # Calculate metrics
    latest_inflation, previous_month_inflation, previous_year_same_month_inflation = calculate_metrics(df)

    # Get the latest month name
    latest_month = df['Fiscal Year'].dt.month_name().iloc[-1]
   
    # Title and Subtitle
    st.title("Base Rate of Commercial Banks")
    st.markdown("<h3 style='color: #7c7c7c;'>Choose the starting and time period from the sidebar</h3>", unsafe_allow_html=True)

    # Display metrics
    display_metrics(latest_inflation, previous_month_inflation, previous_year_same_month_inflation, latest_month)

    # Sidebar for selecting date range
    start_date = st.sidebar.date_input("Select start date", df['Fiscal Year'].min())
    end_date = st.sidebar.date_input("Select end date", df['Fiscal Year'].max())

    # Convert start and end dates to pandas datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on the selected date range
    filtered_df = df[(df['Fiscal Year'] >= start_date) & (df['Fiscal Year'] <= end_date)]

    #Line Chart
    fig = px.line(filtered_df, x='Fiscal Year', y='Base Rate', title=f'Base Rate from {start_date.strftime("%B %Y")} to {end_date.strftime("%B %Y")}', markers=True)
    fig.update_yaxes(tickformat=".0%")  # Display percentages without decimals
    st.plotly_chart(fig, use_container_width=True)

    # Display formatted filtered data table
    st.write("Formatted Filtered Data Table:")
    st.dataframe(filtered_df.style.format({'Fiscal Year': '{:%b-%Y}', 'Base Rate': '{:.2%}'}), use_container_width=True)

if __name__ == "__main__":
    main()
