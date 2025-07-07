#!/usr/bin/env bash

echo "Starting Python application..."

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# テンプレートディレクトリの確認
echo "Templates directory:"
ls -la templates/ 2>/dev/null || echo "Templates directory not found"

# アプリケーションの起動
echo "Starting gunicorn..."
exec gunicorn --workers 1 --bind 0.0.0.0:${PORT:-8000} --timeout 120 --log-level info app:app 