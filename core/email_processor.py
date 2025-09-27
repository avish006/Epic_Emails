from ml_models.feature_engineer import FeatureEngineer
from utils.date_utils import parse_email_date, format_date_for_display
class EmailProcessor:
    def __init__(self, llm_manager):
        self.llm_manager = llm_manager
        self.feature_engineer = FeatureEngineer()
    
    def process_email(self, gmail_service, message_id):
        try:
            message = gmail_service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'
            ).execute()
            headers = message['payload'].get('headers', [])
            date_header = next((h['value'] for h in headers if h['name'].lower() == 'date'), None)
            parsed_date = parse_email_date(date_header)
            features = self.feature_engineer.extract_features(message)
            
            # Use the priority engine which now handles everything
            from ml_models.llm_priority_engine import LLMPriorityEngine
            priority_engine = LLMPriorityEngine(self.llm_manager)
            result = priority_engine.calculate_priority(features)
            formatted_date = format_date_for_display(parsed_date) if parsed_date else "Invalid Date"
            result['formatted_date'] = formatted_date
            return {
                'message_id': message_id,
                'category': result['category'],
                'summary': result['summary'],
                'priority': {
                    'priority_score': result['priority_score'],
                    'priority_level': result['priority_level'],
                    'reasoning': result['reasoning']
                },
                'deadline': result['deadline'],
                'features': {
                    'sender': features['sender'],
                    'subject': features['subject'],
                    'body_preview': features['body'][:200] + '...' if len(features['body']) > 200 else features['body']
                }
            }
            
        except Exception as e:
            print(f"Error processing email {message_id}: {e}")
            return None