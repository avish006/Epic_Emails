import base64
import re
from datetime import datetime

class FeatureEngineer:
    def extract_features(self, message):
        headers = {header['name']: header['value'] for header in message['payload'].get('headers', [])}
        
        subject = headers.get('Subject', '')
        sender = headers.get('From', '')
        body = self._extract_body(message['payload'])
        
        features = {
            'sender': sender,
            'subject': subject,
            'body': body,
            'subject_length': len(subject),
            'body_length': len(body),
            'has_urgency_words': self._check_urgency_words(subject + ' ' + body),
            'has_deadline': self._extract_deadlines(body),
            'sender_importance': self._calculate_sender_importance(sender),
            'contains_questions': self._count_questions(body),
        }
        
        return features
    
    def _extract_body(self, payload):
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        return body
    
    def _check_urgency_words(self, text):
        urgency_indicators = ['urgent', 'asap', 'immediately', 'important', 'critical', 'deadline', 'emergency']
        return any(word in text.lower() for word in urgency_indicators)
    
    def _extract_deadlines(self, body):
        deadline_patterns = [
            r'deadline.*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'due.*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        return any(re.search(pattern, body, re.IGNORECASE) for pattern in deadline_patterns)
    
    def _calculate_sender_importance(self, sender):
        important_domains = ['yourcompany.com', 'company.org']
        important_senders = ['manager@', 'ceo@', 'hr@', 'client@']
        
        for domain in important_domains:
            if domain in sender.lower():
                return 2.0
        
        for important in important_senders:
            if important in sender.lower():
                return 1.5
        
        return 1.0
    
    def _count_questions(self, body):
        return body.count('?')