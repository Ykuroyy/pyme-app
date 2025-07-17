#!/bin/bash

echo "=== pyme-app (無料プラン対応版) を起動します ==="

# Pythonがインストールされているかチェック
if ! command -v python3 &> /dev/null
then
    echo "エラー: Python3 がインストールされていません。"
    echo "Python3 をインストールしてから再度実行してください。"
    echo "参考: https://www.python.org/downloads/"
    exit 1
fi

# 仮想環境が存在しない場合は作成
if [ ! -d "venv" ]; then
    echo "仮想環境を構築中..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "エラー: 仮想環境の構築に失敗しました。"
        exit 1
    fi
    echo "✓ 仮想環境の構築が完了しました。"
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベート中..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "エラー: 仮想環境のアクティベートに失敗しました。"
    exit 1
fi
echo "✓ 仮想環境をアクティベートしました。"

# 依存関係をインストール
echo "必要なライブラリをインストール中..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "エラー: ライブラリのインストールに失敗しました。"
    echo "インターネット接続を確認するか、requirements.txt に問題がないか確認してください。"
    exit 1
fi
echo "✓ ライブラリのインストールが完了しました。"

# 無料プラン用の環境変数を設定
export FLASK_ENV=production
export RENDER=true
export DATABASE_URL=sqlite:///pyme_app.db

# SQLiteデータベースを初期化
echo "データベースを初期化中..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "エラー: データベースの初期化に失敗しました。"
    exit 1
fi
echo "✓ データベースの初期化が完了しました。"

# Flaskアプリケーションを起動
echo "Flaskアプリケーションを起動します..."
echo ""
echo "===================================================="
echo "🌐 アプリケーションは以下のURLで利用可能です:"
echo "   http://localhost:8000"
echo ""
echo "   ブラウザで上記のURLを開いてください。"
echo ""
echo "   アプリケーションを停止するには、このターミナルで Ctrl+C を押してください。"
echo "===================================================="
echo ""

# アプリケーションを起動
python app.py