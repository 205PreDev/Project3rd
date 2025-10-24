"""
Test script to list available Gemini models
"""
import google.generativeai as genai
from app.core.config import get_settings

settings = get_settings()

# Configure API
genai.configure(api_key=settings.GEMINI_API_KEY)

print("🔍 Listing available Gemini models...\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ Model: {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print(f"   Methods: {model.supported_generation_methods}")
        print()
