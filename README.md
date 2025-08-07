# Investment Recommendation System
A personalized investment recommender system for Kenyan investors, built using CRISP-DM methodology. Combines risk profiling, financial goal forecasting, liquidity analysis, and hybrid recommendation algorithms to deliver tailored investment advice across SACCOs, MMFs, stocks, T-bills, and more.

An AI-powered investment recommendation system that provides personalized investment suggestions based on user profiles and financial data.

## 🚀 Features

- **🤖 AI-Powered Analysis**: Advanced machine learning models for investment recommendations
- **📊 Personalized Recommendations**: Tailored suggestions based on user profile
- **🎯 Risk-Adjusted Options**: Investment categories matched to risk tolerance
- **📈 Multiple Investment Categories**: From low-risk to high-growth options
- **🌐 Web Interface**: User-friendly Streamlit application
- **🔌 REST API**: FastAPI backend for integration
- **📋 Model Pipeline**: Automated preprocessing and prediction

## 🏗️ System Architecture

```
Investment_Project/
├── streamlit/
│   └── api.py                  # FastAPI backend
│   ├── streamlit.py            # Main recommendation interface
│   └── Investment_System.py    # Investment information
├── deployment/
│   ├── investment_model_config.pkl      # Model configuration
│   ├── investment_model_pipelines.pkl   # Trained model pipelines
│   └── investment_model_preprocessor.pkl # Data preprocessing pipeline
├── data/                       # Training and test data
├── index.ipynb                 # Model training notebook
├── requirements.txt            # Python dependencies
├── deploy.py                   # Deployment script
└── README.md                   # This file
```
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │  ML Models      │
│   Frontend      │◄──►│    Backend      │◄──►│  & Data         │
│   (Port 8501)   │    │   (Port 8000)   │    │  Processing     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                        
```


## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
Before deployment, you need to train the model:

1. Open `index.ipynb` in Jupyter Notebook or JupyterLab
2. Run all cells to train the models and generate deployment files
3. Ensure the following files are created in the `deployment/` directory:
   - `investment_model_config.pkl`
   - `investment_model_pipelines.pkl`
   - `investment_model_preprocessor.pkl`

## 🚀 Quick Deployment


#### Start the API Server
```bash
cd streamlit
python api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Start the Streamlit App
```bash
cd streamlit
streamlit run streamlit.py
```

The web interface will be available at:
- **Web App**: http://localhost:8501

## 🔧 Configuration

### Model Configuration
The system uses the best performing model from training:
- Decision Tree (default)
- Random Forest
- Gradient Boosting
- Logistic Regression
- Neural Network

### API Configuration
- **Host**: localhost (configurable)
- **Port**: 8000 (configurable)
- **CORS**: Enabled for web app integration

### Streamlit Configuration
- **Port**: 8501 (configurable)
- **Theme**: Light mode
- **Layout**: Wide layout for better UX

### Web App Testing
1. Open http://localhost:8501
2. Fill out the user profile form
3. Submit to get recommendations
4. Verify the results are displayed correctly

## 📈 Model Performance

The system includes multiple models with the following performance metrics:

- **Decision Tree**: F1 Score: 1.000
- **Random Forest**: F1 Score: 1.000
- **Gradient Boosting**: F1 Score: 1.000
- **Logistic Regression**: F1 Score: 0.930
- **Neural Network**: F1 Score: 0.995

## 🔒 Security Considerations

- Input validation on all API endpoints
- CORS configuration for web app integration
- Error handling and logging
- Data privacy protection

## 🚨 Disclaimer

This system provides educational investment recommendations only. Users should:
- Consult with qualified financial advisors before making investment decisions
- Conduct their own research and due diligence
- Understand that past performance doesn't guarantee future results
- Consider their personal financial situation and risk tolerance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For technical support or questions:
- Check the API documentation at http://localhost:8000/docs
- Review the model training notebook for implementation details
- Ensure all dependencies are properly installed
