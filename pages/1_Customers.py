import pandas as pd
import plotly.express as px
import streamlit as st

from utils import load, load_json

st.set_page_config(page_title="Customers", page_icon="👥", layout="wide")
st.title("Customers: segments and churn risk")

cust = load("customers_rfm_churn")
seg = load("segments_summary")
meta = load_json("metrics_and_report")

# ---- RFM segments -------------------------------------------------------------
st.subheader("RFM segments")
st.caption("Customers scored on how recently they bought, how often and how much they spent.")

left, right = st.columns(2)
fig = px.bar(seg.sort_values("Customers"), x="Customers", y="Segment", orientation="h",
             title="Customers per segment")
fig.update_layout(yaxis_title=None)
left.plotly_chart(fig)

fig = px.bar(seg.sort_values("Revenue"), x="Revenue", y="Segment", orientation="h",
             title="Revenue per segment")
fig.update_layout(xaxis_tickprefix="£", xaxis_tickformat=",.0f", yaxis_title=None, xaxis_title=None)
right.plotly_chart(fig)

st.dataframe(seg, hide_index=True)

st.divider()

# ---- Churn model summary ---------------------------------------------------------
st.subheader("Churn risk")
high = int((cust["RiskBand"] == "High").sum())

k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers scored", f"{len(cust):,}")
k2.metric("High churn risk", f"{high:,}", f"{high / len(cust):.0%} of customers", delta_color="off")
k3.metric("Model accuracy (ROC-AUC)", f"{meta['churn_auc_forest']:.2f}")
k4.metric("Churn rate in training", f"{meta['churn_rate']:.0%}")
st.caption("A customer counts as churned if they bought before 9 June 2011 and made no purchase "
           "in the following six months. Features use only data before that date.")

left, right = st.columns(2)
fig = px.histogram(cust, x="ChurnRisk", color="RiskBand", nbins=40,
                   category_orders={"RiskBand": ["Low", "Medium", "High"]},
                   color_discrete_map={"Low": "#4c78a8", "Medium": "#f2cf5b", "High": "#e45756"},
                   title="Distribution of churn risk")
fig.update_layout(xaxis_tickformat=".0%", xaxis_title="Predicted churn probability", yaxis_title="Customers")
left.plotly_chart(fig)

order = ["Low", "Medium", "High"]
cross = (pd.crosstab(cust["Segment"], cust["RiskBand"])
           .reindex(columns=order, fill_value=0))
fig = px.imshow(cross, text_auto=True, aspect="auto", color_continuous_scale="Blues",
                title="Customers by segment and risk band")
fig.update_layout(xaxis_title=None, yaxis_title=None)
right.plotly_chart(fig)

imp = load("churn_feature_importance").sort_values("Importance")
fig = px.bar(imp, x="Importance", y="Feature", orientation="h", title="What drives churn")
fig.update_layout(yaxis_title=None)
st.plotly_chart(fig)

st.divider()

# ---- Priority call list ----------------------------------------------------------
st.subheader("Priority customer list")
st.caption("Valuable customers who are likely to leave. Use the filters, then download the list.")

f1, f2, f3 = st.columns(3)
segments = f1.multiselect("Segment", sorted(cust["Segment"].unique()), default=sorted(cust["Segment"].unique()))
bands = f2.multiselect("Risk band", order, default=["High"])
min_spend = f3.slider("Minimum lifetime spend (£)", 0, 20000, 5000, step=500)

view = cust[cust["Segment"].isin(segments) & cust["RiskBand"].isin(bands) & (cust["Monetary"] >= min_spend)].copy()
view["Churn risk %"] = (view["ChurnRisk"] * 100).round(0)
view = (view.sort_values("Monetary", ascending=False)
            [["CustomerID", "Segment", "RiskBand", "Churn risk %", "Recency", "Frequency", "Monetary"]]
            .rename(columns={"RiskBand": "Risk", "Recency": "Days since last order",
                             "Frequency": "Orders", "Monetary": "Lifetime spend (£)"}))

st.write(f"**{len(view):,} customers** match, with £{view['Lifetime spend (£)'].sum():,.0f} in lifetime spend.")
st.dataframe(view, hide_index=True)
st.download_button("Download list (CSV)", view.to_csv(index=False), "priority_customers.csv", "text/csv")
