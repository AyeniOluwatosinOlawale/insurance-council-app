import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import os

# Global in-memory model and encoders
_xgb_model = None
_label_encoders = {}

def generate_synthetic_data(num_samples=2000):
    """Generates synthetic historical insurance data to train the XGBoost model."""
    np.random.seed(42)
    
    # Features
    ages = np.random.randint(18, 80, num_samples)
    accidents = np.random.poisson(lam=0.5, size=num_samples)
    vehicles = np.random.choice(["BMW", "Toyota", "Ford", "Mercedes", "Honda", "Tesla", "Audi"], num_samples)
    postcodes = np.random.choice(["SE15", "E1", "W1", "N1", "SW1", "NW1", "WC1"], num_samples)
    mileage = np.random.randint(2000, 25000, num_samples)
    
    # Calculate synthetic "true" risk score (0-100) based on realistic rules
    # Young drivers = higher risk
    age_risk = np.where(ages < 25, 40, np.where(ages > 70, 20, 0))
    # Accidents heavily skew risk
    accident_risk = np.minimum(accidents * 25, 50)
    # High mileage = more exposure
    mileage_risk = (mileage / 25000) * 15
    # High value cars cost more/crash harder
    vehicle_risk_map = {"BMW": 15, "Mercedes": 15, "Tesla": 10, "Audi": 10, "Toyota": 5, "Honda": 5, "Ford": 5}
    vehicle_risk = np.array([vehicle_risk_map[v] for v in vehicles])
    
    # Base random variance
    base_risk = 5 + np.random.normal(0, 5, num_samples)
    
    target_risk = age_risk + accident_risk + mileage_risk + vehicle_risk + base_risk
    # Clip between 0 and 100
    target_risk = np.clip(target_risk, 0, 100)
    
    df = pd.DataFrame({
        "age": ages,
        "accidents": accidents,
        "vehicle": vehicles,
        "postcode": postcodes,
        "mileage": mileage,
        "risk_score": target_risk
    })
    return df

def init_xgboost_model():
    """Trains the XGBoost model in-memory using synthetic data."""
    global _xgb_model, _label_encoders
    print("⏳ Initializing Insurtech XGBoost Model...")
    
    df = generate_synthetic_data()
    
    # Encode categorical features
    categorical_cols = ["vehicle", "postcode"]
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        _label_encoders[col] = le
        
    X = df.drop("risk_score", axis=1)
    y = df["risk_score"]
    
    # Train the XGBRegressor
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1
    )
    model.fit(X, y)
    
    _xgb_model = model
    print("✅ XGBoost Model successfully dynamically trained on 2,000 synthetic records!")

def predict_risk(age, vehicle, postcode, accidents, mileage):
    """Predicts a real 0-100 risk score using the trained XGBoost model."""
    global _xgb_model, _label_encoders
    
    if _xgb_model is None:
        init_xgboost_model()
        
    # Safely transform categorical variables (handle unseen gracefully)
    encoded_vehicle = 0
    if vehicle in _label_encoders["vehicle"].classes_:
        encoded_vehicle = _label_encoders["vehicle"].transform([vehicle])[0]
    else:
        # Unknown vehicle defaults to a mid-range fallback
        encoded_vehicle = len(_label_encoders["vehicle"].classes_)
        
    encoded_postcode = 0
    if postcode in _label_encoders["postcode"].classes_:
        encoded_postcode = _label_encoders["postcode"].transform([postcode])[0]
    else:
        encoded_postcode = len(_label_encoders["postcode"].classes_)
        
    input_data = pd.DataFrame({
        "age": [age],
        "accidents": [accidents],
        "vehicle": [encoded_vehicle],
        "postcode": [encoded_postcode],
        "mileage": [mileage]
    })
    
    prediction = _xgb_model.predict(input_data)[0]
    return float(np.clip(prediction, 0, 100))
