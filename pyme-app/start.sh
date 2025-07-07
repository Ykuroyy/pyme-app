#!/usr/bin/env bash

echo "Starting Python application..."

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# アプリケーションの起動
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 