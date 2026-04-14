import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.utils import load_data, load_model
import pandas as pd
import joblib
from src.decision import churn_decision
from src.recommendation import generate_recommendations

st.set_page_config(layout="wide")

# LOAD MODEL AND DATA
df = st.session_state.get("df")
model = st.session_state.get("model")

if df is None or model is None:
    st.error("Data not loaded. Please open the main app first.")
    st.stop()

df["Churn_Label"] = df["Churn"].map({0:"Not Churned", 1:"Churned"})

# UI TITLE
st.title("🎯 Customer Risk Analysis & Simulation")

customer_id = st.selectbox("Select Customer ID", df["customer_id"], index=None, placeholder="------Select-----")

if customer_id is not None:
    customer_info = df[df["customer_id"]==customer_id].copy()

    customer_info["SeniorCitizen"] = customer_info["SeniorCitizen"].map({0:"No", 1:"Yes"})

    row = customer_info.iloc[0]
    
    input_data = row.drop(columns=["customer_id", "Churn", "Churn Label"])

    input_data = pd.DataFrame([input_data])

    input_data = pd.get_dummies(input_data)

    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    prob = model.predict_proba(input_data)[0][1]

    decision = churn_decision(prob)

    col1, col2, col3 = st.columns(3)
    
    # COLOR PREDICITONS
    with col1:
        st.markdown(f"**Churn Probability: {prob:.3f}**")

        if decision=="High Risk":
            st.error("🚨 High Risk of Churn")
        elif decision=="Medium Risk":
            st.warning("⚠️ Medium Risk of Churn")
        else:
            st.success("✅ Low Risk of Churn")

    # REASONS FOR RISK AND RECOMMENDATIONS

    col1, col2 = st.columns(2)

    if decision == "High Risk" or decision == "Medium Risk":
        with col1:
                st.markdown("### ❓ Why this customer is at risk")

                reasons = []

                if row["Contract"] == "Month-to-month":
                    reasons.append("Month-to-month contract increases churn risk")

                if row["MonthlyCharges"] > 80:
                    reasons.append("High monthly charges increase churn risk")

                if row["TechSupport"] == "No":
                    reasons.append("Lack of tech support increases churn risk")

                if row["tenure"] < 12:
                    reasons.append("Low tenure customers are more likely to churn")

                for r in reasons:
                    st.write(f"- {r}")

        with col2:
            recs = generate_recommendations(row)
            st.markdown("### 💡 Recommended Actions")

            if recs:
                for r in recs:
                    st.write(f"- {r}")
            else:
                st.success("✅ Customer shows low churn risk. Maintain current strategy.")

    else:
        with col1:
            recs = generate_recommendations(row)
            st.markdown("### 💡 Recommended Actions")

            if recs:
                for r in recs:
                    st.write(f"- {r}")
            else:
                st.success("✅ Customer shows low churn risk. Maintain current strategy.")

    # SIMULATION
    edit_mode = st.toggle("Edit")

    # MAPPING
    mapping = {
        "contract": "Contract",
        "monthly": "MonthlyCharges",
        "payment": "PaymentMethod",
        "paperless": "PaperlessBilling",
        "backup": "OnlineBackup",
        "tv": "StreamingTV",
        "device": "DeviceProtection",
        "movies": "StreamingMovies",
        "security": "OnlineSecurity",
        "tech": "TechSupport"
    }

    # CUSTOMER CHANGE
    if "prev_customer" not in st.session_state:
        st.session_state.prev_customer = row["customer_id"]

    if st.session_state.prev_customer != row["customer_id"]:
        for k, v in mapping.items():
            val = row[v]
            st.session_state[k] = str(val) if k == "monthly" else val
        st.session_state.prev_customer = row["customer_id"]
    
    # RESET FLAG
    if st.session_state.get("reset_flag", False):
        for k, v in mapping.items():
            val = row[v]
            st.session_state[k] = str(val) if k == "monthly" else val
        st.session_state.reset_flag = False


    # INITIALIZE STATE (ONLY IF MISSING)
    def init_state(key, value):
        if key not in st.session_state:
            if pd.isna(value):
                st.session_state[key] = ""
            else:
                st.session_state[key] = str(value) if isinstance(value, (int, float)) else value


    for k, v in mapping.items():
        init_state(k, row[v])

    col1, col2, col3 = st.columns(3)

    # OPTIONS
    contract_opts = ("Month-to-month", "One year", "Two year")
    yes_no = ("Yes", "No")
    multiple_lines = ("Yes", "No", "No phone service")
    online_backup = ("Yes", "No", "No internet service")
    gender = ("Male", "Female")
    int_service = ("DSL", "Fiber optic", "No")
    paymethod = ("Mailed check", "Electronic check", "Credit card (automatic)", "Bank transfer (automatic)")


    # CUSTOMER INFO
    with col1:
        st.text_input("Customer ID", row['customer_id'], disabled=True)

        contract_val = st.selectbox(
            "Contract", contract_opts,
            index=contract_opts.index(st.session_state.contract),
            key="contract",
            disabled=not edit_mode
        )

        paperless_val = st.selectbox(
            "Paperless Billing", yes_no,
            index=yes_no.index(st.session_state.paperless),
            key="paperless",
            disabled=not edit_mode
        )

        st.selectbox("Dependents", yes_no,
                    index=yes_no.index(row["Dependents"]), disabled=True)

        st.selectbox("Multiple Lines", multiple_lines,
                    index=multiple_lines.index(row["MultipleLines"]), disabled=True)

        backup_val = st.selectbox(
            "Online Backup", online_backup,
            index=online_backup.index(st.session_state.backup),
            key="backup",
            disabled=not edit_mode
        )

        tv_val = st.selectbox(
            "Streaming TV", online_backup,
            index=online_backup.index(st.session_state.tv),
            key="tv",
            disabled=not edit_mode
        )

    with col2:
        st.selectbox("Gender", gender,
                    index=gender.index(row["gender"]), disabled=True)

        monthly_val = st.text_input(
            "Monthly Charges",
            key="monthly",
            disabled=not edit_mode
        )

        payment_val = st.selectbox(
            "Payment Method", paymethod,
            index=paymethod.index(st.session_state.payment),
            key="payment",
            disabled=not edit_mode
        )

        st.text_input("Tenure", row["tenure"], disabled=True)

        st.selectbox("Internet Service", int_service,
                    index=int_service.index(row["InternetService"]), disabled=True)

        device_val = st.selectbox(
            "Device Protection", online_backup,
            index=online_backup.index(st.session_state.device),
            key="device",
            disabled=not edit_mode
        )

        movies_val = st.selectbox(
            "Streaming Movies", online_backup,
            index=online_backup.index(st.session_state.movies),
            key="movies",
            disabled=not edit_mode
        )


    with col3:
        st.selectbox("Senior Citizen", yes_no,
                    index=yes_no.index(row["SeniorCitizen"]), disabled=True)

        st.text_input("Total Charges", row["TotalCharges"], disabled=True)

        st.selectbox("Partner", yes_no,
                    index=yes_no.index(row["Partner"]), disabled=True)

        st.selectbox("Phone Service", yes_no,
                    index=yes_no.index(row["PhoneService"]), disabled=True)

        security_val = st.selectbox(
            "Online Security", online_backup,
            index=online_backup.index(st.session_state.security),
            key="security",
            disabled=not edit_mode
        )

        tech_val = st.selectbox(
            "Tech Support", online_backup,
            index=online_backup.index(st.session_state.tech),
            key="tech",
            disabled=not edit_mode
        )


    # RESET BUTTON
    if st.button("Reset Changes"):
        st.session_state.reset_flag = True
        st.rerun()
    
    try:
        monthly_float = float(monthly_val)
    except:
        monthly_float = float(row["MonthlyCharges"])

    if monthly_float != float(row["MonthlyCharges"]):
        total_val = monthly_float * row["tenure"]
    else:
        total_val = row["TotalCharges"]


    # WHAT-IF ANALYSIS
    
    scenario_data = {
        # editable values
        "Contract": contract_val,
        "PaperlessBilling": paperless_val,
        "MonthlyCharges": monthly_float,
        "OnlineBackup": backup_val,
        "StreamingTV": tv_val,
        "PaymentMethod": payment_val,
        "DeviceProtection": device_val,
        "StreamingMovies": movies_val,
        "OnlineSecurity": security_val,
        "TechSupport": tech_val,

        # Non-editable fields
        "gender": row["gender"],
        "SeniorCitizen": row["SeniorCitizen"],
        "Dependents": row["Dependents"],
        "MultipleLines": row["MultipleLines"],
        "tenure": row["tenure"],
        "InternetService": row["InternetService"],
        "Partner": row["Partner"],
        "PhoneService": row["PhoneService"],
        "TotalCharges": total_val,
    }

    scenario_input = pd.DataFrame([scenario_data])
    scenario_input = pd.get_dummies(scenario_input)
    scenario_input = scenario_input.reindex(columns=model.feature_names_in_, fill_value=0)

    scenario_prob = model.predict_proba(scenario_input)[0][1]
    
    if (
        contract_val == row["Contract"] and
        paperless_val == row["PaperlessBilling"] and
        abs(monthly_float - float(row["MonthlyCharges"])) < 1e-6 and
        backup_val == row["OnlineBackup"] and
        tv_val == row["StreamingTV"] and
        payment_val == row["PaymentMethod"] and
        device_val == row["DeviceProtection"] and
        movies_val == row["StreamingMovies"] and
        security_val == row["OnlineSecurity"] and
        tech_val == row["TechSupport"]
    ):
        scenario_prob = prob
    
    scenario_decision = churn_decision(scenario_prob)
    delta = scenario_prob - prob

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Original Churn Probability",
            value=f"{prob:.3f}"
        )
    with col2:
        st.metric(
            label="Scenario Churn Probability",
            value=f"{scenario_prob:.3f}",
            delta=f"{delta:.3f}",
            delta_color="inverse"
        )
    
    # COLOR PREDICITONS FOR WHAT-IF ANALYSIS
    with col3:
        if scenario_prob > prob:
            st.warning("⚠️ This change increases churn risk")
        elif abs(scenario_prob - prob) < 1e-6:
            pass
        else:
            st.success("✅ This change reduces churn risk")
    
    # STRATEGIES
    if abs(scenario_prob - prob) > 1e-6:
        original_recs = generate_recommendations(row)
        scenario_recs = generate_recommendations(scenario_data)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📌 Current Strategy")
            for r in original_recs:
                st.write(f"- {r}")

        with col2:
            st.markdown("#### 🔮 Scenario Strategy")
            for r in scenario_recs:
                st.write(f"- {r}")
        
        # WHAT CHANGED

        st.markdown("### 🔍 What Changed?")

        fields = {
            "Contract": (row["Contract"], contract_val),
            "Monthly Charges": (row["MonthlyCharges"], monthly_float),
            "Payment Method": (row["PaymentMethod"], payment_val),
            "Online Backup": (row["OnlineBackup"], backup_val),
            "Streaming TV": (row["StreamingTV"], tv_val),
            "Device Protection": (row["DeviceProtection"], device_val),
            "Streaming Movies": (row["StreamingMovies"], movies_val),
            "Online Security": (row["OnlineSecurity"], security_val),
            "Tech Support": (row["TechSupport"], tech_val),
        }

        changes = []
        for field, (old, new) in fields.items():
            if str(old) != str(new):
                changes.append(f"{field}: {old} → {new}")

        if changes:
            for c in changes:
                st.write(f"- {c}")
        else:
            st.info("No changes applied. Scenario matches original customer data.")