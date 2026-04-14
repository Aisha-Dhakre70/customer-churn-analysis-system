USE customer_db;

# Overall Churn Rate

SELECT
ROUND(AVG(churn)*100,2) AS churn_rate
FROM fact_customer_churn;

# Churn by Contract Type

SELECT
a.Contract,
COUNT(*) AS total_customers,
SUM(f.Churn) AS Churned,
ROUND(AVG(f.Churn)*100, 2) AS churn_rate
FROM fact_customer_churn f
INNER JOIN dim_account a ON a.customer_id = f.customer_id
GROUP BY a.Contract;

# High Risk Customers

SELECT
f.customer_id,
f.MonthlyCharges,
a.Contract
FROM fact_customer_churn f
INNER JOIN dim_account a ON a.customer_id = f.customer_id
WHERE Churn = 1
ORDER BY f.MonthlyCharges DESC;

# Window Functions

SELECT 
    customer_id,
    MonthlyCharges,
    RANK() OVER (ORDER BY MonthlyCharges DESC) AS revenue_rank
FROM fact_customer_churn;