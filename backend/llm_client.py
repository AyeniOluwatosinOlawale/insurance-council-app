import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

async def call_llm(model, system, prompt):
    if not API_KEY or API_KEY == "your_api_key_here":
        return f"[MOCK] Simulated response from {model} for prompt '{prompt[:30]}...'"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            res = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            
            if res.status_code != 200:
                return f"⚠️ API Error ({res.status_code}): {res.text}"
                
            data = res.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return f"⚠️ API returned unexpected format: {res.text}"
                
        except Exception as e:
            return f"⚠️ Internal connection error to OpenRouter: {str(e)}"
