def generate_recommendations(data):
    recommendations = []

    # Contract-based
    if data["Contract"] == "Month-to-month":
        recommendations.append("📄 Encourage customer to switch to a long-term contract with incentives.")

    # High monthly charges
    if data["MonthlyCharges"] > 80:
        recommendations.append("💰 Offer discounts or bundled services to reduce perceived cost.")

    # Tech support
    if data["TechSupport"] == "No":
        recommendations.append("🛠️ Provide technical support plans to improve retention.")

    # Tenure
    if data["tenure"] < 12:
        recommendations.append("🎯 Improve onboarding and early engagement experience.")

    # Internet service
    if data["InternetService"] == "Fiber optic":
        recommendations.append("📶 Review pricing/value for fiber customers to reduce churn.")

    return recommendations