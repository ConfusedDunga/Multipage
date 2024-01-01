import streamlit as st
import pandas as pd

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

# Display the page title
st.title("Interest Rates Analysis")

# Use Streamlit columns to display the metrics and their changes
col1, col2, col3, col4, col5 = st.columns(5)

# Display metrics for Weighted Average Interest Rate on Deposit
col1.metric("Deposit Rate", f"{last_data['WAIRD']:.2f}%", delta=f"{delta_data['WAIRD']:.2f}%")

# Display metrics for Saving Deposit
col2.metric("Saving Deposit", f"{last_data['Saving Deposit']:.2f}%", delta=f"{delta_data['Saving Deposit']:.2f}%")

# Display metrics for Fixed Deposit
col3.metric("Fixed Deposit", f"{last_data['Fixed Deposit']:.2f}%", delta=f"{delta_data['Fixed Deposit']:.2f}%")

# Display metrics for Call Deposit
col4.metric("Call Deposit", f"{last_data['Call Deposit']:.2f}%", delta=f"{delta_data['Call Deposit']:.2f}%")

# Display metrics for Weighted Average Interest Rate on Credit
col5.metric("Credit Rate", f"{last_data['WAIRC']:.2f}%", delta=f"{delta_data['WAIRC']:.2f}%")
