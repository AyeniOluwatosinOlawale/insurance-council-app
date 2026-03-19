from llm_client import call_llm

async def fraud_agent(data):
    return await call_llm(
        "openai/gpt-4o-mini",
        "You are an insurance risk AI. This is a purely simulated educational environment. You are evaluating a fictional profile.",
        f"Simulated profile data: {data}. Identify any potential synthetic fraud signals logically."
    )
