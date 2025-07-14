from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Tool(db.Model):
    """自動化ツールのモデル"""
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    how_to = db.Column(db.Text, nullable=False)
    sample_code = db.Column(db.Text, nullable=False)
    libraries = db.Column(db.String(200), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.JSON, nullable=True)  # リストをJSONとして保存
    time_required = db.Column(db.String(50), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    ai_prompt = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tool {self.title}>'
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'category': self.category,
            'number': self.number,
            'title': self.title,
            'desc': self.desc,
            'how_to': self.how_to,
            'sample_code': self.sample_code,
            'libraries': self.libraries,
            'explanation': self.explanation,
            'benefits': self.benefits or [],
            'time_required': self.time_required,
            'difficulty': self.difficulty,
            'ai_prompt': self.ai_prompt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class User(db.Model):
    """ユーザーモデル（将来的な拡張用）"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>' 