## Key Insights
- Churn rates are significantly higher among customers on month-to-month contracts, while two-year contract customers exhibit the lowest churn, suggesting that long-term contractual commitments play a critical role in improving customer retention and reducing attrition risk.

- Customers with low tenure demonstrate a higher propensity to churn, indicating that early-stage engagement and onboarding strategies play a crucial role in improving customer retention.

- Customers with higher monthly charges show a higher tendency to churn, indicating price sensitivity as a key driver of customer attrition.

- Churn rates are significantly higher among customers without technical support, highlighting the importance of customer support services in improving user experience and reducing churn.

## SQL Procedures

- **get_revenue_at_risk()**
    - **Business Value:** How much revenue are we losing due to churn?
    - **What it does:** This procedure estimates both short-term and lifetime revenue loss from churned customers.

- **get_churn_by_segments()**
    - **Business Value:** Which customer segments are most likely to churn?
    - **What it does:** This helps identify high-risk customer segments for targeted retention strategies.

- **get_high_risk_customers(int)**
    - **Business Value:** How many customers are at high risk right now?
    - **What it does:** This allows dynamic filtering of high-risk customers based on business-defined thresholds.
