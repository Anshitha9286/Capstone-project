import streamlit as st

st.set_page_config(page_title="Sales Analytics Platform", page_icon="📊", layout="wide")

pages = [
    st.Page("overview.py", title="Overview", icon="📊", default=True),
    st.Page("pages/1_Customers.py", title="Customers", icon="👥"),
    st.Page("pages/2_Forecast.py", title="Forecast", icon="📈"),
    st.Page("pages/3_Anomalies.py", title="Anomalies", icon="🚨"),
    st.Page("pages/4_Weekly_Report.py", title="Weekly report", icon="📝"),
    st.Page("pages/5_Data_Quality.py", title="Data quality", icon="🧹"),
]
st.navigation(pages).run()
