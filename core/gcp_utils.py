import os
from google.auth.exceptions import DefaultCredentialsError
from google.auth import default

def get_gemini_api_key():
    """환경 변수에서 Gemini API 키 가져오기"""
    return os.getenv("GEMINI_API_KEY")
