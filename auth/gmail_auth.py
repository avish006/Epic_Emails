import pickle
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import config

class GmailAuthenticator:
    def __init__(self):
        self.creds = None
        self.service = None
    
    def authenticate(self):
        if os.path.exists(config.TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, config.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        return self.service
    
    def get_service(self):
        if not self.service:
            return self.authenticate()
        return self.service