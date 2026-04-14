# Customer Churn Prediction & What-If Analysis System
An end-to-end analytics and decision-support system that predicts customer churn risk and enables scenario-based simulation to evaluate how business actions impact retention.

Unlike traditional churn models, this system not only predicts risk but also recommends actionable strategies and quantifies their impact through what-if analysis.

---

## Problem Statement

Customer churn is a major challenge for subscription-based businesses. Losing customers not only impacts revenue but also increases acquisition costs.

Traditional churn prediction systems identify high-risk customers but fail to answer:

- *What actions can reduce churn?*
- *How will changes affect customer behavior?*

This project addresses these gaps by building a system that not only predicts churn but also **simulates business decisions and recommends actions**.

---

## Objectives
- Predict customer churn probability using machine learning
- Identify key drivers of churn through data analysis
- Enable what-if analysis for scenario simulation
- Provide actionable retention recommendations
- Deliver insights through an interactive dashboard

---

## Features
- Churn Probability Prediction using trained ML models
- Interactive Dashboard with KPIs and EDA visualizations
- What-If Analysis Engine to simulate customer scenarios
- Recommendation System for retention strategies
- SQL Stored Procedures for business insights
- Risk Categorization (High / Medium / Low)
- User-friendly Streamlit Interface

---

## Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Streamlit
- Plotly
- MySQL (SQL + Stored Procedures)

---

## Dataset

The dataset includes customer information across multiple dimensions:

### Key Features:
- Demographics (gender, senior citizen, partner, dependents)
- Account details (contract type, billing method, tenure)
- Services (internet service, tech support, streaming, etc.)
- Financials (monthly charges, total charges)

### Target Variable:
- Churn (1 = Churned, 0 = Retained)

