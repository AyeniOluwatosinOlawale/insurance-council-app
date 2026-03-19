from pydantic import BaseModel
from typing import Optional, Dict, Any

class DriverProfile(BaseModel):
    age: int
    vehicle: str
    postcode: str
    accidents: int
    annual_mileage: int
    claim_probability: Optional[float] = None
    expected_claim_cost: Optional[int] = None
    fraud_score: Optional[float] = None
    enriched: Optional[Dict[str, Any]] = None
