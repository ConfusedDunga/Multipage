import streamlit as st
import pandas as pd
import plotly.express as px
from st_pages import Page, Section, show_pages, add_page_title
add_page_title()
# Title and Subtitle
st.title("Inflation Rate of Nepal")
st.markdown("<h3 style='color: #7c7c7c;'>Choose multiple years for line chart in sidebar</h3>", unsafe_allow_html=True)
# Specify the path to the Excel file
excel_file_path = 'NRB_data.xlsx'

# Read the Excel file into a Pandas DataFrame
excel_data = pd.ExcelFile(excel_file_path)
# Read the 'Inflation' sheet into a DataFrame
df = pd.read_excel(excel_data, sheet_name='Inflation')
print(df)
# Get the current year
current_year = pd.to_datetime('now').year

# Filter data based on selected years
available_years = df['Date'].dt.year.unique()
selected_years = st.sidebar.multiselect("Select Years", available_years, default=[current_year] if current_year in available_years else [])


# Get the latest inflation rate and previous month's inflation rate
latest_inflation = df.loc[df['Date'].idxmax(), 'Inflation']
previous_month_date = df['Date'].max() - pd.DateOffset(months=1)
previous_month_inflation = df.loc[df['Date'] == previous_month_date, 'Inflation'].squeeze()
# Get the change from the previous year, same month
previous_year_date = df['Date'].max() - pd.DateOffset(years=1)
previous_year_same_month_inflation = df.loc[df['Date'] == previous_year_date, 'Inflation'].squeeze()

# Get the latest available month from the DataFrame
latest_month = df['Date'].max().strftime('%B %Y')  # Format: Month Year

# Display the gauge chart with the latest inflation rate and change from the previous month
col1, col2, col3 = st.columns(3)
# Display the three metrics: Latest Inflation Rate, Change from Previous Month, Change from Previous Year
col1.metric(f"{latest_month} Base Rate", f"{latest_inflation:.2f}%", help=f"Latest available {latest_month}'s base rate")
col2.metric("Change from Previous Month", f"{latest_inflation - previous_month_inflation:.2f}%", help="Change from the previous month")
col3.metric("Change from Previous Year (Same Month)", f"{latest_inflation - previous_year_same_month_inflation:.2f}%", help="Change from the previous year, same month")

# Create separate 'Year' and 'Month' columns
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()

# Create a line chart for the selected years using Plotly Express
fig = px.line(
    df[df['Date'].dt.year.isin(selected_years)],
    x='Month',
    y='Inflation',
    color='Year',
    labels={'Inflation': 'Inflation (%)'},
    title='Inflation Data Analysis',
    line_shape='spline',
    markers=True,
)

# Configure chart properties
fig.update_xaxes(title_text='Month')
fig.update_yaxes(title_text='Inflation (%)')

# Display the Plotly chart with automatic container width
st.plotly_chart(fig, use_container_width=True)

# Create a pivot table with months as columns and years as rows
pivot_table = pd.pivot_table(
    df, 
    values='Inflation', 
    index=df['Date'].dt.year, 
    columns=df['Date'].dt.month_name(), 
    aggfunc='mean'
)

# Rename the columns to use three-letter month abbreviations
pivot_table.columns = pd.to_datetime(pivot_table.columns, format='%B').strftime('%b')

# Sort the columns in chronological order
sorted_columns = pd.to_datetime(pivot_table.columns, format='%b').sort_values().strftime('%b')
pivot_table = pivot_table[sorted_columns]

# Format the values as percentages and add % sign
pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%" if not pd.isna(x) else '-')

# Format the index (year) without commas
pivot_table.index = pivot_table.index.map(lambda x: f"{x:,.0f}")

# Display the modified pivot table
st.write(pivot_table)
