# Pythonのバージョンを指定
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# gunicornの実行コマンド
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
