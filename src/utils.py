from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import joblib

# CREATE SQL CONNECTION
engine = create_engine("mysql+pymysql://root:szgw_14051@localhost/customer_db")

# LOAD DATA
@st.cache_data
def load_data():
    query = '''
        SELECT
        f.customer_id,
        f.MonthlyCharges,
        f.TotalCharges,
        f.Churn,
        c.gender,
        c.SeniorCitizen,
        c.Partner,
        c.Dependents,
        c.tenure,
        s.PhoneService,
        s.MultipleLines,
        s.InternetService,
        s.OnlineSecurity,
        s.OnlineBackup,
        s.DeviceProtection,
        s.TechSupport,
        s.StreamingTV,
        s.StreamingMovies,
        a.Contract,
        a.PaperlessBilling,
        a.PaymentMethod
        FROM fact_customer_churn f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        JOIN dim_services s ON f.customer_id = s.customer_id
        JOIN dim_account a ON f.customer_id = a.customer_id
    '''
    return pd.read_sql(query, engine)

def get_revenue_at_risk():
    query = "CALL get_revenue_at_risk()"
    return pd.read_sql(query, engine)

def get_high_risk_customers(threshold:int):
    query = f"CALL get_high_risk_customers({threshold})"
    return pd.read_sql(query, engine)

def get_churn_by_segments():
    query = "CALL get_churn_by_segments()"
    return pd.read_sql(query, engine)

# LOAD MODEL
def load_model():
    return joblib.load("C:/Users/User/OneDrive/Desktop/Semester - 8/customer-churn-project/models/model.pkl")

# GET DATA
def get_data():
    import streamlit as st
    if "df" not in st.session_state:
        st.session_state.df = load_data()
    return st.session_state.df

# GET MODEL
def get_model():
    import streamlit as st
    if "model" not in st.session_state:
        st.session_state.model = load_model()
    return st.session_state.model