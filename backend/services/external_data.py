import asyncio
import random

async def fetch_vehicle_data(vehicle_model: str) -> dict:
    """Mock API call to DVLA/Vehicle database."""
    await asyncio.sleep(0.5)  # Simulate network latency
    
    # Mock data logic
    base_values = {"BMW": 35000, "Tesla": 45000, "Ford": 15000, "Toyota": 18000, "Mercedes": 40000, "Audi": 38000, "Honda": 16000}
    default_value = 20000
    
    value = base_values.get(vehicle_model, default_value)
    repair_complexity = "High" if value > 30000 else "Medium"
    theft_risk = round(random.uniform(0.01, 0.08), 3) # e.g. 4.2%
    
    return {
        "base_value_gbp": value,
        "repair_complexity": repair_complexity,
        "theft_risk": theft_risk
    }

async def fetch_postcode_data(postcode: str) -> dict:
    """Mock API call to Geographic Risk DB."""
    await asyncio.sleep(0.3)
    
    # Identify high risk london zones arbitrarily for mockup
    high_risk_zones = ["SE15", "E1", "NW1"]
    
    multiplier = 1.0
    if any(postcode.upper().startswith(zone) for zone in high_risk_zones):
        multiplier = 1.8
    else:
        multiplier = 1.2
        
    return {
        "region_crime_multiplier": multiplier,
        "uninsured_driver_rate": round(random.uniform(0.05, 0.15), 3)
    }

async def fetch_claims_history(data) -> dict:
    """Mock API call to Claims Underwriting Exchange (CUE)."""
    await asyncio.sleep(0.4)
    
    # If they have prior accidents, assume a historical payout
    payout = 0
    if data.accidents > 0:
        payout = data.accidents * random.randint(1500, 8000)
        
    return {
        "verified_prior_accidents": data.accidents,
        "historical_payout_gbp": payout,
        "fraud_flag": bool(payout > 15000)
    }

async def enrich_profile(data) -> dict:
    # Run API calls in parallel
    vehicle_data, postcode_data, claims_data = await asyncio.gather(
        fetch_vehicle_data(data.vehicle),
        fetch_postcode_data(data.postcode),
        fetch_claims_history(data)
    )
    
    # Calculate quoting pipeline based on external APIs
    base_repair_cost = vehicle_data["base_value_gbp"] * 0.10 # Assume 10% of car value is typical crash repair
    geo_modifier = postcode_data["region_crime_multiplier"]
    history_modifier = 1.0 + (claims_data["verified_prior_accidents"] * 0.2) # +20% cost expectance per past accident
    
    dynamic_expected_cost = int(base_repair_cost * geo_modifier * history_modifier)
    
    return {
        "vehicle_db": vehicle_data,
        "postcode_db": postcode_data,
        "claims_db": claims_data,
        "dynamic_expected_cost": dynamic_expected_cost
    }
