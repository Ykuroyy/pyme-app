#!/usr/bin/env bash
# exit on error
set -o errexit

# Pythonの依存関係をインストール
pip install -r requirements.txt

# 起動スクリプトに実行権限を付与
chmod +x start.sh

# アプリケーションの権限を確認
echo "Build completed successfully" 