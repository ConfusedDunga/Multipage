import streamlit as st
st.set_page_config(layout="wide")
from st_pages import Page, Section, show_pages, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indentation in the sidebar

# Specify what pages should be shown in the sidebar, and what their titles should be
show_pages(
    [
        Page("1_Homepage.py", "Home"),
        Section("Macroeconomic Data"),
        # Pages after a section will be indented
        Page("pages/2_Inflation.py", "Inflation"),
        Section("Commercial Banks Data"),
        # Pages after a section will be indented
        Page("pages/5_MajorInd.py", "Major Financial Indicators"),
        Page("pages/3_BaseRate.py", "Base Rates"),
        Page("pages/4_InterestRates.py", "Interest Rates"),
        Page("pages/Financial Access.py", "Financial Access of Commercial Banks"),
    ]
)
