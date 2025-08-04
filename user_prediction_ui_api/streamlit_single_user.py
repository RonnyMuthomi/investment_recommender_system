# streamlit_single_user.py
import streamlit as st
import requests

st.title("🏦 Personalized Investment Strategy Recommender")

with st.form("user_profile_form"):
    area_type = st.radio("Area Type", ["Urban", "Rural"])
    gender = st.radio("Gender", ["Male", "Female"])
    income = st.number_input("Monthly Income", min_value=0.0)
    expenditure = st.number_input("Monthly Expenditure", min_value=0.0)

    st.markdown("### Saving Behavior (0=Never, 1=Used to, 2=Currently)")
    save_bank = st.slider("Save in Bank", 0, 2)
    save_mobile = st.slider("Save via Mobile Money", 0, 2)
    save_sacco = st.slider("Save in SACCO", 0, 2)
    save_friends = st.slider("Save with Friends", 0, 2)
    save_digital = st.slider("Save in Digital App", 0, 2)

    st.markdown("### Loan/Investment Behavior (0=Never, 1=Used to, 2=Currently)")
    loan_mobile = st.slider("Loan via Mobile Banking", 0, 2)
    loan_sacco = st.slider("Loan from SACCO", 0, 2)
    loan_digital = st.slider("Loan from Digital App", 0, 2)
    loan_family = st.slider("Loan from Family/Friends", 0, 2)
    invest_forex = st.slider("Invested in Forex", 0, 2)

    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    user_payload = {
        "area_type": 1 if area_type == "Urban" else 0,
        "gender": 0 if gender == "Male" else 1,
        "monthly_income": income,
        "monthly_expenditure": expenditure,
        "save_bank": save_bank,
        "save_mobile_money": save_mobile,
        "save_sacco": save_sacco,
        "save_friends": save_friends,
        "save_digital": save_digital,
        "loan_mobile": loan_mobile,
        "loan_sacco": loan_sacco,
        "loan_digital": loan_digital,
        "loan_family": loan_family,
        "invest_forex": invest_forex
    }

    response = requests.post("http://localhost:8000/predict_user", json=user_payload)

    if response.status_code == 200:
        st.success(f"✅ Recommended Investment Strategy: **{response.json()['recommended_strategy']}**")
    else:
        st.error("❌ Prediction failed.")
