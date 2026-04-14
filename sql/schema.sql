CREATE DATABASE customer_db;
USE customer_db;

CREATE TABLE fact_customer_churn (
    customer_id VARCHAR(50),
    MonthlyCharges FLOAT,
    TotalCharges FLOAT,
    Churn INT,
    PRIMARY KEY (customer_id)
);

CREATE TABLE dim_customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure INT
);

CREATE TABLE dim_services (
    customer_id VARCHAR(50) PRIMARY KEY,
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20)
);

CREATE TABLE dim_account (
    customer_id VARCHAR(50) PRIMARY KEY,
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(50)
);

ALTER TABLE fact_customer_churn
ADD CONSTRAINT
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

CREATE INDEX idx_customer_id ON fact_customer_churn(customer_id);