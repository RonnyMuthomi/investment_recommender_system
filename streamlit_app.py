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
    page_title="Investment Recommender System",
    page_icon="💰",
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
    .risk-low { border-left: 4px solid #28a745; }
    .risk-medium { border-left: 4px solid #ffc107; }
    .risk-high { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

class StreamlitInvestmentRecommender:
    """Streamlit interface for the investment recommender system"""
    
    def __init__(self):
        self.models = {}
        self.product_catalog = {
            'government_bonds': {
                'name': 'Government Bonds',
                'risk_level': 'Low',
                'expected_return': '6-8%',
                'min_investment': 1000,
                'description': 'Safe government-backed securities with steady returns',
                'liquidity': 'High',
                'time_horizon': '1-5 years'
            },
            'equity_funds': {
                'name': 'Equity Mutual Funds',
                'risk_level': 'High',
                'expected_return': '12-18%',
                'min_investment': 5000,
                'description': 'Growth-oriented funds investing in stocks',
                'liquidity': 'Medium',
                'time_horizon': '5+ years'
            },
            'fixed_deposit': {
                'name': 'Fixed Deposits',
                'risk_level': 'Low',
                'expected_return': '4-6%',
                'min_investment': 500,
                'description': 'Guaranteed returns with capital protection',
                'liquidity': 'Low',
                'time_horizon': '1-3 years'
            },
            'money_market': {
                'name': 'Money Market Funds',
                'risk_level': 'Medium',
                'expected_return': '8-12%',
                'min_investment': 2000,
                'description': 'Short-term investments with good liquidity',
                'liquidity': 'High',
                'time_horizon': '6 months - 2 years'
            },
            'balanced_funds': {
                'name': 'Balanced Funds',
                'risk_level': 'Medium',
                'expected_return': '10-14%',
                'min_investment': 3000,
                'description': 'Mix of stocks and bonds for balanced growth',
                'liquidity': 'Medium',
                'time_horizon': '3-7 years'
            }
        }
        self.load_models()
    
    def load_models(self):
        """Load trained models or create fallback models"""
        try:
            if os.path.exists('models'):
                self.models['hybrid'] = joblib.load('models/hybrid_recommendation_system.pkl')
                self.models['propensity'] = joblib.load('models/investment_propensity_model.pkl')
                st.success("✅ Models loaded successfully!")
            else:
                st.warning("⚠️ Model files not found. Using demo mode.")
                self.create_demo_models()
        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            self.create_demo_models()
    
    def create_demo_models(self):
        """Create demo models for demonstration"""
        class DemoHybridSystem:
            def get_recommendations(self, user_id, user_data, n_recommendations=5):
                # Simple rule-based demo recommendations
                age = user_data.get('age', 35)
                income = user_data.get('monthly_income', 50000)
                risk_tolerance = user_data.get('risk_tolerance', 'medium')
                
                # Base recommendations
                all_products = list(self.product_catalog.keys())
                
                # Risk-based filtering
                if risk_tolerance == 'low' or age > 55:
                    preferred = ['government_bonds', 'fixed_deposit', 'money_market']
                elif risk_tolerance == 'high' and age < 40:
                    preferred = ['equity_funds', 'balanced_funds', 'money_market']
                else:
                    preferred = ['balanced_funds', 'money_market', 'government_bonds']
                
                # Generate scores
                recommendations = []
                for i, product in enumerate(preferred[:n_recommendations]):
                    score = 0.9 - (i * 0.1) + np.random.uniform(-0.05, 0.05)
                    recommendations.append((product, max(0.3, score)))
                
                return {
                    'recommendations': recommendations,
                    'propensity_score': min(0.9, 0.3 + (income / 100000) + (0.2 if risk_tolerance == 'high' else 0)),
                    'method': 'demo'
                }
        
        class DemoPropensityModel:
            def predict_proba(self, user_data_df):
                # Simple rule-based propensity
                if isinstance(user_data_df, dict):
                    user_data = user_data_df
                else:
                    user_data = user_data_df.iloc[0].to_dict()
                
                age = user_data.get('age', 35)
                income = user_data.get('monthly_income', 50000)
                education = user_data.get('education_level', 'secondary')
                
                base_score = 0.4
                if income > 75000: base_score += 0.2
                if education == 'tertiary': base_score += 0.15
                if 25 <= age <= 50: base_score += 0.1
                
                return [min(0.9, base_score)]
        
        self.models['hybrid'] = DemoHybridSystem()
        self.models['propensity'] = DemoPropensityModel()
        self.product_catalog = self.product_catalog  # Make available to demo system
    
    def get_user_input(self):
        """Get user input from Streamlit interface"""
        st.sidebar.markdown("## 👤 User Profile")
        
        # Basic Information
        st.sidebar.markdown("### Basic Information")
        age = st.sidebar.slider("Age", 18, 75, 35)
        gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
        location = st.sidebar.selectbox("Location Type", ["Urban", "Rural"])
        
        # Financial Information
        st.sidebar.markdown("### Financial Profile")
        monthly_income = st.sidebar.number_input(
            "Monthly Income (KES)", 
            min_value=10000, 
            max_value=1000000, 
            value=75000, 
            step=5000
        )
        
        monthly_expenditure = st.sidebar.number_input(
            "Monthly Expenditure (KES)", 
            min_value=5000, 
            max_value=800000, 
            value=min(monthly_income - 5000, 50000), 
            step=5000
        )
        
        # Education and Employment
        st.sidebar.markdown("### Background")
        education = st.sidebar.selectbox(
            "Education Level", 
            ["Primary", "Secondary", "Tertiary"]
        )
        
        employment = st.sidebar.selectbox(
            "Employment Type", 
            ["Formal Employment", "Self-Employed", "Informal Employment"]
        )
        
        # Investment Profile
        st.sidebar.markdown("### Investment Profile")
        investment_experience = st.sidebar.selectbox(
            "Investment Experience", 
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        risk_tolerance = st.sidebar.selectbox(
            "Risk Tolerance", 
            ["Low", "Medium", "High"]
        )
        
        investment_goal = st.sidebar.selectbox(
            "Primary Investment Goal",
            ["Wealth Growth", "Income Generation", "Capital Preservation", "Emergency Fund"]
        )
        
        time_horizon = st.sidebar.selectbox(
            "Investment Time Horizon",
            ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"]
        )
        
        # Additional Information
        st.sidebar.markdown("### Additional Information")
        household_size = st.sidebar.slider("Household Size", 1, 10, 3)
        digital_comfort = st.sidebar.slider(
            "Digital Platform Comfort (1-10)", 1, 10, 7
        )
        
        # Calculate derived metrics
        disposable_income = max(0, monthly_income - monthly_expenditure)
        income_ratio = monthly_income / monthly_expenditure if monthly_expenditure > 0 else 1
        
        return {
            'user_id': 1,
            'age': age,
            'gender': gender.lower(),
            'location_type': location.lower(),
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
            'digital_sophistication': digital_comfort / 10.0
        }
    
    def generate_recommendations(self, user_data):
        """Generate investment recommendations"""
        try:
            if 'hybrid' in self.models and self.models['hybrid']:
                recommendations = self.models['hybrid'].get_recommendations(
                    user_data['user_id'], user_data, n_recommendations=5
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
            st.metric("Digital Comfort", f"{user_data['digital_sophistication']*10:.0f}/10")
    
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
        """Display personalized investment recommendations"""
        st.markdown('<div class="sub-header">💡 Personalized Investment Recommendations</div>', unsafe_allow_html=True)
        
        if not recommendations or 'recommendations' not in recommendations:
            st.error("❌ Unable to generate recommendations")
            return
        
        rec_list = recommendations['recommendations']
        propensity_score = recommendations.get('propensity_score', 0.5)
        
        # Display each recommendation
        for i, (product_key, score) in enumerate(rec_list, 1):
            if product_key in self.product_catalog:
                product = self.product_catalog[product_key]
                
                # Risk level styling
                risk_class = f"risk-{product['risk_level'].lower()}"
                
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
                
                # Suitability explanation
                with st.expander(f"Why {product['name']} is recommended for you"):
                    self.explain_recommendation(product_key, product, user_data, score)
    
    def explain_recommendation(self, product_key, product, user_data, score):
        """Provide explanation for why a product is recommended"""
        explanations = []
        
        # Age-based explanations
        age = user_data['age']
        if age < 30 and product['risk_level'] == 'High':
            explanations.append("✅ Your young age allows for higher risk tolerance and longer investment horizon")
        elif age > 50 and product['risk_level'] == 'Low':
            explanations.append("✅ Conservative approach suitable for your age and retirement planning")
        elif 30 <= age <= 50 and product['risk_level'] == 'Medium':
            explanations.append("✅ Balanced approach appropriate for your life stage")
        
        # Income-based explanations
        if user_data['disposable_income'] >= product['min_investment']:
            surplus = user_data['disposable_income'] - product['min_investment']
            explanations.append(f"✅ Fits comfortably within your budget (surplus: KES {surplus:,})")
        elif user_data['disposable_income'] >= product['min_investment'] * 0.8:
            explanations.append("⚠️ Requires most of your disposable income - consider smaller amounts initially")
        
        # Risk tolerance match
        risk_map = {'low': 'Low', 'medium': 'Medium', 'high': 'High'}
        user_risk = risk_map.get(user_data['risk_tolerance'], 'Medium')
        if user_risk == product['risk_level']:
            explanations.append(f"✅ Perfect match with your {user_risk.lower()} risk tolerance")
        elif (user_risk == 'Medium' and product['risk_level'] in ['Low', 'High']):
            explanations.append(f"✅ Acceptable risk level for your {user_risk.lower()} risk tolerance")
        
        # Time horizon match
        time_horizon = user_data['time_horizon']
        if 'years' in product['time_horizon']:
            if 'Less than 1 year' in time_horizon and 'months' in product['time_horizon']:
                explanations.append("✅ Matches your short-term investment timeline")
            elif any(term in time_horizon for term in ['3-5 years', '5-10 years', 'More than 10 years']) and 'years' in product['time_horizon']:
                explanations.append("✅ Aligns with your long-term investment goals")
        
        # Investment goal alignment
        goal = user_data['investment_goal']
        if goal == 'wealth growth' and product['risk_level'] in ['Medium', 'High']:
            explanations.append("✅ High growth potential aligns with your wealth building goals")
        elif goal == 'income generation' and 'bond' in product_key or 'deposit' in product_key:
            explanations.append("✅ Provides steady income suitable for your income generation goal")
        elif goal == 'capital preservation' and product['risk_level'] == 'Low':
            explanations.append("✅ Low risk helps preserve your capital as desired")
        
        # Digital sophistication
        if user_data['digital_sophistication'] > 0.7:
            explanations.append("✅ Your high digital comfort makes this investment easily manageable")
        elif user_data['digital_sophistication'] < 0.4 and product_key in ['fixed_deposit', 'government_bonds']:
            explanations.append("✅ Simple investment structure suitable for your preferences")
        
        # Display explanations
        if explanations:
            for explanation in explanations[:4]:  # Show top 4 explanations
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
            max_value=10000000, 
            value=min(50000, user_data['disposable_income'] * 6),  # 6 months of disposable income
            step=1000
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
                    allocation_pct = (score / total_score) * 0.8  # Use 80% for proportional allocation
                    allocation_amount = min(remaining_amount, total_investment * allocation_pct)
                else:  # Last item gets remaining amount
                    allocation_amount = remaining_amount
                
                # Ensure minimum investment requirement
                if allocation_amount >= product['min_investment']:
                    allocations.append({
                        'product': product['name'],
                        'amount': allocation_amount,
                        'percentage': (allocation_amount / total_investment) * 100,
                        'risk_level': product['risk_level'],
                        'expected_return': product['expected_return']
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
                    title="Portfolio Allocation by Amount",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(
                    allocation_df, 
                    x='product', 
                    y='percentage',
                    title="Portfolio Allocation by Percentage",
                    color='risk_level',
                    color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
                )
                fig_bar.update_xaxes(tickangle=45)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Allocation table
            st.markdown("### 📋 Detailed Allocation")
            for allocation in allocations:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{allocation['product']}</strong><br>
                    Amount: KES {allocation['amount']:,.0f} ({allocation['percentage']:.1f}%)<br>
                    Risk Level: {allocation['risk_level']} | Expected Return: {allocation['expected_return']}
                </div>
                """, unsafe_allow_html=True)
            
            # Risk summary
            risk_summary = allocation_df.groupby('risk_level')['percentage'].sum()
            st.markdown("### ⚖️ Risk Distribution")
            risk_col1, risk_col2, risk_col3 = st.columns(3)
            
            with risk_col1:
                low_risk = risk_summary.get('Low', 0)
                st.metric("Low Risk", f"{low_risk:.1f}%")
            
            with risk_col2:
                medium_risk = risk_summary.get('Medium', 0)
                st.metric("Medium Risk", f"{medium_risk:.1f}%")
            
            with risk_col3:
                high_risk = risk_summary.get('High', 0)
                st.metric("High Risk", f"{high_risk:.1f}%")
    
    def display_investment_insights(self, user_data, recommendations):
        """Display additional investment insights and tips"""
        st.markdown('<div class="sub-header">💡 Investment Insights & Tips</div>', unsafe_allow_html=True)
        
        insights = []
        
        # Age-based insights
        age = user_data['age']
        if age < 30:
            insights.append("🌱 **Early Starter Advantage**: You have time on your side. Consider higher-risk, higher-reward investments for long-term wealth building.")
        elif age < 45:
            insights.append("⚖️ **Balanced Approach**: Balance growth and stability. Start thinking about diversification across asset classes.")
        elif age < 60:
            insights.append("🛡️ **Preservation Phase**: Focus on capital preservation while maintaining some growth exposure.")
        else:
            insights.append("🏛️ **Conservative Strategy**: Prioritize capital preservation and income generation over growth.")
        
        # Income-based insights
        disposal_ratio = user_data['disposable_income'] / user_data['monthly_income']
        if disposal_ratio > 0.3:
            insights.append(f"💰 **Strong Savings Rate**: Your {disposal_ratio:.1%} savings rate is excellent! You can afford to take calculated risks.")
        elif disposal_ratio > 0.15:
            insights.append(f"👍 **Good Savings Discipline**: Your {disposal_ratio:.1%} savings rate shows good financial discipline.")
        else:
            insights.append(f"⚠️ **Focus on Budgeting**: Your {disposal_ratio:.1%} savings rate suggests you should focus on increasing disposable income first.")
        
        # Risk tolerance insights
        risk_tolerance = user_data['risk_tolerance']
        if risk_tolerance == 'high':
            insights.append("🎢 **Risk Embracer**: Your high risk tolerance allows for aggressive growth strategies, but don't forget diversification.")
        elif risk_tolerance == 'low':
            insights.append("🛡️ **Safety First**: Your conservative approach is wise. Focus on capital preservation with modest growth.")
        else:
            insights.append("⚖️ **Balanced Investor**: Your moderate risk approach is sensible. Mix growth and stability investments.")
        
        # Experience-based insights
        experience = user_data['investment_experience']
        if experience == 'beginner':
            insights.append("📚 **Learning Journey**: Start with simple, low-cost investments. Consider index funds and fixed deposits initially.")
        elif experience == 'intermediate':
            insights.append("📈 **Building Expertise**: You can explore more complex investments. Consider diversifying across asset classes.")
        else:
            insights.append("🎯 **Expert Level**: Your experience allows for sophisticated strategies. Consider alternative investments and tax optimization.")
        
        # Display insights
        for insight in insights:
            st.info(insight)
        
        # Additional tips
        with st.expander("📋 General Investment Tips"):
            st.markdown("""
            **🎯 Key Investment Principles:**
            - **Start Early**: Time is your greatest asset in investing
            - **Diversify**: Don't put all eggs in one basket
            - **Stay Consistent**: Regular investing beats trying to time the market
            - **Keep Learning**: Stay informed about your investments
            - **Review Regularly**: Rebalance your portfolio periodically
            - **Emergency Fund First**: Keep 3-6 months of expenses in accessible savings
            - **Understand Fees**: High fees can erode returns over time
            - **Tax Efficiency**: Consider tax implications of your investments
            """)

def main():
    """Main Streamlit application"""
    
    # Initialize the recommender system
    recommender = StreamlitInvestmentRecommender()
    
    # Main header
    st.markdown('<h1 class="main-header">💰 Smart Investment Recommender</h1>', unsafe_allow_html=True)
    st.markdown("### Get personalized investment recommendations based on your profile and goals")
    
    # Sidebar for user input
    user_data = recommender.get_user_input()
    
    # Main content area
    if st.sidebar.button("🚀 Get My Recommendations", type="primary"):
        with st.spinner("Analyzing your profile and generating recommendations..."):
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
                st.markdown("### 📥 Download Your Recommendations")
                
                # Create downloadable report
                report_data = {
                    'user_profile': user_data,
                    'propensity_score': propensity_score,
                    'recommendations': recommendations,
                    'generated_at': datetime.now().isoformat()
                }
                
                st.download_button(
                    label="📄 Download Detailed Report (JSON)",
                    data=json.dumps(report_data, indent=2, default=str),
                    file_name=f"investment_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.error("❌ Unable to generate recommendations. Please try again or contact support.")
    
    # Footer with additional information
    st.markdown("---")
    with st.expander("ℹ️ About This Recommender System"):
        st.markdown("""
        **How It Works:**
        This AI-powered investment recommender uses machine learning models to analyze your profile and provide personalized investment suggestions.
        
        **Models Used:**
        - **Investment Propensity Model**: Predicts your likelihood to invest based on demographics and financial profile
        - **User Segmentation**: Groups you with similar investors for targeted recommendations
        - **Hybrid Recommendation Engine**: Combines collaborative filtering and content-based approaches
        
        **Disclaimer:**
        This tool provides educational recommendations only. Always consult with a qualified financial advisor before making investment decisions.
        """)
    
    # Contact and support information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📞 Support**")
        st.markdown("Email: support@investmentrecommender.com")
        st.markdown("Phone: +254-XXX-XXXXXX")
    
    with col2:
        st.markdown("**🏢 About Us**")
        st.markdown("Smart Investment Solutions")
        st.markdown("Empowering financial decisions with AI")
    
    with col3:
        st.markdown("**⚖️ Legal**")
        st.markdown("[Terms of Service](#)")
        st.markdown("[Privacy Policy](#)")

if __name__ == "__main__":
    main()