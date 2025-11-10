import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    DATABASE_PATH = 'database/edensaulyk.db'
    
    GITHUB_MODELS_ENDPOINT = 'https://models.inference.ai.azure.com/chat/completions'
    GITHUB_MODEL_NAME = 'gpt-4o-mini'
    
    SESSION_SECRET = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')
