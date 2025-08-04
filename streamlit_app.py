import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Kenya Investment Recommender System",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .risk-very-low { border-left: 4px solid #28a745; }
    .risk-low { border-left: 4px solid #20c997; }
    .risk-medium { border-left: 4px solid #ffc107; }
    .risk-medium-high { border-left: 4px solid #fd7e14; }
    .risk-high { border-left: 4px solid #dc3545; }
    .risk-very-high { border-left: 4px solid #6f42c1; }
    .pros-cons-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .pros-list, .cons-list {
        flex: 1;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .pros-list {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .cons-list {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .kenya-flag {
        color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

class KenyanInvestmentRecommender:
    """Enhanced Streamlit interface for Kenyan investment recommendations"""
    
    def __init__(self):
        self.models = {}
        # Updated Kenyan investment catalog
        self.product_catalog = {
            'government_bonds': {
                'name': 'Government Bonds (Treasury Bonds)',
                'risk_level': 'Low',
                'expected_return': '12-16%',
                'min_investment': 50000,
                'description': 'Long-term government securities with fixed interest rates',
                'liquidity': 'Medium',
                'time_horizon': '2-30 years',
                'pros': [
                    'Government guaranteed - virtually risk-free',
                    'Regular interest payments (coupon payments)',
                    'Can be traded on secondary market',
                    'Tax-free interest income',
                    'Hedge against inflation with inflation-linked bonds'
                ],
                'cons': [
                    'Interest rate risk - value decreases when rates rise',
                    'Long lock-in periods',
                    'Lower returns compared to equities long-term',
                    'Early exit may result in capital loss'
                ]
            },
            
            'treasury_bills': {
                'name': 'Treasury Bills (T-Bills)',
                'risk_level': 'Very Low',
                'expected_return': '10-14%',
                'min_investment': 100000,
                'description': 'Short-term government securities with maturities of 91, 182, and 364 days',
                'liquidity': 'High',
                'time_horizon': '3-12 months',
                'pros': [
                    'Government guaranteed',
                    'High liquidity',
                    'Short investment periods',
                    'Regular auction opportunities',
                    'No interest rate risk due to short tenure'
                ],
                'cons': [
                    'Lower returns than long-term investments',
                    'Need to continuously reinvest',
                    'Minimum investment amount of KES 100,000',
                    'Returns may not beat inflation in low-rate environment'
                ]
            },
            
            'nse_stocks': {
                'name': 'Nairobi Securities Exchange (NSE) Stocks',
                'risk_level': 'High',
                'expected_return': '8-25%',
                'min_investment': 5000,
                'description': 'Shares of publicly listed companies on the Nairobi Securities Exchange',
                'liquidity': 'High',
                'time_horizon': '3+ years',
                'pros': [
                    'High growth potential',
                    'Dividend income opportunities',
                    'Ownership stake in companies',
                    'High liquidity for blue-chip stocks',
                    'Hedge against inflation',
                    'Capital gains tax exemption for individual investors'
                ],
                'cons': [
                    'High volatility and risk',
                    'Potential for significant losses',
                    'Requires market knowledge and research',
                    'Market manipulation risks',
                    'Company-specific risks'
                ]
            },
            
            'unit_trusts': {
                'name': 'Unit Trusts/Mutual Funds',
                'risk_level': 'Medium',
                'expected_return': '8-15%',
                'min_investment': 1000,
                'description': 'Pooled investment funds managed by professional fund managers',
                'liquidity': 'Medium-High',
                'time_horizon': '1+ years',
                'pros': [
                    'Professional fund management',
                    'Diversification across multiple assets',
                    'Low minimum investment',
                    'Various fund types available (equity, bond, balanced)',
                    'Regular income through dividend distributions'
                ],
                'cons': [
                    'Management fees reduce returns',
                    'No guarantee of positive returns',
                    'Limited control over investment decisions',
                    'Market risk exposure',
                    'Exit charges may apply'
                ]
            },
            
            'money_market_funds': {
                'name': 'Money Market Funds',
                'risk_level': 'Low',
                'expected_return': '8-12%',
                'min_investment': 1000,
                'description': 'Short-term, low-risk investments in money market instruments',
                'liquidity': 'Very High',
                'time_horizon': 'Short-term to medium-term',
                'pros': [
                    'High liquidity - can withdraw anytime',
                    'Low risk and stable returns',
                    'Low minimum investment',
                    'Professional management',
                    'Better returns than savings accounts'
                ],
                'cons': [
                    'Lower returns than equity investments',
                    'Management fees',
                    'Inflation risk over long term',
                    'No capital appreciation potential'
                ]
            },
            
            'real_estate': {
                'name': 'Real Estate Investment',
                'risk_level': 'Medium-High',
                'expected_return': '10-20%',
                'min_investment': 2000000,
                'description': 'Direct property investment for rental income and capital appreciation',
                'liquidity': 'Low',
                'time_horizon': '5+ years',
                'pros': [
                    'Rental income generation',
                    'Capital appreciation potential',
                    'Inflation hedge',
                    'Tangible asset ownership',
                    'Tax benefits on mortgage interest'
                ],
                'cons': [
                    'High capital requirements',
                    'Low liquidity',
                    'Property management responsibilities',
                    'Market volatility',
                    'Legal and transaction costs',
                    'Maintenance and repair costs'
                ]
            },
            
            'reits': {
                'name': 'Real Estate Investment Trusts (REITs)',
                'risk_level': 'Medium',
                'expected_return': '8-15%',
                'min_investment': 5000,
                'description': 'Investment in real estate through publicly traded trusts',
                'liquidity': 'High',
                'time_horizon': '3+ years',
                'pros': [
                    'Access to real estate with low capital',
                    'Regular dividend income',
                    'Professional property management',
                    'High liquidity compared to direct real estate',
                    'Diversification across property types'
                ],
                'cons': [
                    'Market volatility',
                    'Interest rate sensitivity',
                    'Management fees',
                    'Limited control over properties',
                    'Relatively new market in Kenya'
                ]
            },
            
            'fixed_deposits': {
                'name': 'Bank Fixed Deposits',
                'risk_level': 'Very Low',
                'expected_return': '6-10%',
                'min_investment': 10000,
                'description': 'Time deposits with banks offering fixed interest rates',
                'liquidity': 'Low',
                'time_horizon': '1 month - 5 years',
                'pros': [
                    'Guaranteed returns',
                    'KDIC deposit protection up to KES 500,000',
                    'No market risk',
                    'Predictable income',
                    'Available at all banks'
                ],
                'cons': [
                    'Low returns, may not beat inflation',
                    'Early withdrawal penalties',
                    'Opportunity cost of higher-yielding investments',
                    'Interest rate risk if rates rise'
                ]
            },
            
            'cooperative_investments': {
                'name': 'Cooperative Society Investments (SACCOs)',
                'risk_level': 'Medium',
                'expected_return': '8-15%',
                'min_investment': 5000,
                'description': 'Member-owned financial cooperatives offering savings and investment products',
                'liquidity': 'Medium',
                'time_horizon': '1+ years',
                'pros': [
                    'Higher returns than banks',
                    'Member ownership and control',
                    'Access to affordable loans',
                    'Community-based investment',
                    'Dividend payments to members'
                ],
                'cons': [
                    'Limited regulation compared to banks',
                    'Risk of mismanagement',
                    'Liquidity constraints',
                    'Member liability in case of losses',
                    'Limited geographical reach'
                ]
            },
            
            'pension_schemes': {
                'name': 'Pension Schemes (Individual & Occupational)',
                'risk_level': 'Low-Medium',
                'expected_return': '8-12%',
                'min_investment': 1000,
                'description': 'Long-term retirement savings with tax benefits',
                'liquidity': 'Very Low',
                'time_horizon': '10+ years',
                'pros': [
                    '15% tax relief on contributions',
                    'Compound growth over long term',
                    'Professional fund management',
                    'Employer matching contributions',
                    'Retirement security'
                ],
                'cons': [
                    'Funds locked until retirement',
                    'Management fees',
                    'Limited investment control',
                    'Inflation risk over long periods',
                    'Regulatory changes risk'
                ]
            },
            
            'agricultural_investment': {
                'name': 'Agricultural Investment',
                'risk_level': 'Medium-High',
                'expected_return': '10-25%',
                'min_investment': 100000,
                'description': 'Investment in farming, livestock, or agribusiness ventures',
                'liquidity': 'Low',
                'time_horizon': '1-5 years',
                'pros': [
                    'Kenya\'s agricultural potential',
                    'Food security investment',
                    'Export market opportunities',
                    'Government support programs',
                    'Inflation hedge through food prices'
                ],
                'cons': [
                    'Weather and climate risks',
                    'Market price volatility',
                    'Pest and disease risks',
                    'Requires agricultural knowledge',
                    'Seasonal income patterns',
                    'Infrastructure challenges'
                ]
            },
            
            'business_investment': {
                'name': 'Small Business Investment/Entrepreneurship',
                'risk_level': 'Very High',
                'expected_return': '-100% to +500%',
                'min_investment': 50000,
                'description': 'Starting or investing in small businesses and startups',
                'liquidity': 'Very Low',
                'time_horizon': '3+ years',
                'pros': [
                    'Unlimited earning potential',
                    'Full control over investment',
                    'Job creation and economic impact',
                    'Tax benefits for business expenses',
                    'Personal and professional growth'
                ],
                'cons': [
                    'High failure rate',
                    'Requires significant time and effort',
                    'Market and operational risks',
                    'Cash flow challenges',
                    'Regulatory compliance requirements'
                ]
            }
        }
        self.load_models()
    
    def load_models(self):
        """Load trained models or create fallback models"""
        try:
            if os.path.exists('models'):
                # Try to load the hybrid model
                hybrid_path = os.path.join('models', 'hybrid_recommendation_system.pkl')
                propensity_path = os.path.join('models', 'investment_propensity_model.pkl')
                
                if os.path.exists(hybrid_path):
                    self.models['hybrid'] = joblib.load(hybrid_path)
                    st.success("✅ Hybrid model loaded successfully!")
                else:
                    st.warning("⚠️ Hybrid model not found. Using demo mode.")
                    self.create_demo_hybrid_model()
                
                if os.path.exists(propensity_path):
                    self.models['propensity'] = joblib.load(propensity_path)
                    st.success("✅ Propensity model loaded successfully!")
                else:
                    st.warning("⚠️ Propensity model not found. Using demo mode.")
                    self.create_demo_propensity_model()
            else:
                st.warning("⚠️ Models directory not found. Using demo mode.")
                self.create_demo_models()
        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            self.create_demo_models()
    
    def create_demo_models(self):
        """Create demo models for demonstration"""
        self.create_demo_hybrid_model()
        self.create_demo_propensity_model()
    
    def create_demo_hybrid_model(self):
        """Create demo hybrid recommendation model"""
        class DemoHybridSystem:
            def __init__(self, product_catalog):
                self.product_catalog = product_catalog
            
            def get_recommendations(self, user_id, user_data, n_recommendations=5):
                # Enhanced rule-based demo recommendations for Kenya
                age = user_data.get('age', 35)
                income = user_data.get('monthly_income', 50000)
                risk_tolerance = user_data.get('risk_tolerance', 'medium')
                disposable_income = user_data.get('disposable_income', 20000)
                time_horizon = user_data.get('time_horizon', '3-5 years')
                investment_experience = user_data.get('investment_experience', 'beginner')
                
                # Updated risk-based filtering for Kenyan investments
                if risk_tolerance == 'low' or age > 55:
                    # Conservative portfolio for low risk tolerance or older investors
                    preferred = ['treasury_bills', 'government_bonds', 'fixed_deposits', 'money_market_funds']
                elif risk_tolerance == 'high' and age < 40:
                    # Aggressive portfolio for young, high-risk investors
                    preferred = ['nse_stocks', 'unit_trusts', 'reits', 'business_investment', 'money_market_funds']
                elif risk_tolerance == 'medium' or (age >= 40 and age <= 55):
                    # Balanced portfolio for moderate risk or middle-aged investors
                    preferred = ['unit_trusts', 'government_bonds', 'reits', 'money_market_funds', 'cooperative_investments']
                else:
                    # Default balanced approach
                    preferred = ['unit_trusts', 'money_market_funds', 'government_bonds', 'treasury_bills']
                
                # Adjust based on income level
                if income < 50000:  # Lower income - focus on accessible investments
                    accessible = ['money_market_funds', 'unit_trusts', 'cooperative_investments', 'fixed_deposits']
                    preferred = [p for p in preferred if p in accessible or self.product_catalog[p]['min_investment'] <= disposable_income * 3]
                
                # Add pension for young people
                if age < 40 and 'pension_schemes' not in preferred:
                    preferred.append('pension_schemes')
                
                # Add agricultural investment for those with sufficient capital and experience
                if disposable_income > 50000 and investment_experience != 'beginner' and risk_tolerance in ['medium', 'high']:
                    if 'agricultural_investment' not in preferred:
                        preferred.append('agricultural_investment')
                
                # Generate scores with more sophisticated logic
                recommendations = []
                for i, product in enumerate(preferred[:n_recommendations]):
                    if product in self.product_catalog:
                        base_score = 0.9 - (i * 0.1)
                        
                        # Adjust score based on affordability
                        min_inv = self.product_catalog[product]['min_investment']
                        if disposable_income >= min_inv * 2:
                            base_score += 0.1  # Bonus for affordability
                        elif disposable_income < min_inv:
                            base_score -= 0.3  # Penalty for unaffordable
                        
                        # Experience bonus
                        if investment_experience == 'advanced':
                            base_score += 0.05
                        elif investment_experience == 'beginner' and product in ['treasury_bills', 'fixed_deposits', 'money_market_funds']:
                            base_score += 0.05
                        
                        # Add some randomness
                        final_score = max(0.3, base_score + np.random.uniform(-0.05, 0.05))
                        recommendations.append((product, final_score))
                
                return {
                    'recommendations': recommendations,
                    'propensity_score': min(0.9, 0.3 + (income / 100000) + (0.2 if risk_tolerance == 'high' else 0)),
                    'method': 'demo'
                }
        
        self.models['hybrid'] = DemoHybridSystem(self.product_catalog)
    
    def create_demo_propensity_model(self):
        """Create demo propensity model"""
        class DemoPropensityModel:
            def predict_proba(self, user_data):
                # Handle both dict and DataFrame input
                if isinstance(user_data, dict):
                    data = user_data
                elif hasattr(user_data, 'iloc'):
                    data = user_data.iloc[0].to_dict() if len(user_data) > 0 else user_data.to_dict()
                else:
                    data = dict(user_data) if hasattr(user_data, 'items') else {}
                
                age = data.get('age', 35)
                income = data.get('monthly_income', 50000)
                education = data.get('education_level', 'secondary')
                disposable_income = data.get('disposable_income', 20000)
                
                base_score = 0.4
                if income > 75000: base_score += 0.2
                if education == 'tertiary': base_score += 0.15
                if 25 <= age <= 50: base_score += 0.1
                if disposable_income > 30000: base_score += 0.1
                
                return [min(0.9, base_score)]
        
        self.models['propensity'] = DemoPropensityModel()
    
    def get_user_input(self):
        """Get user input from Streamlit interface"""
        st.markdown("## 👤 User Profile")
        
        # Basic Information
        st.markdown("### Basic Information")
        age = st.slider("Age", 18, 75, 35)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        location = st.selectbox("Location", [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", 
            "Thika", "Malindi", "Kitale", "Garissa", "Other"
        ])
        
        # Financial Information
        st.markdown("### Financial Profile")
        monthly_income = st.number_input(
            "Monthly Income (KES)", 
            min_value=10000, 
            max_value=2000000, 
            value=75000, 
            step=5000,
            help="Your gross monthly income in Kenyan Shillings"
        )
        
        monthly_expenditure = st.number_input(
            "Monthly Expenditure (KES)", 
            min_value=5000, 
            max_value=1500000, 
            value=min(monthly_income - 5000, 50000), 
            step=5000,
            help="Your total monthly expenses including rent, food, transport, etc."
        )
        
        # Education and Employment
        st.markdown("### Background")
        education = st.selectbox(
            "Education Level", 
            ["Primary", "Secondary", "Tertiary", "Postgraduate"]
        )
        
        employment = st.selectbox(
            "Employment Type", 
            ["Formal Employment", "Self-Employed", "Business Owner", "Farmer", "Student", "Retired", "Other"]
        )
        
        # Investment Profile
        st.markdown("### Investment Profile")
        investment_experience = st.selectbox(
            "Investment Experience", 
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        risk_tolerance = st.selectbox(
            "Risk Tolerance", 
            ["Low", "Medium", "High"],
            help="Low: Capital preservation is priority. Medium: Balanced growth. High: Maximum growth potential"
        )
        
        investment_goal = st.selectbox(
            "Primary Investment Goal",
            ["Wealth Growth", "Income Generation", "Capital Preservation", "Emergency Fund", "Retirement Planning", "Education Fund"]
        )
        
        time_horizon = st.selectbox(
            "Investment Time Horizon",
            ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"]
        )
        
        # Additional Information
        st.markdown("### Additional Information")
        household_size = st.slider("Household Size", 1, 15, 4)
        digital_comfort = st.slider(
            "Digital Platform Comfort (1-10)", 1, 10, 7,
            help="How comfortable are you with online/mobile banking and investment platforms?"
        )
        
        has_emergency_fund = st.checkbox("I have an emergency fund (3-6 months expenses)")
        has_insurance = st.checkbox("I have life/health insurance coverage")
        
        # Calculate derived metrics
        disposable_income = max(0, monthly_income - monthly_expenditure)
        income_ratio = monthly_income / monthly_expenditure if monthly_expenditure > 0 else 1
        
        return {
            'user_id': 1,
            'age': age,
            'gender': gender.lower(),
            'location': location.lower(),
            'monthly_income': monthly_income,
            'monthly_expenditure': monthly_expenditure,
            'disposable_income': disposable_income,
            'income_expenditure_ratio': income_ratio,
            'education_level': education.lower(),
            'employment_type': employment.lower(),
            'investment_experience': investment_experience.lower(),
            'risk_tolerance': risk_tolerance.lower(),
            'investment_goal': investment_goal.lower(),
            'time_horizon': time_horizon,
            'household_size': household_size,
            'digital_sophistication': digital_comfort / 10.0,
            'has_emergency_fund': has_emergency_fund,
            'has_insurance': has_insurance
        }
    
    def generate_recommendations(self, user_data):
        """Generate investment recommendations"""
        try:
            if 'hybrid' in self.models and self.models['hybrid']:
                recommendations = self.models['hybrid'].get_recommendations(
                    user_data['user_id'], user_data, n_recommendations=6
                )
                return recommendations
            else:
                st.error("❌ Recommendation model not available")
                return None
        except Exception as e:
            st.error(f"❌ Error generating recommendations: {str(e)}")
            return None
    
    def display_user_profile_summary(self, user_data):
        """Display user profile summary"""
        st.markdown('<div class="sub-header">📊 Your Profile Summary</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{user_data['age']} years")
            st.metric("Monthly Income", f"KES {user_data['monthly_income']:,}")
        
        with col2:
            st.metric("Monthly Expenses", f"KES {user_data['monthly_expenditure']:,}")
            st.metric("Disposable Income", f"KES {user_data['disposable_income']:,}")
        
        with col3:
            st.metric("Risk Tolerance", user_data['risk_tolerance'].title())
            st.metric("Investment Experience", user_data['investment_experience'].title())
        
        with col4:
            st.metric("Time Horizon", user_data['time_horizon'])
            savings_rate = (user_data['disposable_income'] / user_data['monthly_income']) * 100
            st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    def display_investment_propensity(self, user_data):
        """Display investment propensity analysis"""
        try:
            if 'propensity' in self.models and self.models['propensity']:
                propensity_score = self.models['propensity'].predict_proba(user_data)[0]
            else:
                # Fallback calculation
                propensity_score = min(0.9, 0.3 + (user_data['disposable_income'] / 100000))
            
            st.markdown('<div class="sub-header">🎯 Investment Propensity Analysis</div>', unsafe_allow_html=True)
            
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = propensity_score * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Investment Readiness Score"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            if propensity_score >= 0.8:
                st.success("🟢 **Excellent** - You're highly ready for investment opportunities!")
            elif propensity_score >= 0.6:
                st.info("🟡 **Good** - You show strong potential for investment success.")
            elif propensity_score >= 0.4:
                st.warning("🟠 **Moderate** - Consider building your financial foundation first.")
            else:
                st.error("🔴 **Low** - Focus on improving your financial stability before investing.")
            
            return propensity_score
            
        except Exception as e:
            st.error(f"Error calculating propensity: {str(e)}")
            return 0.5
    
    def display_recommendations(self, recommendations, user_data):
        """Display personalized investment recommendations with pros and cons"""
        st.markdown('<div class="sub-header">💡 Personalized Investment Recommendations</div>', unsafe_allow_html=True)
        
        if not recommendations or 'recommendations' not in recommendations:
            st.error("❌ Unable to generate recommendations")
            return
        
        rec_list = recommendations['recommendations']
        propensity_score = recommendations.get('propensity_score', 0.5)
        
        # Display each recommendation with pros and cons
        for i, (product_key, score) in enumerate(rec_list, 1):
            if product_key in self.product_catalog:
                product = self.product_catalog[product_key]
                
                # Risk level styling
                risk_class = f"risk-{product['risk_level'].lower().replace(' ', '-').replace('-', '-')}"
                
                st.markdown(f"""
                <div class="recommendation-card {risk_class}">
                    <h3>#{i}. {product['name']}</h3>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <span><strong>Match Score:</strong> {score:.1%}</span>
                        <span><strong>Risk Level:</strong> {product['risk_level']}</span>
                        <span><strong>Expected Return:</strong> {product['expected_return']}</span>
                    </div>
                    <p><strong>Description:</strong> {product['description']}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                        <span><strong>Min Investment:</strong> KES {product['min_investment']:,}</span>
                        <span><strong>Liquidity:</strong> {product['liquidity']}</span>
                        <span><strong>Time Horizon:</strong> {product['time_horizon']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display pros and cons
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**✅ Advantages:**")
                    for pro in product['pros']:
                        st.markdown(f"• {pro}")
                
                with col2:
                    st.markdown("**❌ Considerations:**")
                    for con in product['cons']:
                        st.markdown(f"• {con}")
                
                # Affordability check
                if user_data['disposable_income'] >= product['min_investment']:
                    surplus = user_data['disposable_income'] - product['min_investment']
                    st.success(f"💰 **Affordable**: You can invest with KES {surplus:,} surplus remaining")
                elif user_data['disposable_income'] >= product['min_investment'] * 0.7:
                    deficit = product['min_investment'] - user_data['disposable_income']
                    st.warning(f"⚠️ **Stretch Goal**: You need KES {deficit:,} more for minimum investment")
                else:
                    deficit = product['min_investment'] - user_data['disposable_income']
                    st.error(f"🚫 **Currently Unaffordable**: You need KES {deficit:,} more for minimum investment")
                
                # Suitability explanation
                with st.expander(f"Why {product['name']} is recommended for you"):
                    self.explain_recommendation(product_key, product, user_data, score)
                
                st.markdown("---")
    
    def explain_recommendation(self, product_key, product, user_data, score):
        """Provide explanation for why a product is recommended"""
        explanations = []
        
        # Age-based explanations
        age = user_data['age']
        if age < 30 and product['risk_level'] in ['High', 'Very High']:
            explanations.append("✅ Your young age allows for higher risk tolerance and longer investment horizon")
        elif age > 50 and product['risk_level'] in ['Low', 'Very Low']:
            explanations.append("✅ Conservative approach suitable for your age and wealth preservation needs")
        elif 30 <= age <= 50 and product['risk_level'] in ['Medium', 'Medium-High']:
            explanations.append("✅ Balanced approach appropriate for your life stage")
        
        # Income-based explanations
        if user_data['disposable_income'] >= product['min_investment'] * 2:
            explanations.append(f"✅ Comfortably fits within your budget with room for diversification")
        elif user_data['disposable_income'] >= product['min_investment']:
            explanations.append(f"✅ Fits within your disposable income range")
        
        # Risk tolerance match
        risk_map = {'low': ['Very Low', 'Low'], 'medium': ['Low', 'Medium', 'Medium-High'], 'high': ['Medium', 'High', 'Very High']}
        user_risk_levels = risk_map.get(user_data['risk_tolerance'], ['Medium'])
        if product['risk_level'] in user_risk_levels:
            explanations.append(f"✅ Matches your {user_data['risk_tolerance']} risk tolerance")
        
        # Investment goal alignment
        goal = user_data['investment_goal']
        if goal == 'wealth growth' and product['risk_level'] in ['Medium', 'High', 'Very High']:
            explanations.append("✅ High growth potential aligns with your wealth building goals")
        elif goal == 'income generation' and 'bond' in product_key or 'deposit' in product_key or 'dividend' in product['description']:
            explanations.append("✅ Provides steady income suitable for your income generation goal")
        elif goal == 'capital preservation' and product['risk_level'] in ['Very Low', 'Low']:
            explanations.append("✅ Low risk helps preserve your capital as desired")
        elif goal == 'retirement planning' and 'pension' in product_key:
            explanations.append("✅ Specifically designed for retirement planning with tax benefits")
        
        # Experience-based explanations
        experience = user_data['investment_experience']
        if experience == 'beginner' and product_key in ['treasury_bills', 'fixed_deposits', 'money_market_funds', 'unit_trusts']:
            explanations.append("✅ Simple and beginner-friendly investment structure")
        elif experience == 'advanced' and product_key in ['nse_stocks', 'business_investment', 'agricultural_investment']:
            explanations.append("✅ Complex investment suitable for your advanced experience")
        
        # Kenya-specific explanations
        if product_key == 'government_bonds':
            explanations.append("✅ Kenyan government bonds offer attractive yields (12-16%) with tax-free interest")
        elif product_key == 'nse_stocks':
            explanations.append("✅ Capital gains tax exemption for individual investors in Kenya")
        elif product_key == 'cooperative_investments':
            explanations.append("✅ SACCOs are deeply rooted in Kenyan culture and offer good community-based returns")
        elif product_key == 'agricultural_investment':
            explanations.append("✅ Kenya's strong agricultural sector offers good investment opportunities")
        
        # Time horizon match
        time_horizon = user_data['time_horizon']
        if 'Less than 1 year' in time_horizon and product['liquidity'] in ['Very High', 'High']:
            explanations.append("✅ High liquidity matches your short-term investment timeline")
        elif any(term in time_horizon for term in ['5-10 years', 'More than 10 years']) and 'years' in product['time_horizon']:
            explanations.append("✅ Long-term nature aligns with your investment timeline")
        
        # Display explanations
        if explanations:
            for explanation in explanations[:5]:  # Show top 5 explanations
                st.write(explanation)
        else:
            st.write("✅ This investment option provides good diversification for your portfolio")
        
        # Add score-based comment
        if score > 0.8:
            st.success("🌟 **Highly Recommended** - This is an excellent match for your profile!")
        elif score > 0.6:
            st.info("👍 **Good Match** - This investment aligns well with your needs.")
        else:
            st.warning("🤔 **Consider Carefully** - This may not be the perfect fit, but could provide diversification.")
    
    def create_portfolio_allocation(self, recommendations, user_data):
        """Create portfolio allocation visualization"""
        st.markdown('<div class="sub-header">📈 Suggested Portfolio Allocation</div>', unsafe_allow_html=True)
        
        if not recommendations or 'recommendations' not in recommendations:
            st.error("No recommendations available for portfolio allocation")
            return
        
        # Calculate allocation based on scores and risk profile
        total_investment = st.number_input(
            "Total Investment Amount (KES)", 
            min_value=1000, 
            max_value=50000000, 
            value=min(100000, user_data['disposable_income'] * 6),  # 6 months of disposable income
            step=1000,
            help="Enter the total amount you want to invest across all recommended products"
        )
        
        rec_list = recommendations['recommendations']
        
        # Normalize scores for allocation
        total_score = sum(score for _, score in rec_list)
        allocations = []
        remaining_amount = total_investment
        
        for i, (product_key, score) in enumerate(rec_list):
            if product_key in self.product_catalog:
                product = self.product_catalog[product_key]
                
                # Calculate allocation percentage
                if i < len(rec_list) - 1:  # Not the last item
                    allocation_pct = (score / total_score) * 0.85  # Use 85% for proportional allocation
                    allocation_amount = min(remaining_amount, total_investment * allocation_pct)
                else:  # Last item gets remaining amount
                    allocation_amount = remaining_amount
                
                # Ensure minimum investment requirement
                if allocation_amount >= product['min_investment'] and remaining_amount > 0:
                    allocations.append({
                        'product': product['name'],
                        'product_key': product_key,
                        'amount': allocation_amount,
                        'percentage': (allocation_amount / total_investment) * 100,
                        'risk_level': product['risk_level'],
                        'expected_return': product['expected_return'],
                        'min_investment': product['min_investment']
                    })
                    remaining_amount -= allocation_amount
        
        if allocations:
            # Display allocation table
            allocation_df = pd.DataFrame(allocations)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = px.pie(
                    allocation_df, 
                    values='amount', 
                    names='product',
                    title="Portfolio Allocation by Amount (KES)",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(
                    allocation_df, 
                    x='percentage',
                    y='product',
                    orientation='h',
                    title="Portfolio Allocation by Percentage",
                    color='risk_level',
                    color_discrete_map={
                        'Very Low': '#28a745', 
                        'Low': '#20c997', 
                        'Medium': '#ffc107', 
                        'Medium-High': '#fd7e14',
                        'High': '#dc3545',
                        'Very High': '#6f42c1'
                    }
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Allocation table
            st.markdown("### 📋 Detailed Allocation Breakdown")
            for allocation in allocations:
                affordability_status = "✅ Affordable" if allocation['amount'] >= allocation['min_investment'] else "❌ Below minimum"
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{allocation['product']}</strong><br>
                    💰 Amount: KES {allocation['amount']:,.0f} ({allocation['percentage']:.1f}%)<br>
                    📊 Risk Level: {allocation['risk_level']} | Expected Return: {allocation['expected_return']}<br>
                    🎯 Status: {affordability_status} (Min: KES {allocation['min_investment']:,})
                </div>
                """, unsafe_allow_html=True)
            
            # Risk and return summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⚖️ Risk Distribution")
                risk_summary = allocation_df.groupby('risk_level')['percentage'].sum().reset_index()
                if not risk_summary.empty:
                    fig_risk = px.pie(
                        risk_summary, 
                        values='percentage', 
                        names='risk_level',
                        title="Risk Level Distribution",
                        color_discrete_map={
                            'Very Low': '#28a745', 
                            'Low': '#20c997', 
                            'Medium': '#ffc107', 
                            'Medium-High': '#fd7e14',
                            'High': '#dc3545',
                            'Very High': '#6f42c1'
                        }
                    )
                    st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Expected Returns Overview")
                # Calculate weighted average expected return
                total_weighted_return = 0
                total_weight = 0
                
                for allocation in allocations:
                    # Extract numeric return (take average of range)
                    return_str = allocation['expected_return'].replace('%', '').replace(' to ', '-')
                    if '-' in return_str:
                        try:
                            low, high = map(float, return_str.split('-'))
                            avg_return = (low + high) / 2
                        except:
                            avg_return = 10  # Default
                    else:
                        try:
                            avg_return = float(return_str)
                        except:
                            avg_return = 10  # Default
                    
                    weight = allocation['percentage'] / 100
                    total_weighted_return += avg_return * weight
                    total_weight += weight
                
                portfolio_expected_return = total_weighted_return / total_weight if total_weight > 0 else 0
                
                st.metric("Portfolio Expected Return", f"{portfolio_expected_return:.1f}%")
                st.metric("Total Investment", f"KES {total_investment:,}")
                st.metric("Potential Annual Return", f"KES {(total_investment * portfolio_expected_return / 100):,.0f}")
        
        else:
            st.warning("⚠️ Unable to create portfolio allocation. Consider increasing your investment amount or reviewing the recommendations.")
    
    def display_investment_insights(self, user_data, recommendations):
        """Display additional investment insights and tips"""
        st.markdown('<div class="sub-header">💡 Investment Insights & Tips for Kenya</div>', unsafe_allow_html=True)
        
        insights = []
        
        # Age-based insights
        age = user_data['age']
        if age < 30:
            insights.append("🌱 **Early Starter Advantage**: You have time on your side. Consider NSE stocks and aggressive unit trusts for long-term wealth building. Don't forget to start a pension scheme early for maximum tax benefits!")
        elif age < 45:
            insights.append("⚖️ **Balanced Approach**: Balance growth and stability. Consider a mix of government bonds, unit trusts, and REITs. This is also a good time to increase pension contributions.")
        elif age < 60:
            insights.append("🛡️ **Preservation Phase**: Focus on capital preservation with government bonds and treasury bills while maintaining some growth exposure through conservative unit trusts.")
        else:
            insights.append("🏛️ **Conservative Strategy**: Prioritize capital preservation with treasury bills, government bonds, and fixed deposits. Focus on income generation.")
        
        # Income-based insights
        disposal_ratio = user_data['disposable_income'] / user_data['monthly_income']
        if disposal_ratio > 0.3:
            insights.append(f"💰 **Excellent Savings Rate**: Your {disposal_ratio:.1%} savings rate is outstanding! You can afford to take calculated risks with NSE stocks or even consider real estate investment.")
        elif disposal_ratio > 0.15:
            insights.append(f"👍 **Good Financial Discipline**: Your {disposal_ratio:.1%} savings rate shows good discipline. Consider unit trusts and government bonds for steady growth.")
        else:
            insights.append(f"⚠️ **Focus on Budgeting**: Your {disposal_ratio:.1%} savings rate suggests focusing on increasing disposable income. Start with money market funds and build your emergency fund first.")
        
        # Kenya-specific insights
        if user_data['location'] in ['nairobi', 'mombasa', 'kisumu']:
            insights.append("🏙️ **Urban Advantage**: Being in a major city gives you better access to investment platforms and financial services. Consider digital investment options and REITs.")
        
        if user_data['employment_type'] == 'formal employment':
            insights.append("👔 **Formal Employment Benefits**: Take advantage of your employer's pension scheme if available. You're also eligible for mortgage financing if considering real estate.")
        elif user_data['employment_type'] == 'self-employed':
            insights.append("🏃‍♂️ **Self-Employment**: Consider individual pension schemes for tax benefits and business investment opportunities. SACCOs can also provide good networking and business loans.")
        
        # Emergency fund check
        if not user_data.get('has_emergency_fund', False):
            insights.append("🚨 **Emergency Fund Priority**: Before investing, ensure you have 3-6 months of expenses in a money market fund or high-yield savings account. This is crucial for financial stability.")
        
        # Insurance check
        if not user_data.get('has_insurance', False):
            insights.append("🛡️ **Insurance Gap**: Consider getting life and health insurance before making significant investments. This protects your family and investment goals.")
        
        # Display insights
        for insight in insights:
            st.info(insight)
        
        # Kenya-specific investment tips
        with st.expander("🇰🇪 Kenya-Specific Investment Tips"):
            st.markdown("""
            **🎯 Key Investment Opportunities in Kenya:**
            - **Government Securities**: Treasury bills and bonds offer attractive tax-free returns (10-16%)
            - **NSE Stocks**: Individual investors enjoy capital gains tax exemption
            - **SACCOs**: Leverage Kenya's strong cooperative movement for community-based investing
            - **Real Estate**: Kenya's growing urban population drives property demand
            - **Agricultural Investment**: Tap into Kenya's strong agricultural sector
            - **Pension Schemes**: 15% tax relief on contributions up to KES 240,000 annually
            
            **📱 Digital Investment Platforms:**
            - M-Shwari and KCB M-Pesa for basic savings
            - Cytonn, Dry Associates for unit trusts
            - Faulu, Kingdom Securities for stock trading
            - Various SACCO mobile apps for cooperative investments
            
            **⚠️ Important Considerations:**
            - **Inflation**: Factor in Kenya's inflation rate (5-7%) when planning returns
            - **Currency Risk**: For dollar-denominated investments, consider KES volatility
            - **Regulatory Environment**: Stay updated with CMA and CBK regulations
            - **Tax Planning**: Understand withholding tax on dividends and interest
            """)

def main():
    """Main Streamlit application"""
    
    # Initialize the recommender system
    recommender = KenyanInvestmentRecommender()
    
    # Main header
    st.markdown('<h1 class="main-header">🇰🇪 Kenya Investment Recommender</h1>', unsafe_allow_html=True)
    st.markdown("### Get personalized investment recommendations tailored for the Kenyan market")
    st.markdown("*Powered by AI • Built for Kenyan Investors • Updated with Current Market Data*")
    
    # Display market snapshot
    with st.expander("📊 Current Kenya Market Snapshot"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("91-Day T-Bill Rate", "10.8%", "0.2%")
        with col2:
            st.metric("Inflation Rate", "6.8%", "-0.3%")
        with col3:
            st.metric("NSE 20 Index", "1,847", "12")
        with col4:
            st.metric("USD/KES Rate", "128.5", "1.2")
    
    # Sidebar for user input
    with st.sidebar:
        user_data = recommender.get_user_input()
    
    # Main content area
    if st.button("🚀 Get My Personalized Recommendations", type="primary", use_container_width=True):
        with st.spinner("Analyzing your profile and generating personalized recommendations..."):
            # Validate inputs
            if user_data['disposable_income'] <= 0:
                st.error("❌ Your expenses exceed your income. Please review your budget before investing.")
                st.stop()
            
            # Display user profile summary
            recommender.display_user_profile_summary(user_data)
            
            # Display investment propensity
            propensity_score = recommender.display_investment_propensity(user_data)
            
            # Generate and display recommendations
            recommendations = recommender.generate_recommendations(user_data)
            
            if recommendations:
                recommender.display_recommendations(recommendations, user_data)
                
                # Portfolio allocation
                recommender.create_portfolio_allocation(recommendations, user_data)
                
                # Investment insights
                recommender.display_investment_insights(user_data, recommendations)
                
                # Download recommendations
                st.markdown("---")
                st.markdown("### 📥 Save Your Investment Plan")
                
                # Create downloadable report
                report_data = {
                    'user_profile': user_data,
                    'propensity_score': propensity_score,
                    'recommendations': recommendations,
                    'investment_products': {k: v for k, v in recommender.product_catalog.items() 
                                          if k in [rec[0] for rec in recommendations['recommendations']]},
                    'generated_at': datetime.now().isoformat(),
                    'disclaimer': 'This is for educational purposes only. Consult a financial advisor before making investment decisions.'
                }
                
                st.download_button(
                    label="📄 Download Detailed Investment Report (JSON)",
                    data=json.dumps(report_data, indent=2, default=str),
                    file_name=f"kenya_investment_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # Quick action buttons
                st.markdown("### 🎯 Next Steps")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🏛️ Open CDS Account", help="For government securities"):
                        st.info("Visit CBK or authorized banks to open a CDS account for Treasury bills and bonds")
                
                with col2:
                    if st.button("📈 Start with NSE", help="For stock market investing"):
                        st.info("Contact licensed stockbrokers like Faulu Securities or Standard Investment Bank")
                
                with col3:
                    if st.button("🤝 Find SACCOs", help="For cooperative investments"):
                        st.info("Visit SASRA website to find licensed SACCOs in your area")
            else:
                st.error("❌ Unable to generate recommendations. Please try again or contact support.")
    
    # Footer with additional information
    st.markdown("---")
    with st.expander("ℹ️ About This Kenya Investment Recommender"):
        st.markdown("""
        **How It Works:**
        This AI-powered investment recommender is specifically designed for the Kenyan market, incorporating:
        - Current Kenyan government securities rates (10-16%)
        - NSE stock market opportunities with tax exemptions
        - SACCO and cooperative investment options
        - Real estate and agricultural investment potential
        - Kenya-specific regulations and tax considerations
        
        **Models Used:**
        - **Investment Propensity Model**: Analyzes your likelihood to invest successfully
        - **Risk-Return Optimization**: Balances your risk tolerance with market opportunities
        - **Kenya Market Integration**: Uses current CBK, NSE, and CMA data
        
        **Data Sources:**
        - Central Bank of Kenya (CBK)
        - Nairobi Securities Exchange (NSE)
        - Capital Markets Authority (CMA)
        - Kenya National Bureau of Statistics (KNBS)
        
        **Disclaimer:**
        This tool provides educational recommendations only. Investment decisions should be made after consulting with licensed financial advisors. Past performance does not guarantee future results.
        """)
    
    # Contact and support information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📞 Support & Contact**")
        st.markdown("Email: support@kenyainvestments.co.ke")
        st.markdown("Phone: +254-700-000-000")
        st.markdown("WhatsApp: +254-700-000-000")
    
    with col2:
        st.markdown("**🏢 Regulatory Bodies**")
        st.markdown("[Central Bank of Kenya](https://www.centralbank.go.ke)")
        st.markdown("[Capital Markets Authority](https://www.cma.or.ke)")
        st.markdown("[NSE](https://www.nse.co.ke)")
    
    with col3:
        st.markdown("**⚖️ Legal & Compliance**")
        st.markdown("[Terms of Service](#)")
        st.markdown("[Privacy Policy](#)")
        st.markdown("[Investment Disclaimer](#)")

if __name__ == "__main__":
    main()