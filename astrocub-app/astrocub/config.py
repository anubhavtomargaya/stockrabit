# astrocub/config.py

import os
from datetime import timedelta
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

class Config:
    """Single configuration class with environment-based settings."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Supabase settings
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    
    # Security settings - automatically enabled in production
    if os.getenv('FLASK_ENV') == 'production':
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        REMEMBER_COOKIE_SECURE = True
        REMEMBER_COOKIE_HTTPONLY = True
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with this configuration."""
        # Create upload folder if it doesn't exist
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER)
        
        # Set up basic logging
        if not app.debug:
            import logging
            from logging.handlers import RotatingFileHandler
            
            # Ensure logs directory exists
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            # Set up file handler
            file_handler = RotatingFileHandler(
                'logs/astrocub.log',
                maxBytes=10240000,
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)