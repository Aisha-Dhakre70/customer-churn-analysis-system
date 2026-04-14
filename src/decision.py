def churn_decision(prob):
    if prob > 0.5:
        return "High Risk"
    elif prob > 0.3:
        return "Medium Risk"
    else:
        return "Low Risk"