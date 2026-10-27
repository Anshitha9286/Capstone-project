import streamlit as st

from utils import load_json

st.title("Weekly insight report")

meta = load_json("metrics_and_report")
report = meta["report"]

st.caption(f"Generated automatically from the model outputs. Data up to {meta['data_end']}.")

with st.container(border=True):
    for line in report:
        st.markdown(f"- {line}")

text = "Weekly insight report (data up to " + meta["data_end"] + ")\n\n" + "\n".join(f"- {l}" for l in report)
st.download_button("Download report (text)", text, "weekly_report.txt", "text/plain")

st.divider()
st.markdown(
    """
**How it works.** One function reads the daily sales, the churn scores, the anomaly flags and the forecast, compares
the latest week with the previous week and with last year, and writes each finding as a sentence. The same code can run
for any week, so the report can be refreshed automatically whenever new data arrives.
"""
)
