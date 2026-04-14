import streamlit as st
from src.utils import get_data, get_model

st.set_page_config(layout="wide")

st.title("📊 Customer Churn Analysis App")

df = get_data()
model = get_model()

st.markdown("""
Welcome to the Customer Churn Analysis System.

### 📌 Pages:
- Dashboard → Business insights
- What-if Analysis → Scenario simulation
""")