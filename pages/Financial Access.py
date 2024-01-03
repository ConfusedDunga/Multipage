import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .st-emotion-cache-1r6slb0 {
            width: calc(33.3333% - 1rem);
            flex: 1 1 calc(33.3333% - 1rem);
            padding: 3%;
        }   
    </style>
    """,
    unsafe_allow_html=True
)


# Load data
file_path = "NRB_Data.xlsx"
sheet_name = "MajorIndicators"
df = pd.read_excel(file_path, sheet_name=sheet_name)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)


latest_date = df.index.max()

# Display headers with the latest date
st.header('Financial Access of Commercial Banks')
st.subheader(f'As of {latest_date.strftime("%B %Y")}')


# Specify the metrics you want to include in the dashboard
selected_metrics = [
    'Total Institutions', 'Total Branches', 'Total Deposit Accounts',
    'Total Loan Accounts', 'Total BLB Centers',
    'Total BLB Customers', 'Total Mobile Banking Customers',
    'Total Internet Banking Customers', 'Total no of Operating ATMs', 'Total Debit Cards',
    'Total Credit Cards', 'Total Prepaid Cards'
]

# Filter the DataFrame to include only selected metrics
selected_df = df[selected_metrics]

# Set the page to 4 rows and 3 columns
num_rows = 4
num_cols = 3

# Organize metrics and line charts in a 4x3 grid
columns = st.columns(num_cols)

for i, metric in enumerate(selected_df.columns):
    row = i // num_cols
    col = i % num_cols

    # Create a metric section
    with columns[col]:
        st.write(metric)

        # Display the latest metric value
        latest_metric_value = selected_df[metric].iloc[-1]
        delta_value = int(latest_metric_value - selected_df[metric].iloc[-2])
        st.metric(label='Latest Number', value=latest_metric_value, delta=delta_value)

        # Create a Plotly line chart below the metric
        fig = px.line(selected_df, x=selected_df.index, y=metric, title=f'Trend of {metric}',line_shape='spline',markers=True)

        # Hide grids for both x and y axes
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig, use_container_width=True)