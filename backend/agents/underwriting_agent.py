from llm_client import call_llm

async def underwriting_agent(data, debate):
    return await call_llm(
        "openai/gpt-4o",
        "You are a senior underwriter.",
        f"""
Driver data: {data}

Council debate:
{debate}

Produce:
- Risk score
- Premium range
- Fraud risk signals
- Compliance notes
- Final underwriting decision
"""
    )
