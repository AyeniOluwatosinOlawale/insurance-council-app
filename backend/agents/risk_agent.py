from llm_client import call_llm

async def risk_agent(data):
    return await call_llm(
        "openai/gpt-4o-mini",
        "You are a UK insurance risk analyst.",
        f"Driver age {data.age}, accidents {data.accidents}, claim probability {data.claim_probability}. Assess risk."
    )
