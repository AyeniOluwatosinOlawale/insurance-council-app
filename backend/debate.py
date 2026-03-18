from llm_client import call_llm

async def debate(risk, fraud, regulation):
    return await call_llm(
        "google/gemini-2.5-flash",
        "You are a moderator of an insurance council.",
        f"""
Risk Analyst: {risk}
Fraud Analyst: {fraud}
Regulation Advisor: {regulation}

Make them debate and summarize disagreements.
"""
    )
