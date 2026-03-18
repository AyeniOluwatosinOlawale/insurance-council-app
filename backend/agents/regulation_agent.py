from llm_client import call_llm

async def regulation_agent(data):
    return await call_llm(
        "openai/gpt-4o-mini",
        "You are a UK FCA compliance advisor.",
        f"Check compliance for driver age {data.age}, vehicle {data.vehicle}."
    )
