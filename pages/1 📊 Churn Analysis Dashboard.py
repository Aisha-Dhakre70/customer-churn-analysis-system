import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.express as px
import pandas as pd
from src.utils import load_data, get_churn_by_segments, get_high_risk_customers, get_revenue_at_risk

st.set_page_config(layout="wide")

# LOAD DATA
df = st.session_state.get("df")

if df is None:
    st.error("Data not loaded. Please open the main app first.")
    st.stop()

df["Churn_Label"] = df["Churn"].map({0:"Not Churned", 1:"Churned"})

# UI TITLE
st.title("📊 Customer Churn Analysis Dashboard")

# METRICS
high_risk = (df["Churn"] == 1).sum()

churn_rate_tech_df = df.groupby("TechSupport")["Churn"].mean().reset_index()
churn_rate_tech_df["Churn"] *= 100

churn_rate_contract_df = df.groupby("Contract")["Churn"].mean().reset_index()
churn_rate_contract_df["Churn"] *= 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(df))

with col2:
    churn_rate = df["Churn"].mean() * 100
    st.metric("Churn Rate", f"{churn_rate:.2f}%")

with col3:
    st.metric("Customers Lost", f"{high_risk}")

# KEY INSIGHTS
st.subheader("🔍 Key Insights")

st.markdown("""
- Month-to-month contracts have the highest churn  
- Customers with low tenure are more likely to churn  
- Customers paying high monthly charges show high churn
- Lack of Tech Support increases churn risk
""")

# DATA PREVIEW
preview = df.copy()
preview["SeniorCitizen"] = preview["SeniorCitizen"].map({0:"No", 1:"Yes"})
with st.expander("📋 View Customer Data"):
    st.dataframe(preview.head(20))

# EDA VISUALIZATION
st.header("📈 Exploratory Data Analysis")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        churn_rate_contract_df,
        x="Contract",
        y="Churn",
        title="Churn Rate by Contract Type",
        labels={"Churn":"Churn Rate (%)"}
        )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("""
                ##### 📌 Insight:
                Customers on month-to-month contracts exhibit the highest churn, while long-term contracts show strong retention.

                ##### 💡 Recommendation:
                Encourage long-term subscriptions through discounts, loyalty programs, or contract upgrade incentives.
                """)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
                ##### 📌 Insight:
                Customers with lower tenure exhibit a significantly higher likelihood of churn, indicating that customers are most vulnerable during the early stages of their lifecycle.

                ##### 💡 Recommendation:
                Focus on improving early customer engagement through onboarding programs, personalized communication, and retention offers during the initial months.
                """)

with col2:
    fig2 = px.box(
        df,
        x="Churn_Label",
        y="tenure",
        color="Churn_Label",
        title="Churn Distribution by Tenure",
        labels={"Churn_Label":"Churn", "tenure":"Tenure"}
        )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(
        df,
        x="Churn_Label",
        y="MonthlyCharges",
        color="Churn_Label",
        title="Churn Distribution by Monthly Charges",
        labels={"Churn_Label":"Churn", "MonthlyCharges":"Monthly Charges"}
        )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("""
                ##### 📌 Insight:
                Customers with higher monthly charges show a greater tendency to churn, suggesting that pricing and perceived value play a key role in customer retention.

                ##### 💡 Recommendation:
                Introduce pricing optimization strategies such as discounts, bundled services, or loyalty benefits to improve perceived value and reduce churn among high-paying customers.
                """)


st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
                ##### 📌 Insight:
                Customers without technical support account for a large proportion of churned users, indicating a potential link between lack of support and customer attrition.
                ##### 💡 Recommendation:
                Provide proactive technical support, offer support bundles, or incentivize customers to adopt support services to improve retention.
                """)

with col2:
    fig4 = px.bar(
        churn_rate_tech_df,
        x="TechSupport",
        y="Churn",
        title="Churn Rate by Tech Support",
        labels={"Churn": "Churn Rate (%)", "TechSupport":"Tech Support"},
        category_orders={
            "TechSupport":["No", "Yes", "No internet service"]
            }
        )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

with st.expander("🛠️ Advanced Insights (SQL)"):

    st.markdown("### 💰 Revenue Impact")

    df_risk = get_revenue_at_risk()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Monthly Revenue at Risk", df_risk["monthly_revenue_at_risk"][0])
    with col2:
        st.metric("Total Revenue Lost", df_risk["total_revenue_at_risk"][0])

    st.caption("Estimated revenue loss due to churned customers.")


    st.divider()


    st.markdown("### ⚠️ High-Risk Customers")

    threshold = st.slider("Monthly Charge Threshold", 50, 150, 80)

    df_high_risk = get_high_risk_customers(threshold)

    st.metric("Customers Above Risk Threshold", df_high_risk["high_risk_customers"][0])

    st.caption("Customers with high monthly charges are more likely to churn.")


    st.divider()


    st.markdown("### 🔍 High-Risk Segments")

    df_segments = get_churn_by_segments()

    st.dataframe(df_segments.head(5))

    st.caption("Top customer segments with highest churn rates.")