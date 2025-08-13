from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from fastapi.responses import RedirectResponse
from pyngrok import ngrok
import webbrowser
import json
from datetime import datetime
import numpy as np
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from Investment_System import InvestmentRecommendationSystem
except ImportError:
    logger.error("Could not import InvestmentRecommendationSystem")
    # Create a dummy class for deployment
    class InvestmentRecommendationSystem:
        def __init__(self):
            self.investment_products = {}
        
        def get_recommendations(self, user_data):
            return []
        
        def get_user_segment(self, user_data):
            return "balanced_investor"
        
        def get_portfolio_allocation(self, risk_tolerance):
            return {"bonds": 60, "stocks": 40}

app = FastAPI(
    title="Kenya Investment Advisor API",
    description="AI-powered investment recommendation system for the Kenyan market",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models with proper validation
class UserProfile(BaseModel):
    name: str
    age: int = 30
    location: str = "Urban"
    education: str = "Secondary"
    employment: str = "Employed"
    household_size: int = 3
    monthly_income: float
    monthly_expenses: float
    current_savings: float = 0
    debt_amount: float = 0
    dependents: int = 0
    emergency_fund: str = "No"
    risk_tolerance: str = "Medium"
    investment_horizon: str = "Medium-term (2-5 years)"
    investment_amount: float
    investment_goals: List[str] = []
    investment_experience: str = "Beginner"
    preferred_sectors: List[str] = []

class RecommendationResponse(BaseModel):
    user_segment: str
    risk_tolerance: str
    recommendations: List[Dict[str, Any]]
    portfolio_allocation: Dict[str, float]
    investment_probability: Optional[float] = None
    generated_date: datetime

# Initialize system with error handling
try:
    system = InvestmentRecommendationSystem()
    logger.info("Investment system initialized successfully")
except Exception as e:
    logger.error(f"Error initializing system: {e}")
    system = InvestmentRecommendationSystem()

@app.get("/")
async def redirect_root():
    return RedirectResponse(url="/docs")

@app.get("/model-status")
async def get_model_status():
    """Get information about loaded ML models"""
    try:
        model_info = system.get_model_info()
        return {
            "status": "success",
            "models_loaded": model_info['models_loaded'],
            "best_model": model_info['best_model'],
            "available_models": model_info['available_models'],
            "timestamp": datetime.now()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now()
        }

@app.get("/health")
async def health_check():
    model_info = system.get_model_info() if hasattr(system, 'get_model_info') else {}
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "system_initialized": hasattr(system, 'investment_products'),
        "models_loaded": model_info.get('models_loaded', False),
        "best_model": model_info.get('best_model', None)
    }

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(user_profile: UserProfile):
    """Generate personalized investment recommendations"""
    try:
        # Convert to dict safely
        user_data = user_profile.model_dump()
        
        # Get recommendations with error handling
        try:
            recommendations = system.get_recommendations(user_data=user_data)
            if not recommendations:
                recommendations = []
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            recommendations = []
        
        # Get user segment safely
        try:
            user_segment = system.get_user_segment(user_data)
        except Exception as e:
            logger.error(f"Error getting user segment: {e}")
            user_segment = "balanced_investor"
        
        # Get portfolio allocation safely
        try:
            portfolio_allocation = system.get_portfolio_allocation(user_data['risk_tolerance'])
        except Exception as e:
            logger.error(f"Error getting portfolio allocation: {e}")
            # Default allocation based on risk tolerance
            risk = user_data['risk_tolerance'].lower()
            if risk == 'low':
                portfolio_allocation = {"Government Bonds": 50, "Money Market": 30, "Fixed Deposits": 20}
            elif risk == 'high':
                portfolio_allocation = {"Stocks": 40, "Unit Trusts": 30, "REITs": 20, "Bonds": 10}
            else:
                portfolio_allocation = {"Unit Trusts": 35, "Bonds": 30, "Stocks": 20, "Money Market": 15}
        
        # Calculate investment probability
        try:
            investment_probability = min(0.95, 
                0.6 + (user_data['monthly_income'] / 100000) * 0.2 + 
                (user_data['age'] / 100) * 0.15
            )
        except:
            investment_probability = 0.75
        
        # Ensure recommendations is a list
        if not isinstance(recommendations, list):
            if isinstance(recommendations, dict):
                recommendations = recommendations.get('detailed_products', [])
            else:
                recommendations = []
        
        response = RecommendationResponse(
            user_segment=user_segment,
            risk_tolerance=user_data['risk_tolerance'],
            recommendations=recommendations[:5],
            portfolio_allocation=portfolio_allocation,
            investment_probability=investment_probability,
            generated_date=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return {
        "error": {
            "message": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    }

if __name__ == "__main__":
    public_url = ngrok.connect(8000)
    print(f"Public URL: {public_url} (will redirect to /docs)")
    webbrowser.open(f"{public_url}/docs")
    uvicorn.run(app, host="localhost", port=8000, reload=False)
