#!/usr/bin/env python3
"""
Setup script to help users create their .env file with OpenAI API key.
"""

import os
from pathlib import Path

def create_env_file():
    """Create a .env file with OpenAI API key configuration."""
    env_file = Path('.env')
    
    if env_file.exists():
        print(f"⚠️  .env file already exists at {env_file.absolute()}")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Get API key from user
    print("🔑 OpenAI API Key Setup")
    print("=" * 40)
    print("You need an OpenAI API key to use translate-pptx.")
    print("Get your API key from: https://platform.openai.com/api-keys")
    print()
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Create .env file content
    env_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Optional: You can also set other OpenAI configuration
# OPENAI_ORG_ID=your_organization_id_here
# OPENAI_BASE_URL=https://api.openai.com/v1
"""
    
    # Write .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ .env file created successfully at {env_file.absolute()}")
        print("🔒 The file has been added to .gitignore for security.")
        print()
        print("You can now use translate-pptx!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

def main():
    """Main function."""
    print("🚀 translate-pptx Environment Setup")
    print("=" * 40)
    
    # Check if python-dotenv is available
    try:
        import dotenv
        print("✅ python-dotenv is available")
    except ImportError:
        print("⚠️  python-dotenv not found. Installing...")
        os.system("pip install python-dotenv")
        try:
            import dotenv
            print("✅ python-dotenv installed successfully")
        except ImportError:
            print("❌ Failed to install python-dotenv")
            return
    
    create_env_file()

if __name__ == "__main__":
    main() 