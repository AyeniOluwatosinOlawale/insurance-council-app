from agents.risk_agent import risk_agent
from agents.fraud_agent import fraud_agent
from agents.regulation_agent import regulation_agent
from agents.underwriting_agent import underwriting_agent
from debate import debate

async def run_insurance_council(data):
    risk = await risk_agent(data)
    fraud = await fraud_agent(data)
    regulation = await regulation_agent(data)

    council_debate = await debate(risk, fraud, regulation)

    final = await underwriting_agent(data, council_debate)

    return {
        "risk": risk,
        "fraud": fraud,
        "regulation": regulation,
        "debate": council_debate,
        "final": final
    }
