#!/bin/bash

echo "=== Railway URL確認 ==="

# Railway CLIがインストールされているかチェック
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLIがインストールされていません"
    echo "インストール方法: npm install -g @railway/cli"
    echo ""
    echo "📋 手動でURLを確認する方法:"
    echo "1. https://railway.app/dashboard にアクセス"
    echo "2. プロジェクト一覧から pyme-app を選択"
    echo "3. 「Settings」タブをクリック"
    echo "4. 「Domains」セクションでURLを確認"
    exit 1
fi

# ログイン確認
echo "Railwayにログインしてください..."
railway login

# プロジェクトリンク確認
echo "プロジェクトをリンクしてください..."
railway link

# ステータス確認
echo "プロジェクトステータスを確認中..."
railway status

# デプロイメント確認
echo "最新のデプロイメントを確認中..."
railway logs

echo ""
echo "🌐 アプリケーションURL:"
echo "Railwayダッシュボードの「Settings」→「Domains」で確認してください"
echo ""
echo "🔍 確認すべきエンドポイント:"
echo "- メインアプリ: /"
echo "- ヘルスチェック: /health"
echo "- デバッグ情報: /debug"
echo "- データベーステスト: /db-test" 