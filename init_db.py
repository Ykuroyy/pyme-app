#!/usr/bin/env python3
"""
データベース初期化スクリプト
PostgreSQLデータベースの作成、テーブル作成、サンプルデータ投入を行います
"""

import os
import sys
from flask import Flask
from config import config
from models import db, Tool
from tools_extra import EXTRA_TOOLS

def create_app(config_name='development'):
    """Flaskアプリケーションを作成"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # データベース初期化
    db.init_app(app)
    
    return app

def init_database():
    """データベースを初期化"""
    app = create_app()
    
    with app.app_context():
        try:
            # テーブルを作成
            print("データベーステーブルを作成中...")
            db.create_all()
            print("✓ テーブル作成完了")
            
            # 既存のデータをチェック
            existing_tools = Tool.query.count()
            if existing_tools > 0:
                print(f"✓ 既に {existing_tools} 件のツールデータが存在します")
                return
            
            # サンプルデータを投入
            print("サンプルデータを投入中...")
            for tool_data in EXTRA_TOOLS:
                # benefitsをJSON形式で保存
                benefits = tool_data.get('benefits', [])
                
                tool = Tool(
                    category=tool_data['category'],
                    number=tool_data['number'],
                    title=tool_data['title'],
                    desc=tool_data['desc'],
                    how_to=tool_data['how_to'],
                    sample_code=tool_data['sample_code'],
                    libraries=tool_data['libraries'],
                    explanation=tool_data['explanation'],
                    benefits=benefits,
                    time_required=tool_data.get('time_required'),
                    difficulty=tool_data.get('difficulty'),
                    ai_prompt=tool_data.get('ai_prompt')
                )
                db.session.add(tool)
            
            db.session.commit()
            print(f"✓ {len(EXTRA_TOOLS)} 件のサンプルデータを投入しました")
            
        except Exception as e:
            print(f"✗ エラーが発生しました: {e}")
            db.session.rollback()
            sys.exit(1)

def check_database_connection():
    """データベース接続をチェック"""
    app = create_app()
    
    with app.app_context():
        try:
            # データベース接続テスト
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            print("✓ データベース接続成功")
            return True
        except Exception as e:
            print(f"✗ データベース接続エラー: {e}")
            return False

if __name__ == '__main__':
    print("=== データベース初期化スクリプト ===")
    
    # データベース接続チェック
    if not check_database_connection():
        print("\nデータベース接続に失敗しました。以下を確認してください：")
        print("1. PostgreSQLが起動しているか")
        print("2. DATABASE_URLの設定が正しいか")
        print("3. データベースとユーザーが作成されているか")
        sys.exit(1)
    
    # データベース初期化
    init_database()
    
    print("\n=== 初期化完了 ===") 