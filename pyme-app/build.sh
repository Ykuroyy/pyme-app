#!/usr/bin/env bash
# exit on error
set -o errexit

# Pythonの依存関係をインストール
pip install -r requirements.txt

# 起動スクリプトに実行権限を付与
chmod +x start.sh
chmod +x start_alternative.sh

# ファイル構造の確認
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

echo "Build completed successfully" 