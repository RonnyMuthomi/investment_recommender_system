import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
from typing import Dict, Any, List
import warnings
warnings.filterwarnings('ignore')

# Import your InvestmentRecommendationSystem class here
from Investment_System import InvestmentRecommendationSystem


# Initialize the system
@st.cache_resource
def load_system():
    return InvestmentRecommendationSystem()

# Page config
st.set_page_config(
    page_title="Kenya Investment Advisor",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("<h1 style='text-align: center;'>🏛️ Kenya Investment Advisor</h1>", unsafe_allow_html=True)

# Initialize theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme-adaptive CSS function
def get_theme_css(theme):
    if theme == 'dark':
        return """
<style>
    /* Main content styling */
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #81C784;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.1);
    }
    .metric-card {
        background: linear-gradient(45deg, #4CAF50, #66BB6A);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    .risk-low {
        border-left-color: #4CAF50;
    }
    .risk-medium {
        border-left-color: #FF9800;
    }
    .risk-high {
        border-left-color: #F44336;
    }
    .risk-very-high {
        border-left-color: #9C27B0;
    }
    
    /* App background */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1cypcdb {
        background-color: #2d2d2d !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #2d2d2d !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Sidebar text and headers */
    .css-1cypcdb h1, .css-1cypcdb h2, .css-1cypcdb h3, .css-1cypcdb h4, .css-1cypcdb h5, .css-1cypcdb h6 {
        color: #ffffff !important;
    }
    .css-1cypcdb p, .css-1cypcdb div, .css-1cypcdb span {
        color: #ffffff !important;
    }
    
    /* Header area */
    header[data-testid="stHeader"] {
        background-color: #1e1e1e !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #1e1e1e;
    }
    
    /* Radio buttons in sidebar */
    .css-1cypcdb .stRadio > div {
        background-color: transparent !important;
    }
    .css-1cypcdb .stRadio label {
        color: #ffffff !important;
    }
    
    /* Form inputs */
    .stSelectbox > div > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #4CAF50 !important;
    }
    .stSelectbox label {
        color: #ffffff !important;
    }
    /* Selectbox dropdown options - comprehensive targeting */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] ul {
        background-color: #2d2d2d !important;
    }
    .stSelectbox div[data-baseweb="select"] li {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] li:hover {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
    }
    /* Additional dropdown targeting */
    div[role="listbox"] {
        background-color: #2d2d2d !important;
        border: 1px solid #4CAF50 !important;
    }
    div[role="option"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    div[role="option"]:hover {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
    }
    /* Base Web select component styling */
    [data-baseweb="select"] [data-baseweb="popover"] {
        background-color: #2d2d2d !important;
    }
    [data-baseweb="select"] [data-baseweb="menu"] {
        background-color: #2d2d2d !important;
        border: 1px solid #4CAF50 !important;
    }
    [data-baseweb="menu"] > ul {
        background-color: #2d2d2d !important;
    }
    [data-baseweb="menu-item"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    [data-baseweb="menu-item"]:hover {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
    }
    /* Universal dropdown styling */
    .css-1wa3eu0-placeholder, .css-1uccc91-singleValue {
        color: #ffffff !important;
    }
    .css-1pahdxg-control {
        background-color: #2d2d2d !important;
        border: 1px solid #4CAF50 !important;
    }
    .css-1n7v3ny-option {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .css-1n7v3ny-option:hover {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
    }
    /* Streamlit select widget specific */
    .stSelectbox > div > div > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .stSelectbox div[data-testid="stSelectbox"] > div > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4CAF50;
    }
    .stTextInput label {
        color: #ffffff !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4CAF50;
    }
    .stTextArea label {
        color: #ffffff !important;
    }
    .stNumberInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4CAF50;
    }
    .stNumberInput label {
        color: #ffffff !important;
    }
    .stMultiSelect > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4CAF50;
    }
    .stMultiSelect label {
        color: #ffffff !important;
    }
    .stCheckbox label {
        color: #ffffff !important;
    }
    
    /* Form labels and text */
    .stForm label {
        color: #ffffff !important;
    }
    
    /* Expander styling */
    div[data-testid="stExpander"] {
        background-color: #2d2d2d;
        border: 1px solid #4CAF50;
    }
    div[data-testid="stExpander"] > div:first-child {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    
    /* Progress bar */
    .stProgress .st-bo {
        background-color: #4CAF50 !important;
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #2d2d2d;
        border: 1px solid #4CAF50;
        padding: 1rem;
        border-radius: 5px;
    }
    div[data-testid="metric-container"] > label {
        color: #81C784 !important;
    }
    div[data-testid="metric-container"] > div {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    
    /* Global dropdown styling - most aggressive approach */
    * [data-baseweb="select"] * {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    * [data-baseweb="menu"] * {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    * [data-baseweb="popover"] * {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* General text */
    p, div, span, li {
        color: #ffffff;
    }
    
    /* Headers in main content */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
</style>
"""
    else:  # light theme
        return """
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(45deg, #2E8B57, #4682B4);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .risk-low {
        border-left-color: #28a745;
    }
    .risk-medium {
        border-left-color: #ffc107;
    }
    .risk-high {
        border-left-color: #dc3545;
    }
    .risk-very-high {
        border-left-color: #6f42c1;
    }
</style>
"""

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# --- Initialize session state for navigation ---
if "theme" not in st.session_state:
    # Detect system theme on first load
    system_dark = streamlit_js_eval(
        js_expressions="window.matchMedia('(prefers-color-scheme: dark)').matches",
        key="system_theme"
    )
    if system_dark is not None:
        st.session_state.theme = "dark" if system_dark else "light"
    else:
        st.session_state.theme = "light"  # fallback

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    # Theme toggle button at the top
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🌓", help="Toggle Theme"):
            current_page = st.session_state.page
            st.session_state.theme = ('dark' if st.session_state.theme == 'light' else 'light')
            st.session_state.page = current_page
            st.rerun()
    with col2:
        st.write(f"Theme: {st.session_state.theme.title()}")
    
    st.markdown("---")
    
    st.header("Navigation")

    page = st.radio(
        "Menu",
        options=["🏠 Home", "💼 Recommendations", "📊 Investments", "ℹ️ About Us", "📞 Contact"],
        index=["🏠 Home", "💼 Recommendations", "📊 Investments", "ℹ️ About Us", "📞 Contact"].index(st.session_state.page),
        key="nav_radio"
    )
    if page != st.session_state.page:
        st.session_state.page = page
    st.markdown("---")
    
    # You can add other sidebar elements here if needed
    st.write("Kenya Investment Recommender System")

# --- Render content based on current page ---
page = st.session_state.page

# # Handle default page (e.g., on first load)
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# # Update session state with selection
if 'page' in locals():
    st.session_state.page = page

if page == "🏠 Home":
    st.subheader("Welcome to the Kenya Investment Recommender System")
    st.write("This tool helps you find the best investment options based on your preferences.")
elif page == "💼 Recommendations":
    st.subheader("Investment Recommendations")
    st.write("Here you will get personalized investment suggestions.")
    # Add your recommendation logic or function here
elif page == "📊 Investments":
    st.subheader("Available Investment Options")
    st.write("Explore various investment products available in Kenya.")
    # Add your data display or plots here
elif page == "ℹ️ About Us":
    st.subheader("About Us")
    st.write("We aim to simplify investment decisions for Kenyans by providing data-driven recommendations.")
elif page == "📞 Contact":
    st.subheader("Contact")
    st.write("Reach out to us at: [support@example.com](mailto:support@example.com) or call +254-700-000-000")


# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# Load system
system = load_system()

# HOME PAGE
if page == "🏠 Home":
        
    col1, col2, col3 = st.columns([1, 2, 1])
    
    st.markdown("""
    <div class="card">
        <h2>Your Personal Investment Guide</h2>
        <p style="font-size: 1.2rem;">
            Make informed investment decisions with our AI-powered recommendation system, 
            specifically designed for the Kenyan market. Get personalized advice based on 
            your financial profile, goals, and risk tolerance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    st.markdown('<h2 class="sub-header">🌟 Key Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 Personalized Recommendations</h3>
            <p>Get investment advice tailored to your unique financial situation and goals.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📈 Kenya Market Focus</h3>
            <p>Specialized knowledge of Kenyan investment products and market conditions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🤖 AI-Powered Analysis</h3>
            <p>Advanced algorithms analyze your profile to suggest the best investment options.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown('<h2 class="sub-header">📊 Investment Landscape Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>16+</h3>
            <p>Investment Options</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>3-50%</h3>
            <p>Return Range</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>All Levels</h3>
            <p>Risk Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Personalized</h3>
            <p>Recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    

# INVESTMENT RECOMMENDATIONS PAGE
elif page == "💼 Recommendations":
    st.markdown('<h1 class="main-header">Get Your Investment Recommendations</h1>', unsafe_allow_html=True)
    
    # Progress bar
    progress = (st.session_state.current_step - 1) / 4
    st.progress(progress)
    
    st.markdown(f"**Step {st.session_state.current_step} of 4**")
    
    # Step 1: Personal Information
    if st.session_state.current_step == 1:
        st.markdown('<h2 class="sub-header">👤 Personal Information</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", value=st.session_state.user_profile.get('name', ''), help="Required field")
            age = st.number_input("Age *", min_value=18, max_value=100, 
                                value=st.session_state.user_profile.get('age', 30), help="Required field")
            location = st.selectbox("Location Type *", 
                                  ["Please select...", "Urban", "Semi-Urban", "Rural"],
                                  index=0 if st.session_state.user_profile.get('location', '') == '' else 
                                  ["Please select...", "Urban", "Semi-Urban", "Rural"].index(
                                      st.session_state.user_profile.get('location', 'Urban')))
        
        with col2:
            education = st.selectbox("Education Level *", 
                                   ["Please select...", "Primary", "Secondary", "College/University", "Postgraduate"],
                                   index=0 if st.session_state.user_profile.get('education', '') == '' else
                                   ["Please select...", "Primary", "Secondary", "College/University", "Postgraduate"].index(
                                       st.session_state.user_profile.get('education', 'Secondary')))
            employment = st.selectbox("Employment Status *",
                                    ["Please select...", "Employed", "Self-Employed", "Student", "Retired", "Unemployed"],
                                    index=0 if st.session_state.user_profile.get('employment', '') == '' else
                                    ["Please select...", "Employed", "Self-Employed", "Student", "Retired", "Unemployed"].index(
                                        st.session_state.user_profile.get('employment', 'Employed')))
            household_size = st.number_input("Household Size *", min_value=1, max_value=20,
                                           value=st.session_state.user_profile.get('household_size', 3), help="Required field")
        
        # Validation
        if st.button("Next →", type="primary"):
            # Check for mandatory fields
            errors = []
            if not name or name.strip() == "":
                errors.append("Full Name is required")
            if location == "Please select...":
                errors.append("Location Type is required")
            if education == "Please select...":
                errors.append("Education Level is required")
            if employment == "Please select...":
                errors.append("Employment Status is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                st.session_state.user_profile.update({
                    'name': name, 'age': age, 'location': location,
                    'education': education, 'employment': employment,
                    'household_size': household_size
                })
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 2: Financial Information
    elif st.session_state.current_step == 2:
        st.markdown('<h2 class="sub-header">💰 Financial Information</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_income = st.number_input("Monthly Income (KES) *", min_value=0, 
                                           value=st.session_state.user_profile.get('monthly_income', 30000),
                                           step=5000, help="Required field")
            monthly_expenses = st.number_input("Monthly Expenses (KES) *", min_value=0,
                                             value=st.session_state.user_profile.get('monthly_expenses', 20000),
                                             step=1000, help="Required field")
            current_savings = st.number_input("Current Savings (KES)", min_value=0,
                                            value=st.session_state.user_profile.get('current_savings', 50000),
                                            step=10000)
        
        with col2:
            debt_amount = st.number_input("Outstanding Debt (KES)", min_value=0,
                                        value=st.session_state.user_profile.get('debt_amount', 0),
                                        step=5000)
            dependents = st.number_input("Number of Dependents", min_value=0, max_value=10,
                                       value=st.session_state.user_profile.get('dependents', 0))
            emergency_fund = st.selectbox("Do you have an emergency fund? *",
                                        ["Please select...", "Yes", "No", "Partial"],
                                        index=0 if st.session_state.user_profile.get('emergency_fund', '') == '' else
                                        ["Please select...", "Yes", "No", "Partial"].index(
                                            st.session_state.user_profile.get('emergency_fund', 'No')))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.current_step = 1
                st.rerun()
        
        with col2:
            if st.button("Next →", type="primary"):
                # Validation
                errors = []
                if monthly_income <= 0:
                    errors.append("Monthly Income must be greater than 0")
                if monthly_expenses < 0:
                    errors.append("Monthly Expenses cannot be negative")
                if monthly_expenses >= monthly_income:
                    errors.append("Monthly Expenses should be less than Monthly Income")
                if emergency_fund == "Please select...":
                    errors.append("Emergency Fund status is required")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    disposable_income = monthly_income - monthly_expenses
                    st.session_state.user_profile.update({
                        'monthly_income': monthly_income,
                        'monthly_expenses': monthly_expenses,
                        'current_savings': current_savings,
                        'debt_amount': debt_amount,
                        'dependents': dependents,
                        'emergency_fund': emergency_fund,
                        'disposable_income': disposable_income
                    })
                    st.session_state.current_step = 3
                    st.rerun()
    
    # Step 3: Investment Preferences
    elif st.session_state.current_step == 3:
        st.markdown('<h2 class="sub-header">🎯 Investment Preferences</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_tolerance = st.selectbox("Risk Tolerance *",
                                        ["Please select...",
                                         "Low - I prefer safe investments",
                                         "Medium - I can accept some risk for better returns",
                                         "High - I'm comfortable with high risk for high returns"],
                                        index=0 if st.session_state.user_profile.get('risk_tolerance', '') == '' else
                                        ["Please select...", "Low", "Medium", "High"].index(
                                            st.session_state.user_profile.get('risk_tolerance', 'Medium')) + 1)
            
            investment_horizon = st.selectbox("Investment Time Horizon *",
                                            ["Please select...",
                                             "Short-term (< 2 years)",
                                             "Medium-term (2-5 years)",
                                             "Long-term (5+ years)"],
                                            index=0 if st.session_state.user_profile.get('investment_horizon', '') == '' else
                                            ["Please select...", "Short-term (< 2 years)", "Medium-term (2-5 years)", "Long-term (5+ years)"].index(
                                                st.session_state.user_profile.get('investment_horizon', 'Medium-term (2-5 years)')))
            
            investment_amount = st.number_input("Amount to Invest (KES) *", min_value=1000,
                                              value=st.session_state.user_profile.get('investment_amount', 10000),
                                              step=1000, help="Required field - Minimum KES 1,000")
        
        with col2:
            investment_goals = st.multiselect("Investment Goals * (Select at least one)",
                                            ["Retirement Planning", "Children's Education", 
                                             "Emergency Fund", "Wealth Building", 
                                             "Regular Income", "Home Purchase",
                                             "Business Investment", "Travel/Leisure"],
                                            default=st.session_state.user_profile.get('investment_goals', []),
                                            help="Required - Select at least one goal")
            
            investment_experience = st.selectbox("Investment Experience *",
                                               ["Please select...",
                                                "Beginner - No prior experience",
                                                "Intermediate - Some experience",
                                                "Advanced - Experienced investor"],
                                               index=0 if st.session_state.user_profile.get('investment_experience', '') == '' else
                                               ["Please select...", "Beginner", "Intermediate", "Advanced"].index(
                                                   st.session_state.user_profile.get('investment_experience', 'Beginner')) + 1)
            
            preferred_sectors = st.multiselect("Preferred Investment Sectors (Optional)",
                                             ["Government Securities", "Banking/Finance", "Real Estate",
                                              "Technology", "Agriculture", "Energy", "Manufacturing",
                                              "Telecommunications", "No Preference"],
                                             default=st.session_state.user_profile.get('preferred_sectors', []))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.current_step = 2
                st.rerun()
        
        with col2:
            if st.button("Get Recommendations →", type="primary"):
                # Validation
                errors = []
                if risk_tolerance == "Please select...":
                    errors.append("Risk Tolerance is required")
                if investment_horizon == "Please select...":
                    errors.append("Investment Time Horizon is required")
                if investment_amount < 1000:
                    errors.append("Investment Amount must be at least KES 1,000")
                if not investment_goals or len(investment_goals) == 0:
                    errors.append("Please select at least one Investment Goal")
                if investment_experience == "Please select...":
                    errors.append("Investment Experience is required")
                
                # Check if investment amount exceeds disposable income
                disposable_income = st.session_state.user_profile.get('disposable_income', 0)
                if investment_amount > disposable_income:
                    st.warning(f"⚠️ Your investment amount (KES {investment_amount:,}) exceeds your disposable income (KES {disposable_income:,}). Consider reducing the amount.")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Extract risk tolerance level
                    risk_level = risk_tolerance.split(' - ')[0]
                    st.session_state.user_profile.update({
                        'risk_tolerance': risk_level,
                        'investment_horizon': investment_horizon,
                        'investment_amount': investment_amount,
                        'investment_goals': investment_goals,
                        'investment_experience': investment_experience.split(' - ')[0],
                        'preferred_sectors': preferred_sectors
                    })
                    st.session_state.current_step = 4
                    st.rerun()
    
    # Step 4: Recommendations
    elif st.session_state.current_step == 4:
        st.markdown('<h1 class="main-header">🎯 Your Personalized Investment Recommendations</h1>', unsafe_allow_html=True)
        
        # Display user summary
        with st.expander("📋 Your Profile Summary"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Name:** {st.session_state.user_profile.get('name')}")
                st.write(f"**Age:** {st.session_state.user_profile.get('age')}")
                st.write(f"**Location:** {st.session_state.user_profile.get('location')}")
                st.write(f"**Monthly Income:** KES {st.session_state.user_profile.get('monthly_income'):,}")
            with col2:
                st.write(f"**Risk Tolerance:** {st.session_state.user_profile.get('risk_tolerance')}")
                st.write(f"**Investment Horizon:** {st.session_state.user_profile.get('investment_horizon')}")
                st.write(f"**Investment Amount:** KES {st.session_state.user_profile.get('investment_amount'):,}")
                st.write(f"**Experience:** {st.session_state.user_profile.get('investment_experience')}")
            with col3:
                goals = st.session_state.user_profile.get('investment_goals', [])
                st.write(f"**Goals:** {', '.join(goals) if goals else 'None specified'}")
                disposable = st.session_state.user_profile.get('disposable_income', 0)
                st.write(f"**Disposable Income:** KES {disposable:,}")
        
        # Generate recommendations
        recommendations = system.get_recommendations(user_data=st.session_state.user_profile)

        # Display recommendations
        st.markdown('<h2 class="sub-header">🏆 Top Recommendations for You</h2>', unsafe_allow_html=True)
        if recommendations and recommendations.get('detailed_products'):
            # Get the products list first
            recommendations_list = recommendations.get('detailed_products', [])
            
            # Then slice the first 3 items
            top_recommendations = recommendations_list[:4]
            
            for i, rec in enumerate(top_recommendations, 1):
                risk_class = f"risk-{rec['risk_level']}"
                
                st.markdown(f"""
                <div class="card {risk_class}">
                    <h3>#{i} {rec['name']}</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <span><strong>Risk Level:</strong> {rec['risk_level']}</span>
                        <span><strong>Expected Return:</strong> {rec['expected_return']}</span>
                        <span><strong>Liquidity:</strong> {rec['liquidity']}</span>
                        <span><strong>Suitability:</strong> {rec['suitability_score']:.1%}</span>
                    </div>
                    <p>{rec['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show pros and cons in expandable sections
                with st.expander(f"View details for {rec['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**✅ Advantages:**")
                        for pro in rec['pros']:
                            st.write(f"• {pro}")
                    with col2:
                        st.markdown("**⚠️ Considerations:**")
                        for con in rec['cons']:
                            st.write(f"• {con}")
        else:
            st.error("Unable to generate recommendations. Please try again.")


        # Portfolio allocation chart
        st.markdown('<h2 class="sub-header">📊 Recommended Portfolio Allocation</h2>', unsafe_allow_html=True)
        
        # Create sample allocation based on risk tolerance
        risk_tolerance = st.session_state.user_profile.get('risk_tolerance', 'Medium')
        
        if risk_tolerance == 'Low':
            allocation = {
                'Government Bonds (Treasury Bonds)': 20,
                'Treasury Bills (T-Bills)': 15,
                'Money Market Funds': 15,
                'Bank Fixed Deposits': 10,
                'High-Yield Savings Accounts': 10,
                'Pension Schemes (Individual & Occupational)': 10,
                'Education Savings Plans': 10,
                'Cooperative Society Investments (SACCOs)': 10
                }
        elif risk_tolerance == 'Medium':
            allocation = {
                'Unit Trusts/Mutual Funds': 15,
                'Real Estate Investment': 15,
                'Real Estate Investment Trusts (REITs)': 10,
                'Nairobi Securities Exchange (NSE) Stocks': 10,
                'Money Market Funds': 10,
                'Government Bonds (Treasury Bonds)': 10,
                'Treasury Bills (T-Bills)': 5,
                'Cooperative Society Investments (SACCOs)': 5,
                'Agricultural Investment': 10,
                'Pension Schemes (Individual & Occupational)': 5,
                'Education Savings Plans': 5
                }
        else:  # High
            allocation = {
                'Nairobi Securities Exchange (NSE) Stocks': 20,
                'Commodity Trading': 15,
                'Small Business Investment/Entrepreneurship': 15,
                'Real Estate Investment Trusts (REITs)': 10,
                'Unit Trusts/Mutual Funds': 10,
                'Foreign Exchange (Forex) Trading': 10,
                'Real Estate Investment': 5,
                'Agricultural Investment': 5,
                'Cooperative Society Investments (SACCOs)': 5,
                'Government Bonds (Treasury Bonds)': 5
                }
        
        # Adjust pie chart colors based on theme
        colors = ['#2E8B57', '#4682B4', '#FF9800', '#F44336', '#9C27B0'] if st.session_state.theme == 'light' else ['#4CAF50', '#81C784', '#FFA726', '#EF5350', '#BA68C8']
        text_color = 'black' if st.session_state.theme == 'light' else 'white'

        fig = px.pie(values=list(allocation.values()), names=list(allocation.keys()), 
                     title="Recommended Portfolio Distribution", color_discrete_sequence=colors)
        fig.update_traces(
                        textposition='outside', 
                        textinfo='percent+label',
                        outsidetextfont=dict(color=text_color)
                        )
        
        # Adjust chart background based on theme
        if st.session_state.theme == 'dark':
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=text_color),
                legend=dict(font=dict(color=text_color))
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Action items
        st.markdown('<h2 class="sub-header">📝 Next Steps</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h4>🎯 Immediate Actions</h4>
                <ul>
                    <li>Research recommended investment options</li>
                    <li>Set up emergency fund if not available</li>
                    <li>Compare fees and terms across providers</li>
                    <li>Start with smaller amounts initially</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h4>💡 Long-term Strategy</h4>
                <ul>
                    <li>Diversify investments across asset classes</li>
                    <li>Review and rebalance portfolio annually</li>
                    <li>Increase investment amounts as income grows</li>
                    <li>Stay informed about market conditions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Reset and download options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("← Back to Preferences"):
                st.session_state.current_step = 3
                st.rerun()
        
        with col2:
            if st.button("🔄 New Assessment", type="primary"):
                st.session_state.current_step = 1
                st.session_state.user_profile = {}
                st.rerun()
        
        with col3:
            # Create downloadable report
            report_data = {
            'user_profile': st.session_state.user_profile,
            # Get the first 4 recommendations from the detailed_products list
            'recommendations': recommendations.get('detailed_products', [])[:4],
            'portfolio_allocation': allocation,
            'generated_date': datetime.now().isoformat()
            }
            
            st.download_button(
                label="📄 Download Report",
                data=json.dumps(report_data, indent=2),
                file_name=f"investment_recommendations_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

# INVESTMENT OPTIONS PAGE
elif page == "📊 Investments":
    st.markdown('<h1 class="main-header">📊 Kenya Investment Options Guide</h1>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        risk_filter = st.selectbox("Filter by Risk Level", 
                                 ["All", "Low", "Medium", "High", "Very High"])
    
    with col2:
        liquidity_filter = st.selectbox("Filter by Liquidity", 
                                      ["All", "High", "Medium", "Low", "Very Low"])
    
    # Get all products
    products = system.investment_products
    
    # Filter products
    filtered_products = {}
    for name, details in products.items():
        if risk_filter != "All" and details['risk_level'] != risk_filter:
            continue
        if liquidity_filter != "All" and details['liquidity'] != liquidity_filter:
            continue
        filtered_products[name] = details
    
    # Display products
    st.markdown(f'<h2 class="sub-header">Found {len(filtered_products)} Investment Options</h2>', unsafe_allow_html=True)
    
    for name, details in filtered_products.items():
        risk_class = f"risk-{details['risk_level']}" #.lower().replace(' ', '-')
        
        with st.expander(f"🔍 {name} - {details['risk_level']} Risk | {details['expected_return']} Returns"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {details['description']}")
                
                # Key metrics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Risk Level", details['risk_level'])
                with col_b:
                    st.metric("Expected Return", details['expected_return'])
                with col_c:
                    st.metric("Liquidity", details['liquidity'])
            
            with col2:
                # Risk indicator
                risk_colors = {
                    'Low': '#28a745' if st.session_state.theme == 'light' else '#4CAF50',
                    'Medium': '#ffc107' if st.session_state.theme == 'light' else '#FF9800', 
                    'High': '#dc3545' if st.session_state.theme == 'light' else '#F44336',
                    'Very High': '#6f42c1' if st.session_state.theme == 'light' else '#BA68C8'
                }
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = {'Low': 25, 'Medium': 50, 'High': 75, 'Very High': 100}[details['risk_level']],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Risk Level"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': risk_colors[details['risk_level']]},
                        'steps': [
                            {'range': [0, 25], 'color': "lightgray"},
                            {'range': [25, 50], 'color': "gray"},
                            {'range': [50, 75], 'color': "lightgray"},
                            {'range': [75, 100], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                
                # Adjust gauge background based on theme
                if st.session_state.theme == 'dark':
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                
                st.plotly_chart(fig, use_container_width=True, key=f"risk_gauge_{name}")
            
            # Pros and Cons
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Advantages:**")
                for pro in details['pros']:
                    st.write(f"• {pro}")
            
            with col2:
                st.markdown("**⚠️ Considerations:**")
                for con in details['cons']:
                    st.write(f"• {con}")

# ABOUT US PAGE
elif page == "ℹ️ About Us":
    st.markdown('<h1 class="main-header">ℹ️ About Kenya Investment Advisor</h1>', unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>Our Mission</h2>
            <p style="font-size: 1.1rem;">
                To democratize investment knowledge and make professional-grade financial advice 
                accessible to every Kenyan, regardless of their economic background or investment experience.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h2>What We Do</h2>
            <p>
                Kenya Investment Advisor is an AI-powered platform that provides personalized 
                investment recommendations tailored to the Kenyan market. Our system analyzes 
                your financial profile, risk tolerance, and investment goals to suggest the 
                most suitable investment options from Kenya's diverse financial landscape.
            </p>
        </div>
        """, unsafe_allow_html=True)

    
    # Our approach
    st.markdown('<h2 class="sub-header">🔬 Our Approach</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 Data-Driven</h3>
            <p>
                We use advanced machine learning algorithms trained on comprehensive 
                financial data to provide accurate and reliable recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🇰🇪 Kenya-Focused</h3>
            <p>
                Our recommendations are specifically designed for the Kenyan market, 
                considering local regulations, economic conditions, and cultural factors.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>👤 Personalized</h3>
            <p>
                Every recommendation is tailored to your unique financial situation, 
                goals, and risk tolerance - no one-size-fits-all solutions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Why choose us
    st.markdown('<h2 class="sub-header">🌟 Why Choose Kenya Investment Advisor?</h2>', unsafe_allow_html=True)
    
    advantages = [
        ("🆓 Free to Use", "Our basic investment recommendations are completely free, making professional advice accessible to everyone."),
        ("🔒 Secure & Private", "We prioritize your data security and privacy. Your personal information is never shared with third parties."),
        ("📚 Educational", "Beyond recommendations, we provide comprehensive information about each investment option to help you make informed decisions."),
        ("🚀 Continuously Updated", "Our algorithms and investment data are regularly updated to reflect current market conditions and new opportunities."),
        ("💬 User-Friendly", "Simple, intuitive interface designed for users of all technical backgrounds and experience levels."),
        ("🎯 Comprehensive Coverage", "We cover 16+ different investment options available in Kenya, from government securities to alternative investments.")
    ]
    
    for title, description in advantages:
        st.markdown(f"""
        <div class="card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology section
    if hasattr(system, 'get_model_info'):
        model_info = system.get_model_info()
        
        st.markdown('<h2 class="sub-header">🤖 AI System Status</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if model_info['models_loaded']:
                st.markdown("""
                <div class="card">
                    <h3>✅ Advanced ML Models Active</h3>
                    <p>Using trained machine learning models for enhanced prediction accuracy.</p>
                    <p><strong>Active Model:</strong> {}</p>
                </div>
                """.format(model_info['best_model']), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card">
                    <h3>📊 Rule-Based System Active</h3>
                    <p>Using expert-designed rules and heuristics for reliable recommendations.</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card">
                <h3>Development Framework</h3>
                <ul>
                    <li>Python for backend processing</li>
                    <li>Streamlit for user interface</li>
                    <li>Scikit-learn for machine learning</li>
                    <li>Plotly for data visualization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
       
    # Team section (placeholder)
    st.markdown('<h2 class="sub-header">👥 Our Commitment</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p style="font-size: 1.1rem; text-align: center; font-style: italic;">
            "We believe that everyone deserves access to quality financial advice. Our team is committed 
            to continuously improving our platform and expanding our services to better serve the Kenyan 
            investment community."
        </p>
    </div>
    """, unsafe_allow_html=True)
    

# CONTACT PAGE
elif page == "📞 Contact":
    st.markdown('<h1 class="main-header">📞 Contact Us</h1>', unsafe_allow_html=True)
    
    # Contact information
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>Get In Touch</h2>
            <p>We'd love to hear from you! Whether you have questions about our recommendations, 
            need technical support, or want to provide feedback, we're here to help.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contact details
        st.markdown("""
        <div class="card">
            <h3>📧 Email</h3>
            <p><strong>General Inquiries:</strong> info@kenyainvestmentadvisor.com</p>
            <p><strong>Technical Support:</strong> support@kenyainvestmentadvisor.com</p>
            <p><strong>Partnerships:</strong> partnerships@kenyainvestmentadvisor.com</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>📱 Phone</h3>
            <p><strong>Main Line:</strong> +254 700 000 000</p>
            <p><strong>WhatsApp:</strong> +254 700 000 001</p>
            <p><strong>Hours:</strong> Monday-Friday, 8AM-6PM EAT</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>🌐 Social Media</h3>
            <p><strong>LinkedIn:</strong> KenyaInvestmentAdvisor</p>
            <p><strong>Twitter:</strong> @KenyaInvestAI</p>
            <p><strong>Facebook:</strong> Kenya Investment Advisor</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contact form
        st.markdown("""
        <div class="card">
            <h3>💬 Send us a Message</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number")
            
            subject = st.selectbox("Subject", [
                "General Inquiry",
                "Technical Support",
                "Investment Question", 
                "Partnership Opportunity",
                "Feedback/Suggestion",
                "Other"
            ])
            
            message = st.text_area("Message *", height=150)
            
            # Privacy consent
            consent = st.checkbox("I agree to the privacy policy and terms of service")
            
            submitted = st.form_submit_button("Send Message", type="primary")
            
            if submitted:
                if name and email and message and consent:
                    st.success("✅ Thank you! Your message has been sent successfully. We'll get back to you within 24 hours.")
                    
                    # Here you would typically send the email or save to database
                    # For demo purposes, we'll just show a success message
                    
                else:
                    st.error("❌ Please fill in all required fields and accept the privacy policy.")
    
    # FAQ Section
    st.markdown('<h2 class="sub-header">❓ Frequently Asked Questions</h2>', unsafe_allow_html=True)
    
    faqs = [
        ("Is the service really free?", "Yes, our basic investment recommendations are completely free. We believe everyone should have access to quality financial advice."),
        ("How accurate are your recommendations?", "Our AI models are trained on comprehensive financial data and achieve high accuracy rates. However, all investments carry risk and past performance doesn't guarantee future results."),
        ("Do you provide financial planning services?", "Currently, we focus on investment recommendations. For comprehensive financial planning, we recommend consulting with a certified financial planner."),
        ("How often should I update my profile?", "We recommend updating your profile annually or whenever your financial situation changes significantly (job change, major life events, etc.)."),
        ("Can I invest directly through your platform?", "We provide recommendations only. To make investments, you'll need to contact the respective financial institutions or brokers."),
        ("Is my personal information secure?", "Yes, we take data security seriously. Your information is encrypted and never shared with third parties without your consent.")
    ]
    
    for question, answer in faqs:
        with st.expander(f"🤔 {question}"):
            st.write(answer)
    
    # Office hours and response times
    st.markdown('<h2 class="sub-header">⏰ Response Times</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>📧 Email</h4>
            <p><strong>Response Time:</strong> Within 24 hours</p>
            <p><strong>Best for:</strong> Detailed inquiries, technical issues</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>📱 Phone/WhatsApp</h4>
            <p><strong>Response Time:</strong> Immediate during business hours</p>
            <p><strong>Best for:</strong> Urgent questions, quick clarifications</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4>🌐 Social Media</h4>
            <p><strong>Response Time:</strong> Within 4-6 hours</p>
            <p><strong>Best for:</strong> General questions, community discussions</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
footer_card_class = "card" if st.session_state.theme == 'light' else "card"
st.markdown(f"""
<div class="{footer_card_class}" style="text-align: center; margin-top: 2rem;">
    <h4>🏛️ Kenya Investment Advisor</h4>
    <p>Empowering Kenyans to make informed investment decisions</p>
    <p>© 2024 Kenya Investment Advisor. All rights reserved.</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        <strong>Disclaimer:</strong> This platform provides educational information and general investment guidance only. 
        It is not personalized investment advice. Please consult with qualified financial professionals before making investment decisions.
    </p>
</div>
""", unsafe_allow_html=True)
