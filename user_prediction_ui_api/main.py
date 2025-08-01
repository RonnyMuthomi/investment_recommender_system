# investment_recommender_app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import joblib

app = FastAPI(title="Single User Investment Recommender")

# Load trained model and scaler
model = load_model("investment_model.h5")
scaler = joblib.load("scaler.pkl")

# Match training features
feature_cols = [
    "area_type", "gender", "monthly_income", "monthly_expenditure",
    "save_bank", "save_mobile_money", "save_sacco", "save_friends", "save_digital",
    "loan_mobile", "loan_sacco", "loan_digital", "loan_family", "invest_forex"
]

label_map = {0: "aggressive", 1: "balanced", 2: "conservative"}

class UserProfile(BaseModel):
    area_type: int  # 0 = Rural, 1 = Urban
    gender: int     # 0 = Male, 1 = Female
    monthly_income: float
    monthly_expenditure: float
    save_bank: int
    save_mobile_money: int
    save_sacco: int
    save_friends: int
    save_digital: int
    loan_mobile: int
    loan_sacco: int
    loan_digital: int
    loan_family: int
    invest_forex: int

@app.post("/predict_user")
def predict_user(user: UserProfile):
    try:
        input_df = pd.DataFrame([user.dict()])[feature_cols]
        scaled = scaler.transform(input_df)
        preds = model.predict(scaled)
        label = label_map[np.argmax(preds)]
        return {"recommended_strategy": label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
