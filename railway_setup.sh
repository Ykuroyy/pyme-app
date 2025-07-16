#!/bin/bash

echo "=== Railway環境変数設定 ==="

# Railway CLIがインストールされているかチェック
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLIがインストールされていません"
    echo "インストール方法: npm install -g @railway/cli"
    exit 1
fi

# ログイン確認
echo "Railwayにログインしてください..."
railway login

# プロジェクト選択
echo "プロジェクトを選択してください..."
railway link

# 環境変数を設定
echo "環境変数を設定中..."

# Flask設定
railway variables set FLASK_ENV=production
railway variables set RENDER=true
railway variables set DATABASE_URL=sqlite:///pyme_app.db

# セキュリティキー（ランダム生成）
SECRET_KEY=$(openssl rand -hex 32)
railway variables set SECRET_KEY=$SECRET_KEY

# 確認
echo "✅ 環境変数設定完了"
echo "設定された環境変数:"
railway variables list

echo ""
echo "🚀 デプロイを開始します..."
railway up 