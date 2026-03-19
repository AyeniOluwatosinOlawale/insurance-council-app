import json
import re
from llm_client import call_llm

async def underwriting_agent(data, debate, ml_risk_score):
    response = await call_llm(
        "openai/gpt-4o",
        "You are a senior underwriter and risk dashboard engine.",
        f"""
Driver data: {data}
Algorithm Risk Score: {ml_risk_score:.1f}/100

Council debate:
{debate}

You MUST return EXACTLY and ONLY a valid JSON object (no markdown, no extra text) with the following structure:
{{
  "risk_score": {int(ml_risk_score)},
  "premium": (int, the calculated premium in £ based on the Algorithm Risk Score),
  "decision": "Approve" | "Reject" | "Refer",
  "explanation": (string detailing your reasoning)
}}
"""
    )
    
    try:
        # Robustly extract only the JSON object, ignoring any markdown block ticks
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            clean_json = response[start:end+1]
            parsed = json.loads(clean_json)
            # Enforce true mathematically calculated score mathematically overriding any LLM deviation
            parsed["risk_score"] = int(ml_risk_score)
            return parsed
        else:
            raise ValueError("No JSON object found")
    except Exception as e:
        return {
            "risk_score": 50,
            "premium": data.expected_claim_cost, # safe fallback
            "decision": "Refer",
            "explanation": f"Failed to parse underlying decision JSON. Raw output: {response}"
        }
