import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from utils import load

st.title("Sales forecast: the next 28 days")

forecast = load("forecast_next28")
daily = load("daily_sales")
forecast["Date"] = pd.to_datetime(forecast["Date"])
daily["Date"] = pd.to_datetime(daily["Date"])

total = forecast["Forecast"].sum()
last_year = forecast["LastYear"].sum()
closed = int((forecast["Forecast"] == 0).sum())
start, end = forecast["Date"].min(), forecast["Date"].max()

k1, k2, k3 = st.columns(3)
k1.metric(f"Forecast {start:%d %b} to {end:%d %b %Y}", f"£{total:,.0f}")
k2.metric("Versus the same period last year", f"{total / last_year - 1:+.1%}", f"last year £{last_year:,.0f}", delta_color="off")
k3.metric("Days with no sales expected", f"{closed} of {len(forecast)}", "Saturdays and the Christmas closure", delta_color="off")

# ---- Forecast chart ----------------------------------------------------------------
recent = daily.sort_values("Date").tail(90)
fig = go.Figure()
fig.add_trace(go.Scatter(x=recent["Date"], y=recent["Revenue"], name="Actual (last 90 days)",
                         line=dict(color="#9aa5b1")))
fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["Forecast"], name="Forecast",
                         line=dict(color="#e45756", width=3)))
fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["LastYear"], name="Same weekday last year",
                         line=dict(color="#4c78a8", dash="dot")))
fig.update_layout(title="Daily revenue: actual and forecast", yaxis_tickprefix="£", yaxis_tickformat=",.0f",
                  yaxis_title=None, legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig)

st.info("Daily forecasts are noisy: single days were typically off by 30% to 45% in tests. "
        "The 28-day total is far more reliable, typically within about 5% to 8%.")

with st.expander("Daily forecast table"):
    table = forecast[["Date", "Forecast"]].copy()
    table["Weekday"] = table["Date"].dt.day_name()
    table["Date"] = table["Date"].dt.strftime("%Y-%m-%d")
    table = table[["Date", "Weekday", "Forecast"]]
    st.dataframe(table, hide_index=True)
    st.download_button("Download forecast (CSV)", table.to_csv(index=False), "forecast_next28.csv", "text/csv")

st.divider()

# ---- How the forecast was chosen -------------------------------------------------------
st.subheader("How the forecast was chosen")
st.markdown(
    """
Models were compared on data they had never seen. Two situations were tested separately.

- **Ordinary periods:** the average of Holt-Winters (learns the weekly pattern and recent level) and last year's
  same-weekday revenue won an eight-window backtest, with a daily error (WAPE) of 29.6% and a 28-day total
  typically within about 8%.
- **Periods containing the Christmas closure:** Holt-Winters overshot by 70% and the average of the two by 33%.
  Last year's pattern scaled by recent growth was within about 5%, so it is used for this forecast.
- **LSTM (deep learning):** tested and not selected. With two years of data it forecast a flat level and
  missed the peak season (daily error 31.8%, 28-day total 28% too low).
"""
)

comparison = load("forecast_model_comparison")
st.markdown("**Test on the last 28 days of the data**")
st.dataframe(comparison, hide_index=True)

bt = load("forecast_backtest")
bt_long = bt.melt(id_vars="Window", var_name="Model", value_name="WAPE")
fig2 = px.bar(bt_long, x="Window", y="WAPE", color="Model", barmode="group",
              title="Eight-window backtest: daily error (lower is better)")
fig2.update_layout(yaxis_tickformat=".0%", xaxis_title=None, yaxis_title=None, legend=dict(orientation="h", y=-0.3))
st.plotly_chart(fig2)
