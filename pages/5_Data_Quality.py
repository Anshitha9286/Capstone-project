import plotly.express as px
import streamlit as st

from utils import load

st.title("Data quality")
st.caption("Every cleaning decision is logged. Problem rows were moved to their own tables, not deleted.")

log = load("cleaning_log")

start = int(log["rows_before"].iloc[0])
end = int(log["rows_after"].iloc[-1])

k1, k2, k3 = st.columns(3)
k1.metric("Rows in the raw data", f"{start:,}")
k2.metric("Rows in the clean sales table", f"{end:,}")
k3.metric("Share kept", f"{end / start:.1%}")

fig = px.bar(log[log["rows_removed"] > 0], x="rows_removed", y="step", orientation="h",
             title="Rows removed or set aside, by step")
fig.update_layout(xaxis_title="Rows", yaxis_title=None, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig)

st.dataframe(log.rename(columns={"step": "Step", "rows_before": "Rows before",
                                 "rows_after": "Rows after", "rows_removed": "Rows removed"}), hide_index=True)

st.markdown(
    """
**Decisions**
- **Duplicate rows** were dropped, because counting the same sale twice inflates revenue.
- **Cancellation invoices** (starting with C) went to a returns table.
- **Zero or negative quantity or price** rows went to an adjustments table (stock write-offs and accounting entries).
- **Non-product codes** such as postage and bank charges went to their own table.
- **Same-day cancelled bulk orders** (28 lines worth £274,971.60) were removed from sales and returns, because that
  revenue never happened.
- **Missing Customer IDs** (about 22.8% of the raw rows) were kept for revenue analysis and excluded from customer analysis.
"""
)
