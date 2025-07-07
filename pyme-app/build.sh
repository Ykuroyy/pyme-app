#!/usr/bin/env bash
# exit on error
set -o errexit

# Pythonの依存関係をインストール
pip install -r requirements.txt

# アプリケーションの権限を確認
echo "Build completed successfully" 