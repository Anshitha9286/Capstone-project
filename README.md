# Sales Analytics Platform

An end-to-end analytics project on the Online Retail II dataset: data cleaning, exploratory analysis, customer segmentation, churn prediction, sales forecasting (including deep learning), anomaly detection and automated weekly insight generation, delivered as a Streamlit dashboard.

**Live app:** 
https://capstone-project-xsuzbrjviw2gx9ttkud75s.streamlit.app/

## Problem
Dashboards show numbers, but an analyst still has to clean the data, find the patterns, forecast the next period and write the summary by hand. This project automates that chain: the same pipeline cleans the data, models it and writes the weekly report.

## Dataset
[Online Retail II (UCI / Kaggle)](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci): about 1.07 million transaction lines from a UK online giftware retailer, 1 Dec 2009 to 9 Dec 2011.

## What the project does
| Stage | What it does | Key result |
|---|---|---|
| Data cleaning | Logged pipeline: duplicates, cancellations, adjustments, non-product codes, same-day cancelled bulk orders | 94.0% of rows kept; £274,971.60 of phantom revenue from cancelled bulk orders removed |
| EDA | KPIs, seasonality, orders and order value, products, countries, buying times, order size, customer concentration, returns | Revenue roughly doubles from summer to November; top 20% of customers generate 76.8% of identified revenue |
| RFM segmentation | Scores customers on recency, frequency and monetary value | Champions: about 25% of customers, about 70% of identified revenue |
| Churn prediction | Logistic regression and random forest on pre-cutoff behaviour, labelled by the following six months | ROC-AUC 0.80; recency and orders per month are the main drivers |
| Forecasting | 28-day daily revenue: baselines, Holt-Winters, LSTM, rolling backtest, Christmas-window test | Ordinary periods: average of Holt-Winters and last year (WAPE 29.6%); Christmas window: last year scaled by growth (within about 5% of the actual total). The LSTM was tested and did not beat the statistical models on two years of data |
| Anomaly detection | LSTM autoencoder on trading days | 16 days flagged, 8 of them UK bank holidays |
| Insight generator | Writes the weekly report in plain English from the model outputs | Revenue vs previous week and last year, top product and market, anomalies, customers at risk, forecast |

## Project structure
```
app.py                 Streamlit entry point and menu
overview.py            Overview page
pages/                 Customers, Forecast, Anomalies, Weekly report, Data quality
utils.py               Data loading helpers
data/                  Summary tables produced by the notebook
sales_analytics.ipynb  Full analysis notebook (cleaning, EDA, models, report)
requirements.txt
```

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
The notebook (`sales_analytics.ipynb`) was run in Google Colab. It reads the raw CSV from the Kaggle dataset and writes the files in `data/`.

## Tech stack
Python, pandas, NumPy, scikit-learn, statsmodels, Keras (LSTM and LSTM autoencoder), Plotly, Streamlit.

## Limitations
- Only two years of data, so each season is seen at most twice.
- About 22.8% of raw rows have no Customer ID, so customer analysis covers about 77% of sales.
- The Christmas forecast rule is supported by a single test window.
- The data has no costs, so the analysis covers revenue, not profit.

## Next steps
- Add a UK holiday calendar so expected closures are not flagged as anomalies.
- Add more years of data and test further forecasting models.
- Schedule the weekly report to refresh automatically, with written commentary from a language model.
