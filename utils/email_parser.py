import base64
import re
from datetime import datetime

class EmailParser:
    def parse_email_headers(self, message):
        headers = {}
        for header in message['payload'].get('headers', []):
            headers[header['name']] = header['value']
        return headers
    
    def get_email_body(self, payload):
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
        elif payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
        return body
    
    def parse_date(self, date_string):
        try:
            from dateutil import parser
            return parser.parse(date_string)
        except:
            return datetime.now()