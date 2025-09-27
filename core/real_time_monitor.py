import time
from googleapiclient.errors import HttpError
from config import config

class RealTimeMonitor:
    def __init__(self, gmail_service, email_processor):
        self.gmail_service = gmail_service
        self.email_processor = email_processor
        self.processed_emails = set()
    
    def start_monitoring(self, check_interval=None):
        interval = check_interval or config.CHECK_INTERVAL
        print(f"Starting email monitoring (checking every {interval} seconds)...")
        
        while True:
            try:
                self._check_new_emails()
                time.sleep(interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(interval * 2)
    
    def _check_new_emails(self):
        try:
            results = self.gmail_service.users().messages().list(
                userId='me', 
                maxResults=10,
                labelIds=['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            
            for message in messages:
                if message['id'] in self.processed_emails:
                    continue
                
                result = self.email_processor.process_email(self.gmail_service, message['id'])
                if result:
                    self._handle_processed_email(result)
                    self.processed_emails.add(message['id'])
                
        except HttpError as error:
            print(f'Gmail API error: {error}')
    
    def _handle_processed_email(self, result):
        print(f"\n📧 New Email Processed:")
        print(f"From: {result['features']['sender']}")
        print(f"Subject: {result['features']['subject']}")
        print(f"Category: {result['category']}")
        print(f"Priority: {result['priority']['priority_level']} ({result['priority']['priority_score']}/100)")
        print(f"Summary: {result['summary']}")
        if result['priority']['llm_reasoning']:
            print(f"Reasoning: {result['priority']['llm_reasoning'][:100]}...")
        print("-" * 50)