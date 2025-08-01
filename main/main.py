# investment_recommender_app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import io

app = FastAPI(title="Household Investment Recommender", description="Upload FinAccess Excel file and get labeled investment strategies.")

@app.post("/recommend")
def recommend_investments(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="File must be an Excel .xlsx file")

    # Read Excel
    contents = file.file.read()
    df = pd.read_excel(io.BytesIO(contents))

    # Step 1: Select relevant columns
    relevant_cols = [
        "A08", "A13", "B3Ii", "U23", "C1_1a", "C1_2", "C1_4", "C1_6", "C1_9",
        "C1_15", "C1_17", "C1_19", "C1_25", "C1_35"
    ]
    df_subset = df[relevant_cols].copy()
    df_subset.columns = [
        "area_type", "gender", "monthly_income", "monthly_expenditure",
        "save_bank", "save_mobile_money", "save_sacco", "save_friends", "save_digital",
        "loan_mobile", "loan_sacco", "loan_digital", "loan_family", "invest_forex"
    ]

    # Step 2: Transform behavior
    usage_map = {"Never used": 0, "Used to use": 1, "Currently use": 2, pd.NA: 0, None: 0}
    behavior_cols = [
        'save_bank', 'save_mobile_money', 'save_sacco', 'save_friends', 'save_digital',
        'loan_mobile', 'loan_sacco', 'loan_digital', 'loan_family', 'invest_forex'
    ]
    df_subset[behavior_cols] = df_subset[behavior_cols].applymap(lambda x: usage_map.get(x, 0))

    # Step 3: Encode categoricals
    df_subset['gender'] = df_subset['gender'].map({'Male': 0, 'Female': 1})
    df_subset['area_type'] = df_subset['area_type'].map({'Rural': 0, 'Urban': 1})

    # Step 4: Handle missing income/expenses
    df_subset['monthly_income'] = df_subset['monthly_income'].fillna(df_subset['monthly_income'].median())
    df_subset['monthly_expenditure'] = df_subset['monthly_expenditure'].fillna(df_subset['monthly_expenditure'].median())

    # Step 5: Standardize and compute similarity
    scaler = StandardScaler()
    household_scaled = scaler.fit_transform(df_subset)

    investment_profiles = pd.DataFrame([
        [1, 1, 0.3, 0.3, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0.6, 0.6, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2]
    ], columns=df_subset.columns, index=['conservative', 'balanced', 'aggressive'])

    investment_scaled = scaler.transform(investment_profiles)
    similarity_matrix = cosine_similarity(household_scaled, investment_scaled)
    recommendations = pd.DataFrame(similarity_matrix, columns=investment_profiles.index)

    df_subset["investment_label"] = recommendations.apply(lambda row: row.nlargest(1).index[0], axis=1)
    return df_subset.to_dict(orient="records")
