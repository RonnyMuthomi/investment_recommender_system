import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000/api"  # Replace with your API URL

def main():
    st.set_page_config(page_title="Investment Recommender", layout="wide")
    
    # Initialize session state
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Navigation
    st.sidebar.title("Navigation")
    if st.session_state.token:
        menu_options = ["Get Recommendations", "My Profile", "Financial Products", "Logout"]
    else:
        menu_options = ["Login", "Register"]
    
    choice = st.sidebar.selectbox("Menu", menu_options)

    if choice == "Login" and not st.session_state.token:
        show_login()
    elif choice == "Register" and not st.session_state.token:
        show_register()
    elif choice == "Get Recommendations" and st.session_state.token:
        show_recommendations()
    elif choice == "My Profile" and st.session_state.token:
        show_profile()
    elif choice == "Financial Products" and st.session_state.token:
        show_products()
    elif choice == "Logout" and st.session_state.token:
        st.session_state.token = None
        st.session_state.user_data = {}
        st.success("Logged out successfully")

def show_login():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            response = requests.post(
                f"{API_BASE_URL}/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                st.session_state.token = response.json().get('token')
                st.session_state.user_data = get_user_profile()
                st.success("Logged in successfully")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

def show_register():
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if password != confirm_password:
                st.error("Passwords don't match")
            else:
                response = requests.post(
                    f"{API_BASE_URL}/register",
                    json={
                        "username": username,
                        "email": email,
                        "password": password
                    }
                )
                
                if response.status_code == 201:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(response.json().get('message', 'Registration failed'))

def show_recommendations():
    st.title("Your Investment Recommendations")
    
    # Get user profile if not already loaded
    if not st.session_state.user_data:
        st.session_state.user_data = get_user_profile()
    
    # Display current profile
    with st.expander("Your Current Profile"):
        display_profile(st.session_state.user_data)
    
    # Update profile section
    st.subheader("Update Your Profile for Better Recommendations")
    with st.form("profile_form"):
        age = st.number_input("Age", min_value=18, max_value=100, 
                            value=st.session_state.user_data.get('age', 30))
        income = st.number_input("Annual Income (KSh)", min_value=0, 
                               value=st.session_state.user_data.get('income', 500000))
        risk_tolerance = st.selectbox("Risk Tolerance", 
                                    ["Low", "Medium", "High"],
                                    index=["Low", "Medium", "High"].index(
                                        st.session_state.user_data.get('risk_tolerance', 'Medium')))
        
        submitted = st.form_submit_button("Update Profile and Get Recommendations")
        
        if submitted:
            update_data = {
                "age": age,
                "income": income,
                "risk_tolerance": risk_tolerance
            }
            
            # Update profile in backend
            response = requests.put(
                f"{API_BASE_URL}/user/{st.session_state.user_data['user_id']}",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                json=update_data
            )
            
            if response.status_code == 200:
                st.session_state.user_data = response.json()
                st.success("Profile updated successfully")
            else:
                st.error("Failed to update profile")
    
    # Get recommendations
    if st.button("Get Recommendations") or submitted:
        with st.spinner("Generating recommendations..."):
            response = requests.post(
                f"{API_BASE_URL}/recommend",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                json=st.session_state.user_data
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                display_recommendations(recommendations)
            else:
                st.error("Failed to get recommendations")

def display_recommendations(recommendations):
    if not recommendations:
        st.warning("No recommendations found based on your profile")
        return
    
    st.subheader("Recommended Investment Products")
    
    for idx, product in enumerate(recommendations, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {idx}. {product['name']}")
                st.markdown(f"**Category:** {product['category']}")
                st.markdown(f"**Risk Level:** {product['risk_level']}")
                st.markdown(f"**Minimum Amount:** KSh {product['min_amount']:,.2f}")
                st.markdown(f"**Expected Return:** {product['expected_return']}%")
                
            with col2:
                if st.button("Learn More", key=f"btn_{product['product_id']}"):
                    show_product_detail(product)
            
            st.markdown("---")

def show_product_detail(product):
    st.markdown(f"## {product['name']}")
    st.markdown(f"**Category:** {product['category']}")
    st.markdown(f"**Risk Level:** {product['risk_level']}")
    st.markdown(f"**Minimum Investment:** KSh {product['min_amount']:,.2f}")
    st.markdown(f"**Expected Return:** {product['expected_return']}%")
    st.markdown(f"**Liquidity:** {product.get('liquidity', 'Medium')}")
    
    st.markdown("### Features")
    for feature in product.get('features', []):
        st.markdown(f"- {feature}")
    
    st.markdown("### Description")
    st.write(product['description'])
    
    if st.button("Back to Recommendations"):
        pass  # Will automatically go back

def show_profile():
    st.title("My Profile")
    
    if not st.session_state.user_data:
        st.session_state.user_data = get_user_profile()
    
    if st.session_state.user_data:
        display_profile(st.session_state.user_data)
        
        if st.button("Refresh Profile Data"):
            st.session_state.user_data = get_user_profile()
            st.experimental_rerun()
    else:
        st.error("Failed to load profile data")

def display_profile(profile):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personal Information")
        st.markdown(f"**Username:** {profile.get('username', 'N/A')}")
        st.markdown(f"**Email:** {profile.get('email', 'N/A')}")
        st.markdown(f"**Member Since:** {datetime.strptime(profile['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')}")
    
    with col2:
        st.markdown("### Financial Profile")
        st.markdown(f"**Age:** {profile.get('age', 'N/A')}")
        st.markdown(f"**Annual Income:** KSh {profile.get('income', 0):,.2f}")
        st.markdown(f"**Risk Tolerance:** {profile.get('risk_tolerance', 'Medium')}")
    
    st.markdown("---")

def show_products():
    st.title("Available Financial Products")
    
    with st.spinner("Loading products..."):
        response = requests.get(
            f"{API_BASE_URL}/products",
            headers={"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else None
        )
        
        if response.status_code == 200:
            products = response.json()
            
            # Add search and filter
            col1, col2 = st.columns(2)
            
            with col1:
                search_term = st.text_input("Search Products")
            
            with col2:
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All"] + list(set(p['category'] for p in products))
                )
            # Apply filters
            if search_term:
                products = [p for p in products 
                           if search_term.lower() in p['name'].lower() 
                           or search_term.lower() in p['description'].lower()]
            
            if category_filter != "All":
                products = [p for p in products if p['category'] == category_filter]
            
            # Display products
            for product in products:
                with st.expander(product['name']):
                    st.markdown(f"**Category:** {product['category']}")
                    st.markdown(f"**Risk Level:** {product['risk_level']}")
                    st.markdown(f"**Minimum Amount:** KSh {product['min_amount']:,.2f}")
                    st.markdown("**Description:**")
                    st.write(product['description'])
                    
                    if st.session_state.token:
                        if st.button("Get Recommendation Details", key=f"rec_{product['product_id']}"):
                            response = requests.post(
                                f"{API_BASE_URL}/recommend",
                                headers={"Authorization": f"Bearer {st.session_state.token}"},
                                json={**st.session_state.user_data, "product_id": product['product_id']}
                            )
                            
                            if response.status_code == 200:
                                rec_details = response.json()
                                show_product_detail(rec_details[0] if rec_details else product)
        else:
            st.error("Failed to load products")

def get_user_profile():
    if not st.session_state.token:
        return None
    
    response = requests.get(
        f"{API_BASE_URL}/user",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    main()