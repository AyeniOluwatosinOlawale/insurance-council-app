from agents.risk_agent import risk_agent
from agents.fraud_agent import fraud_agent
from agents.regulation_agent import regulation_agent
from agents.underwriting_agent import underwriting_agent
from debate import debate
from ml.xgboost_model import predict_risk

async def run_insurance_council(data):
    # Calculate real mathematical ML risk score via XGBoost
    ml_risk_score = predict_risk(data.age, data.vehicle, data.postcode, data.accidents, data.annual_mileage)

    risk = await risk_agent(data)
    fraud = await fraud_agent(data)
    regulation = await regulation_agent(data)

    council_debate = await debate(risk, fraud, regulation)

    final = await underwriting_agent(data, council_debate, ml_risk_score)

    return {
        "risk": risk,
        "fraud": fraud,
        "regulation": regulation,
        "debate": council_debate,
        "final": final
    }
