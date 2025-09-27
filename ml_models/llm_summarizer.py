from llm.llm_manager import LLMManager

class LLMSummarizer:
    def __init__(self, llm_manager):
        self.llm = llm_manager
    
    def summarize_email(self, email_data):
        prompt = f"""Summarize this email concisely, focusing on key points, actions required, and deadlines.

FROM: {email_data.get('sender', '')}
SUBJECT: {email_data.get('subject', '')}
BODY: {email_data.get('body', '')[:4000]}

Provide a clear 1-2 sentence summary:"""
        
        response = self.llm.generate_response(prompt, max_tokens=200, temperature=0.5)
        return self._clean_summary(response)
    
    def _clean_summary(self, text):
        # Remove common AI response prefixes
        prefixes = ["Sure, here is a summary:", "The email is about", "This email discusses"]
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        return text.strip()