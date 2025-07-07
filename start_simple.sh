#!/usr/bin/env bash

echo "=== Starting Python application ==="

# 環境変数の確認
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Pythonの確認
echo "Python version:"
python --version

# 依存関係の確認
echo "Installed packages:"
pip list | grep -E "(Flask|gunicorn)"

# テンプレートディレクトリの確認
echo "Templates directory:"
if [ -d "templates" ]; then
    ls -la templates/
else
    echo "Templates directory not found!"
fi

# アプリケーションの起動
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 1 --timeout 120 --log-level debug app:app 