#!/bin/bash

echo "📱 スマートフォン対応サーバーを起動します..."

# IPアドレスを取得
IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS="localhost"
fi

echo ""
echo "🚀 サーバー情報:"
echo "   IP Address: $IP_ADDRESS"
echo "   Port: 8000"
echo "   URL: http://$IP_ADDRESS:8000"
echo ""

# QRコード用HTMLを開く
echo "📋 QRコード付きアクセスページ:"
echo "   file://$(pwd)/mobile_access.html"
echo ""

# MacならブラウザでQRコードページを開く
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🌐 QRコードページを開いています..."
    open "$(pwd)/mobile_access.html"
fi

echo "📱 スマートフォンでのアクセス方法:"
echo ""
echo "   方法1: QRコードを読み取り"
echo "   方法2: ブラウザで http://$IP_ADDRESS:8000 にアクセス"
echo ""
echo "✨ スマホの新機能:"
echo "   🎤 音声入力"
echo "   📷 カメラ撮影"
echo "   ⚡ プリセット機能"
echo "   📱 PWAインストール"
echo ""

# サーバーが起動していなければ起動
if ! curl -s "http://$IP_ADDRESS:8000" > /dev/null; then
    echo "⚠️  サーバーが起動していません。"
    echo "💡 別のターミナルで以下のコマンドを実行してください:"
    echo "   ./start_free.sh"
    echo ""
else
    echo "✅ サーバーは正常に動作中です"
    echo ""
fi

echo "🔄 リアルタイム確認: watch curl -s http://$IP_ADDRESS:8000 > /dev/null && echo '✅ OK' || echo '❌ Down'"
echo ""
echo "Press Ctrl+C to exit this message..."

# 継続的にサーバー状態を確認
while true; do
    sleep 5
    if curl -s "http://$IP_ADDRESS:8000" > /dev/null; then
        echo "$(date '+%H:%M:%S') - ✅ Server is running"
    else
        echo "$(date '+%H:%M:%S') - ❌ Server is down"
    fi
done