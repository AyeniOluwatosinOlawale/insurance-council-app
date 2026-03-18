from llm_client import call_llm

async def fraud_agent(data):
    return await call_llm(
        "anthropic/claude-3-haiku",
        "You are a fraud investigator.",
        f"Fraud score {data.fraud_score}, postcode {data.postcode}. Identify fraud signals."
    )
