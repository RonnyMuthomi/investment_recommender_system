#  Smart Investment Plan Recommender

##  Personalized Investment Strategy Recommendation Using Machine Learning


## The Problem

<img width="850" height="380" alt="image" src="https://github.com/user-attachments/assets/82d4c01a-62f6-4673-8145-2123423d0bf6" />


In Kenya, deciding on the right investment plan is a challenge for many people. While there are a growing number of financial products  such as government bonds, unit trusts, SACCOs, insurance-linked investments, and real estate options  most potential investors still struggle to make informed choices that align with their financial goals and risk appetite. According to a [Central Bank of Kenya Financial Access Survey](https://www.centralbank.go.ke), a significant portion of the population either does not invest at all or chooses investment vehicles that do not meet their long-term objectives. 

One of the most common reasons is **limited access to clear, comparative, and personalized investment information**. Many Kenyans rely on word-of-mouth recommendations or informal advice, which can lead to mismatched investments, poor returns, and in some cases, complete loss of capital. A 2023 report by [FSD Kenya](https://fsdkenya.org) revealed that less than 30% of respondents felt confident that they understood the risks and returns of the investment products they had chosen. Furthermore, **hidden fees, unclear terms, and the absence of tailored financial guidance** remain major deterrents for those who wish to start investing.

In my own experience engaging with investment discussions in community groups and online forums, I have observed that most potential investors ask the same questions:  
- *“Which investment plan will give me the best returns?”*  
- *“Is this option safe or is it a scam?”*  
- *“How do I compare different plans fairly?”*  

This uncertainty often results in inaction, overreliance on low-yield savings accounts, or rushed decisions into high-risk investments. Even for those who do invest, the lack of a structured decision-making process means their choices are often not aligned with their income level, future plans, or personal risk tolerance. **Without tools that simplify comparison and provide data-driven recommendations, many Kenyans are unable to make optimal investment decisions.**


<img width="850" height="380" alt="image" src="https://github.com/user-attachments/assets/d7d08fc7-f08c-4149-a725-490a707fbd6d" />


## Business Understanding

Over the past decade, Kenya’s financial landscape has rapidly expanded, offering citizens a wide range of investment opportunities. Products such as government bonds, treasury bills, unit trusts, SACCO savings, insurance-linked investments, and real estate ventures have become increasingly accessible to the public. According to the 2024 [FinAccess Household Survey](https://fsdkenya.org/publication/2024-finaccess-household-survey/), the proportion of Kenyans who have ever invested in a formal financial product has grown steadily yet nearly **40% of adults still rely exclusively on low-interest savings accounts or informal savings groups (chamas)**. This gap is not simply due to lack of funds; it is often driven by a shortage of clear, personalized, and easily comparable investment information.

Several factors have contributed to this situation. First, while financial institutions market their products widely, the details are often presented in complex terms that are difficult for the average consumer to interpret. Second, most potential investors rely heavily on word-of-mouth recommendations from friends or family, which, while trustworthy, may not align with their financial goals or risk tolerance. Third, hidden costs, unclear contract terms, and inconsistent guidance from advisors create barriers that discourage first-time investors from exploring higher-yield opportunities. 

The FinAccess data also highlights an interesting behavioral trend: **many Kenyans choose "safe" investment options by default, even when higher-return opportunities with manageable risk are available**. For example, despite the steady returns from regulated unit trusts or government bonds, uptake remains low compared to informal savings channels. This shows that the challenge is not simply increasing product availability, but helping citizens match products to their financial profiles.

<img width="850" height="380" alt="image" src="https://github.com/user-attachments/assets/2ea9ab7b-8ce5-4611-b03e-a3a696f5b93c" />


At the same time, there is a growing national push toward financial inclusion and digital finance adoption. The Central Bank of Kenya, in partnership with FSD Kenya and the Kenya National Bureau of Statistics, continues to track financial behavior trends, providing a rich dataset that can be leveraged to create intelligent decision-support tools. With the rise of mobile technology, there is an opportunity to reach millions of people with personalized investment recommendations bridging the gap between financial products and consumer understanding.

An **Investment Plan Recommender System** could help solve this challenge. By analyzing a potential investor’s income, goals, time horizon, and risk appetite, such a system could recommend a short, ranked list of suitable investment options. This would reduce decision-making complexity, empower first-time investors, and improve portfolio quality for seasoned ones.

## Purpose of Analysis

The goal of this project is to build a data-driven model that recommends optimal investment plans for individuals based on their unique financial profiles. Using publicly available datasets such as the 2024 FinAccess Household Survey, we aim to identify patterns in investment behavior, segment investors by risk preference, and map suitable products to these segments. 

<img width="850" height="380" alt="image" src="https://github.com/user-attachments/assets/7579156d-4fda-4c7c-a341-3d39f4c6ca2b" />

The model will focus on:
- **Accuracy**: Recommending plans that truly match the investor’s profile.
- **Personalization**: Factoring in income, age, goals, and risk tolerance.
- **Trust**: Ensuring recommendations are drawn from credible, regulated financial products.

Ultimately, the system will serve as a prototype for a mobile or web-based advisory tool, giving Kenyans the confidence to make informed investment choices — and in turn, driving higher participation in formal financial markets.


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
