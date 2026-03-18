from llm_client import call_llm

async def regulation_agent(data):
    return await call_llm(
        "meta-llama/llama-3-70b",
        "You are a UK FCA compliance advisor.",
        f"Check compliance for driver age {data.age}, vehicle {data.vehicle}."
    )
