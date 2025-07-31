#!/usr/bin/env python3
"""
Quick setup script to ensure the Investment Recommender app runs properly
"""

import os
import sys
import subprocess
from pathlib import Path

def create_models_directory():
    """Create models directory if it doesn't exist"""
    models_dir = Path("models")
    if not models_dir.exists():
        models_dir.mkdir()
        print("✅ Created models directory")
        
        # Create a demo info file
        demo_info = {
            "status": "demo_mode",
            "message": "No trained models found - running in demo mode",
            "features": ["Rule-based recommendations", "Basic propensity scoring"]
        }
        
        import json
        with open(models_dir / "demo_info.json", "w") as f:
            json.dump(demo_info, f, indent=2)
        print("✅ Created demo info file")
    else:
        print("✅ Models directory already exists")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False
    
    return True

def create_app_file():
    """Ensure the main app file exists"""
    app_files = ["streamlit_app.py", "app.py"]
    
    for app_file in app_files:
        if Path(app_file).exists():
            print(f"✅ Found app file: {app_file}")
            return app_file
    
    print("❌ No app file found. Please save the fixed code as 'streamlit_app.py'")
    return None

def main():
    """Main setup function"""
    print("🚀 Investment Recommender - Setup Script")
    print("=" * 50)
    
    # Step 1: Create models directory
    create_models_directory()
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("❌ Setup failed due to dependency issues")
        return 1
    
    # Step 3: Check for app file
    app_file = create_app_file()
    if not app_file:
        print("❌ Setup incomplete - no app file found")
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To run the application:")
    print(f"   streamlit run {app_file}")
    print("\n🌐 The app will be available at: http://localhost:8501")
    
    # Ask if user wants to start the app now
    response = input("\n🤔 Would you like to start the app now? (y/N): ").lower().strip()
    if response == 'y':
        print(f"\n🚀 Starting {app_file}...")
        try:
            subprocess.run(["streamlit", "run", app_file])
        except KeyboardInterrupt:
            print("\n👋 App stopped by user")
        except FileNotFoundError:
            print("❌ Streamlit not found. Please install it with: pip install streamlit")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())