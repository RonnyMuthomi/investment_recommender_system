# streamlit_app.py
import streamlit as st
import pandas as pd
import requests

st.title("📊 Household Investment Strategy Recommender")

uploaded_file = st.file_uploader("Upload your FinAccess Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    st.success("File uploaded. Sending to model...")

    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://localhost:8000/recommend", files={"file": uploaded_file})

    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        st.subheader("Recommended Investment Strategies:")
        st.dataframe(data)
        st.download_button("Download CSV", data.to_csv(index=False), file_name="investment_recommendations.csv")
    else:
        st.error("Failed to get recommendations from API.")
