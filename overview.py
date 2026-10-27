import plotly.express as px
import streamlit as st

from utils import load

st.title("Sales Analytics Platform")
st.caption("Online Retail II  ·  1 Dec 2009 to 9 Dec 2011  ·  UK online giftware retailer")

# ---- KPI cards -------------------------------------------------------------
kpis = load("kpis")
for start in range(0, len(kpis), 4):
    cols = st.columns(4)
    for col, (_, row) in zip(cols, kpis.iloc[start:start + 4].iterrows()):
        col.metric(row["KPI"], row["Value"])

st.divider()

# ---- Monthly revenue --------------------------------------------------------
monthly = load("monthly_sales")
monthly = monthly[monthly["YearMonth"] < "2011-12"]          # December 2011 is a partial month

fig = px.line(monthly, x="YearMonth", y="Revenue", markers=True, title="Monthly revenue")
fig.update_layout(yaxis_tickprefix="£", yaxis_tickformat=",.0f", xaxis_title=None, yaxis_title=None)
st.plotly_chart(fig)
st.caption("December 2011 is excluded because the data ends on 9 December.")

# ---- Seasonality 2010 vs 2011 ------------------------------------------------
seas = monthly.copy()
seas["Year"] = seas["YearMonth"].str[:4]
seas["Month"] = seas["YearMonth"].str[5:].astype(int)
seas = seas[seas["Year"].isin(["2010", "2011"])]

fig2 = px.line(seas, x="Month", y="Revenue", color="Year", markers=True,
               title="Seasonality: 2010 vs 2011")
fig2.update_xaxes(tickmode="array", tickvals=list(range(1, 13)),
                  ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
fig2.update_layout(yaxis_tickprefix="£", yaxis_tickformat=",.0f", yaxis_title=None)
st.plotly_chart(fig2)

# ---- Products and countries -------------------------------------------------
left, right = st.columns(2)

top_products = load("products").nlargest(10, "Revenue").sort_values("Revenue")
fig3 = px.bar(top_products, x="Revenue", y="Name", orientation="h", title="Top 10 products by revenue")
fig3.update_layout(xaxis_tickprefix="£", xaxis_tickformat=",.0f", yaxis_title=None, xaxis_title=None)
left.plotly_chart(fig3)

countries = load("country_monthly").groupby("Country", as_index=False)["Revenue"].sum()
uk_share = countries.loc[countries["Country"] == "United Kingdom", "Revenue"].sum() / countries["Revenue"].sum()
top_c = countries[countries["Country"] != "United Kingdom"].nlargest(10, "Revenue").sort_values("Revenue")
fig4 = px.bar(top_c, x="Revenue", y="Country", orientation="h",
              title=f"Top 10 countries excluding the UK (UK = {uk_share:.1%} of revenue)")
fig4.update_layout(xaxis_tickprefix="£", xaxis_tickformat=",.0f", yaxis_title=None, xaxis_title=None)
right.plotly_chart(fig4)
