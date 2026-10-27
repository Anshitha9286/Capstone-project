import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import load

st.title("Anomaly detection")
st.caption("An LSTM autoencoder learns what normal trading days look like and flags the days it cannot rebuild. "
           "Saturdays and the Christmas closure are removed first.")

df = load("anomalies")
df["Date"] = pd.to_datetime(df["Date"])

pct = st.slider("Sensitivity: flag the top share of days by anomaly score", 0.5, 10.0, 2.5, step=0.5,
                format="%.1f%%")
threshold = np.percentile(df["Error"], 100 - pct)
df["Flagged"] = df["Error"] >= threshold
flag = df[df["Flagged"]].copy()


def reason(row):
    if row["Revenue"] == 0 and row["Date"].dayofweek < 5:
        return "No sales on a weekday (likely a bank holiday)"
    if row["vs typical"] >= 2:
        return "Unusually high revenue"
    if row["vs typical"] < 1:
        return "Unusually low revenue"
    return "Unusual pattern"


flag["Likely reason"] = flag.apply(reason, axis=1)

k1, k2, k3 = st.columns(3)
k1.metric("Trading days analysed", f"{len(df):,}")
k2.metric("Days flagged", f"{len(flag):,}")
k3.metric("Bank-holiday type closures", f"{int((flag['Likely reason'].str.startswith('No sales')).sum())}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Revenue"], name="Daily revenue", line=dict(color="#4c78a8", width=1)))
fig.add_trace(go.Scatter(x=flag["Date"], y=flag["Revenue"], mode="markers", name="Anomaly",
                         marker=dict(color="#e45756", size=9)))
fig.update_layout(title="Daily revenue with detected anomalies", yaxis_tickprefix="£", yaxis_tickformat=",.0f",
                  yaxis_title=None, legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig)

st.subheader("Flagged days")
view = (flag.sort_values("Error", ascending=False)
            [["Date", "Revenue", "Typical", "vs typical", "Likely reason"]]
            .rename(columns={"Typical": "Typical for that weekday", "vs typical": "Ratio to typical"}))
view["Date"] = view["Date"].dt.strftime("%a %d %b %Y")
st.dataframe(view, hide_index=True)

st.info("Many flags are UK public holidays. In production a holiday calendar would label them as expected, "
        "so analysts would only see the unexplained spikes and drops.")
