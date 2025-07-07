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

# 最も基本的な起動方法
echo "Starting with basic gunicorn command..."
exec gunicorn app:app 