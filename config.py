import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    ADMIN_IDS: list = [int(id) for id in os.getenv('ADMIN_IDS', '').split(',') if id]
    
    # APIs
    FOOTBALL_API_KEY: str = os.getenv('FOOTBALL_API_KEY')
    RAPIDAPI_KEY: str = os.getenv('RAPIDAPI_KEY')
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    REDIS_URL: str = os.getenv('REDIS_URL')
    
    # Webhook
    WEBHOOK_URL: str = os.getenv('WEBHOOK_URL')
    WEBHOOK_PORT: int = int(os.getenv('WEBHOOK_PORT', 8443))
    
    # Cache
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', 300))
    MODEL_UPDATE_INTERVAL: int = int(os.getenv('MODEL_UPDATE_INTERVAL', 3600))

config = Config()
