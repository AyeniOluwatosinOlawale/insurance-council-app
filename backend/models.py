from pydantic import BaseModel

class DriverProfile(BaseModel):
    age: int
    vehicle: str
    postcode: str
    accidents: int
    annual_mileage: int
    claim_probability: float
    expected_claim_cost: float
    fraud_score: float