### Source:
- [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

> Note: The dataset is not included in this repository. Please download it from the provided Kaggle link and place it inside the data/raw/ directory before running the project.

---

## Model Overview
- Machine learning model trained to predict churn probability
- ROC-AUC: ~0.93
- Uses SMOTE to handle class imbalance
- Handles categorical features using encoding techniques
- Outputs probability score used for risk classification

The model is optimized for identifying high-risk customers to support proactive retention strategies.

### Output:
- Churn Probability
- Risk Category (High / Medium / Low)

---

## System Design Highlights

- Modular architecture separating data loading, business logic, and UI
- Shared state management across pages using Streamlit session_state
- Feature alignment using model.feature_names_in_ to prevent mismatch errors
- Efficient SQL integration with stored procedures for scalable analytics

---

## Dashboard Insights

The dashboard highlights key churn drivers:

- Month-to-month contracts have the highest churn
- Customers with low tenure are more likely to leave
- Higher monthly charges correlate with higher churn
- Lack of tech support increases churn risk

These insights guide business strategies for customer retention.

---

## What-If Analysis

This system goes beyond prediction by enabling scenario simulation.

Users can modify key customer attributes such as:

- Contract type
- Monthly charges
- Payment method
- Service subscriptions

The system dynamically:
- Recalculates churn probability
- Compares original vs scenario outcomes
- Shows whether risk increases or decreases

| Scenario           | Churn Probability |
| ------------------ | ----------------- |
| Original           | 0.42              |
| With Tech Support  | 0.28              |
| Long-term Contract | 0.19              |

This helps businesses evaluate the impact of retention strategies before implementation.

---

## Recommendation Engine

The system provides actionable suggestions based on customer risk:

Examples:
- Offer discounts for high monthly charges
- Encourage long-term contracts
- Provide tech support services
- Improve early customer engagement

Recommendations are rule-based and business-aligned, making them easy to interpret and implement. This bridges the gap between model predictions and real-world business actions.

---

## Advanced SQL Insights

Stored procedures are used to encapsulate business logic and improve query performance. The project integrates SQL stored procedures to generate business-critical insights:

### Key Metrics:
- Revenue at risk due to churn
- High-risk customer segments
- Customers above risk thresholds

These insights complement ML predictions with data-driven business intelligence.

---

## Business Impact

This system supports decision-making by combining prediction with action.

- Identifies high-risk customers proactively
- Simulates impact of retention strategies
- Reduces revenue loss due to churn
- Enables data-driven business decisions

In real-world applications, this can:

- Improve customer retention
- Optimize pricing and service strategies
- Increase customer lifetime value

---

## Risk Consideration

Different prediction outcomes have different impacts:

- False Negatives → Missing high-risk customers → Revenue loss
- False Positives → Over-targeting low-risk customers → Resource inefficiency

The system balances prediction with actionable insights to minimize both risks.

---

## Limitations
- Model performance depends on data quality
- Rule-based recommendations may not cover all scenarios
- Dataset may not fully represent all customer behaviors

---

## Future Improvements
- Add real-time data integration
- Enhance recommendation engine using ML
- Deploy as a cloud-based application
- Integrate customer segmentation models
- Add explainability (e.g., SHAP) for deeper insights

---

## Project Structure
    customer-churn-project/
    │
    ├── data/
    |   └── raw/
    |
    ├── pages/
    │   ├── 1 📊 Churn Analysis Dashboard.py
    │   └── 2 🎯 Customer Risk Analysis.py
    │
    ├── src/
    │   ├── recommendation.py
    │   ├── decision.py
    │   └── utils.py
    │
    ├── models/
    │   └── model.pkl
    |
    ├── notebooks/
    │   ├── data_loading.ipnyb
    │   ├── eda.ipnyb
    │   └── model.ipnyb
    |
    ├── sql/
    │   ├── schema.sql
    │   ├── queries.sql
    │   └── procedures.sql
    |
    ├── app.py
    ├── requirements.txt
    ├── insights.md
    └── README.md

---

## Pretrained Model

A pre-trained model (model.pkl) is included in the repository for quick testing and demonstration purposes.

Users can directly run the Streamlit application without retraining the model.

> Note: The model was trained using the dataset referenced above. To retrain the model, follow the notebooks and sql files provided in the notebooks/ and sql/ directories, respectively, in this order: schema.sql < procedures.sql < data_loading.ipnyb < model.ipnyb

---

## Run Locally
    pip install -r requirements.txt
    streamlit run app.py

> The app uses a pre-trained model, so no training step is required.
---

## Screenshots

### Churn Analysis Dashboard

<img width="1854" height="899" alt="image" src="https://github.com/user-attachments/assets/9d8f7ed9-998f-45f2-aab3-306bd979a94e" />

<img width="1915" height="894" alt="image" src="https://github.com/user-attachments/assets/c326a738-93e8-4e8f-9ed8-0852600e2de0" />

<img width="1919" height="867" alt="image" src="https://github.com/user-attachments/assets/26146c3d-b1bc-4149-afd4-ef12304542dd" />

<img width="1919" height="711" alt="image" src="https://github.com/user-attachments/assets/1afd5274-e3d6-4b73-9351-c3b01584ec42" />

### Customer Risk Analysis

<img width="1919" height="822" alt="image" src="https://github.com/user-attachments/assets/189e3498-0885-4e06-ab39-3ee54a90248f" />

<img width="1919" height="853" alt="image" src="https://github.com/user-attachments/assets/b8ca832a-c089-4906-b437-b9f7ae1f75de" />

---

## Key Learning Outcomes
- Building end-to-end ML systems
- Designing user-centric data applications for business decision support
- Implementing what-if analysis for decision support
- Integrating SQL with ML workflows
- Translating data insights into business actions

---

## Why This Project Matters

This project demonstrates how machine learning can move beyond prediction to become a decision-support system.

It reflects real-world challenges such as:

- Customer retention
- Business trade-offs
- Actionable analytics

---

## Conclusion

This project combines machine learning, business intelligence, and interactive analytics to address customer churn.

By integrating prediction, simulation, and recommendations, it provides a practical framework for data-driven decision-making in real-world business environments.
