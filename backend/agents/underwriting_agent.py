import json
import re
from llm_client import call_llm

async def underwriting_agent(data, debate, ml_risk_score):
    # Mathematics for Pricing Engine
    # risk_margin scaled from XGBoost score (e.g. 72 / 100 = 0.72)
    risk_margin = ml_risk_score / 100.0
    expenses = 0.20 # Constants for overhead
    premium = int(data.expected_claim_cost * (1 + risk_margin + expenses))

    response = await call_llm(
        "openai/gpt-4o",
        "You are a senior underwriter summarization engine.",
        f"""
Driver data: {data}
Algorithm Risk Score: {ml_risk_score:.1f}/100

Council debate:
{debate}

You MUST return EXACTLY and ONLY a valid JSON object (no markdown, no extra text) with the following structure summarizing the debate concisely.
{{
  "decision": "approve" | "reject" | "refer",
  "fraud_summary": "very short 2-4 word summary (e.g. 'low risk', 'high fraud signals')",
  "regulation_summary": "very short 2-4 word summary (e.g. 'compliant', 'flagged')",
  "explanation": "A detailed 2-3 sentence paragraph explaining your final underwriting logic"
}}
"""
    )
    
    try:
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            clean_json = response[start:end+1]
            parsed = json.loads(clean_json)
            # Enforce true mathematically calculated scores
            parsed["risk_score"] = int(ml_risk_score)
            parsed["risk_summary"] = f"score: {risk_margin:.2f}"
            parsed["premium"] = premium
            return parsed
        else:
            raise ValueError("No JSON object found")
    except Exception as e:
        return {
            "risk_score": int(ml_risk_score),
            "risk_summary": f"score: {risk_margin:.2f}",
            "premium": premium,
            "decision": "refer",
            "fraud_summary": "unknown",
            "regulation_summary": "unknown"
        }
