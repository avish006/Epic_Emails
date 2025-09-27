import os
from dataclasses import dataclass

@dataclass
class Config:
    # Gmail API settings
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.json'
    
    # LLM settings
    MAX_EMAIL_LENGTH = 4000
    CACHE_RESPONSES = True
    
    # Processing settings
    CHECK_INTERVAL = 60  # seconds
    MAX_EMAILS_PER_RUN = 50
    
    # Priority thresholds
    HIGH_PRIORITY_THRESHOLD = 75
    MEDIUM_PRIORITY_THRESHOLD = 50

config = Config()