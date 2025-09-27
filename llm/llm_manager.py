import os
import requests
import json
from config import config
from dotenv import load_dotenv
load_dotenv()
class LLMManager:
    def __init__(self, model_name=None):
        self.model_name = "x-ai/grok-4-fast:free"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            print("❌ OPENROUTER_API_KEY environment variable not set")
            print("Get your API key from: https://openrouter.ai/")
            print("Then set it: export OPENROUTER_API_KEY='your-key-here'")
    
    def generate_response(self, prompt, max_tokens=1024, temperature=0.7):
        if not self.api_key:
            return "Error: API key not configured"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Email AI Prioritizer"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"API Error: {str(e)}"

    def load_model(self):
        print(f"✅ OpenRouter LLM configured: {self.model_name}")
        return True