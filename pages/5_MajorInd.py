import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
add_page_title()


c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns([6,3,2])

with st.container():
    c1.write("c1")
    c2.write("c2")
    c3.write("c3")

with st.container():
    c4.write("c4")
    c5.write("c5")
    c6.write("c6")