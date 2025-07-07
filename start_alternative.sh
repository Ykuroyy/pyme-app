#!/usr/bin/env bash

echo "Starting Python application (alternative method)..."

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Pythonのバージョン確認
echo "Python version:"
python --version

# 依存関係の確認
echo "Installed packages:"
pip list

# 直接Pythonで起動
echo "Starting with Python directly..."
python app.py 