#!/usr/bin/env bash

echo "Starting Python application (alternative method)..."

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# 直接Pythonで起動
python app.py 