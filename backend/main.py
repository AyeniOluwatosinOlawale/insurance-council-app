from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import DriverProfile
from council import run_insurance_council

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Insurance Council API running"}

@app.post("/underwrite")
async def underwrite(profile: DriverProfile):
    return await run_insurance_council(profile)
