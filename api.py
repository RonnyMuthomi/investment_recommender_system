from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://recommender:securepassword@localhost/investment_recommender')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Numeric)
    risk_tolerance = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class FinancialProduct(db.Model):
    __tablename__ = 'financial_products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    risk_level = db.Column(db.String(20))
    min_amount = db.Column(db.Numeric)
    expected_return = db.Column(db.Numeric)
    features = db.Column(db.JSON)

# Load recommendation model
model = joblib.load('recommendation_model.pkl')
product_features = pd.read_csv('product_features.csv')

# Helper functions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['sub'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'sub': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

@app.route('/api/user', methods=['GET'])
@token_required
def get_user(current_user):
    user_data = {
        'user_id': current_user.user_id,
        'username': current_user.username,
        'email': current_user.email,
        'age': current_user.age,
        'income': float(current_user.income) if current_user.income else None,
        'risk_tolerance': current_user.risk_tolerance,
        'created_at': current_user.created_at.isoformat()
    }
    return jsonify(user_data)

@app.route('/api/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    current_user.age = data.get('age', current_user.age)
    current_user.income = data.get('income', current_user.income)
    current_user.risk_tolerance = data.get('risk_tolerance', current_user.risk_tolerance)
    
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = FinancialProduct.query.all()
    
    result = []
    for product in products:
        product_data = {
            'product_id': product.product_id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'risk_level': product.risk_level,
            'min_amount': float(product.min_amount) if product.min_amount else None,
            'expected_return': float(product.expected_return) if product.expected_return else None,
            'features': product.features
        }
        result.append(product_data)
    
    return jsonify(result)

@app.route('/api/recommend', methods=['POST'])
@token_required
def recommend(current_user):
    data = request.get_json()
    
    # Prepare user features for the model
    user_features = pd.DataFrame({
        'age': [data.get('age', current_user.age)],
        'income': [data.get('income', float(current_user.income)) if current_user.income else 500000],
        'risk_tolerance': [data.get('risk_tolerance', current_user.risk_tolerance) or 'Medium']
    })
    
    # Convert categorical to numerical
    risk_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    user_features['risk_tolerance'] = user_features['risk_tolerance'].map(risk_mapping)
    
    # Get recommendations
    distances, indices = model.kneighbors(user_features)
    
    # Get recommended products
    recommended_products = []
    for idx in indices[0]:
        product = FinancialProduct.query.get(product_features.iloc[idx]['product_id'])
        if product:
            recommended_products.append({
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'description': product.description,
                'risk_level': product.risk_level,
                'min_amount': float(product.min_amount) if product.min_amount else None,
                'expected_return': float(product.expected_return) if product.expected_return else None,
                'features': product.features
            })
    
    return jsonify(recommended_products)

if __name__ == '__main__':
    app.run(debug=True)