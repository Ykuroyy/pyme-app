import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration
    # Renderの無料プランではSQLiteを使用、有料プランではPostgreSQLを使用
    if os.environ.get('RENDER'):
        # Render環境では環境変数のDATABASE_URLを使用
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
            # RenderのPostgreSQL URLをSQLAlchemy形式に変換
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    else:
        # ローカル開発環境ではSQLiteを使用
        DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///pyme_app.db'
    
    # PostgreSQL specific settings (ローカル開発用)
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'aroma_app_db')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'pyme_user')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'pyme_password')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 