import streamlit as st
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
import joblib
import os
warnings.filterwarnings('ignore')


class InvestmentRecommendationSystem:
    def __init__(self):
        self.investment_products = self._define_investment_products()
        self.risk_categories = self._define_risk_categories()
        self.segment_recommendations = self._define_segment_recommendations()
        self.best_model_name = None
        self.model_pipelines = {}
        self.model_config = None
        self.preprocessor = None
        
        # Automatically load saved models on initialization
        self.load_saved_models()

    def set_model(self, model_name, pipeline):
        """Set the ML model for predictions"""
        self.best_model_name = model_name
        self.model_pipelines = {model_name: {'pipeline': pipeline}}

    def load_saved_models(self):
        """Load all saved model components from deployment folder"""
        try:
            deployment_folder = "deployment"
            
            # Check if deployment folder exists
            if not os.path.exists(deployment_folder):
                print(f"Deployment folder '{deployment_folder}' not found. Using rule-based recommendations only.")
                return False
            
            # Define file paths
            config_path = os.path.join(deployment_folder, "investment_model_config.pkl")
            pipelines_path = os.path.join(deployment_folder, "investment_model_pipelines.pkl")
            preprocessor_path = os.path.join(deployment_folder, "investment_model_preprocessor.pkl")
            
            # Load model configuration
            if os.path.exists(config_path):
                self.model_config = joblib.load(config_path)
                print(f"✅ Loaded model configuration")
            else:
                print(f"❌ Model config file not found: {config_path}")
                return False
            
            # Load model pipelines
            if os.path.exists(pipelines_path):
                self.model_pipelines = joblib.load(pipelines_path)
                print(f"✅ Loaded model pipelines: {list(self.model_pipelines.keys())}")
                
                # Set the best model from config
                if self.model_config and 'best_model' in self.model_config:
                    self.best_model_name = self.model_config['best_model']
                    print(f"✅ Best model set to: {self.best_model_name}")
                else:
                    # Use the first available model
                    self.best_model_name = list(self.model_pipelines.keys())[1] if self.model_pipelines else None
                    print(f"✅ Using first available model: {self.best_model_name}")
                    
            else:
                print(f"❌ Model pipelines file not found: {pipelines_path}")
                return False
            
            # Load preprocessor
            if os.path.exists(preprocessor_path):
                self.preprocessor = joblib.load(preprocessor_path)
                print(f"✅ Loaded preprocessor")
            else:
                print(f"❌ Preprocessor file not found: {preprocessor_path}")
                return False
            
            print(f"🚀 All model components loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading saved models: {str(e)}")
            print("Continuing with rule-based recommendations only.")
            return False

    def _map_user_data_to_model_features(self, user_data):
        """Map current user data fields to expected model features"""
        try:
            # Create a mapping from your current fields to model expected fields
            mapped_data = {}
            
            # Direct mappings (if field names match)
            direct_mappings = {
                'age': 'age',
                'monthly_income': 'monthly_income', 
                'monthly_expenses': 'monthly_expenses',
                'current_savings': 'current_savings',
                'debt_amount': 'debt_amount',
                'dependents': 'dependents',
                'household_size': 'household_size'
            }
            
            for current_field, model_field in direct_mappings.items():
                if current_field in user_data:
                    mapped_data[model_field] = user_data[current_field]
            
            # Complex mappings for encoded features
            
            # Education level encoding
            education_mapping = {
                'Primary': 0,
                'Secondary': 1,
                'College/University': 2,
                'Postgraduate': 3
            }
            education = user_data.get('education', 'Secondary')
            mapped_data['education_level_encoded'] = education_mapping.get(education, 1)
            
            # Location type encoding
            location_mapping = {
                'Rural': 0,
                'Semi-Urban': 1,
                'Urban': 2
            }
            location = user_data.get('location', 'Urban')
            mapped_data['location_type_encoded'] = location_mapping.get(location, 2)
            
            # Savings usage (derive from current_savings and monthly_income)
            current_savings = user_data.get('current_savings', 0)
            monthly_income = user_data.get('monthly_income', 30000)
            if monthly_income > 0:
                mapped_data['savings_usage'] = min(1.0, current_savings / (monthly_income * 6))  # Months of savings
            else:
                mapped_data['savings_usage'] = 0.0
            
            # Formal service use (derive from investment experience and employment)
            experience = user_data.get('investment_experience', 'Beginner')
            employment = user_data.get('employment', 'Employed')
            
            formal_service_score = 0
            if 'Advanced' in experience:
                formal_service_score += 0.4
            elif 'Intermediate' in experience:
                formal_service_score += 0.2
            
            if employment in ['Employed', 'Self-Employed']:
                formal_service_score += 0.3
            
            if monthly_income > 50000:
                formal_service_score += 0.3
            
            mapped_data['formal_service_use'] = min(1.0, formal_service_score)
            
            # Mobile banking usage (assume based on age and location)
            age = user_data.get('age', 30)
            mobile_banking_score = 0.5  # Base assumption
            
            if age < 45:  # Younger people more likely to use mobile banking
                mobile_banking_score += 0.3
            if location in ['Urban', 'Semi-Urban']:
                mobile_banking_score += 0.2
            if monthly_income > 30000:
                mobile_banking_score += 0.2
                
            mapped_data['mobile_banking'] = min(1.0, mobile_banking_score)
            
            # Add any other features that might be missing with default values
            default_features = {
                'risk_score': self._calculate_risk_score(user_data),
                'investment_capacity': self._calculate_investment_capacity(user_data),
                'financial_stability': self._calculate_financial_stability(user_data)
            }
            
            mapped_data.update(default_features)
            
            print(f"✅ Mapped {len(user_data)} input features to {len(mapped_data)} model features")
            return mapped_data
            
        except Exception as e:
            print(f"❌ Error mapping user data: {str(e)}")
            return user_data  # Return original if mapping fails

    def _calculate_risk_score(self, user_data):
        """Calculate a risk score for the user"""
        try:
            age = user_data.get('age', 30)
            income = user_data.get('monthly_income', 30000)
            experience = user_data.get('investment_experience', 'Beginner')
            
            risk_score = 0.3  # Base risk
            
            if age < 35:
                risk_score += 0.3
            elif age > 55:
                risk_score -= 0.2
                
            if income > 100000:
                risk_score += 0.2
            elif income < 25000:
                risk_score -= 0.1
                
            if 'Advanced' in experience:
                risk_score += 0.3
            elif 'Beginner' in experience:
                risk_score -= 0.2
                
            return max(0.0, min(1.0, risk_score))
        except:
            return 0.5

    def _calculate_investment_capacity(self, user_data):
        """Calculate investment capacity based on income and expenses"""
        try:
            income = user_data.get('monthly_income', 30000)
            expenses = user_data.get('monthly_expenses', 20000)
            debt = user_data.get('debt_amount', 0)
            
            disposable_income = income - expenses
            debt_to_income_ratio = debt / income if income > 0 else 1
            
            capacity = disposable_income / income if income > 0 else 0
            capacity = capacity * (1 - debt_to_income_ratio)  # Reduce by debt burden
            
            return max(0.0, min(1.0, capacity))
        except:
            return 0.3

    def _calculate_financial_stability(self, user_data):
        """Calculate financial stability score"""
        try:
            income = user_data.get('monthly_income', 30000)
            savings = user_data.get('current_savings', 0)
            employment = user_data.get('employment', 'Unemployed')
            emergency_fund = user_data.get('emergency_fund', 'No')
            
            stability = 0.2  # Base stability
            
            # Employment stability
            if employment == 'Employed':
                stability += 0.3
            elif employment == 'Self-Employed':
                stability += 0.2
            
            # Emergency fund
            if emergency_fund == 'Yes':
                stability += 0.3
            elif emergency_fund == 'Partial':
                stability += 0.15
            
            # Savings buffer
            if income > 0:
                savings_months = savings / income
                stability += min(0.2, savings_months * 0.05)
            
            return max(0.0, min(1.0, stability))
        except:
            return 0.5

    def get_model_prediction(self, user_data):
        """Get prediction from loaded ML model with proper feature mapping"""
        try:
            if not self.best_model_name or self.best_model_name not in self.model_pipelines:
                print("No model available for prediction")
                return None
            
            # Map user data to expected model features
            mapped_data = self._map_user_data_to_model_features(user_data)
            
            # Convert to DataFrame
            user_df = pd.DataFrame([mapped_data])
            
            # Ensure all required features are present
            user_df = self._add_missing_features(user_df)
            
            print(f"🔧 Model input features: {list(user_df.columns)}")
            
            # Get the pipeline
            pipeline = self.model_pipelines[self.best_model_name]['pipeline']
            
            # Make prediction
            if hasattr(pipeline, 'predict_proba'):
                # Get probability of investing (assuming binary classification)
                prediction_proba = pipeline.predict_proba(user_df)
                if prediction_proba.shape[1] > 1:
                    investment_probability = prediction_proba[0][1]  # Probability of positive class
                else:
                    investment_probability = prediction_proba[0][0]
            else:
                # Fallback to regular prediction
                prediction = pipeline.predict(user_df)[0]
                investment_probability = float(prediction) if isinstance(prediction, (int, float)) else 0.5
            
            print(f"🎯 Model prediction: {investment_probability:.2%} investment probability")
            return investment_probability
            
        except Exception as e:
            print(f"❌ Error making model prediction: {str(e)}")
            import traceback
            print(f"Full error: {traceback.format_exc()}")
            return None

    def _add_missing_features(self, user_df):
        """Add any missing features expected by the model with default values"""
        
        # List of features your model expects
        expected_features = [
            'savings_usage', 'education_level_encoded', 'location_type_encoded', 
            'formal_service_use', 'mobile_banking', 'age', 'monthly_income',
            'monthly_expenses', 'current_savings', 'debt_amount', 'dependents',
            'household_size'
        ]
        
        # Add missing features with sensible defaults
        for feature in expected_features:
            if feature not in user_df.columns:
                if feature == 'savings_usage':
                    user_df[feature] = 0.3  # Default savings usage
                elif feature == 'education_level_encoded':
                    user_df[feature] = 1  # Default to secondary education
                elif feature == 'location_type_encoded':
                    user_df[feature] = 2  # Default to urban
                elif feature == 'formal_service_use':
                    user_df[feature] = 0.5  # Default moderate usage
                elif feature == 'mobile_banking':
                    user_df[feature] = 0.7  # Default high mobile banking usage
                else:
                    user_df[feature] = 0  # Default numeric value
        
        return user_df

    def _define_investment_products(self):
        """Define investment product categories with detailed information"""
        return {
            'Government Bonds (Treasury Bonds)': {
                'description': 'Long-term debt securities issued by the Kenyan government, typically with maturities of 2+ years, offering fixed interest payments to investors.',
                'risk_level': 'Low',
                'expected_return': '8-12%',
                'liquidity': 'Medium',
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
            
            'Treasury Bills (T-Bills)': {
                'description': 'Short-term government debt instruments with maturities of 91, 182, or 364 days, sold at discount and redeemed at face value.',
                'risk_level': 'Low',
                'expected_return': '6-10%',
                'liquidity': 'High',
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
            
            'Nairobi Securities Exchange (NSE) Stocks': {
                'description': 'Equity shares of publicly traded companies listed on Kenya\'s main stock exchange, representing ownership stakes in businesses.',
                'risk_level': 'High',
                'expected_return': '12-25%',
                'liquidity': 'High',
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
            
            'Unit Trusts/Mutual Funds': {
                'description': 'Pooled investment vehicles managed by professional fund managers, allowing investors to access diversified portfolios with small amounts.',
                'risk_level': 'Medium',
                'expected_return': '8-15%',
                'liquidity': 'Medium',
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
            
            'Money Market Funds': {
                'description': 'Investment funds that invest in short-term, high-quality debt instruments, offering better returns than savings accounts with easy access to funds.',
                'risk_level': 'Low',
                'expected_return': '6-9%',
                'liquidity': 'High',
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
            
            'Real Estate Investment': {
                'description': 'Direct investment in physical property for rental income and capital appreciation, including residential, commercial, or land investments.',
                'risk_level': 'Medium',
                'expected_return': '10-20%',
                'liquidity': 'Low',
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
            
            'Real Estate Investment Trusts (REITs)': {
                'description': 'Investment vehicles that own and operate income-generating real estate, allowing investors to buy shares and receive dividends from property investments.',
                'risk_level': 'Medium',
                'expected_return': '8-14%',
                'liquidity': 'Medium',
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
            
            'Bank Fixed Deposits': {
                'description': 'Time deposits with predetermined interest rates and fixed maturity periods, offering guaranteed returns with bank protection.',
                'risk_level': 'Low',
                'expected_return': '5-8%',
                'liquidity': 'Low',
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
            
            'High-Yield Savings Accounts': {
                'description': 'Bank accounts offering higher interest rates than regular savings accounts while maintaining full liquidity and deposit protection.',
                'risk_level': 'Low',
                'expected_return': '3-6%',
                'liquidity': 'High',
                'pros': [
                    'Highest liquidity',
                    'KDIC deposit protection',
                    'No risk of capital loss',
                    'Easy access to funds',
                    'Low minimum balance requirements'
                ],
                'cons': [
                    'Very low returns',
                    'Inflation erodes purchasing power',
                    'Opportunity cost',
                    'Bank charges may apply'
                ]
            },
            
            'Commodity Trading': {
                'description': 'Investment in physical commodities like gold, oil, agricultural products, or commodity futures contracts for portfolio diversification.',
                'risk_level': 'High',
                'expected_return': '10-30%',
                'liquidity': 'Medium',
                'pros': [
                    'Inflation hedge',
                    'Portfolio diversification',
                    'Potential for high returns',
                    'Tangible assets',
                    'Kenya is a commodity-producing economy'
                ],
                'cons': [
                    'High price volatility',
                    'Storage and insurance costs',
                    'Seasonal price fluctuations',
                    'Limited commodity exchanges in Kenya',
                    'Requires specialized knowledge'
                ]
            },
            
            'Foreign Exchange (Forex) Trading': {
                'description': 'Trading of currency pairs in the global foreign exchange market, often using leverage to amplify potential returns and risks.',
                'risk_level': 'Very High',
                'expected_return': '-50% to +100%',
                'liquidity': 'High',
                'pros': [
                    '24/7 market availability',
                    'High liquidity',
                    'Leverage opportunities',
                    'Currency hedging benefits',
                    'Low transaction costs'
                ],
                'cons': [
                    'Extremely high risk',
                    'Potential for total loss',
                    'Requires extensive knowledge',
                    'Leverage amplifies losses',
                    'Regulatory risks',
                    'Emotional stress'
                ]
            },
            
            'Pension Schemes (Individual & Occupational)': {
                'description': 'Long-term retirement savings plans with tax benefits, designed to provide income security after retirement through systematic contributions.',
                'risk_level': 'Low',
                'expected_return': '7-12%',
                'liquidity': 'Very Low',
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
            
            'Cooperative Society Investments (SACCOs)': {
                'description': 'Member-owned financial cooperatives that pool resources to provide savings, credit, and investment services to their members.',
                'risk_level': 'Medium',
                'expected_return': '8-15%',
                'liquidity': 'Medium',
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
            
            'Small Business Investment/Entrepreneurship': {
                'description': 'Starting or investing in small businesses or entrepreneurial ventures to generate income and build wealth through business ownership.',
                'risk_level': 'High',
                'expected_return': '15-50%',
                'liquidity': 'Very Low',
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
            },
            
            'Agricultural Investment': {
                'description': 'Investment in farming activities, agricultural land, or agribusiness ventures to capitalize on Kenya\'s agricultural sector potential.',
                'risk_level': 'Medium',
                'expected_return': '10-25%',
                'liquidity': 'Low',
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

            'Education Savings Plans': {
                'description': 'Specialized investment products designed to save and grow funds specifically for educational expenses, often with insurance components.',
                'risk_level': 'Low',
                'expected_return': '6-10%',
                'liquidity': 'Low',
                'pros': [
                    'Disciplined long-term saving',
                    'Investment growth for education costs',
                    'Some plans offer insurance benefits',
                    'Goal-oriented saving',
                    'Professional fund management'
                ],
                'cons': [
                    'Funds locked for specific purpose',
                    'Management fees',
                    'Limited flexibility',
                    'Penalty for early withdrawal',
                    'Market risk exposure'
                ]
            }
        }
    
    def _define_risk_categories(self):
        """Categorize investment products by risk level"""
        risk_categories = {
            'low_risk': [],
            'medium_risk': [],
            'high_risk': [],
            'very_high_risk': [],
            'alternative': []
        }
        
        # Categorize products based on risk level
        for product_name, details in self.investment_products.items():
            risk_level = details.get('risk_level', 'Medium')
            
            if risk_level == 'Low':
                risk_categories['low_risk'].append(product_name)
            elif risk_level == 'Medium':
                risk_categories['medium_risk'].append(product_name)
            elif risk_level == 'High':
                risk_categories['high_risk'].append(product_name)
            elif risk_level == 'Very High':
                risk_categories['very_high_risk'].append(product_name)
        
        # Alternative investments (unique/specialized products)
        risk_categories['alternative'] = [
            'Cooperative Society Investments (SACCOs)',
            'Agricultural Investment',
            'Small Business Investment/Entrepreneurship',
            'Education Savings Plans'
        ]
        
        return risk_categories

    def _define_segment_recommendations(self):
        """Define recommendations by user segment using proper risk categories"""
        return {
            'growth_seeker': ['high_risk', 'medium_risk'],
            'balanced_investor': ['medium_risk', 'low_risk'],
            'income_focused': ['low_risk', 'alternative'],
            'opportunity_seeker': ['medium_risk', 'alternative'],
            'moderate': ['medium_risk']
        }
    
    def get_products_by_risk(self, risk_level):
        """Get all products for a specific risk level"""
        if not hasattr(self, 'risk_categories'):
            self.risk_categories = self._define_risk_categories()
        
        return self.risk_categories.get(risk_level, [])
 
    def get_product_details(self, product_name):
        """Get detailed information about a specific product"""
        return self.investment_products.get(product_name, {})
    
    def get_recommendations_by_risk_tolerance(self, risk_tolerance):
        """Get product recommendations based on risk tolerance"""
                
        risk_mapping = {
            'Low': ['low_risk'],
            'Medium': ['medium_risk', 'low_risk'], 
            'High': ['high_risk', 'medium_risk'],
            'Very High': ['very_high_risk', 'high_risk']
        }
        
        risk_categories = risk_mapping.get(risk_tolerance, ['medium_risk'])
        
        recommendations = []
        for category in risk_categories:
            products = self.get_products_by_risk(category)
            for product in products[:3]:  # Limit to top 3 per category
                if product in self.investment_products:
                    details = self.investment_products[product]
                    recommendations.append({
                        'product': product,
                        'risk_level': details.get('risk_level', 'Medium'),
                        'expected_return': details.get('expected_return', '8-12%'),
                        'liquidity': details.get('liquidity', 'Medium'),
                        'description': details.get('description', '')
                    })
        
        return recommendations

    def get_user_segment(self, user_data):
        """Determine user segment based on profile"""
        try:
            age = user_data.get('age', 30)
            location = user_data.get('location', 'Urban')
            income = user_data.get('monthly_income', 30000)
            
            if age < 30 and income > 50000:
                return 'growth_seeker'
            elif age >= 50:
                return 'income_focused'
            elif 'rural' in str(location).lower():
                return 'opportunity_seeker'
            elif 30 <= age < 50:
                return 'balanced_investor'
            else:
                return 'moderate'
        except Exception:
            return 'balanced_investor'

    def get_risk_tolerance(self, user_data):
        """Determine risk tolerance based on profile"""
        try:
            age = user_data.get('age', 30)
            income = user_data.get('monthly_income', 30000)
            experience = user_data.get('investment_experience', 'Beginner')
            
            score = 0
            
            # Age factor
            if age < 35: score += 2
            elif age < 50: score += 1
            
            # Income factor  
            if income > 100000: score += 2
            elif income > 50000: score += 1
            
            # Experience factor
            if 'Advanced' in experience: score += 2
            elif 'Intermediate' in experience: score += 1
            
            if score >= 4:
                return 'High'
            elif score >= 2:
                return 'Medium'
            else:
                return 'Low'
        except Exception:
            return 'Medium'

    def get_portfolio_allocation(self, risk_tolerance):
        """Get portfolio allocation based on risk tolerance"""
        if isinstance(risk_tolerance, str):
            risk_tolerance = risk_tolerance.lower()
        
        allocations = {
            'low': {
                'Government Bonds': 40,
                'Money Market Funds': 30,
                'Bank Fixed Deposits': 20,
                'High-Yield Savings': 10
            },
            'medium': {
                'Unit Trusts/Mutual Funds': 30,
                'Government Bonds': 25,
                'Real Estate Investment Trusts (REITs)': 20,
                'NSE Stocks': 15,
                'Money Market Funds': 10
            },
            'high': {
                'NSE Stocks': 35,
                'Unit Trusts/Mutual Funds': 25,
                'Small Business Investment': 15,
                'Real Estate Investment Trusts (REITs)': 15,
                'Commodity Trading': 10
            }
        }
        
        return allocations.get(risk_tolerance, allocations['medium'])

    def get_recommendations(self, user_id=None, user_data=None, df=None):
        """Generate personalized investment recommendations using both ML models and rules"""
        
        if user_data is None and user_id is not None and df is not None:
            if user_id in df.index:
                user_data = df.loc[user_id].to_dict()
            else:
                print(f"User {user_id} not found in dataset")
                return self._get_emergency_recommendations(None)
        
        if user_data is None:
            print("No user data provided")
            return self._get_emergency_recommendations(None)
        
        try:
            # Get user characteristics with fallback values
            user_segment = self.get_user_segment(user_data)
            
            # Handle risk_tolerance from user_data directly if available
            risk_tolerance = user_data.get('risk_tolerance', 'Medium')
            if not risk_tolerance:
                risk_tolerance = self.get_risk_tolerance(user_data)
            
            print(f"🎯 Investment Recommendations for User")
            print(f"📊 User Segment: {user_segment}")
            print(f"⚖️ Risk Tolerance: {risk_tolerance}")
            
            recommendations = {
                'user_segment': user_segment,
                'risk_tolerance': risk_tolerance,
                'segment_recommendations': [],
                'risk_recommendations': [],
                'detailed_products': [],
                'investment_probability': None
            }
            
            # 1. Get ML model prediction first (if available)
            ml_prediction = self.get_model_prediction(user_data)
            if ml_prediction is not None:
                recommendations['investment_probability'] = ml_prediction
            else:
                # Fallback probability calculation
                try:
                    age = user_data.get('age', 30)
                    income = user_data.get('monthly_income', 30000)
                    prob = min(0.95, 0.4 + (income / 100000) * 0.3 + (age / 100) * 0.2)
                    recommendations['investment_probability'] = prob
                except:
                    recommendations['investment_probability'] = 0.65
            
            # 2. Segment-based recommendations
            if user_segment in self.segment_recommendations:
                segment_risk_categories = self.segment_recommendations[user_segment]
                recommendations['segment_recommendations'] = segment_risk_categories
                
                print(f"📋 Segment-Based Risk Categories:")
                for risk_category in segment_risk_categories:
                    try:
                        products = self.get_products_by_risk(risk_category)
                        print(f"  🎯 {risk_category.replace('_', ' ').title()}: {len(products)} products")
                    except Exception as e:
                        print(f"❌ Error getting products for {risk_category}: {e}")
            
            # 3. Risk-based recommendations
            try:
                risk_based_products = self.get_recommendations_by_risk_tolerance(risk_tolerance)
                if risk_based_products:
                    recommendations['risk_recommendations'] = [p['product'] for p in risk_based_products]
                    recommendations['detailed_products'] = risk_based_products
                    
                    print(f"💡 Risk-Based Product Recommendations ({len(risk_based_products)} products):")
                    for product_info in risk_based_products[:5]:  # Show top 5
                        print(f"  • {product_info['product']}")
                        print(f"    📊 Risk: {product_info['risk_level'].title()} | 💰 Return: {product_info['expected_return']} | 🔄 Liquidity: {product_info['liquidity'].title()}")
            except Exception as e:
                print(f"❌ Error getting risk-based recommendations: {e}")
                risk_based_products = []
            
            # 4. Final recommendation formatting
            if not risk_based_products:
                # Fallback recommendations if the main method fails
                risk_based_products = self._get_fallback_recommendations(risk_tolerance)
                recommendations['detailed_products'] = risk_based_products
            
            # Create final formatted recommendations
            final_recommendations = []
            for i, product_info in enumerate(risk_based_products[:5], 1):  # Top 5
                try:
                    details = self.get_product_details(product_info['product'])
                    
                    # Create standardized recommendation format
                    rec = {
                        'name': product_info['product'],
                        'rank': i,
                        'expected_return': product_info['expected_return'],
                        'risk_level': product_info['risk_level'].title(),
                        'liquidity': product_info['liquidity'].title(),
                        'description': product_info.get('description', details.get('description', ''))[:200],
                        'suitability_score': self._calculate_suitability_score(product_info, user_data),
                        'pros': details.get('pros', [])[:3],  # Limit to top 3
                        'cons': details.get('cons', [])[:3],  # Limit to top 3
                    }
                    final_recommendations.append(rec)
                    
                except Exception as e:
                    print(f"❌ Error processing recommendation {i}: {e}")
                    continue
            
            # Update the detailed_products with the final format
            recommendations['detailed_products'] = final_recommendations
            
            print(f"✅ Summary: Generated {len(final_recommendations)} recommendations")
            if ml_prediction is not None:
                print(f"🤖 ML Model Prediction: {ml_prediction:.1%} investment probability")
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
            # Return fallback recommendations instead of None
            return self._get_emergency_recommendations(user_data)

    def _get_fallback_recommendations(self, risk_tolerance):
        """Fallback recommendations when main method fails"""
                
        fallback_products = {
            'Low': [
                {'product': 'Treasury Bills (T-Bills)', 'risk_level': 'Low', 'expected_return': '6-10%', 'liquidity': 'High'},
                {'product': 'Money Market Funds', 'risk_level': 'Low', 'expected_return': '6-9%', 'liquidity': 'High'},
                {'product': 'Bank Fixed Deposits', 'risk_level': 'Low', 'expected_return': '5-8%', 'liquidity': 'Low'}
            ],
            'Medium': [
                {'product': 'Unit Trusts/Mutual Funds', 'risk_level': 'Medium', 'expected_return': '8-15%', 'liquidity': 'Medium'},
                {'product': 'Government Bonds (Treasury Bonds)', 'risk_level': 'Low', 'expected_return': '8-12%', 'liquidity': 'Medium'},
                {'product': 'Real Estate Investment Trusts (REITs)', 'risk_level': 'Medium', 'expected_return': '8-14%', 'liquidity': 'Medium'}
            ],
            'High': [
                {'product': 'Nairobi Securities Exchange (NSE) Stocks', 'risk_level': 'High', 'expected_return': '12-25%', 'liquidity': 'High'},
                {'product': 'Unit Trusts/Mutual Funds', 'risk_level': 'Medium', 'expected_return': '8-15%', 'liquidity': 'Medium'},
                {'product': 'Real Estate Investment', 'risk_level': 'Medium', 'expected_return': '10-20%', 'liquidity': 'Low'}
            ]
        }
        
        return fallback_products.get(risk_tolerance, fallback_products['Medium'])

    def _get_emergency_recommendations(self, user_data):
        """Emergency fallback when everything fails"""
        print("⚠️ Using emergency recommendations")
        
        try:
            risk_tolerance = user_data.get('risk_tolerance', 'Medium') if user_data else 'Medium'
        except:
            risk_tolerance = 'Medium'
        
        return {
            'user_segment': 'balanced_investor',
            'risk_tolerance': risk_tolerance,
            'segment_recommendations': ['medium_risk'],
            'risk_recommendations': ['Government Bonds', 'Unit Trusts'],
            'detailed_products': [
                {
                    'name': 'Government Bonds (Treasury Bonds)',
                    'rank': 1,
                    'expected_return': '8-12%',
                    'risk_level': 'Low',
                    'liquidity': 'Medium',
                    'description': 'Safe government securities with guaranteed returns',
                    'suitability_score': 0.8,
                    'pros': ['Government guaranteed', 'Regular interest payments'],
                    'cons': ['Lower returns', 'Interest rate risk']
                },
                {
                    'name': 'Unit Trusts/Mutual Funds',
                    'rank': 2,
                    'expected_return': '8-15%',
                    'risk_level': 'Medium',
                    'liquidity': 'Medium',
                    'description': 'Professional managed diversified investment funds',
                    'suitability_score': 0.75,
                    'pros': ['Professional management', 'Diversification'],
                    'cons': ['Management fees', 'Market risk']
                }
            ],
            'investment_probability': 0.65
        }

    def _calculate_suitability_score(self, product_info, user_data):
        """Calculate how suitable a product is for the user"""
        try:
            score = 0.5  # Base score
            
            # Risk alignment (40% weight)
            user_risk = user_data.get('risk_tolerance', 'Medium')
            product_risk = product_info.get('risk_level', 'Medium')
            
            risk_levels = ['Low', 'Medium', 'High', 'Very High']
            try:
                user_risk_idx = risk_levels.index(user_risk)
                product_risk_idx = risk_levels.index(product_risk)
                
                if user_risk_idx == product_risk_idx:
                    score += 0.4
                elif abs(user_risk_idx - product_risk_idx) == 1:
                    score += 0.2
                else:
                    score += 0.0
            except ValueError:
                score += 0.2  # Default if risk level not found
            
            # Age factor (20% weight)
            age = user_data.get('age', 30)
            if age < 35 and product_risk in ['Medium', 'High']:
                score += 0.2
            elif age >= 50 and product_risk == 'Low':
                score += 0.2
            elif 35 <= age < 50:
                score += 0.1
            
            # Income factor (20% weight)
            income = user_data.get('monthly_income', 30000)
            if income > 100000:
                score += 0.2
            elif income > 50000:
                score += 0.1
            
            # Investment horizon factor (20% weight)
            horizon = user_data.get('investment_horizon', '')
            liquidity = product_info.get('liquidity', '')
            
            if 'Long-term' in horizon and liquidity in ['Low', 'Very Low']:
                score += 0.2
            elif 'Short-term' in horizon and liquidity == 'High':
                score += 0.2
            else:
                score += 0.1
            
            return min(1.0, max(0.0, score))  # Ensure score is between 0 and 1
            
        except Exception as e:
            print(f"❌ Error calculating suitability score: {e}")
            return 0.75  # Default score

    def get_model_info(self):
        """Get information about loaded models"""
        info = {
            'models_loaded': self.best_model_name is not None,
            'best_model': self.best_model_name,
            'available_models': list(self.model_pipelines.keys()) if self.model_pipelines else [],
            'preprocessor_loaded': self.preprocessor is not None,
            'config_loaded': self.model_config is not None
        }
        
        if self.model_config:
            info.update({
                'model_config': self.model_config
            })
        
        return info

    def print_model_status(self):
        """Print detailed model loading status"""
        print("\n" + "="*50)
        print("🤖 MODEL STATUS REPORT")
        print("="*50)
        
        info = self.get_model_info()
        
        print(f"📊 Models Loaded: {'✅ YES' if info['models_loaded'] else '❌ NO'}")
        print(f"🎯 Best Model: {info['best_model'] if info['best_model'] else 'None'}")
        print(f"📋 Available Models: {info['available_models'] if info['available_models'] else 'None'}")
        print(f"🔧 Preprocessor: {'✅ Loaded' if info['preprocessor_loaded'] else '❌ Not Loaded'}")
        print(f"⚙️ Config: {'✅ Loaded' if info['config_loaded'] else '❌ Not Loaded'}")
        
        if info['config_loaded'] and self.model_config:
            print("\n📈 Model Configuration:")
            for key, value in self.model_config.items():
                print(f"  • {key}: {value}")
        
        print("\n" + "="*50)
