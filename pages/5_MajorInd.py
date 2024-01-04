import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from st_pages import Page, Section, show_pages, add_page_title, add_indentation
add_indentation()

# Load data
file_path = "NRB_Data.xlsx"
sheet_name = "MajorIndicators"
df = pd.read_excel(file_path, sheet_name=sheet_name)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

latest_date = df.index.max()
default_year = latest_date.year
default_month = latest_date.strftime("%B")

# Display headers with the latest date
st.header('Major Indicators for Commercial Banks')
st.subheader(f'As of {latest_date.strftime("%B %Y")}')

# Create an expander for Year and Month selection
with st.expander("Select Year and Month for specific month data"):
    # Year and Month selection side by side
    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox('Select Year:', df.index.year.unique(), index=df.index.year.unique().tolist().index(default_year))

    with col2:
        selected_month = st.selectbox('Select Month:', df.index.month_name().unique(), index=df.index.month_name().unique().tolist().index(default_month))

# Filter the DataFrame based on user selection
selected_df = df[(df.index.year == selected_year) & (df.index.month_name() == selected_month)]


# Specify the metrics you want to include in the dashboard
selected_metrics = [
    'Total Deposit/GDP', 'Total Credit/GDP', 'Total Credit/ Total Deposit',
    'CD Ratio', 'Fixed Deposit/Total Deposit', 'Saving Deposit/Total Deposit',
    'Current Deposit/Total Deposit', 'Call Deposit/Total Deposit',
    'NPL/ Total Loan', 'Total LLP /Total Loan', 'Deprived Sector Loan/Total Loan',
    'Cash & Bank Balance/Total Deposit', 'Investment in GovSecurities/Total Deposit',
    'Total Liquid Assets/Total Deposit', 'Core Capital/RWA', 'Total Capital/RWA'
]

# Set the page to 2 rows and 8 columns
num_rows = 2
num_cols = 8

# Organize metrics in a 2x8 grid
columns = st.columns(num_cols)

for i, metric in enumerate(selected_metrics):
    col = i % num_cols

    # Create a metric section
    with columns[col]:
        latest_metric_value = selected_df[metric].iloc[-1]

        # Check if there are enough data points to calculate delta
        if len(selected_df) > 1:
            delta_value = latest_metric_value - selected_df[metric].iloc[-2]
            delta_value_formatted = round(delta_value, 2)
        else:
            delta_value_formatted = None

        # Format metric and delta with two digits rounded off and a '%'
        metric_formatted = f"{round(latest_metric_value, 2):,.2f}%"
        delta_formatted = f"{delta_value_formatted:,.2f}%" if delta_value_formatted is not None else None

        st.metric(label=metric, value=metric_formatted, delta=delta_formatted)
