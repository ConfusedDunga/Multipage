import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
from pyBSDate import convert_BS_to_AD
from st_pages import Page, Section, show_pages, add_page_title, add_indentation
add_indentation()

# Assuming df is your DataFrame containing the interest rates data
# Make sure your DataFrame is loaded with the data before using this code
def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Load data
file_path = "NRB_Data.xlsx"
sheet_name = "Interest"
df = load_data(file_path, sheet_name)

# Get the last available data
last_data = df.iloc[-1]

# Get the previous month's data
previous_month_data = df.iloc[-2]

# Calculate the change from the previous month
delta_data = last_data - previous_month_data

# Determine the title based on the last available data date
title_month_year = last_data['Date'].strftime('%B %Y')

st.title("Interest Rates of Commercial Banks")
# Display the page title with the month and year of the last available data
st.subheader(f"Interest Rates as of {title_month_year}")

st.markdown(
    """
    <i><b>Note:</b><br>
    <b>WAIRD:</b> Weighted Average Interest Rate on Deposit <br>
    <b>WAIRC:</b> Weighted Average Interest Rate on Credit</i>
    """,
    unsafe_allow_html=True
)

#Metrics Section 
col1, col2, col3, col4, col5 = st.columns(5)

# Display metrics for Weighted Average Interest Rate on Deposit
col1.metric("WAIRD", f"{last_data['WAIRD']:.2f}%", delta=f"{delta_data['WAIRD']:.2f}%")

# Display metrics for Saving Deposit
col2.metric("Saving Deposit", f"{last_data['Saving Deposit']:.2f}%", delta=f"{delta_data['Saving Deposit']:.2f}%")

# Display metrics for Fixed Deposit
col3.metric("Fixed Deposit", f"{last_data['Fixed Deposit']:.2f}%", delta=f"{delta_data['Fixed Deposit']:.2f}%")

# Display metrics for Call Deposit
col4.metric("Call Deposit", f"{last_data['Call Deposit']:.2f}%", delta=f"{delta_data['Call Deposit']:.2f}%")

# Display metrics for Weighted Average Interest Rate on Credit
col5.metric("WAIRC", f"{last_data['WAIRC']:.2f}%", delta=f"{delta_data['WAIRC']:.2f}%")

#Charts and other section

#Fiscal Year Wise

def convert_to_english_year_month(nepali_fy):
    # Assuming Nepali fiscal years start from Saun and end in Asar
    start_month = 4
    end_month = 3

    # Extract Nepali fiscal year components
    beg_year, beg_month, _ = convert_BS_to_AD(int(nepali_fy.split('/')[0]), start_month, 1)
    end_year, end_month, _ = convert_BS_to_AD(int(nepali_fy.split('/')[1]), end_month, 1)

    # Return the English year and month
    return beg_year, beg_month, end_year, end_month

def read_data(file_path, sheet_name):
    # Read a specific sheet from an Excel workbook into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

    # Convert the date column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # 'coerce' will handle invalid dates by setting them to NaT

    return df

def filter_data_by_fiscal_year(df, nepali_fy):
    # Convert to English year and month
    start_year, start_month, end_year, end_month = convert_to_english_year_month(nepali_fy)

    # Filter the data for the specified fiscal year
    start_date = pd.to_datetime(f'{start_year}-{start_month:02d}-01')
    end_date = pd.to_datetime(f'{end_year}-{end_month:02d}-1')

    filtered_data = df[
        (df['Date'] >= start_date) &  # Filter by start date
        (df['Date'] <= end_date)  # Filter by end date
    ]

    return filtered_data

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# ... (your existing code)

# Default columns to display
default_columns = ['WAIRD', 'WAIRC', 'Fixed Deposit']

# Create a sidebar with options for the user to choose
chart_option = st.selectbox("Choose Chart Type", ["Date Range", "Nepali Fiscal Year"])

if chart_option == "Date Range":
    # Use calendar inputs for date range in two separate columns
    start_date, end_date = st.columns(2)
    start_date = start_date.date_input("Select Start Date", min_value=df['Date'].min().date(), max_value=df['Date'].max().date(), value=df['Date'].min().date())
    end_date = end_date.date_input("Select End Date", min_value=df['Date'].min().date(), max_value=df['Date'].max().date(), value=df['Date'].max().date())

    # Filter data based on the user-selected date range
    filtered_data = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

elif chart_option == "Nepali Fiscal Year":
    # Dropdown for Nepali fiscal years
    nepali_fy_options = [
        "2065/2066", "2066/2067", "2067/2068", "2068/2069", "2069/2070",
        "2070/2071", "2071/2072", "2072/2073", "2073/2074", "2074/2075",
        "2075/2076", "2076/2077", "2077/2078", "2078/2079", "2079/2080",
        "2080/2081", "2081/2082", "2082/2083"
    ]
    # Set default selected Nepali fiscal year to "2079/2080"
    selected_nepali_fy = st.selectbox("Select Nepali Fiscal Year", nepali_fy_options, index=nepali_fy_options.index("2079/2080"))

    # Filter data based on the selected Nepali fiscal year
    filtered_data = filter_data_by_fiscal_year(df, selected_nepali_fy)

# Column to choose selected columns
selected_columns = st.multiselect("Select Columns", df.columns[1:], default=default_columns)

# Use Plotly Express to create an interactive line chart
fig = px.line(filtered_data, x='Date', y=selected_columns,
              labels={'value': 'Interest Rate', 'Date': 'Date'},
              title=f'Interest Rates Over Time - {selected_nepali_fy if chart_option == "Nepali Fiscal Year" else "Date Range"}')

# Customize the chart
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Interest Rate',
    legend_title='Interest Types'
)

# Display the chart with full container width
st.plotly_chart(fig, use_container_width=True)

# ... (continue with the rest of your code)

st.subheader("Filtered Data Table")
filtered_data_display = filtered_data.copy()
filtered_data_display['Date'] = filtered_data['Date'].dt.strftime('%b-%Y')
st.dataframe(filtered_data_display)