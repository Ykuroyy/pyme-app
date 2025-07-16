from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import os
import logging
import sys
import subprocess
import tempfile
import json
import re
from datetime import datetime
from config import config
from models import db, Tool
import secrets

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# アプリケーション起動時のログ
logger.info("Flask application starting...")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")

# Flaskアプリケーションの初期化
app = Flask(__name__)

# 設定の読み込み
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# データベース初期化
db.init_app(app)

logger.info("Flask app initialized successfully")
logger.info(f"App name: {app.name}")
logger.info(f"App instance path: {app.instance_path}")
logger.info(f"Template folder: {app.template_folder}")

# テンプレートディレクトリの確認
if os.path.exists(app.template_folder):
    logger.info(f"Template folder exists: {app.template_folder}")
    logger.info(f"Template files: {os.listdir(app.template_folder)}")
else:
    logger.error(f"Template folder not found: {app.template_folder}")

# アプリケーション起動時の確認（Flask 3.xではbefore_first_requestが削除されたため削除）

# 自動化ツールリスト（シンプル版）
from tools_extra import EXTRA_TOOLS

TOOLS = [
    {
        "id": 1, 
        "category": "メール・コミュニケーション",
        "number": "1/100",
        "title": "メール自動送信", 
        "desc": "Pythonでメールを自動送信する方法",
        "how_to": "smtplibライブラリを使ってメールサーバーに接続し、メールを送信します。",
        "sample_code": "import smtplib\nfrom email.mime.text import MIMEText\n\n# メール設定\nsender_email = 'your_email@gmail.com'\nsender_password = 'your_password'\nreceiver_email = 'receiver@example.com'\n\n# メール作成\nmsg = MIMEText('これは自動送信されたメールです。')\nmsg['Subject'] = '自動送信メール'\nmsg['From'] = sender_email\nmsg['To'] = receiver_email\n\n# 送信\nserver = smtplib.SMTP('smtp.gmail.com', 587)\nserver.starttls()\nserver.login(sender_email, sender_password)\nserver.send_message(msg)\nserver.quit()\nprint('メール送信完了！')",
        "libraries": "smtplib（標準ライブラリ）、email（標準ライブラリ）",
        "explanation": "Pythonの標準ライブラリを使って、簡単にメールの自動送信ができます。定期レポートの送信や通知メールの送信に便利です。",
        "benefits": ["時間を節約できる", "ミスを減らせる", "一括送信が可能"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでメール自動送信のコードを作成してください。以下の条件でお願いします：\n\n1. smtplibライブラリを使う\n2. GmailのSMTPサーバーを使用する\n3. 件名、本文、送信者、受信者を設定する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n6. セキュリティのため、パスワードは環境変数から読み込む\n\n送信者: 自分のGmailアドレス\n受信者: 指定したメールアドレス\n件名: 自動送信メール\n本文: 簡単なメッセージ\n\n注意: Gmailを使用する場合は、アプリパスワードの設定が必要です。\n\nコピペ用プロンプト:\nPythonでメール自動送信のコードを作成してください。smtplibライブラリを使ってGmailのSMTPサーバーに接続し、指定したメールアドレスに自動でメールを送信するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 2, 
        "category": "データ処理・分析",
        "number": "2/100",
        "title": "Excel自動処理", 
        "desc": "Excelファイルを自動で編集・集計",
        "how_to": "openpyxlライブラリを使ってExcelファイルを読み込み、データを編集・集計します。",
        "sample_code": "from openpyxl import load_workbook\nimport pandas as pd\n\n# Excelファイル読み込み\nwb = load_workbook('data.xlsx')\nws = wb.active\n\n# データの読み込み\ndata = []\nfor row in ws.iter_rows(min_row=2, values_only=True):\n    data.append(row)\n\n# pandasでデータ分析\ndf = pd.DataFrame(data, columns=['名前', '売上', '日付'])\ntotal_sales = df['売上'].sum()\n\n# 結果を新しいセルに書き込み\nws['D1'] = '合計売上'\nws['D2'] = total_sales\n\n# ファイル保存\nwb.save('result.xlsx')\nprint(f'合計売上: {total_sales:,}円')",
        "libraries": "openpyxl、pandas",
        "explanation": "Excelファイルの自動処理は、ビジネスで最もよく使われる自動化の一つです。売上データの集計やレポートの自動作成に便利です。",
        "benefits": ["手作業の時間を大幅削減", "計算ミスを防げる", "大量データも瞬時に処理"],
        "time_required": "1〜2時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでExcel自動処理のコードを作成してください。以下の条件でお願いします：\n\n1. openpyxlライブラリを使う\n2. Excelファイルを読み込んでデータを取得する\n3. 売上データを集計する\n4. 結果を新しいセルに書き込む\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: data.xlsx\n集計項目: 売上列の合計\n出力先: 新しいセル（D2など）\n\nコピペ用プロンプト:\nPythonでExcel自動処理のコードを作成してください。openpyxlライブラリを使ってExcelファイルを読み込み、売上データを集計して結果を新しいセルに書き込むコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 3, 
        "category": "文書作成・管理",
        "number": "3/100",
        "title": "PDF自動生成", 
        "desc": "PDFファイルを自動で作成",
        "how_to": "reportlabライブラリを使ってPDFドキュメントを作成し、テキストや表を追加します。",
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import letter\n\n# PDF作成\nc = canvas.Canvas('report.pdf', pagesize=letter)\n\n# タイトル\nc.setFont('Helvetica-Bold', 16)\nc.drawString(100, 750, '月次レポート')\n\n# 内容\nc.setFont('Helvetica', 12)\nc.drawString(100, 700, '売上: 1,000,000円')\nc.drawString(100, 680, '利益: 200,000円')\n\nc.save()\nprint('PDF作成完了！')",
        "libraries": "reportlab",
        "explanation": "PythonでPDFファイルを自動生成することで、レポートや請求書の作成を自動化できます。",
        "benefits": ["レポート作成が自動化", "フォーマットが統一される", "大量のPDFも一括作成"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでPDF自動生成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. 月次レポートのPDFを作成する\n3. タイトル、売上、利益を表示する\n4. 見やすいレイアウトにする\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nPDF内容: 月次レポート\n表示項目: 売上、利益\nファイル名: report.pdf\n\nコピペ用プロンプト:\nPythonでPDF自動生成のコードを作成してください。reportlabライブラリを使って月次レポートのPDFを作成し、タイトル、売上、利益を表示するコードを書いてください。見やすいレイアウトにして、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 4, 
        "category": "データ収集・分析",
        "number": "4/100",
        "title": "Webスクレイピング", 
        "desc": "Webサイトから自動でデータ取得",
        "how_to": "requestsとBeautifulSoupを使ってWebページから情報を取得し、データを整理します。",
        "sample_code": "import requests\nfrom bs4 import BeautifulSoup\nimport pandas as pd\n\n# Webページを取得\nurl = 'https://example.com'\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.content, 'html.parser')\n\n# 商品情報を抽出\nproducts = []\nfor item in soup.find_all('div', class_='product'):\n    name = item.find('h3').text.strip()\n    price = item.find('span', class_='price').text.strip()\n    products.append({'商品名': name, '価格': price})\n\n# DataFrameに変換して保存\ndf = pd.DataFrame(products)\ndf.to_csv('products.csv', index=False)\nprint(f'{len(products)}件の商品情報を取得しました')",
        "libraries": "requests、beautifulsoup4、pandas",
        "explanation": "Webスクレイピングは、Webサイトから自動で情報を収集する技術です。競合調査やデータ収集に便利です。",
        "benefits": ["手作業の時間を大幅削減", "大量データも瞬時に取得", "定期的な情報収集が自動化"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでWebスクレイピングのコードを作成してください。以下の条件でお願いします：\n\n1. requestsとBeautifulSoupを使う\n2. 指定したWebサイトから商品名と価格を取得する\n3. 取得したデータをCSVファイルに保存する\n4. 初心者でも理解できるようにコメントを詳しく書く\n5. エラーハンドリングも含める\n\n対象サイト: [サイトURLを指定]\n取得したい情報: 商品名、価格、説明文\n\nコピペ用プロンプト:\nPythonでWebスクレイピングのコードを作成してください。requestsとBeautifulSoupライブラリを使って指定したWebサイトから商品名と価格を取得し、CSVファイルに保存するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 5, 
        "category": "データ処理・分析",
        "number": "5/100",
        "title": "データ可視化グラフ作成", 
        "desc": "データをグラフで見やすく表示",
        "how_to": "matplotlibやplotlyを使ってデータをグラフ化し、見やすい図表を作成します。",
        "sample_code": "import matplotlib\nmatplotlib.use('Agg')  # Web環境用のバックエンド\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport os\n\nprint('=== データ可視化グラフ作成 ===')\n\n# アップロードされたファイルを確認\nuploaded_files = [f for f in os.listdir('.') if f.endswith(('.csv', '.xlsx', '.xls'))]\n\nif uploaded_files:\n    # アップロードされたファイルを使用\n    filename = uploaded_files[0]\n    print(f'アップロードされたファイルを使用: {filename}')\n    \n    if filename.endswith('.csv'):\n        df = pd.read_csv(filename)\n    else:\n        df = pd.read_excel(filename)\n    \n    print(f'データ件数: {len(df)}件')\n    print(f'列名: {list(df.columns)}')\n    \n    # 数値列を自動検出\n    numeric_columns = df.select_dtypes(include=['number']).columns\n    if len(numeric_columns) > 0:\n        target_column = numeric_columns[0]\n        print(f'分析対象列: {target_column}')\n        \n        print(f'合計: {df[target_column].sum():,}')\n        print(f'平均: {df[target_column].mean():.1f}')\n        print(f'最大: {df[target_column].max():,}')\n        \n        # グラフ作成\n        plt.figure(figsize=(10, 6))\n        plt.plot(df.index, df[target_column], marker='o', linewidth=2, markersize=8, color='blue')\n        plt.title(f'{target_column}の推移', fontsize=16, fontweight='bold')\n        plt.xlabel('データ番号', fontsize=12)\n        plt.ylabel(target_column, fontsize=12)\n        plt.grid(True, alpha=0.3)\n        \n        # データラベルを追加\n        for i, v in enumerate(df[target_column]):\n            plt.text(i, v + df[target_column].max() * 0.01, f'{v:,.0f}', ha='center', va='bottom', fontsize=8)\n        \n        # グラフ保存\n        plt.savefig('data_chart.png', dpi=300, bbox_inches='tight')\n        print(f'\\n✅ グラフを保存しました: data_chart.png')\n    else:\n        print('数値データが見つかりませんでした。')\nelse:\n    # サンプルデータを使用\n    print('アップロードされたファイルがないため、サンプルデータを使用します。')\n    data = {\n        '月': ['1月', '2月', '3月', '4月', '5月', '6月'],\n        '売上': [100, 150, 200, 180, 250, 300]\n    }\n    df = pd.DataFrame(data)\n    \n    print(f'データ件数: {len(df)}件')\n    print(f'売上合計: {df[\"売上\"].sum():,}万円')\n    print(f'平均売上: {df[\"売上\"].mean():.1f}万円')\n    print(f'最大売上: {df[\"売上\"].max():,}万円（{df.loc[df[\"売上\"].idxmax(), \"月\"]}）')\n    \n    # グラフ作成\n    plt.figure(figsize=(10, 6))\n    plt.plot(df['月'], df['売上'], marker='o', linewidth=2, markersize=8, color='blue')\n    plt.title('月次売上推移', fontsize=16, fontweight='bold')\n    plt.xlabel('月', fontsize=12)\n    plt.ylabel('売上（万円）', fontsize=12)\n    plt.grid(True, alpha=0.3)\n    \n    # データラベルを追加\n    for i, v in enumerate(df['売上']):\n        plt.text(i, v + 10, f'{v:,}', ha='center', va='bottom', fontweight='bold')\n    \n    # グラフ保存\n    plt.savefig('sales_chart.png', dpi=300, bbox_inches='tight')\n    print('\\n✅ グラフを保存しました: sales_chart.png')\n\nprint('\\n=== グラフ作成完了 ===')\nprint('実際の使用時は、plt.show()でグラフを表示できます。')",
        "libraries": "matplotlib、pandas、plotly（オプション）",
        "explanation": "データをグラフで可視化することで、数字の意味を直感的に理解できます。プレゼンテーションやレポート作成に便利です。",
        "benefits": ["データの傾向が一目で分かる", "プレゼンが分かりやすくなる", "意思決定がスピードアップ"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでデータ可視化のコードを作成してください。以下の条件でお願いします：\n\n1. matplotlibを使う\n2. 月次売上データを折れ線グラフで表示する\n3. グラフのタイトル、軸ラベル、グリッド線を設定する\n4. グラフを画像ファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nデータ形式: CSVファイル（月、売上の列がある）\nグラフの種類: 折れ線グラフ\n\nコピペ用プロンプト:\nPythonでデータ可視化のコードを作成してください。matplotlibライブラリを使って月次売上データを折れ線グラフで表示し、グラフのタイトル、軸ラベル、グリッド線を設定して画像ファイルとして保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 6, 
        "category": "ファイル管理",
        "number": "6/100",
        "title": "ファイル自動整理", 
        "desc": "フォルダ内のファイルを自動で整理",
        "how_to": "osライブラリを使ってフォルダ内のファイルを種類別に自動整理します。",
        "sample_code": "import os\nimport shutil\nfrom pathlib import Path\n\n# 整理対象フォルダ\nfolder_path = 'C:/Users/YourName/Downloads'\n\n# ファイル種類の定義\nfile_types = {\n    '画像': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],\n    '文書': ['.pdf', '.doc', '.docx', '.txt', '.xlsx'],\n    '動画': ['.mp4', '.avi', '.mov', '.wmv'],\n    '音楽': ['.mp3', '.wav', '.flac', '.aac']\n}\n\n# フォルダ作成\nfor folder_name in file_types.keys():\n    new_folder = os.path.join(folder_path, folder_name)\n    if not os.path.exists(new_folder):\n        os.makedirs(new_folder)\n\n# ファイル整理\nfor filename in os.listdir(folder_path):\n    file_path = os.path.join(folder_path, filename)\n    if os.path.isfile(file_path):\n        file_ext = Path(filename).suffix.lower()\n        \n        for folder_name, extensions in file_types.items():\n            if file_ext in extensions:\n                destination = os.path.join(folder_path, folder_name, filename)\n                shutil.move(file_path, destination)\n                print(f'{filename} → {folder_name}フォルダに移動')\n                break\n\nprint('ファイル整理完了！')",
        "libraries": "os、shutil、pathlib（全て標準ライブラリ）",
        "explanation": "ダウンロードフォルダやデスクトップが散らかっていませんか？Pythonで自動整理できます。",
        "benefits": ["作業効率が向上", "ファイルが見つけやすくなる", "ストレスが減る"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでファイル自動整理のコードを作成してください。以下の条件でお願いします：\n\n1. 指定したフォルダ内のファイルを拡張子別に整理する\n2. 画像、文書、動画、音楽の4つのカテゴリに分類する\n3. 各カテゴリ用のフォルダを自動作成する\n4. ファイルを適切なフォルダに移動する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: ダウンロードフォルダ\n分類カテゴリ: 画像、文書、動画、音楽\n\nコピペ用プロンプト:\nPythonでファイル自動整理のコードを作成してください。指定したフォルダ内のファイルを拡張子別に整理し、画像、文書、動画、音楽の4つのカテゴリに分類して各カテゴリ用のフォルダを自動作成し、ファイルを適切なフォルダに移動するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 7, 
        "category": "メール・コミュニケーション",
        "number": "7/100",
        "title": "チャットボット作成", 
        "desc": "簡単な自動応答チャットボット",
        "how_to": "if文や辞書を使って応答パターンを定義し、ユーザーの入力に応じて自動で返答します。",
        "sample_code": "# 簡単なチャットボット（Web実行用）\nresponses = {\n    'こんにちは': 'こんにちは！お疲れ様です。',\n    '天気': '今日は晴れの予定です。',\n    '時間': '現在の時刻をお知らせします。',\n    'ありがとう': 'どういたしまして！',\n    'さようなら': 'お疲れ様でした。またお話ししましょう！'\n}\n\nprint('チャットボット: こんにちは！何かお手伝いできることはありますか？')\nprint('\\n=== デモンストレーション ===')\n\n# サンプル会話を実行\nsample_inputs = ['こんにちは', '天気', 'ありがとう', 'さようなら']\n\nfor user_input in sample_inputs:\n    print(f'\\nあなた: {user_input}')\n    \n    if user_input.lower() in ['終了', 'さようなら', 'bye']:\n        print('チャットボット: お疲れ様でした！')\n        break\n    \n    # 応答を探す\n    response = responses.get(user_input, 'すみません、その質問にはお答えできません。')\n    print(f'チャットボット: {response}')\n\nprint('\\n=== チャットボットの動作確認完了 ===')\nprint('実際の使用時は、input()関数を使って対話形式で実行できます。')",
        "libraries": "標準ライブラリのみ使用",
        "explanation": "チャットボットは、よくある質問に自動で答えてくれる便利なツールです。カスタマーサポートや社内FAQに活用できます。",
        "benefits": ["24時間対応可能", "人件費を削減", "応答速度が速い"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで簡単なチャットボットのコードを作成してください。以下の条件でお願いします：\n\n1. 辞書を使って質問と回答のパターンを定義する\n2. ユーザーの入力を受け取って適切な回答を返す\n3. 終了コマンドでプログラムを終了できる\n4. 知らない質問には適切なメッセージを返す\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対応したい質問: 挨拶、天気、時間、感謝の言葉\n終了コマンド: さようなら、終了、bye\n\nコピペ用プロンプト:\nPythonで簡単なチャットボットのコードを作成してください。辞書を使って質問と回答のパターンを定義し、ユーザーの入力を受け取って適切な回答を返すコードを書いてください。終了コマンドでプログラムを終了でき、知らない質問には適切なメッセージを返すようにしてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 8, 
        "category": "ファイル管理",
        "number": "8/100",
        "title": "画像自動リサイズ", 
        "desc": "画像ファイルを自動でリサイズ",
        "how_to": "PIL（Pillow）ライブラリを使って画像ファイルを一括でリサイズします。",
        "sample_code": "from PIL import Image\nimport os\n\ndef resize_images(folder_path, new_width=800):\n    # 対応する画像形式\n    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']\n    \n    for filename in os.listdir(folder_path):\n        if any(filename.lower().endswith(ext) for ext in image_extensions):\n            file_path = os.path.join(folder_path, filename)\n            \n            # 画像を開く\n            with Image.open(file_path) as img:\n                # アスペクト比を保ってリサイズ\n                ratio = new_width / img.width\n                new_height = int(img.height * ratio)\n                \n                # リサイズ\n                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)\n                \n                # 保存（元ファイル名に_resizedを追加）\n                name, ext = os.path.splitext(filename)\n                new_filename = f'{name}_resized{ext}'\n                new_path = os.path.join(folder_path, new_filename)\n                \n                resized_img.save(new_path, quality=85)\n                print(f'{filename} → {new_filename}')\n\n# 使用例\nresize_images('C:/Users/YourName/Pictures', 800)\nprint('画像リサイズ完了！')",
        "libraries": "Pillow (PIL)、os（標準ライブラリ）",
        "explanation": "大量の画像を一括でリサイズすることで、Webサイトやメールでの送信が楽になります。",
        "benefits": ["大量画像も一括処理", "ファイルサイズを削減", "Web表示が高速化"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで画像自動リサイズのコードを作成してください。以下の条件でお願いします：\n\n1. Pillowライブラリを使う\n2. 指定したフォルダ内の画像を一括でリサイズする\n3. アスペクト比を保ってリサイズする\n4. 元ファイルは残して、新しいファイル名で保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: 画像フォルダのパス\nリサイズサイズ: 幅800px（高さは自動調整）\n対応形式: JPG、PNG、GIF、BMP\n\nコピペ用プロンプト:\nPythonで画像自動リサイズのコードを作成してください。Pillowライブラリを使って指定したフォルダ内の画像を一括でリサイズし、アスペクト比を保って元ファイルは残して新しいファイル名で保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 9, 
        "category": "メール・コミュニケーション",
        "number": "9/100",
        "title": "定期レポート自動送信", 
        "desc": "定期的にレポートを自動送信",
        "how_to": "scheduleライブラリで定期実行を設定し、レポート作成とメール送信を自動化します。",
        "sample_code": "import schedule\nimport time\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom datetime import datetime\n\ndef create_daily_report():\n    today = datetime.now().strftime('%Y年%m月%d日')\n    report = f'''\n    日次レポート - {today}\n    \n    - 本日の売上: 150,000円\n    - 新規顧客数: 5名\n    - 処理件数: 25件\n    \n    Thank you for your work.\n    '''\n    return report\n\ndef send_report():\n    report = create_daily_report()\n    \n    # メール設定\n    sender_email = 'your_email@gmail.com'\n    sender_password = 'your_password'\n    receiver_email = 'boss@company.com'\n    \n    # メール作成\n    msg = MIMEText(report, 'plain')\n    msg['Subject'] = f'日次レポート - {datetime.now().strftime(\"%Y/%m/%d\")}'\n    msg['From'] = sender_email\n    msg['To'] = receiver_email\n    \n    # 送信\n    server = smtplib.SMTP('smtp.gmail.com', 587)\n    server.starttls()\n    server.login(sender_email, sender_password)\n    server.send_message(msg)\n    server.quit()\n    \n    print(f'レポート送信完了: {datetime.now()}')\n\n# 毎日18時に実行\nschedule.every().day.at('18:00').do(send_report)\n\n# スケジュール実行（デモ用）\nprint('スケジュール設定完了！')\nprint('実際の使用時は、以下のコードで定期実行されます：')\nprint('# while True:')\nprint('#     schedule.run_pending()')\nprint('#     time.sleep(60)  # 1分ごとにチェック')",
        "libraries": "schedule、smtplib（標準ライブラリ）、datetime（標準ライブラリ）",
        "explanation": "毎日のルーチンワークを自動化することで、時間を節約し、ミスを防げます。",
        "benefits": ["手作業が不要", "忘れることがない", "時間を大幅節約"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで定期レポート自動送信のコードを作成してください。以下の条件でお願いします：\n\n1. scheduleライブラリで毎日18時に実行する\n2. 日次レポートを作成する（売上、顧客数、処理件数を含む）\n3. 作成したレポートをメールで送信する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n送信時間: 毎日18時\nレポート内容: 売上、新規顧客数、処理件数\n送信先: 上司のメールアドレス\n\nコピペ用プロンプト:\nPythonで定期レポート自動送信のコードを作成してください。scheduleライブラリで毎日18時に実行し、日次レポートを作成してメールで送信するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 10, 
        "category": "メール・コミュニケーション",
        "number": "10/100",
        "title": "SNS自動投稿", 
        "desc": "Twitterなどに自動で投稿",
        "how_to": "tweepyライブラリを使ってTwitter APIに接続し、定期的に投稿を自動化します。",
        "sample_code": "import tweepy\nimport schedule\nimport time\nfrom datetime import datetime\n\n# Twitter API認証\nconsumer_key = 'your_consumer_key'\nconsumer_secret = 'your_consumer_secret'\naccess_token = 'your_access_token'\naccess_token_secret = 'your_access_token_secret'\n\nauth = tweepy.OAuthHandler(consumer_key, consumer_secret)\nauth.set_access_token(access_token, access_token_secret)\napi = tweepy.API(auth)\n\ndef post_daily_tip():\n    # 毎日のTipsを投稿\n    tips = [\n        '今日のビジネスTips: 朝一番に重要なタスクから始めましょう！',\n        '効率化のコツ: 同じ作業は3回以上やったら自動化を検討してください。',\n        'コミュニケーション: 相手の立場に立って考えることが大切です。',\n        '時間管理: 15分単位でタスクを区切ると集中力が続きます。'\n    ]\n    \n    today = datetime.now().day\ntip = tips[today % len(tips)]\n    \n    try:\n        api.update_status(tip)\n        print(f'投稿完了: {tip}')\n    except Exception as e:\n        print(f'投稿エラー: {e}')\n\n# 毎日9時に投稿\nschedule.every().day.at('09:00').do(post_daily_tip)\n\n# スケジュール実行（デモ用）\nprint('スケジュール設定完了！')\nprint('実際の使用時は、以下のコードで定期実行されます：')\nprint('# while True:')\nprint('#     schedule.run_pending()')\nprint('#     time.sleep(60)')",
        "libraries": "tweepy、schedule、datetime（標準ライブラリ）",
        "explanation": "SNSの投稿を自動化することで、ブランディングや情報発信を効率化できます。",
        "benefits": ["投稿を忘れることがない", "時間を節約", "一貫したブランディング"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでSNS自動投稿のコードを作成してください。以下の条件でお願いします：\n\n1. tweepyライブラリを使ってTwitterに投稿する\n2. 毎日9時にビジネスTipsを自動投稿する\n3. 複数のTipsからランダムに選択する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n投稿時間: 毎日9時\n投稿内容: ビジネスTips（複数パターン）\n投稿先: Twitter\n\nコピペ用プロンプト:\nPythonでSNS自動投稿のコードを作成してください。tweepyライブラリを使ってTwitterに毎日9時にビジネスTipsを自動投稿し、複数のTipsからランダムに選択するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 11, 
        "category": "スケジュール管理",
        "number": "11/100",
        "title": "カレンダー自動登録", 
        "desc": "予定を自動でGoogleカレンダーに登録",
        "how_to": "Google Calendar APIを使って予定を自動でカレンダーに登録します。",
        "sample_code": "from google.oauth2.credentials import Credentials\nfrom googleapiclient.discovery import build\nfrom datetime import datetime, timedelta\n\n# Google Calendar API設定\ncreds = Credentials.from_authorized_user_file('token.json', SCOPES)\nservice = build('calendar', 'v3', credentials=creds)\n\n# 予定を作成\nevent = {\n    'summary': '会議',\n    'description': 'プロジェクト会議',\n    'start': {\n        'dateTime': '2024-01-15T10:00:00+09:00',\n        'timeZone': 'Asia/Tokyo',\n    },\n    'end': {\n        'dateTime': '2024-01-15T11:00:00+09:00',\n        'timeZone': 'Asia/Tokyo',\n    }\n}\n\nevent = service.events().insert(calendarId='primary', body=event).execute()\nprint(f'予定を作成しました: {event.get(\"htmlLink\")}')",
        "libraries": "google-auth、google-api-python-client",
        "explanation": "Google Calendar APIを使って予定を自動登録することで、スケジュール管理を効率化できます。",
        "benefits": ["手動入力が不要", "ミスを防げる", "一括登録が可能"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでGoogleカレンダー自動登録のコードを作成してください。以下の条件でお願いします：\n\n1. Google Calendar APIを使う\n2. 指定した日時に予定を登録する\n3. 予定のタイトル、説明、開始・終了時間を設定する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n予定内容: 会議\n日時: 指定した日時\nカレンダー: プライマリカレンダー\n\nコピペ用プロンプト:\nPythonでGoogleカレンダー自動登録のコードを作成してください。Google Calendar APIを使って指定した日時に予定を登録し、予定のタイトル、説明、開始・終了時間を設定するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 12, 
        "category": "顧客管理",
        "number": "12/100",
        "title": "名刺データ自動整理", 
        "desc": "名刺画像から情報を自動抽出",
        "how_to": "OCR技術を使って名刺画像から文字を認識し、連絡先情報を自動抽出します。",
        "sample_code": "import cv2\nimport pytesseract\nimport re\n\n# 名刺画像を読み込み\ndef extract_business_card(image_path):\n    # 画像を読み込み\n    image = cv2.imread(image_path)\n    \n    # OCRで文字認識\n    text = pytesseract.image_to_string(image, lang='jpn')\n    \n    # 正規表現で情報を抽出\n    name_pattern = r'([\\u4e00-\\u9fa5]{2,4})'  # 日本語の名前\n    phone_pattern = r'(\\d{2,4}-\\d{2,4}-\\d{4})'  # 電話番号\n    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})'  # メールアドレス\n    \n    # 情報を抽出\n    name = re.search(name_pattern, text)\n    phone = re.search(phone_pattern, text)\n    email = re.search(email_pattern, text)\n    \n    return {\n        'name': name.group(1) if name else '',\n        'phone': phone.group(1) if phone else '',\n        'email': email.group(1) if email else ''\n    }\n\n# 使用例\nresult = extract_business_card('business_card.jpg')\nprint(f'名前: {result[\"name\"]}')\nprint(f'電話: {result[\"phone\"]}')\nprint(f'メール: {result[\"email\"]}')",
        "libraries": "opencv-python、pytesseract、re（標準ライブラリ）",
        "explanation": "名刺の画像から自動で連絡先情報を抽出することで、手動入力の手間を大幅に削減できます。",
        "benefits": ["手動入力が不要", "大量処理が可能", "データベース化が簡単"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで名刺データ自動整理のコードを作成してください。以下の条件でお願いします：\n\n1. OpenCVとTesseract OCRを使う\n2. 名刺画像から文字を認識する\n3. 名前、電話番号、メールアドレスを抽出する\n4. 正規表現で情報を整理する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: 名刺の画像ファイル\n抽出情報: 名前、電話番号、メールアドレス\n出力形式: 辞書形式\n\nコピペ用プロンプト:\nPythonで名刺データ自動整理のコードを作成してください。OpenCVとTesseract OCRを使って名刺画像から文字を認識し、名前、電話番号、メールアドレスを抽出して正規表現で情報を整理するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 13, 
        "category": "文書作成・管理",
        "number": "13/100",
        "title": "請求書自動作成", 
        "desc": "請求書を自動で作成",
        "how_to": "テンプレートを使って請求書を自動生成し、PDFファイルとして保存します。",
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom datetime import datetime\n\ndef create_invoice(client_name, items, total_amount):\n    # PDF作成\n    c = canvas.Canvas('invoice.pdf', pagesize=A4)\n    \n    # ヘッダー\n    c.setFont('Helvetica-Bold', 16)\n    c.drawString(100, 750, '請求書')\n    \n    # 日付\n    c.setFont('Helvetica', 12)\n    c.drawString(100, 720, f'発行日: {datetime.now().strftime(\"%Y年%m月%d日\")}')\n    \n    # 顧客名\n    c.drawString(100, 690, f'顧客名: {client_name}')\n    \n    # 明細\n    y = 650\n    for item in items:\n        c.drawString(100, y, f'{item[\"name\"]} - {item[\"price\"]:,}円')\n        y -= 20\n    \n    # 合計\n    c.setFont('Helvetica-Bold', 14)\n    c.drawString(100, y-20, f'合計: {total_amount:,}円')\n    \n    c.save()\n    print('請求書を作成しました')\n\n# 使用例\nitems = [\n    {'name': 'Webサイト制作', 'price': 100000},\n    {'name': '保守費用', 'price': 20000}\n]\ncreate_invoice('株式会社サンプル', items, 120000)",
        "libraries": "reportlab、datetime（標準ライブラリ）",
        "explanation": "請求書を自動生成することで、経理作業を効率化し、ミスを防げます。",
        "benefits": ["手動作成が不要", "フォーマットが統一", "大量作成が可能"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで請求書自動作成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. 顧客名、明細、合計金額を含む請求書を作成する\n3. 見やすいレイアウトにする\n4. PDFファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n請求書内容: 顧客名、明細、合計金額\n出力形式: PDFファイル\nファイル名: invoice.pdf\n\nコピペ用プロンプト:\nPythonで請求書自動作成のコードを作成してください。reportlabライブラリを使って顧客名、明細、合計金額を含む請求書を作成し、見やすいレイアウトにしてPDFファイルとして保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 14, 
        "category": "データ処理・分析",
        "number": "14/100",
        "title": "アンケート自動集計", 
        "desc": "アンケート結果を自動で集計",
        "how_to": "ExcelやCSVファイルのアンケート結果を読み込み、自動で集計・分析します。",
        "sample_code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\n# アンケートデータを読み込み\ndf = pd.read_csv('survey_results.csv')\n\n# 基本統計\nprint('=== 基本統計 ===')\nprint(f'回答者数: {len(df)}人')\nprint(f'平均年齢: {df[\"年齢\"].mean():.1f}歳')\n\n# 性別の集計\nprint('\\n=== 性別集計 ===')\ngender_counts = df['性別'].value_counts()\nprint(gender_counts)\n\n# 満足度の集計\nprint('\\n=== 満足度集計 ===')\nsatisfaction_counts = df['満足度'].value_counts().sort_index()\nprint(satisfaction_counts)\n\n# グラフ作成\nplt.figure(figsize=(10, 6))\nsatisfaction_counts.plot(kind='bar')\nplt.title('満足度分布')\nplt.xlabel('満足度')\nplt.ylabel('回答者数')\nplt.savefig('satisfaction_chart.png')\nplt.show()\n\nprint('集計完了！グラフを保存しました。')",
        "libraries": "pandas、matplotlib",
        "explanation": "アンケート結果を自動集計することで、手作業の時間を大幅に削減し、正確な分析が可能になります。",
        "benefits": ["手作業が不要", "正確な集計", "グラフも自動作成"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでアンケート自動集計のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルのアンケート結果を読み込む\n3. 基本統計（回答者数、平均年齢など）を計算する\n4. 性別、満足度などの集計を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: survey_results.csv\n集計項目: 性別、年齢、満足度\n出力: 統計結果とグラフ\n\nコピペ用プロンプト:\nPythonでアンケート自動集計のコードを作成してください。pandasライブラリを使ってCSVファイルのアンケート結果を読み込み、基本統計を計算して性別、満足度などの集計を行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 15, 
        "category": "音声・画像処理",
        "number": "15/100",
        "title": "音声データ自動文字起こし", 
        "desc": "音声ファイルを自動でテキスト化",
        "how_to": "音声認識APIを使って音声ファイルを自動でテキストに変換します。",
        "sample_code": "import speech_recognition as sr\nimport os\n\ndef transcribe_audio(audio_file_path):\n    # 音声認識エンジンを初期化\n    recognizer = sr.Recognizer()\n    \n    # 音声ファイルを読み込み\n    with sr.AudioFile(audio_file_path) as source:\n        # 音声を録音\n        audio = recognizer.record(source)\n        \n        try:\n            # Google Speech Recognitionで文字起こし\n            text = recognizer.recognize_google(audio, language='ja-JP')\n            return text\n        except sr.UnknownValueError:\n            return '音声を認識できませんでした'\n        except sr.RequestError as e:\n            return f'エラーが発生しました: {e}'\n\n# 使用例\nresult = transcribe_audio('meeting_recording.wav')\nprint('文字起こし結果:')\nprint(result)\n\n# 結果をファイルに保存\nwith open('transcription.txt', 'w', encoding='utf-8') as f:\n    f.write(result)\nprint('文字起こし結果をファイルに保存しました')",
        "libraries": "SpeechRecognition、pyaudio",
        "explanation": "会議の録音やインタビュー音声を自動でテキスト化することで、議事録作成の時間を大幅に短縮できます。",
        "benefits": ["手動入力が不要", "時間を大幅節約", "正確な文字起こし"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで音声データ自動文字起こしのコードを作成してください。以下の条件でお願いします：\n\n1. SpeechRecognitionライブラリを使う\n2. 音声ファイル（WAV形式）を読み込む\n3. Google Speech Recognitionで文字起こしする\n4. 日本語に対応する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: 音声ファイル（WAV形式）\n言語: 日本語\n出力: テキストファイル\n\nコピペ用プロンプト:\nPythonで音声データ自動文字起こしのコードを作成してください。SpeechRecognitionライブラリを使って音声ファイルを読み込み、Google Speech Recognitionで日本語の文字起こしを行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 16, 
        "category": "音声・画像処理",
        "number": "16/100",
        "title": "画像から文字抽出", 
        "desc": "画像内の文字を自動で抽出",
        "how_to": "OCR技術を使って画像内の文字を認識し、テキストとして抽出します。",
        "sample_code": "import pytesseract\nfrom PIL import Image\nimport cv2\nimport numpy as np\n\ndef extract_text_from_image(image_path):\n    # 画像を読み込み\n    image = cv2.imread(image_path)\n    \n    # グレースケールに変換\n    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n    \n    # ノイズ除去\n    denoised = cv2.medianBlur(gray, 3)\n    \n    # 二値化\n    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\n    \n    # OCRで文字認識\n    text = pytesseract.image_to_string(binary, lang='jpn')\n    \n    return text.strip()\n\n# 使用例\nresult = extract_text_from_image('document_image.jpg')\nprint('抽出されたテキスト:')\nprint(result)\n\n# 結果をファイルに保存\nwith open('extracted_text.txt', 'w', encoding='utf-8') as f:\n    f.write(result)\nprint('テキストをファイルに保存しました')",
        "libraries": "pytesseract、opencv-python、Pillow",
        "explanation": "画像内の文字を自動で抽出することで、手動入力の手間を大幅に削減できます。",
        "benefits": ["手動入力が不要", "大量処理が可能", "正確な文字認識"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで画像から文字抽出のコードを作成してください。以下の条件でお願いします：\n\n1. pytesseractライブラリを使う\n2. 画像ファイルを読み込む\n3. 前処理（グレースケール化、ノイズ除去）を行う\n4. 日本語の文字を認識する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: 文字が含まれる画像ファイル\n言語: 日本語\n出力: テキストファイル\n\nコピペ用プロンプト:\nPythonで画像から文字抽出のコードを作成してください。pytesseractライブラリを使って画像ファイルを読み込み、前処理を行って日本語の文字を認識するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 17, 
        "category": "ファイル管理",
        "number": "17/100",
        "title": "ファイル自動バックアップ", 
        "desc": "重要ファイルを自動でバックアップ",
        "how_to": "指定したフォルダのファイルを定期的にバックアップフォルダにコピーします。",
        "sample_code": "import shutil\nimport os\nfrom datetime import datetime\nimport schedule\nimport time\n\ndef backup_files(source_folder, backup_folder):\n    # バックアップフォルダを作成（日付付き）\n    today = datetime.now().strftime('%Y%m%d')\n    backup_path = os.path.join(backup_folder, f'backup_{today}')\n    \n    if not os.path.exists(backup_path):\n        os.makedirs(backup_path)\n    \n    # ファイルをコピー\n    for item in os.listdir(source_folder):\n        source_item = os.path.join(source_folder, item)\n        backup_item = os.path.join(backup_path, item)\n        \n        if os.path.isfile(source_item):\n            shutil.copy2(source_item, backup_item)\n            print(f'バックアップ完了: {item}')\n        elif os.path.isdir(source_item):\n            shutil.copytree(source_item, backup_item)\n            print(f'フォルダバックアップ完了: {item}')\n    \n    print(f'バックアップ完了: {backup_path}')\n\n# 毎日18時にバックアップ\nschedule.every().day.at('18:00').do(\n    backup_files, \n    'C:/Users/YourName/Documents', \n    'C:/Users/YourName/Backups'\n)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
        "libraries": "shutil、os、datetime、schedule（標準ライブラリ）",
        "explanation": "重要ファイルを自動でバックアップすることで、データ損失のリスクを軽減できます。",
        "benefits": ["データ保護", "手動バックアップが不要", "定期的な実行"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでファイル自動バックアップのコードを作成してください。以下の条件でお願いします：\n\n1. shutilライブラリを使う\n2. 指定したフォルダのファイルをバックアップする\n3. 日付付きのフォルダにコピーする\n4. 毎日指定した時間に自動実行する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: バックアップしたいフォルダ\nバックアップ先: 指定したフォルダ\n実行時間: 毎日18時\n\nコピペ用プロンプト:\nPythonでファイル自動バックアップのコードを作成してください。shutilライブラリを使って指定したフォルダのファイルをバックアップし、日付付きのフォルダにコピーして毎日指定した時間に自動実行するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 18, 
        "category": "文書作成・管理",
        "number": "18/100",
        "title": "会議議事録自動作成", 
        "desc": "会議音声から議事録を自動作成",
        "how_to": "音声認識とAIを使って会議の録音から議事録を自動生成します。",
        "sample_code": "import speech_recognition as sr\nfrom datetime import datetime\nimport re\n\ndef create_meeting_minutes(audio_file_path):\n    # 音声認識\n    recognizer = sr.Recognizer()\n    \n    with sr.AudioFile(audio_file_path) as source:\n        audio = recognizer.record(source)\n        \n        try:\n            # 文字起こし\n            text = recognizer.recognize_google(audio, language='ja-JP')\n            \n            # 議事録の形式に整理\n            minutes = f'''\n会議議事録\n\n日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n参加者: [参加者名を記入]\n\n【議題】\n[議題を記入]\n\n【議事内容】\n{text}\n\n【決定事項】\n[決定事項を記入]\n\n【次回予定】\n[次回予定を記入]\n            '''\n            \n            return minutes\n            \n        except sr.UnknownValueError:\n            return '音声を認識できませんでした'\n\n# 使用例\nminutes = create_meeting_minutes('meeting.wav')\nprint(minutes)\n\n# ファイルに保存\nwith open('meeting_minutes.txt', 'w', encoding='utf-8') as f:\n    f.write(minutes)\nprint('議事録を保存しました')",
        "libraries": "SpeechRecognition、datetime（標準ライブラリ）",
        "explanation": "会議の録音から自動で議事録を作成することで、手動での議事録作成の時間を大幅に短縮できます。",
        "benefits": ["議事録作成が自動化", "時間を大幅節約", "正確な記録"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで会議議事録自動作成のコードを作成してください。以下の条件でお願いします：\n\n1. SpeechRecognitionライブラリを使う\n2. 会議の音声ファイルを文字起こしする\n3. 議事録の形式に整理する（日時、参加者、議題、議事内容、決定事項）\n4. テキストファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: 会議の音声ファイル\n出力形式: 議事録テキストファイル\n内容: 日時、参加者、議題、議事内容、決定事項\n\nコピペ用プロンプト:\nPythonで会議議事録自動作成のコードを作成してください。SpeechRecognitionライブラリを使って会議の音声ファイルを文字起こしし、議事録の形式に整理してテキストファイルとして保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 19, 
        "category": "メール・コミュニケーション",
        "number": "19/100",
        "title": "翻訳自動化", 
        "desc": "テキストを自動で翻訳",
        "how_to": "Google Translate APIを使ってテキストを自動翻訳します。",
        "sample_code": "from googletrans import Translator\nimport pandas as pd\n\ndef translate_text(text, target_lang='en'):\n    translator = Translator()\n    \n    try:\n        # 翻訳実行\n        result = translator.translate(text, dest=target_lang)\n        return result.text\n    except Exception as e:\n        return f'翻訳エラー: {e}'\n\ndef translate_file(input_file, output_file, target_lang='en'):\n    # ファイルを読み込み\n    with open(input_file, 'r', encoding='utf-8') as f:\n        content = f.read()\n    \n    # 翻訳\n    translated_content = translate_text(content, target_lang)\n    \n    # 結果を保存\n    with open(output_file, 'w', encoding='utf-8') as f:\n        f.write(translated_content)\n    \n    print(f'翻訳完了: {output_file}')\n\n# 使用例\n# 単一テキストの翻訳\ntranslated = translate_text('こんにちは、世界', 'en')\nprint(f'翻訳結果: {translated}')\n\n# ファイルの翻訳\ntranslate_file('japanese_text.txt', 'english_text.txt', 'en')",
        "libraries": "googletrans==4.0.0rc1、pandas",
        "explanation": "テキストを自動翻訳することで、多言語対応や国際的なコミュニケーションを効率化できます。",
        "benefits": ["手動翻訳が不要", "多言語対応", "大量翻訳が可能"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで翻訳自動化のコードを作成してください。以下の条件でお願いします：\n\n1. googletransライブラリを使う\n2. 日本語のテキストを英語に翻訳する\n3. ファイル全体を翻訳する機能も含める\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象言語: 日本語→英語\n入力: テキストファイル\n出力: 翻訳されたテキストファイル\n\nコピペ用プロンプト:\nPythonで翻訳自動化のコードを作成してください。googletransライブラリを使って日本語のテキストを英語に翻訳し、ファイル全体を翻訳する機能も含めてエラーハンドリングも行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 20, 
        "category": "スケジュール管理",
        "number": "20/100",
        "title": "タスク自動リマインド", 
        "desc": "タスクを自動でリマインド",
        "how_to": "scheduleライブラリを使ってタスクの期限を管理し、自動でリマインドメールを送信します。",
        "sample_code": "import schedule\nimport time\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom datetime import datetime\n\ntasks = [\n    {'title': 'レポート提出', 'deadline': '2024-01-15', 'email': 'boss@company.com'},\n    {'title': '会議準備', 'deadline': '2024-01-16', 'email': 'team@company.com'}\n]\n\ndef send_reminder(task):\n    # メール設定\n    sender_email = 'your_email@gmail.com'\n    sender_password = 'your_password'\n    \n    # メール作成\n    msg = MIMEText(f'タスクリマインド: {task[\"title\"]}の期限が近づいています。')\n    msg['Subject'] = f'タスクリマインド: {task[\"title\"]}'\n    msg['From'] = sender_email\n    msg['To'] = task['email']\n    \n    # 送信\n    server = smtplib.SMTP('smtp.gmail.com', 587)\n    server.starttls()\n    server.login(sender_email, sender_password)\n    server.send_message(msg)\n    server.quit()\n    \n    print(f'リマインド送信: {task[\"title\"]}')\n\n# 毎日9時にチェック\nschedule.every().day.at('09:00').do(lambda: [send_reminder(task) for task in tasks])\n\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
        "libraries": "schedule、smtplib（標準ライブラリ）、datetime（標準ライブラリ）",
        "explanation": "タスクの期限を自動で管理し、リマインドメールを送信することで、タスクの忘れを防げます。",
        "benefits": ["タスク忘れを防ぐ", "自動リマインド", "時間管理が向上"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでタスク自動リマインドのコードを作成してください。以下の条件でお願いします：\n\n1. scheduleライブラリで毎日9時にチェックする\n2. タスクリストから期限が近いものを確認する\n3. リマインドメールを自動送信する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nチェック時間: 毎日9時\nリマインド内容: タスク名と期限\n送信先: 指定したメールアドレス\n\nコピペ用プロンプト:\nPythonでタスク自動リマインドのコードを作成してください。scheduleライブラリで毎日9時にチェックし、タスクリストから期限が近いものを確認してリマインドメールを自動送信するコードを書いてください。エラーハンドリングも含めて、初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 21,
        "category": "データ処理・分析",
        "number": "21/100",
        "title": "CSVデータ自動変換", 
        "desc": "CSVファイルを自動で変換・整形",
        "how_to": "pandasライブラリを使ってCSVファイルを読み込み、データを変換・整形します。",
        "sample_code": "import pandas as pd\nimport numpy as np\n\n# CSVファイルを読み込み\ndf = pd.read_csv('input_data.csv')\n\n# データの前処理\n# 欠損値を処理\ndf = df.fillna(0)\n\n# 日付列を変換\ndf['日付'] = pd.to_datetime(df['日付'])\n\n# 数値列の計算\ndf['合計'] = df['売上'] + df['手数料']\n\n# データの並び替え\ndf = df.sort_values('日付', ascending=False)\n\n# 結果を保存\ndf.to_csv('processed_data.csv', index=False, encoding='utf-8')\nprint('データ変換完了！')\nprint(f'処理件数: {len(df)}件')",
        "libraries": "pandas、numpy",
        "explanation": "CSVファイルのデータを自動で変換・整形することで、データ分析の準備作業を効率化できます。",
        "benefits": ["手作業が不要", "大量データも瞬時処理", "データ品質が向上"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでCSVデータ自動変換のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルを読み込んで前処理する\n3. 欠損値の処理、日付変換、計算を行う\n4. 結果を新しいCSVファイルに保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: input_data.csv\n処理内容: 欠損値処理、日付変換、計算\n出力ファイル: processed_data.csv\n\nコピペ用プロンプト:\nPythonでCSVデータ自動変換のコードを作成してください。pandasライブラリを使ってCSVファイルを読み込み、欠損値の処理、日付変換、計算を行って結果を新しいCSVファイルに保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 22,
        "category": "ファイル管理",
        "number": "22/100",
        "title": "画像自動分類", 
        "desc": "画像を自動で分類・整理",
        "how_to": "機械学習を使って画像を自動で分類し、適切なフォルダに整理します。",
        "sample_code": "import os\nimport shutil\nfrom PIL import Image\nimport numpy as np\nfrom sklearn.cluster import KMeans\n\ndef classify_images_by_color(image_folder, output_folder):\n    # 画像を色で分類\n    for filename in os.listdir(image_folder):\n        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):\n            image_path = os.path.join(image_folder, filename)\n            \n            # 画像を読み込み\n            img = Image.open(image_path)\n            img_array = np.array(img)\n            \n            # 平均色を計算\n            avg_color = img_array.mean(axis=(0, 1))\n            \n            # 色で分類（例：明るい/暗い）\n            brightness = avg_color.mean()\n            \n            if brightness > 128:\n                category = '明るい画像'\n            else:\n                category = '暗い画像'\n            \n            # フォルダを作成\n            category_folder = os.path.join(output_folder, category)\n            if not os.path.exists(category_folder):\n                os.makedirs(category_folder)\n            \n            # 画像を移動\n            shutil.copy2(image_path, os.path.join(category_folder, filename))\n            print(f'{filename} → {category}')\n\n# 使用例\nclassify_images_by_color('input_images', 'classified_images')\nprint('画像分類完了！')",
        "libraries": "Pillow、numpy、scikit-learn、os、shutil（標準ライブラリ）",
        "explanation": "画像を自動で分類することで、大量の画像を効率的に整理できます。",
        "benefits": ["手動分類が不要", "大量画像も一括処理", "整理が自動化"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで画像自動分類のコードを作成してください。以下の条件でお願いします：\n\n1. Pillowとnumpyライブラリを使う\n2. 画像の色や明度で分類する\n3. 分類結果に応じてフォルダを作成する\n4. 画像を適切なフォルダに移動する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: 指定したフォルダ内の画像\n分類基準: 明度（明るい/暗い）\n出力: 分類されたフォルダ\n\nコピペ用プロンプト:\nPythonで画像自動分類のコードを作成してください。Pillowとnumpyライブラリを使って画像の色や明度で分類し、分類結果に応じてフォルダを作成して画像を適切なフォルダに移動するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 23,
        "category": "データ収集・分析",
        "number": "23/100",
        "title": "Webサイト監視", 
        "desc": "Webサイトの変更を自動で監視",
        "how_to": "requestsライブラリを使ってWebサイトの変更を定期的にチェックし、変更があれば通知します。",
        "sample_code": "import requests\nimport hashlib\nimport time\nimport smtplib\nfrom email.mime.text import MIMEText\n\ndef monitor_website(url, check_interval=3600):\n    # 初期状態を取得\n    response = requests.get(url)\n    initial_hash = hashlib.md5(response.content).hexdigest()\n    \n    print(f'監視開始: {url}')\n    print(f'初期ハッシュ: {initial_hash}')\n    \n    while True:\n        try:\n            # 現在の状態を取得\n            response = requests.get(url)\n            current_hash = hashlib.md5(response.content).hexdigest()\n            \n            # 変更をチェック\n            if current_hash != initial_hash:\n                # 変更があった場合、メール通知\n                send_notification(url, 'Webサイトに変更が検出されました')\n                print(f'変更検出: {url}')\n                break\n            else:\n                print(f'変更なし: {time.strftime(\"%Y-%m-%d %H:%M:%S\")}')\n            \n            # 指定時間待機\n            time.sleep(check_interval)\n            \n        except Exception as e:\n            print(f'エラー: {e}')\n            time.sleep(60)\n\ndef send_notification(url, message):\n    # メール通知の実装\n    print(f'通知: {message} - {url}')\n\n# 使用例\nmonitor_website('https://example.com', 1800)  # 30分ごとにチェック",
        "libraries": "requests、hashlib、time、smtplib（標準ライブラリ）",
        "explanation": "Webサイトの変更を自動で監視することで、競合サイトの動向や価格変更を素早く把握できます。",
        "benefits": ["24時間監視", "変更を即座に検出", "手動チェックが不要"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでWebサイト監視のコードを作成してください。以下の条件でお願いします：\n\n1. requestsライブラリを使う\n2. 指定したWebサイトを定期的にチェックする\n3. 変更があった場合に通知する\n4. ハッシュ値で変更を検出する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n監視対象: 指定したWebサイトURL\nチェック間隔: 30分\n通知方法: メールまたはコンソール出力\n\nコピペ用プロンプト:\nPythonでWebサイト監視のコードを作成してください。requestsライブラリを使って指定したWebサイトを定期的にチェックし、ハッシュ値で変更を検出して変更があった場合に通知するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 24,
        "category": "ファイル管理",
        "number": "24/100",
        "title": "データベース自動バックアップ", 
        "desc": "データベースを自動でバックアップ",
        "how_to": "SQLiteやMySQLのデータベースを定期的に自動バックアップします。",
        "sample_code": "import sqlite3\nimport shutil\nimport os\nfrom datetime import datetime\nimport schedule\nimport time\n\ndef backup_sqlite_database(db_path, backup_folder):\n    # バックアップファイル名（日時付き）\n    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n    backup_filename = f'backup_{timestamp}.db'\n    backup_path = os.path.join(backup_folder, backup_filename)\n    \n    # バックアップフォルダを作成\n    if not os.path.exists(backup_folder):\n        os.makedirs(backup_folder)\n    \n    # データベースをコピー\n    shutil.copy2(db_path, backup_path)\n    \n    print(f'バックアップ完了: {backup_path}')\n    \n    # 古いバックアップを削除（30日以上前）\n    cleanup_old_backups(backup_folder, days=30)\n\ndef cleanup_old_backups(backup_folder, days=30):\n    current_time = datetime.now()\n    \n    for filename in os.listdir(backup_folder):\n        if filename.startswith('backup_') and filename.endswith('.db'):\n            file_path = os.path.join(backup_folder, filename)\n            file_time = datetime.fromtimestamp(os.path.getctime(file_path))\n            \n            if (current_time - file_time).days > days:\n                os.remove(file_path)\n                print(f'古いバックアップを削除: {filename}')\n\n# 毎日深夜2時にバックアップ\nschedule.every().day.at('02:00').do(\n    backup_sqlite_database, \n    'database.db', \n    'backups'\n)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
        "libraries": "sqlite3、shutil、os、datetime、schedule（標準ライブラリ）",
        "explanation": "データベースを自動でバックアップすることで、データ損失のリスクを軽減し、復旧を容易にします。",
        "benefits": ["データ保護", "自動実行", "古いバックアップの自動削除"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでデータベース自動バックアップのコードを作成してください。以下の条件でお願いします：\n\n1. sqlite3ライブラリを使う\n2. SQLiteデータベースを定期的にバックアップする\n3. 日時付きのファイル名で保存する\n4. 古いバックアップを自動削除する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象データベース: SQLiteファイル\nバックアップ間隔: 毎日深夜2時\n保持期間: 30日\n\nコピペ用プロンプト:\nPythonでデータベース自動バックアップのコードを作成してください。sqlite3ライブラリを使ってSQLiteデータベースを定期的にバックアップし、日時付きのファイル名で保存して古いバックアップを自動削除するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 25,
        "category": "データ処理・分析",
        "number": "25/100",
        "title": "ログファイル自動分析", 
        "desc": "ログファイルを自動で分析・集計",
        "how_to": "ログファイルを読み込み、エラーやアクセスパターンを自動で分析します。",
        "sample_code": "import re\nfrom collections import Counter\nfrom datetime import datetime\nimport pandas as pd\n\ndef analyze_log_file(log_file_path):\n    # ログファイルを読み込み\n    with open(log_file_path, 'r', encoding='utf-8') as f:\n        lines = f.readlines()\n    \n    # 分析結果を格納\n    analysis = {\n        'total_lines': len(lines),\n        'errors': [],\n        'access_patterns': [],\n        'ip_addresses': []\n    }\n    \n    # 各行を分析\n    for line in lines:\n        # エラーログを検出\n        if 'ERROR' in line or 'error' in line.lower():\n            analysis['errors'].append(line.strip())\n        \n        # IPアドレスを抽出\n        ip_pattern = r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b'\n        ips = re.findall(ip_pattern, line)\n        analysis['ip_addresses'].extend(ips)\n        \n        # アクセスパターンを抽出\n        if 'GET' in line or 'POST' in line:\n            analysis['access_patterns'].append(line.strip())\n    \n    # 統計を計算\n    error_count = len(analysis['errors'])\n    unique_ips = len(set(analysis['ip_addresses']))\n    \n    # 結果を表示\n    print(f'=== ログ分析結果 ===')\n    print(f'総行数: {analysis[\"total_lines\"]:,}行')\n    print(f'エラー数: {error_count}件')\n    print(f'ユニークIP数: {unique_ips}件')\n    print(f'アクセス数: {len(analysis[\"access_patterns\"])}件')\n    \n    # 結果をCSVに保存\n    results_df = pd.DataFrame({\n        '項目': ['総行数', 'エラー数', 'ユニークIP数', 'アクセス数'],\n        '数値': [analysis['total_lines'], error_count, unique_ips, len(analysis['access_patterns'])]\n    })\n    results_df.to_csv('log_analysis.csv', index=False, encoding='utf-8')\n    \n    print('分析結果をlog_analysis.csvに保存しました')\n\n# 使用例\nanalyze_log_file('application.log')",
        "libraries": "re、collections、datetime、pandas（標準ライブラリ）",
        "explanation": "ログファイルを自動で分析することで、システムの問題やアクセスパターンを素早く把握できます。",
        "benefits": ["手動分析が不要", "問題の早期発見", "統計データの自動作成"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでログファイル自動分析のコードを作成してください。以下の条件でお願いします：\n\n1. 標準ライブラリ（re、collections）を使う\n2. ログファイルを読み込んで分析する\n3. エラー数、IPアドレス、アクセスパターンを集計する\n4. 結果をCSVファイルに保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: ログファイル\n分析項目: エラー数、IPアドレス、アクセスパターン\n出力: CSVファイル\n\nコピペ用プロンプト:\nPythonでログファイル自動分析のコードを作成してください。標準ライブラリ（re、collections）を使ってログファイルを読み込み、エラー数、IPアドレス、アクセスパターンを集計して結果をCSVファイルに保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 26,
        "category": "メール・コミュニケーション",
        "number": "26/100",
        "title": "メール自動振り分け", 
        "desc": "受信メールを自動で振り分け",
        "how_to": "imaplibライブラリを使って受信メールを自動で分類・振り分けします。",
        "sample_code": "import imaplib\nimport email\nimport re\nfrom email.header import decode_header\n\ndef auto_sort_emails(email_address, password):\n    # メールサーバーに接続\n    mail = imaplib.IMAP4_SSL('imap.gmail.com')\n    mail.login(email_address, password)\n    mail.select('INBOX')\n    \n    # 未読メールを検索\n    _, messages = mail.search(None, 'UNSEEN')\n    \n    for num in messages[0].split():\n        # メールを取得\n        _, msg_data = mail.fetch(num, '(RFC822)')\n        email_body = msg_data[0][1]\n        email_message = email.message_from_bytes(email_body)\n        \n        # 件名と送信者を取得\n        subject = decode_header(email_message['subject'])[0][0]\n        if isinstance(subject, bytes):\n            subject = subject.decode()\n        \n        sender = email_message['from']\n        \n        # 振り分けルール\n        if '請求書' in subject or 'invoice' in subject.lower():\n            folder = '請求書'\n        elif '会議' in subject or 'meeting' in subject.lower():\n            folder = '会議'\n        elif '報告' in subject or 'report' in subject.lower():\n            folder = '報告書'\n        else:\n            folder = 'その他'\n        \n        print(f'件名: {subject}')\n        print(f'送信者: {sender}')\n        print(f'振り分け先: {folder}')\n        print('---')\n        \n        # 実際の振り分け処理（フォルダ作成と移動）\n        # mail.create(folder)  # フォルダ作成\n        # mail.copy(num, folder)  # メール移動\n    \n    mail.close()\n    mail.logout()\n\n# 使用例\n# auto_sort_emails('your_email@gmail.com', 'your_password')",
        "libraries": "imaplib、email、re（標準ライブラリ）",
        "explanation": "受信メールを自動で振り分けることで、メール管理を効率化し、重要なメールを見逃すことを防げます。",
        "benefits": ["メール管理が自動化", "重要なメールを見逃さない", "作業効率が向上"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonでメール自動振り分けのコードを作成してください。以下の条件でお願いします：\n\n1. imaplibライブラリを使う\n2. GmailのIMAPに接続する\n3. 未読メールを検索する\n4. 件名や送信者で振り分けルールを設定する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象メール: Gmailの未読メール\n振り分け基準: 件名のキーワード\n振り分け先: 請求書、会議、報告書、その他\n\nコピペ用プロンプト:\nPythonでメール自動振り分けのコードを作成してください。imaplibライブラリを使ってGmailのIMAPに接続し、未読メールを検索して件名や送信者で振り分けルールを設定するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 27,
        "category": "ファイル管理",
        "number": "27/100",
        "title": "ファイル重複チェック", 
        "desc": "重複ファイルを自動で検出・削除",
        "how_to": "ファイルのハッシュ値を比較して重複ファイルを検出し、自動で削除します。",
        "sample_code": "import os\nimport hashlib\nfrom collections import defaultdict\n\ndef find_duplicate_files(folder_path):\n    # ファイルのハッシュ値を格納\n    hash_dict = defaultdict(list)\n    \n    # フォルダ内の全ファイルをスキャン\n    for root, dirs, files in os.walk(folder_path):\n        for filename in files:\n            file_path = os.path.join(root, filename)\n            \n            try:\n                # ファイルのハッシュ値を計算\n                with open(file_path, 'rb') as f:\n                    file_hash = hashlib.md5(f.read()).hexdigest()\n                    hash_dict[file_hash].append(file_path)\n            except Exception as e:\n                print(f'エラー: {file_path} - {e}')\n    \n    # 重複ファイルを検出\n    duplicates = []\n    for file_hash, file_paths in hash_dict.items():\n        if len(file_paths) > 1:\n            duplicates.append({\n                'hash': file_hash,\n                'files': file_paths,\n                'size': os.path.getsize(file_paths[0])\n            })\n    \n    return duplicates\ndef remove_duplicates(duplicates, keep_oldest=True):\n    total_saved = 0\n    \n    for duplicate in duplicates:\n        files = duplicate['files']\n        \n        if keep_oldest:\n            # 最も古いファイルを残す\n            files.sort(key=lambda x: os.path.getctime(x))\n            files_to_remove = files[1:]\n        else:\n            # 最も新しいファイルを残す\n            files.sort(key=lambda x: os.path.getctime(x), reverse=True)\n            files_to_remove = files[1:]\n        \n        # 重複ファイルを削除\n        for file_path in files_to_remove:\n            try:\n                os.remove(file_path)\n                total_saved += duplicate['size']\n                print(f'削除: {file_path}')\n            except Exception as e:\n                print(f'削除エラー: {file_path} - {e}')\n    \n    return total_saved\n\n# 使用例\nduplicates = find_duplicate_files('C:/Users/YourName/Documents')\nprint(f'重複ファイル数: {len(duplicates)}件')\n\nif duplicates:\n    saved_space = remove_duplicates(duplicates)\n    print(f'節約した容量: {saved_space / (1024*1024):.2f} MB')",
        "libraries": "os、hashlib、collections（標準ライブラリ）",
        "explanation": "重複ファイルを自動で検出・削除することで、ディスク容量を節約し、ファイル管理を効率化できます。",
        "benefits": ["ディスク容量を節約", "ファイル管理が整理", "手動削除が不要"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでファイル重複チェックのコードを作成してください。以下の条件でお願いします：\n\n1. hashlibライブラリを使う\n2. 指定したフォルダ内のファイルをスキャンする\n3. ハッシュ値で重複ファイルを検出する\n4. 重複ファイルを削除する（古いファイルを残す）\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: 指定したフォルダ\n検出方法: MD5ハッシュ値比較\n削除方法: 古いファイルを残して新しいファイルを削除\n\nコピペ用プロンプト:\nPythonでファイル重複チェックのコードを作成してください。hashlibライブラリを使って指定したフォルダ内のファイルをスキャンし、ハッシュ値で重複ファイルを検出して重複ファイルを削除するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 28,
        "category": "ファイル管理",
        "number": "28/100",
        "title": "画像自動ウォーターマーク", 
        "desc": "画像に自動でウォーターマークを追加",
        "how_to": "PILライブラリを使って画像に自動でウォーターマーク（透かし）を追加します。",
        "sample_code": "from PIL import Image, ImageDraw, ImageFont\nimport os\n\ndef add_watermark(image_path, watermark_text, output_path=None):\n    # 画像を開く\n    with Image.open(image_path) as img:\n        # 画像のサイズを取得\n        width, height = img.size\n        \n        # 透かし用の画像を作成\n        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))\n        draw = ImageDraw.Draw(watermark)\n        \n        # フォントを設定（デフォルトフォントを使用）\n        try:\n            font = ImageFont.truetype('arial.ttf', 36)\n        except:\n            font = ImageFont.load_default()\n        \n        # テキストのサイズを取得\n        bbox = draw.textbbox((0, 0), watermark_text, font=font)\n        text_width = bbox[2] - bbox[0]\n        text_height = bbox[3] - bbox[1]\n        \n        # テキストの位置を計算（右下に配置）\n        x = width - text_width - 20\n        y = height - text_height - 20\n        \n        # 透かしを描画\n        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))\n        \n        # 元画像と透かしを合成\n        result = Image.alpha_composite(img.convert('RGBA'), watermark)\n        \n        # 出力ファイル名を決定\n        if output_path is None:\n            name, ext = os.path.splitext(image_path)\n            output_path = f'{name}_watermarked{ext}'\n        \n        # 保存\n        result.save(output_path)\n        print(f'ウォーターマーク追加完了: {output_path}')\n\ndef batch_add_watermark(folder_path, watermark_text):\n    # フォルダ内の画像に一括でウォーターマークを追加\n    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']\n    \n    for filename in os.listdir(folder_path):\n        if any(filename.lower().endswith(ext) for ext in image_extensions):\n            image_path = os.path.join(folder_path, filename)\n            add_watermark(image_path, watermark_text)\n\n# 使用例\n# 単一画像\nadd_watermark('photo.jpg', '© 2024 Company Name')\n\n# 一括処理\n# batch_add_watermark('photos_folder', '© 2024 Company Name')",
        "libraries": "Pillow (PIL)、os（標準ライブラリ）",
        "explanation": "画像に自動でウォーターマークを追加することで、著作権保護やブランディングを効率化できます。",
        "benefits": ["著作権保護", "ブランディング", "一括処理が可能"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで画像自動ウォーターマークのコードを作成してください。以下の条件でお願いします：\n\n1. Pillowライブラリを使う\n2. 画像にテキストのウォーターマークを追加する\n3. 右下に半透明で表示する\n4. フォルダ内の画像に一括で適用する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: JPG、PNG、BMPファイル\nウォーターマーク: 指定したテキスト\n位置: 右下、半透明\n\nコピペ用プロンプト:\nPythonで画像自動ウォーターマークのコードを作成してください。Pillowライブラリを使って画像にテキストのウォーターマークを追加し、右下に半透明で表示してフォルダ内の画像に一括で適用するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 29,
        "category": "データ処理・分析",
        "number": "29/100",
        "title": "データ自動検証", 
        "desc": "データの整合性を自動でチェック",
        "how_to": "pandasライブラリを使ってデータの整合性を自動でチェックし、エラーを検出します。",
        "sample_code": "import pandas as pd\nimport numpy as np\nfrom datetime import datetime\n\ndef validate_data(data_file):\n    # データを読み込み\n    df = pd.read_csv(data_file)\n    \n    # 検証結果を格納\n    validation_results = {\n        'total_rows': len(df),\n        'errors': [],\n        'warnings': []\n    }\n    \n    # 1. 欠損値チェック\n    missing_data = df.isnull().sum()\n    for column, missing_count in missing_data.items():\n        if missing_count > 0:\n            validation_results['warnings'].append(\n                f'列「{column}」に{missing_count}件の欠損値があります'\n            )\n    \n    # 2. データ型チェック\n    for column in df.columns:\n        if '日付' in column or 'date' in column.lower():\n            try:\n                pd.to_datetime(df[column])\n            except:\n                validation_results['errors'].append(\n                    f'列「{column}」の日付形式が正しくありません'\n                )\n        \n        if '金額' in column or 'price' in column.lower():\n            if not pd.api.types.is_numeric_dtype(df[column]):\n                validation_results['errors'].append(\n                    f'列「{column}」が数値形式ではありません'\n                )\n    \n    # 3. 範囲チェック\n    if '年齢' in df.columns:\n        age_errors = df[(df['年齢'] < 0) | (df['年齢'] > 120)]\n        if len(age_errors) > 0:\n            validation_results['errors'].append(\n                f'年齢に不正な値が{len(age_errors)}件あります'\n            )\n    \n    # 4. 重複チェック\n    duplicates = df.duplicated().sum()\n    if duplicates > 0:\n        validation_results['warnings'].append(\n            f'重複データが{duplicates}件あります'\n        )\n    \n    # 結果を表示\n    print('=== データ検証結果 ===')\n    print(f'総行数: {validation_results[\"total_rows\"]:,}行')\n    print(f'エラー数: {len(validation_results[\"errors\"])}件')\n    print(f'警告数: {len(validation_results[\"warnings\"])}件')\n    \n    if validation_results['errors']:\n        print('\\n【エラー】')\n        for error in validation_results['errors']:\n            print(f'• {error}')\n    \n    if validation_results['warnings']:\n        print('\\n【警告】')\n        for warning in validation_results['warnings']:\n            print(f'• {warning}')\n    \n    # 結果をファイルに保存\n    with open('validation_report.txt', 'w', encoding='utf-8') as f:\n        f.write('データ検証レポート\\n')\n        f.write(f'検証日時: {datetime.now()}\\n')\n        f.write(f'総行数: {validation_results[\"total_rows\"]}\\n')\n        f.write(f'エラー数: {len(validation_results[\"errors\"])}\\n')\n        f.write(f'警告数: {len(validation_results[\"warnings\"])}\\n')\n        \n        if validation_results['errors']:\n            f.write('\\nエラー詳細:\\n')\n            for error in validation_results['errors']:\n                f.write(f'• {error}\\n')\n    \n    print('\\n検証レポートをvalidation_report.txtに保存しました')\n\n# 使用例\nvalidate_data('customer_data.csv')",
        "libraries": "pandas、numpy、datetime（標準ライブラリ）",
        "explanation": "データの整合性を自動でチェックすることで、データ品質の問題を早期に発見し、分析の精度を向上させます。",
        "benefits": ["データ品質の向上", "エラーの早期発見", "分析精度の向上"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでデータ自動検証のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルのデータを検証する\n3. 欠損値、データ型、範囲、重複をチェックする\n4. エラーと警告を分類して報告する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: CSVファイル\n検証項目: 欠損値、データ型、範囲、重複\n出力: 検証レポートファイル\n\nコピペ用プロンプト:\nPythonでデータ自動検証のコードを作成してください。pandasライブラリを使ってCSVファイルのデータを検証し、欠損値、データ型、範囲、重複をチェックしてエラーと警告を分類して報告するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 30,
        "category": "データ処理・分析",
        "number": "30/100",
        "title": "自動データクレンジング", 
        "desc": "データを自動でクレンジング・整形",
        "how_to": "pandasライブラリを使ってデータの前処理を自動化し、分析用のデータを整形します。",
        "sample_code": "import pandas as pd\nimport numpy as np\nimport re\nfrom datetime import datetime\n\ndef clean_data(input_file, output_file):\n    # データを読み込み\n    df = pd.read_csv(input_file)\n    \n    print(f'元データ: {len(df)}行')\n    \n    # 1. 欠損値の処理\n    # 数値列は平均値で補完\n    numeric_columns = df.select_dtypes(include=[np.number]).columns\n    for col in numeric_columns:\n        if df[col].isnull().sum() > 0:\n            mean_value = df[col].mean()\n            df[col].fillna(mean_value, inplace=True)\n            print(f'列「{col}」の欠損値を平均値で補完')\n    \n    # 文字列列は最頻値で補完\n    string_columns = df.select_dtypes(include=['object']).columns\n    for col in string_columns:\n        if df[col].isnull().sum() > 0:\n            mode_value = df[col].mode()[0]\n            df[col].fillna(mode_value, inplace=True)\n            print(f'列「{col}」の欠損値を最頻値で補完')\n    \n    # 2. 文字列の正規化\n    for col in string_columns:\n        if df[col].dtype == 'object':\n            # 前後の空白を削除\n            df[col] = df[col].str.strip()\n            # 大文字小文字を統一\n            df[col] = df[col].str.lower()\n    \n    # 3. 異常値の処理\n    for col in numeric_columns:\n        # 外れ値を検出（3シグマ法）\n        mean = df[col].mean()\n        std = df[col].std()\n        lower_bound = mean - 3 * std\n        upper_bound = mean + 3 * std\n        \n        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]\n        if len(outliers) > 0:\n            # 外れ値を中央値で置換\n            median_value = df[col].median()\n            df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = median_value\n            print(f'列「{col}」の外れ値{len(outliers)}件を中央値で置換')\n    \n    # 4. 重複データの削除\n    initial_rows = len(df)\n    df.drop_duplicates(inplace=True)\n    removed_rows = initial_rows - len(df)\n    if removed_rows > 0:\n        print(f'重複データ{removed_rows}件を削除')\n    \n    # 5. データ型の最適化\n    # 日付列の変換\n    date_columns = [col for col in df.columns if '日付' in col or 'date' in col.lower()]\n    for col in date_columns:\n        try:\n            df[col] = pd.to_datetime(df[col])\n            print(f'列「{col}」を日付型に変換')\n        except:\n            pass\n    \n    # 結果を保存\n    df.to_csv(output_file, index=False, encoding='utf-8')\n    \n    print(f'\\nクレンジング完了！')\n    print(f'処理後データ: {len(df)}行')\n    print(f'保存先: {output_file}')\n    \n    # 処理サマリーを表示\n    print('\\n=== 処理サマリー ===')\n    print(f'• 欠損値補完: {len(numeric_columns) + len(string_columns)}列')\n    print(f'• 文字列正規化: {len(string_columns)}列')\n    print(f'• 異常値処理: {len(numeric_columns)}列')\n    print(f'• 重複削除: {removed_rows}件')\n    print(f'• データ型変換: {len(date_columns)}列')\n\n# 使用例\nclean_data('raw_data.csv', 'cleaned_data.csv')",
        "libraries": "pandas、numpy、re、datetime（標準ライブラリ）",
        "explanation": "データを自動でクレンジングすることで、分析の準備作業を効率化し、データ品質を向上させます。",
        "benefits": ["データ品質の向上", "分析準備の自動化", "時間の大幅節約"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで自動データクレンジングのコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルのデータをクレンジングする\n3. 欠損値補完、異常値処理、重複削除を行う\n4. 文字列の正規化とデータ型変換を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: 生データのCSVファイル\n処理内容: 欠損値補完、異常値処理、重複削除、正規化\n出力ファイル: クレンジング済みCSVファイル\n\nコピペ用プロンプト:\nPythonで自動データクレンジングのコードを作成してください。pandasライブラリを使ってCSVファイルのデータをクレンジングし、欠損値補完、異常値処理、重複削除を行って文字列の正規化とデータ型変換を行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    }
]

# 追加ツールを統合
TOOLS = TOOLS + EXTRA_TOOLS

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    logger.info("Index page accessed")
    try:
        # データベースからツールデータを取得
        tools = []
        try:
            tools = [tool.to_dict() for tool in Tool.query.all()]
            logger.info(f"Retrieved {len(tools)} tools from database")
        except Exception as db_error:
            logger.warning(f"Database error, using fallback data: {db_error}")
            # データベースエラーの場合はフォールバックデータを使用
            tools = TOOLS
        
        # テンプレートファイルの存在確認
        template_path = os.path.join(app.template_folder, 'index.html')
        if not os.path.exists(template_path):
            logger.error(f"Template file not found: {template_path}")
            return f"Template file not found: {template_path}", 500
        
        logger.info(f"Rendering template: {template_path}")
        return render_template('index.html', tools=tools)
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        return f"Internal Server Error: {str(e)}", 500

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    logger.info(f"Tool detail page accessed for tool_id: {tool_id}")
    try:
        # データベースからツールを取得
        tool = Tool.query.get(tool_id)
        if tool is None:
            logger.warning(f"Tool not found for tool_id: {tool_id}")
            return "ツールが見つかりません", 404
        return render_template('detail.html', tool=tool.to_dict())
    except Exception as db_error:
        logger.warning(f"Database error, using fallback data: {db_error}")
        # データベースエラーの場合はフォールバックデータを使用
        tool = next((t for t in TOOLS if t['id'] == tool_id), None)
        if tool is None:
            logger.warning(f"Tool not found for tool_id: {tool_id}")
            return "ツールが見つかりません", 404
        return render_template('detail.html', tool=tool)

# ヘルスチェック用エンドポイント
@app.route('/health')
def health_check():
    return {"status": "healthy", "app": "pyme-app"}, 200

# デバッグ用エンドポイント
@app.route('/debug')
def debug_info():
    try:
        import platform
        template_folder = app.template_folder
        
        # データベース接続テスト
        db_status = "unknown"
        db_tools_count = 0
        try:
            db_tools_count = Tool.query.count()
            db_status = "connected"
        except Exception as db_error:
            db_status = f"error: {str(db_error)}"
        
        return {
            "app_name": "pyme-app",
            "python_version": sys.version,
            "platform": platform.platform(),
            "working_directory": os.getcwd(),
            "port": os.environ.get('PORT', '8000'),
            "flask_env": os.environ.get('FLASK_ENV', 'production'),
            "database_url": app.config.get('SQLALCHEMY_DATABASE_URI', 'not_set'),
            "database_status": db_status,
            "database_tools_count": db_tools_count,
            "fallback_tools_count": len(TOOLS),
            "app_imported": True,
            "template_folder": template_folder,
            "templates_exist": os.path.exists(template_folder),
            "templates_files": os.listdir(template_folder) if os.path.exists(template_folder) else [],
            "index_template_exists": os.path.exists(os.path.join(template_folder, 'index.html')) if os.path.exists(template_folder) else False,
            "detail_template_exists": os.path.exists(os.path.join(template_folder, 'detail.html')) if os.path.exists(template_folder) else False,
            "all_files": os.listdir('.') if os.path.exists('.') else []
        }, 200
    except Exception as e:
        return {"error": str(e), "error_type": type(e).__name__}, 500

# データベース接続テスト用エンドポイント
@app.route('/db-test')
def database_test():
    try:
        # データベース接続テスト
        with db.engine.connect() as connection:
            # SQLiteとPostgreSQLの両方に対応
            if 'sqlite' in str(db.engine.url):
                connection.execute(db.text('SELECT 1'))
            else:
                connection.execute(db.text('SELECT 1'))
        tools_count = Tool.query.count()
        return {
            "status": "success",
            "message": "Database connection successful",
            "tools_count": tools_count,
            "database_url": app.config.get('SQLALCHEMY_DATABASE_URI', 'not_set')
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "database_url": app.config.get('SQLALCHEMY_DATABASE_URI', 'not_set')
        }, 500

# favicon.icoのハンドリング
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content

# 新しいルート: AIプロンプト実行ページ
@app.route('/execute/<int:tool_id>')
def execute_tool(tool_id):
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if not tool:
        return redirect(url_for('index'))
    return render_template('execute.html', tool=tool)

# AIプロンプトからコードを生成するAPI
@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        tool_id = data.get('tool_id')
        custom_prompt = data.get('custom_prompt', '')
        
        tool = next((t for t in TOOLS if t['id'] == tool_id), None)
        if not tool:
            return jsonify({'error': 'Tool not found'}), 404
        
        # デフォルトのプロンプトを使用
        base_prompt = tool.get('ai_prompt', '')
        
        # カスタムプロンプトがある場合は使用
        if custom_prompt:
            final_prompt = custom_prompt
        else:
            final_prompt = base_prompt
        
        # OpenAI APIを使用してコードを生成（オプション）
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if openai_api_key:
            try:
                import openai
                openai.api_key = openai_api_key
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたはPythonプログラミングの専門家です。ユーザーの要求に応じて、安全で実用的なPythonコードを生成してください。"},
                        {"role": "user", "content": final_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                
                generated_code = response.choices[0].message.content
                
                # コードブロックからPythonコードを抽出
                import re
                code_match = re.search(r'```python\n(.*?)\n```', generated_code, re.DOTALL)
                if code_match:
                    generated_code = code_match.group(1)
                
            except Exception as e:
                logger.warning(f"OpenAI API error: {e}, using sample code")
                generated_code = tool.get('sample_code', '')
        else:
            # OpenAI APIキーがない場合はサンプルコードを使用
            generated_code = tool.get('sample_code', '')
        
        return jsonify({
            'success': True,
            'code': generated_code,
            'prompt': final_prompt
        })
        
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        return jsonify({'error': str(e)}), 500

# コードを実行するAPI
@app.route('/api/execute-code', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        tool_id = data.get('tool_id')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # セキュリティチェック（危険なコードを実行しない）
        dangerous_patterns = [
            'os.system', 'subprocess.call', 'subprocess.run', 'eval', 'exec', '__import__',
            'input(', 'while True:', 'schedule.run_pending()', 'time.sleep(',
            'open(', 'file(', 'import os', 'import subprocess'
        ]
        for pattern in dangerous_patterns:
            if pattern in code:
                return jsonify({'error': f'Security: {pattern} is not allowed in web execution'}), 403
        
        # アップロードされたファイルのパスをコードに追加
        if 'uploaded_files' in session and session['uploaded_files']:
            # ファイルパスを環境変数として設定
            for file_id, file_info in session['uploaded_files'].items():
                env_var_name = f"UPLOADED_{file_id.upper()}"
                os.environ[env_var_name] = file_info['path']
                # コード内のファイル名を実際のパスに置換
                code = code.replace(file_info['filename'], file_info['path'])
        
        # 一時ファイルにコードを保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # コードを実行（タイムアウト付き）
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=60  # 60秒に延長
            )
            
            # 結果を返す
            return jsonify({
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            })
            
        finally:
            # 一時ファイルを削除
            os.unlink(temp_file)
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return jsonify({'error': str(e)}), 500

# 設定ウィザードページ
@app.route('/wizard/<int:tool_id>')
def setup_wizard(tool_id):
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if not tool:
        return redirect(url_for('index'))
    return render_template('wizard.html', tool=tool)

# 設定を保存するAPI
@app.route('/api/save-config', methods=['POST'])
def save_config():
    try:
        data = request.get_json()
        tool_id = data.get('tool_id')
        config_data = data.get('config', {})
        
        # 設定をセッションやファイルに保存
        # ここでは簡単な例として、設定をログに出力
        logger.info(f"Saved config for tool {tool_id}: {config_data}")
        
        return jsonify({'success': True, 'message': '設定を保存しました'})
        
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return jsonify({'error': str(e)}), 500

# ファイルアップロード機能を追加
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        # ファイルの拡張子をチェック
        allowed_extensions = {'csv', 'xlsx', 'xls', 'txt', 'json', 'jpg', 'jpeg', 'png', 'gif', 'pdf'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({'error': '許可されていないファイル形式です'}), 400
        
        # 一時ファイルとして保存
        import tempfile
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        # セッションにファイル情報を保存
        if 'uploaded_files' not in session:
            session['uploaded_files'] = {}
        
        file_id = f"file_{len(session['uploaded_files']) + 1}"
        session['uploaded_files'][file_id] = {
            'path': file_path,
            'filename': filename,
            'temp_dir': temp_dir
        }
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'message': f'ファイル "{filename}" をアップロードしました'
        })
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return jsonify({'error': 'ファイルのアップロードに失敗しました'}), 500

# アップロードされたファイルの一覧を取得
@app.route('/api/uploaded-files', methods=['GET'])
def get_uploaded_files():
    if 'uploaded_files' not in session:
        return jsonify({'files': []})
    
    files = []
    for file_id, file_info in session['uploaded_files'].items():
        files.append({
            'id': file_id,
            'filename': file_info['filename']
        })
    
    return jsonify({'files': files})

# ファイルを削除
@app.route('/api/delete-file/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        if 'uploaded_files' in session and file_id in session['uploaded_files']:
            file_info = session['uploaded_files'][file_id]
            
            # ファイルを削除
            if os.path.exists(file_info['path']):
                os.unlink(file_info['path'])
            
            # 一時ディレクトリを削除
            if os.path.exists(file_info['temp_dir']):
                import shutil
                shutil.rmtree(file_info['temp_dir'])
            
            # セッションから削除
            del session['uploaded_files'][file_id]
            
            return jsonify({'success': True, 'message': 'ファイルを削除しました'})
        else:
            return jsonify({'error': 'ファイルが見つかりません'}), 404
            
    except Exception as e:
        logger.error(f"File deletion error: {e}")
        return jsonify({'error': 'ファイルの削除に失敗しました'}), 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8000))
        # 本番環境ではデバッグモードを無効にする
        debug_mode = os.environ.get('FLASK_ENV') == 'development'
        logger.info(f"Starting Flask app on port {port}, debug={debug_mode}")
        logger.info(f"App will be available at: http://0.0.0.0:{port}")
        logger.info("Press Ctrl+C to stop the server")
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        logger.error(f"Error details: {type(e).__name__}: {e}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Files in current directory: {os.listdir('.')}")
        sys.exit(1) 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
