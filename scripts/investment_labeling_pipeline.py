import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


def transform_finaccess_data(input_excel_path: str, output_csv_path: str = "labeled_household_investments.csv") -> pd.DataFrame:
    """
    Reads a raw FinAccess Excel file, selects and transforms features, and assigns
    investment strategy labels using cosine similarity.
    
    Parameters:
        input_excel_path (str): Path to the raw Excel file.
        output_csv_path (str): Path where the labeled CSV will be saved.

    Returns:
        pd.DataFrame: Transformed and labeled household data.
    """
    # === 1. Load Excel ===
    df = pd.read_excel(input_excel_path)

    # === 2. Select Relevant Columns ===
    relevant_cols = [
        "A08", "A13", "B3Ii", "U23",
        "C1_1a", "C1_2", "C1_4", "C1_6", "C1_9",
        "C1_15", "C1_17", "C1_19", "C1_25", "C1_35"
    ]
    df_subset = df[relevant_cols].copy()

    # === 3. Rename Columns ===
    df_subset.columns = [
        "area_type", "gender", "monthly_income", "monthly_expenditure",
        "save_bank", "save_mobile_money", "save_sacco", "save_friends", "save_digital",
        "loan_mobile", "loan_sacco", "loan_digital", "loan_family", "invest_forex"
    ]

    # === 4. Map Usage Levels ===
    usage_map = {"Never used": 0, "Used to use": 1, "Currently use": 2, pd.NA: 0, None: 0}
    behavior_cols = [
        'save_bank', 'save_mobile_money', 'save_sacco', 'save_friends', 'save_digital',
        'loan_mobile', 'loan_sacco', 'loan_digital', 'loan_family', 'invest_forex'
    ]
    df_subset[behavior_cols] = df_subset[behavior_cols].applymap(lambda x: usage_map.get(x, 0))

    # === 5. Encode Demographics ===
    df_subset['gender'] = df_subset['gender'].map({'Male': 0, 'Female': 1})
    df_subset['area_type'] = df_subset['area_type'].map({'Rural': 0, 'Urban': 1})

    # === 6. Fill NaNs ===
    df_subset['monthly_income'] = df_subset['monthly_income'].fillna(df_subset['monthly_income'].median())
    df_subset['monthly_expenditure'] = df_subset['monthly_expenditure'].fillna(df_subset['monthly_expenditure'].median())

    # === 7. Scale Features ===
    scaler = StandardScaler()
    household_scaled = scaler.fit_transform(df_subset)

    # === 8. Create Dummy Investment Profiles ===
    investment_profiles = pd.DataFrame([
        [1, 1, 0.3, 0.3, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0],  # Conservative
        [1, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # Balanced
        [1, 1, 0.6, 0.6, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2]   # Aggressive
    ], columns=df_subset.columns, index=['conservative', 'balanced', 'aggressive'])

    investment_scaled = scaler.transform(investment_profiles)

    # === 9. Cosine Similarity ===
    similarity_matrix = cosine_similarity(household_scaled, investment_scaled)
    recommendations = pd.DataFrame(similarity_matrix, columns=investment_profiles.index)
    df_subset["investment_label"] = recommendations.apply(lambda row: row.nlargest(1).index[0], axis=1)

    # === 10. Save and return ===
    df_subset.to_csv(output_csv_path, index=False)
    return df_subset


# Example usage
if __name__ == "__main__":
    result_df = transform_finaccess_data("200_rows_finaccess_data.xlsx")
    print("✅ Labeled data saved. Preview:")
    print(result_df.head())
