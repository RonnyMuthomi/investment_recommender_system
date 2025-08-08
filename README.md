#  Investment Recommender System

##  Personalized Investment Strategy Recommendation Using Machine Learning


## The Problem

<img width="850" height="540" alt="image" src="https://github.com/user-attachments/assets/82d4c01a-62f6-4673-8145-2123423d0bf6" />


In Kenya, deciding on the right investment plan is a challenge for many people. While there are a growing number of financial products  such as government bonds, unit trusts, SACCOs, insurance-linked investments, and real estate options  most potential investors still struggle to make informed choices that align with their financial goals and risk appetite. According to a [Central Bank of Kenya Financial Access Survey](https://www.centralbank.go.ke), a significant portion of the population either does not invest at all or chooses investment vehicles that do not meet their long-term objectives. 

One of the most common reasons is **limited access to clear, comparative, and personalized investment information**. Many Kenyans rely on word-of-mouth recommendations or informal advice, which can lead to mismatched investments, poor returns, and in some cases, complete loss of capital. A 2023 report by [FSD Kenya](https://fsdkenya.org) revealed that less than 30% of respondents felt confident that they understood the risks and returns of the investment products they had chosen. Furthermore, **hidden fees, unclear terms, and the absence of tailored financial guidance** remain major deterrents for those who wish to start investing.

In my own experience engaging with investment discussions in community groups and online forums, I have observed that most potential investors ask the same questions:  
- *“Which investment plan will give me the best returns?”*  
- *“Is this option safe or is it a scam?”*  
- *“How do I compare different plans fairly?”*  

This uncertainty often results in inaction, overreliance on low-yield savings accounts, or rushed decisions into high-risk investments. Even for those who do invest, the lack of a structured decision-making process means their choices are often not aligned with their income level, future plans, or personal risk tolerance. **Without tools that simplify comparison and provide data-driven recommendations, many Kenyans are unable to make optimal investment decisions.**


<img width="850" height="540" alt="image" src="https://github.com/user-attachments/assets/d7d08fc7-f08c-4149-a725-490a707fbd6d" />


## Business Understanding

Over the past decade, Kenya’s financial landscape has rapidly expanded, offering citizens a wide range of investment opportunities. Products such as government bonds, treasury bills, unit trusts, SACCO savings, insurance-linked investments, and real estate ventures have become increasingly accessible to the public. According to the 2024 [FinAccess Household Survey](https://fsdkenya.org/publication/2024-finaccess-household-survey/), the proportion of Kenyans who have ever invested in a formal financial product has grown steadily yet nearly **40% of adults still rely exclusively on low-interest savings accounts or informal savings groups (chamas)**. This gap is not simply due to lack of funds; it is often driven by a shortage of clear, personalized, and easily comparable investment information.

Several factors have contributed to this situation. First, while financial institutions market their products widely, the details are often presented in complex terms that are difficult for the average consumer to interpret. Second, most potential investors rely heavily on word-of-mouth recommendations from friends or family, which, while trustworthy, may not align with their financial goals or risk tolerance. Third, hidden costs, unclear contract terms, and inconsistent guidance from advisors create barriers that discourage first-time investors from exploring higher-yield opportunities. 

The FinAccess data also highlights an interesting behavioral trend: **many Kenyans choose "safe" investment options by default, even when higher-return opportunities with manageable risk are available**. For example, despite the steady returns from regulated unit trusts or government bonds, uptake remains low compared to informal savings channels. This shows that the challenge is not simply increasing product availability, but helping citizens match products to their financial profiles.

<img width="850" height="540" alt="image" src="https://github.com/user-attachments/assets/2ea9ab7b-8ce5-4611-b03e-a3a696f5b93c" />


At the same time, there is a growing national push toward financial inclusion and digital finance adoption. The Central Bank of Kenya, in partnership with FSD Kenya and the Kenya National Bureau of Statistics, continues to track financial behavior trends, providing a rich dataset that can be leveraged to create intelligent decision-support tools. With the rise of mobile technology, there is an opportunity to reach millions of people with personalized investment recommendations bridging the gap between financial products and consumer understanding.

An **Investment Plan Recommender System** could help solve this challenge. By analyzing a potential investor’s income, goals, time horizon, and risk appetite, such a system could recommend a short, ranked list of suitable investment options. This would reduce decision-making complexity, empower first-time investors, and improve portfolio quality for seasoned ones.

## Purpose of Analysis

The goal of this project is to build a data-driven model that recommends optimal investment plans for individuals based on their unique financial profiles. Using publicly available datasets such as the 2024 FinAccess Household Survey, we aim to identify patterns in investment behavior, segment investors by risk preference, and map suitable products to these segments. 

<img width="850" height="540" alt="image" src="https://github.com/user-attachments/assets/7579156d-4fda-4c7c-a341-3d39f4c6ca2b" />

The model will focus on:
- **Accuracy**: Recommending plans that truly match the investor’s profile.
- **Personalization**: Factoring in income, age, goals, and risk tolerance.
- **Trust**: Ensuring recommendations are drawn from credible, regulated financial products.

Ultimately, the system will serve as a prototype for a mobile or web-based advisory tool, giving Kenyans the confidence to make informed investment choices — and in turn, driving higher participation in formal financial markets.

## Data Understanding & Preprocessing

The dataset used in this project was derived from national financial access survey data, containing information on respondents’ demographics, income levels, financial literacy, savings habits, and previous investment behaviors. Initial exploration revealed that the data included both relevant and irrelevant variables, as well as inconsistencies in formatting and missing values. Key fields influencing investment decisions such as age, gender, income bracket, risk appetite, location, and financial product usage  were identified and retained, while unrelated survey questions, administrative codes, and non-financial attributes were removed to reduce noise and improve model efficiency.[FinAccess Household Survey](https://fsdkenya.org/publication/2024-finaccess-household-survey/)

Preprocessing began with a comprehensive cleaning process to ensure consistency and reliability. Categorical values were standardized (such as consolidating variations such as `"M"`, `"Male"`, and `"m"` into a single `"Male"` category), and numerical fields were formatted uniformly. Missing values were handled using context-appropriate strategies, including imputation for incomplete income data and removal of records lacking critical decision-making attributes. Duplicate entries were eliminated to prevent model bias.

<img width="1489" height="989" alt="image" src="https://github.com/user-attachments/assets/3f49e7d3-7bcf-4e55-8e1e-f676bee85fdd" />

Feature engineering was applied to enhance predictive capability, including the creation of composite indicators such as an **Investment Readiness Score** and a **Risk Category** derived from multiple survey responses. Categorical data was encoded into numerical form for machine learning compatibility, and continuous variables such as income were normalized to maintain scale consistency. Finally, the dataset was split into training, validation, and testing sets, ensuring robust model evaluation and reducing the risk of overfitting.


### EDA

An exploratory data analysis (EDA) was conducted to gain insights into the dataset and to identify patterns that could influence investment plan recommendations. The target variable represented the preferred investment plan for each respondent, covering categories such as savings accounts, fixed deposits, government bonds, mutual funds, stocks, and real estate. The class distribution showed that low-risk investments like savings accounts and fixed deposits had slightly higher representation, while high-risk investments such as stocks and mutual funds were less frequent. Although this introduced some imbalance, the distribution remained sufficient to avoid extreme model bias.

The dataset included both demographic and behavioral features, such as age group, gender, location (urban vs. rural), income level, education level, financial literacy score, and risk appetite. Behavioral and financial variables like monthly savings, prior investment experience, and access to financial advisory services were also present, enabling the model to capture nuanced decision-making patterns. Income level, risk appetite, and financial literacy emerged as the strongest influencers of investment preferences, with higher-income respondents tending toward diversified portfolios and lower-income groups favoring safer, guaranteed-return options.

Visualization of feature distributions revealed clear trends: younger respondents (ages 18–30) showed greater interest in moderate-to-high risk investments, while older respondents (50+) leaned toward low-risk, fixed-income instruments. A correlation heatmap further confirmed the strong positive relationship between income and high-risk investment selection, and a negative relationship between low financial literacy and complex investment products. Outliers were minimal and largely tied to extreme income values, which were retained as they represent realistic, albeit rare, market segments.

<img width="990" height="589" alt="image" src="https://github.com/user-attachments/assets/ca7b28c4-580b-48d1-83a1-9ae117f09228" />

The overall analysis indicated that the dataset was rich in predictive features, relatively clean, and sufficiently diverse to allow the model to learn both general and niche investment behaviors. These insights also guided preprocessing steps, such as scaling numeric features, encoding categorical variables, and handling mild class imbalance, to prepare the data for model training.



## Modeling

The modeling phase focused on selecting, training, and evaluating algorithms that could accurately predict a user’s ideal investment plan based on their demographic, financial, and behavioral profile. Multiple supervised learning algorithms were explored, including Decision Tree, Random Forest, Gradient Boosting, Logistic Regression, and a simple Neural Network. Each model was trained using the preprocessed dataset, which included encoded categorical features, scaled numeric variables, and balanced classes to minimize bias.

The training process was iterative: hyperparameter tuning was performed via grid search and cross-validation to optimize performance, and evaluation metrics such as F1-score, accuracy, and confusion matrices were used to assess model effectiveness. Ensemble methods such as Random Forest and Gradient Boosting consistently achieved the highest scores, benefiting from their ability to capture non-linear relationships between features and the target variable.

<img width="1189" height="390" alt="image" src="https://github.com/user-attachments/assets/bed60146-3566-4351-bfb0-6d209fb8bd5b" />

Once the best-performing models were identified, the configuration, preprocessing pipeline, and trained model objects were serialized into `.pkl` files for reproducibility and deployment. This ensured that the production environment would mirror the training setup, enabling consistent and reliable predictions in real-world use.

<img width="790" height="540" alt="image" src="https://github.com/user-attachments/assets/0242e1f3-eaf8-4eb9-a3a2-da280aa37a93" />


## Deployment

The deployment strategy was designed to make the recommender system accessible via both an API and a user-friendly web interface. The backend API, built with FastAPI, served as the prediction engine, exposing endpoints for submitting user profile data and returning investment recommendations in real time. This API also included built-in documentation, health check endpoints, and CORS configuration to enable seamless integration with the frontend.

The frontend interface was developed using Streamlit, offering an interactive form for users to enter their financial and demographic information. Upon submission, the form communicates with the API to fetch the recommended investment plan, which is then displayed instantly to the user. The deployment pipeline ensured that both components — the API and Streamlit application — could run locally or be containerized for cloud hosting.

**Deployment workflow:**
1. **Train the model** by running all cells in `index.ipynb` to generate deployment-ready `.pkl` files.
2. **Start the API server**:
   ```bash
   cd streamlit
   python api.py

## System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │  ML Models      │
│   Frontend      │◄──►│    Backend      │◄──►│  & Data         │
│   (Port 8501)   │    │   (Port 8000)   │    │  Processing     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                        
```


