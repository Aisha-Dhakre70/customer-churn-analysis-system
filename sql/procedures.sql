USE customer_db; 

DELIMITER $$ 

# How much revenue is lost due to churn?

CREATE PROCEDURE get_revenue_at_risk()
BEGIN
    SELECT 
        ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_at_risk,
        ROUND(SUM(TotalCharges), 2) AS total_revenue_at_risk,
        COUNT(*) AS churned_customers
    FROM fact_customer_churn
    WHERE Churn = 1;
END $$

# Which customer segments are more likely to churn?

CREATE PROCEDURE get_churn_by_segments()
BEGIN
    SELECT 
        Contract,
        InternetService,
        TechSupport,
        ROUND(AVG(Churn) * 100, 2) AS churn_rate,
        COUNT(*) AS total_customers
    FROM fact_customer_churn f
    JOIN dim_account a ON f.customer_id = a.customer_id
    JOIN dim_services s ON f.customer_id = s.customer_id
    GROUP BY Contract, InternetService, TechSupport
    ORDER BY churn_rate DESC;
END $$

# How many customers are at high risk right now?

CREATE PROCEDURE get_high_risk_customers(IN threshold FLOAT)
BEGIN
    SELECT 
        COUNT(*) AS high_risk_customers
    FROM fact_customer_churn
    WHERE Churn = 1 AND MonthlyCharges > threshold;
END $$

DELIMITER ;