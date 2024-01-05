import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load data
file_path = "NRB_Data.xlsx"
sheet_name = "MajorIndicators"
df = pd.read_excel(file_path, sheet_name=sheet_name)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

latest_date = df.index.max()
default_year = latest_date.year
default_month = latest_date.strftime("%B")
early_data=df.index.min()
early_year=early_data.year



# Display headers with the latest date
st.header('Major Indicators for Commercial Banks')
st.subheader(f'As of {latest_date.strftime("%B %Y")}')

# Create an expander for Year and Month selection
with st.expander("Select Year and Month for specific month data",expanded= True):
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

# Trend Analysis Section
with st.expander("Click Here for Trend Analysis of Major Indicators (Line Chart)"):
    st.write("Explore the trends over time for selected major indicators.")

    # Allow user to select metrics for trend analysis
    selected_metrics_trend = st.multiselect('Select Metrics for Trend Analysis', selected_metrics, default=['Total Deposit/GDP', 'Total Credit/GDP'])

    # Year and Month selection side by side
    col1, col2 = st.columns(2)

    with col1:
        start_year = st.selectbox('Select Start Year:', df.index.year.unique(), index=df.index.year.unique().tolist().index(early_year))

    with col2:
        start_month = st.selectbox('Select Start Month:', df.index.month_name().unique(), index=df.index.month_name().unique().tolist().index(default_month))

    # Add content specific to the second column or any additional content within the expander
    with col1:
        end_year = st.selectbox('Select End Year:', df.index.year.unique(), index=df.index.year.unique().tolist().index(default_year))

    with col2:
        end_month = st.selectbox('Select End Month:', df.index.month_name().unique(), index=df.index.month_name().unique().tolist().index(default_month))

    # Filter the DataFrame for trend analysis based on user selection
    trend_df = df.loc[f"{start_year}-{start_month}":f"{end_year}-{end_month}"]

    # Plot trends using Plotly Express
    if selected_metrics_trend:
        # Plot trends using Plotly Express with a horizontal legend
        fig_trend = px.line(trend_df, x=trend_df.index, y=selected_metrics_trend, title='Trend Analysis of Major Indicators')

        fig_trend.update_layout(
            legend_orientation="h", yaxis_title="" 
        )

        # Show the chart
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Please select at least one metric for trend analysis.")
    # Display the filtered data table for selected metrics
    st.write("Filtered Data Table:") 
    filtered_data_table = trend_df[selected_metrics_trend]

    # Format the date column to display as "Month Year"
    filtered_data_table.index = filtered_data_table.index.strftime('%B %Y')

    st.write(filtered_data_table)
