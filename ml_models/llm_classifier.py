from llm.llm_manager import LLMManager

class LLMClassifier:
    def __init__(self, llm_manager):
        self.llm = llm_manager
    
    def classify_email(self, email_data):
        prompt = f"""Analyze this email and determine its category and priority level.

EMAIL FROM: {email_data.get('sender', '')}
SUBJECT: {email_data.get('subject', '')}
BODY: {email_data.get('body', '')[:3000]}

Respond in EXACTLY this format:
CATEGORY: [urgent_alert/work_deadline/meeting_invite/direct_question/internal_update/newsletter/sales_pitch/personal/notification/social/spam]
PRIORITY: [high/medium/low]
DEADLINE: [extract any dates or "none" if no deadline]
SUMMARY: [1-2 sentence summary]

Do not add any other text."""
        
        response = self.llm.generate_response(prompt, max_tokens=500, temperature=0.3)
        return self._parse_classification_response(response)
    
    def _parse_classification_response(self, response):
        # Default values
        result = {
            'category': 'notification',
            'priority': 'medium',
            'deadline': 'none',
            'summary': 'No summary available',
            'raw_response': response
        }
        
        try:
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('CATEGORY:'):
                    result['category'] = line.replace('CATEGORY:', '').strip()
                elif line.startswith('PRIORITY:'):
                    result['priority'] = line.replace('PRIORITY:', '').strip()
                elif line.startswith('DEADLINE:'):
                    result['deadline'] = line.replace('DEADLINE:', '').strip()
                elif line.startswith('SUMMARY:'):
                    result['summary'] = line.replace('SUMMARY:', '').strip()
        except:
            # If parsing fails, use the raw response as summary
            result['summary'] = response[:200] + '...' if len(response) > 200 else response
        
        return result