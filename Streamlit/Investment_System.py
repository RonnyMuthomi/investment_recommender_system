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
warnings.filterwarnings('ignore')


class InvestmentRecommendationSystem:
    def __init__(self):
        self.investment_products = self._define_investment_products()
        self.risk_categories = self._define_risk_categories()
        self.segment_recommendations = self._define_segment_recommendations()
        self.best_model_name = None
        self.model_pipelines = {}

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
        
    def set_model(self, model_name, pipeline):
        """Set the ML model for predictions"""
        self.best_model_name = model_name
        self.model_pipelines = {model_name: {'pipeline': pipeline}}

    def get_portfolio_allocation(self, risk_tolerance):
        """Get portfolio allocation based on risk tolerance"""
        risk_tolerance = risk_tolerance.lower()
        
        allocations = {
            'Low': {
                'Government Bonds': 40,
                'Money Market Funds': 30,
                'Bank Fixed Deposits': 20,
                'High-Yield Savings': 10
            },
            'Medium': {
                'Unit Trusts/Mutual Funds': 30,
                'Government Bonds': 25,
                'Real Estate Investment Trusts (REITs)': 20,
                'NSE Stocks': 15,
                'Money Market Funds': 10
            },
            'High': {
                'NSE Stocks': 35,
                'Unit Trusts/Mutual Funds': 25,
                'Small Business Investment': 15,
                'Real Estate Investment Trusts (REITs)': 15,
                'Commodity Trading': 10
            }
        }
        
        return allocations.get(risk_tolerance, allocations['Medium'])

    def get_recommendations(self, user_id=None, user_data=None, df=None):
        """Generate personalized investment recommendations with proper risk categorization"""
    
        if user_data is None and user_id is not None and df is not None:
            if user_id in df.index:
                user_data = df.loc[user_id].to_dict()
            else:
                # Use logging instead of print in production
                import logging
                logging.warning(f"User {user_id} not found in dataset")
                return []  # Return empty list instead of None
        
        if user_data is None:
            import logging
            logging.warning("No user data provided")
            return []  # Return empty list instead of None
        
        try:
            # Get user characteristics with fallback values
            user_segment = self.get_user_segment(user_data)
            
            # Fix: Handle risk_tolerance from user_data directly if available
            risk_tolerance = user_data.get('risk_tolerance', 'Medium')
            if not risk_tolerance:
                risk_tolerance = self.get_risk_tolerance(user_data)
            
            # Use logging instead of print in production
            import logging
            logging.info(f"Investment Recommendations for User")
            logging.info(f"User Segment: {user_segment}")
            logging.info(f"Risk Tolerance: {risk_tolerance}")
            
            recommendations = {
                'user_segment': user_segment,
                'risk_tolerance': risk_tolerance,
                'segment_recommendations': [],
                'risk_recommendations': [],
                'detailed_products': [],
                'investment_probability': None
            }
            
            # 1. Segment-based recommendations
            if user_segment in self.segment_recommendations:
                segment_risk_categories = self.segment_recommendations[user_segment]
                recommendations['segment_recommendations'] = segment_risk_categories
                
                logging.info(f"Segment-Based Risk Categories:")
                for risk_category in segment_risk_categories:
                    try:
                        products = self.get_products_by_risk(risk_category)
                        logging.info(f"  {risk_category.replace('_', ' ').title()}: {len(products)} products")
                    except Exception as e:
                        logging.error(f"Error getting products for {risk_category}: {e}")
            
            # 2. Risk-based recommendations
            try:
                risk_based_products = self.get_recommendations_by_risk_tolerance(risk_tolerance)
                if risk_based_products:
                    recommendations['risk_recommendations'] = [p['product'] for p in risk_based_products]
                    recommendations['detailed_products'] = risk_based_products
                    
                    logging.info(f"Risk-Based Product Recommendations ({len(risk_based_products)} products):")
                    for product_info in risk_based_products[:5]:  # Show top 5
                        logging.info(f"  • {product_info['product']}")
                        logging.info(f"    Risk: {product_info['risk_level'].title()} | Return: {product_info['expected_return']} | Liquidity: {product_info['liquidity'].title()}")
            except Exception as e:
                logging.error(f"Error getting risk-based recommendations: {e}")
                risk_based_products = []
            
            # 3. Model-based prediction (if model available)
            if self.best_model_name and self.best_model_name in self.model_pipelines:
                try:
                    import pandas as pd
                    # Create user features dataframe
                    user_df = pd.DataFrame([user_data])
                    
                    # Get prediction
                    pipeline = self.model_pipelines[self.best_model_name]['pipeline']
                    
                    # Try to predict probability
                    if hasattr(pipeline, 'named_steps') and hasattr(pipeline.named_steps.get('classifier'), 'predict_proba'):
                        prob = pipeline.predict_proba(user_df)[0][1]
                    elif hasattr(pipeline, 'predict_proba'):
                        prob = pipeline.predict_proba(user_df)[0][1]
                    else:
                        prob = pipeline.predict(user_df)[0]
                    
                    recommendations['investment_probability'] = float(prob)
                    logging.info(f"Model Prediction: {prob:.1%} likelihood to invest in formal products")
                    
                except Exception as e:
                    logging.warning(f"Could not generate model prediction: {str(e)}")
                    # Set a default probability based on user profile
                    try:
                        age = user_data.get('age', 30)
                        income = user_data.get('monthly_income', 30000)
                        prob = min(0.95, 0.4 + (income / 100000) * 0.3 + (age / 100) * 0.2)
                        recommendations['investment_probability'] = prob
                    except:
                        recommendations['investment_probability'] = 0.65
            
            # 4. Final recommendation summary and create proper return format
            if not risk_based_products:
                # Fallback recommendations if the main method fails
                risk_based_products = self._get_fallback_recommendations(risk_tolerance)
                recommendations['detailed_products'] = risk_based_products
            
            logging.info(f"Summary: Generated {len(risk_based_products)} recommendations")
            
            # Return the recommendations in a format compatible with your API
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
                    logging.error(f"Error processing recommendation {i}: {e}")
                    continue
            
            # Update the detailed_products with the final format
            recommendations['detailed_products'] = final_recommendations
            
            return recommendations
            
        except Exception as e:
            import logging
            logging.error(f"Error generating recommendations: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            
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
        
        return fallback_products.get(risk_tolerance, fallback_products['medium'])

    def _get_emergency_recommendations(self, user_data):
        """Emergency fallback when everything fails"""
        import logging
        logging.error("Using emergency recommendations")
        
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
            
            if user_risk == product_risk:
                score += 0.4
            elif abs(['Low', 'Medium', 'High'].index(user_risk) - ['Low', 'Medium', 'High'].index(product_risk)) == 1:
                score += 0.2
            
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
            if 'Long-term' in horizon and product_info.get('liquidity', '') in ['Low', 'Very Low']:
                score += 0.2
            elif 'Short-term' in horizon and product_info.get('liquidity', '') == 'High':
                score += 0.2
            else:
                score += 0.1
            
            return min(1.0, max(0.0, score))  # Ensure score is between 0 and 1
            
        except Exception as e:
            import logging
            logging.error(f"Error calculating suitability score: {e}")
            return 0.75  # Default score