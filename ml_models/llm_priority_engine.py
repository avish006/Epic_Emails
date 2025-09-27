import json
import os
from llm.llm_manager import LLMManager

class LLMPriorityEngine:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.preferences_file = 'user_preferences.json'
        self.load_preferences()
    
    def load_preferences(self):
        try:
            with open(self.preferences_file, 'r') as f:
                self.preferences = json.load(f)
        except:
            self.preferences = {
                "priority_senders": ["boss@", "manager@", "hr@", "ceo@"],
                "important_keywords": ["urgent", "asap", "deadline", "important", "critical"]
            }
    
    def calculate_priority(self, email_data):
        # Get classification from the classifier (which now includes priority)
        from ml_models.llm_classifier import LLMClassifier
        classifier = LLMClassifier(self.llm)
        classification = classifier.classify_email(email_data)
        
        # Convert priority level to score
        priority_scores = {'high': 85, 'medium': 60, 'low': 30}
        base_score = priority_scores.get(classification['priority'], 50)
        
        # Apply sender boost
        final_score = self._apply_sender_boost(base_score, email_data.get('sender', ''))
        
        return {
            'priority_score': min(100, final_score),
            'priority_level': classification['priority'],
            'category': classification['category'],
            'deadline': classification['deadline'],
            'summary': classification['summary'],
            'reasoning': f"AI classified as {classification['priority']} priority due to content analysis"
        }
    
    def _apply_sender_boost(self, base_score, sender):
        if any(important_sender in sender.lower() for important_sender in self.preferences['priority_senders']):
            return min(100, base_score + 20)
        return base_score