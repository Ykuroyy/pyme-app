# 🚂 Railway デプロイ設定手順

## 📋 前提条件
- GitHubアカウント
- Railwayアカウント（https://railway.app/）

## 🚀 手順

### 1. Railwayアカウント作成
1. https://railway.app/ にアクセス
2. GitHubアカウントでログイン
3. アカウント作成完了

### 2. プロジェクト作成
1. Railwayダッシュボードで「New Project」をクリック
2. 「Deploy from GitHub repo」を選択
3. `Ykuroyy/pyme-app` リポジトリを選択
4. プロジェクト名を入力（例：`pyme-app`）

### 3. 環境変数設定
Railwayダッシュボードで以下の環境変数を設定：

| 変数名 | 値 | 説明 |
|--------|----|----|
| `FLASK_ENV` | `production` | Flask環境設定 |
| `RENDER` | `true` | Render環境フラグ |
| `DATABASE_URL` | `sqlite:///pyme_app.db` | データベースURL |
| `SECRET_KEY` | `your-secret-key-here` | セキュリティキー |

### 4. 環境変数設定方法

#### 方法A: Railwayダッシュボード
1. プロジェクトダッシュボードを開く
2. 「Variables」タブをクリック
3. 「New Variable」をクリック
4. 上記の変数を1つずつ追加

#### 方法B: Railway CLI
```bash
# CLIインストール
npm install -g @railway/cli

# ログイン
railway login

# プロジェクトリンク
railway link

# 環境変数設定
railway variables set FLASK_ENV=production
railway variables set RENDER=true
railway variables set DATABASE_URL=sqlite:///pyme_app.db
railway variables set SECRET_KEY=your-secret-key-here
```

### 5. デプロイ実行
1. 「Deployments」タブをクリック
2. 「Deploy Now」をクリック
3. デプロイ完了まで待機（約2-3分）

### 6. 動作確認
デプロイ完了後、以下のURLでアクセス：
- **アプリケーション**: https://your-app-name.railway.app
- **デバッグ情報**: https://your-app-name.railway.app/debug
- **データベーステスト**: https://your-app-name.railway.app/db-test

## 🔧 トラブルシューティング

### デプロイエラー
- **ログ確認**: Railwayダッシュボードの「Deployments」でログを確認
- **環境変数確認**: すべての環境変数が正しく設定されているか確認
- **依存関係確認**: `requirements.txt`が正しく設定されているか確認

### アプリケーションエラー
- **ヘルスチェック**: `/health`エンドポイントで動作確認
- **デバッグ情報**: `/debug`エンドポイントで詳細情報確認
- **データベース接続**: `/db-test`エンドポイントでDB接続確認

## 📊 監視・管理

### ログ確認
```bash
# Railway CLIでログ確認
railway logs
```

### 環境変数確認
```bash
# Railway CLIで環境変数確認
railway variables list
```

### アプリケーション再起動
```bash
# Railway CLIで再起動
railway service restart
```

## 💰 コスト管理

### 無料プラン制限
- **月額**: $5クレジット
- **使用量**: 約750時間相当
- **制限**: 100個アプリまで対応可能

### コスト監視
1. Railwayダッシュボードで「Usage」タブを確認
2. 月間使用量を監視
3. 必要に応じてプランアップグレード

## 🎯 次のステップ

### 1. 最初のデプロイ完了後
- [ ] 動作確認
- [ ] パフォーマンステスト
- [ ] エラーログ確認

### 2. スケールアップ準備
- [ ] 2つ目のアプリデプロイ
- [ ] 自動化スクリプト作成
- [ ] 監視システム構築

### 3. 100個アプリデプロイ計画
- [ ] テンプレート作成
- [ ] 一括デプロイスクリプト
- [ ] コスト最適化 