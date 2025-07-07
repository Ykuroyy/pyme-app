#!/usr/bin/env bash

echo "Starting Python application..."

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# アプリケーションの起動（最もシンプルな設定）
exec gunicorn --workers 1 --threads 4 --bind 0.0.0.0:${PORT:-8000} --log-file - app:app 