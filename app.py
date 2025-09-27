from flask import Flask, render_template, jsonify, request
from auth.gmail_auth import GmailAuthenticator
from llm.llm_manager import LLMManager
from core.email_processor import EmailProcessor
from core.real_time_monitor import RealTimeMonitor
import threading
import time
import os

app = Flask(__name__)

# Global variables
gmail_service = None
llm_manager = None
email_processor = None
monitor = None
monitor_thread = None
is_monitoring = False
processed_emails = []

def initialize_services():
    global gmail_service, llm_manager, email_processor, monitor
    
    # Initialize Gmail service
    try:
        authenticator = GmailAuthenticator()
        gmail_service = authenticator.authenticate()
        print("✅ Gmail service initialized")
    except Exception as e:
        print(f"❌ Gmail auth failed: {e}")
        return False
    
    # Initialize LLM
    llm_manager = LLMManager()
    llm_manager.load_model()
    
    # Initialize email processor
    email_processor = EmailProcessor(llm_manager)
    
    # Initialize monitor
    monitor = RealTimeMonitor(gmail_service, email_processor)
    
    print("✅ All services initialized successfully")
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global is_monitoring, monitor_thread
    
    if not is_monitoring:
        is_monitoring = True
        monitor_thread = threading.Thread(target=monitor.start_monitoring)
        monitor_thread.daemon = True
        monitor_thread.start()
        return jsonify({'status': 'Monitoring started'})
    
    return jsonify({'status': 'Already monitoring'})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global is_monitoring
    is_monitoring = False
    return jsonify({'status': 'Monitoring stopped'})

@app.route('/process_emails', methods=['POST'])
def process_emails():
    global processed_emails
    
    try:
        results = gmail_service.users().messages().list(
            userId='me', 
            maxResults=5,
            labelIds=['INBOX']
        ).execute()
        
        emails = []
        for message in results.get('messages', []):
            result = email_processor.process_email(gmail_service, message['id'])
            if result:
                emails.append(result)
                processed_emails.append(result)
        
        return jsonify({'status': 'success', 'emails': emails})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_emails')
def get_emails():
    return jsonify({'emails': processed_emails[-10:]})

if __name__ == '__main__':
    print("🚀 Starting Email AI with OpenRouter...")
    if initialize_services():
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize services")