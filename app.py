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
        "sample_code": "import smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart\nimport os\nfrom datetime import datetime\n\nprint('=== メール自動送信（デモ版） ===')\nprint('実際のメール送信には設定が必要です。')\nprint('\\n📧 必要な設定:')\nprint('1. Gmailアカウントのアプリパスワードを取得')\nprint('2. 送信者メールアドレスを設定')\nprint('3. 受信者メールアドレスを設定')\nprint('\\n🔒 セキュリティ注意:')\nprint('• パスワードは環境変数に保存してください')\nprint('• コードに直接パスワードを書かないでください')\n\n# デモ用の設定（実際の使用時は変更してください）\ntry:\n    # 設定値（実際の使用時は環境変数から読み込み）\n    sender_email = 'your_email@gmail.com'  # ← ここにあなたのGmailアドレスを入力\n    sender_password = 'your_app_password'  # ← ここにGmailのアプリパスワードを入力\n    receiver_email = 'receiver@example.com'  # ← ここに受信者のメールアドレスを入力\n    \n    # メール内容\n    subject = 'Python自動送信メール'\n    message_body = f'''\n    こんにちは！\n    \n    これはPythonで自動送信されたメールです。\n    送信日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n    \n    このメールは以下の設定で送信されました:\n    • 送信者: {sender_email}\n    • 受信者: {receiver_email}\n    • 件名: {subject}\n    \n    自動化が成功しました！\n    \n    よろしくお願いします。\n    '''\n    \n    # メールオブジェクト作成\n    msg = MIMEMultipart()\n    msg['From'] = sender_email\n    msg['To'] = receiver_email\n    msg['Subject'] = subject\n    \n    # 本文を追加\n    msg.attach(MIMEText(message_body, 'plain', 'utf-8'))\n    \n    # デモ用の処理（実際の送信はコメントアウト）\n    print('\\n📝 作成されたメール内容:')\n    print(f'送信者: {sender_email}')\n    print(f'受信者: {receiver_email}')\n    print(f'件名: {subject}')\n    print(f'本文: {len(message_body)}文字')\n    \n    # 実際の送信（設定が正しい場合のみ実行）\n    if sender_email != 'your_email@gmail.com' and sender_password != 'your_app_password':\n        print('\\n🚀 メール送信を実行します...')\n        \n        # Gmail SMTPサーバーに接続\n        server = smtplib.SMTP('smtp.gmail.com', 587)\n        server.starttls()\n        \n        # ログイン\n        server.login(sender_email, sender_password)\n        \n        # メール送信\n        text = msg.as_string()\n        server.sendmail(sender_email, receiver_email, text)\n        server.quit()\n        \n        print('✅ メール送信完了！')\n    else:\n        print('\\n⚠️ デモモード: 実際の送信はスキップされました')\n        print('実際に送信するには、上記の設定値を変更してください')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• Gmailの「2段階認証」を有効にしてください')\n    print('• 「アプリパスワード」を生成して使用してください')\n    print('• パスワードは環境変数（.envファイル）に保存してください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• Gmailアドレスとパスワードが正しいか確認してください')\n    print('• アプリパスワードが設定されているか確認してください')\n    print('• インターネット接続を確認してください')\n\nprint('\\n=== メール自動送信完了 ===')",
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
        "sample_code": "import pandas as pd\nimport numpy as np\nfrom datetime import datetime\n\nprint('=== Excel自動処理（サンプルデータ版） ===')\nprint('実際のExcelファイルがないため、サンプルデータで処理を実行します...')\n\ntry:\n    # サンプルデータを作成（実際のExcelファイルの代わり）\n    sample_data = {\n        '名前': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲', '伊藤健太'],\n        '売上': [150000, 200000, 180000, 220000, 190000],\n        '日付': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19']\n    }\n    \n    # データフレーム作成\n    df = pd.DataFrame(sample_data)\n    \n    print(f'データ件数: {len(df)}件')\n    print(f'列名: {list(df.columns)}')\n    print('\\n=== 元データ ===')\n    print(df.to_string(index=False))\n    \n    # データ分析\n    print('\\n=== 分析結果 ===')\n    total_sales = df['売上'].sum()\n    avg_sales = df['売上'].mean()\n    max_sales = df['売上'].max()\n    min_sales = df['売上'].min()\n    \n    print(f'合計売上: {total_sales:,}円')\n    print(f'平均売上: {avg_sales:,.0f}円')\n    print(f'最大売上: {max_sales:,}円（{df.loc[df[\"売上\"].idxmax(), \"名前\"]}）')\n    print(f'最小売上: {min_sales:,}円（{df.loc[df[\"売上\"].idxmin(), \"名前\"]}）')\n    \n    # ランキング作成\n    df_ranked = df.sort_values('売上', ascending=False).reset_index(drop=True)\n    df_ranked['順位'] = range(1, len(df_ranked) + 1)\n    \n    print('\\n=== 売上ランキング ===')\n    print(df_ranked[['順位', '名前', '売上']].to_string(index=False))\n    \n    # 統計情報を追加\n    stats_data = {\n        '名前': ['統計情報'],\n        '売上': [total_sales],\n        '日付': [datetime.now().strftime('%Y-%m-%d')]\n    }\n    \n    # 結果を新しいデータフレームに追加\n    result_df = pd.concat([df, pd.DataFrame(stats_data)], ignore_index=True)\n    \n    # 結果をCSVファイルとして保存（Excelの代わり）\n    result_df.to_csv('sales_analysis_result.csv', index=False, encoding='utf-8-sig')\n    \n    print('\\n=== 処理完了 ===')\n    print('✅ 分析結果を sales_analysis_result.csv に保存しました')\n    print('\\n📊 実行された処理:')\n    print('• 売上データの読み込み')\n    print('• 合計・平均・最大・最小の計算')\n    print('• 売上ランキングの作成')\n    print('• 結果のCSVファイル保存')\n    \nexcept Exception as e:\n    print(f'エラーが発生しました: {e}')\n    print('データ処理に失敗しました。')\n\nprint('\\n💡 実際の使用時は、Excelファイルをアップロードして同じ処理を実行できます。')",
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
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom reportlab.lib import colors\nfrom reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle\nfrom reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle\nfrom reportlab.lib.units import inch\nfrom datetime import datetime\n\nprint('=== PDF自動生成 ===')\nprint('月次レポートのPDFを作成します...')\n\ntry:\n    # PDFファイル名\n    filename = 'monthly_report.pdf'\n    \n    # ドキュメント作成\n    doc = SimpleDocTemplate(filename, pagesize=A4)\n    styles = getSampleStyleSheet()\n    \n    # カスタムスタイル\n    title_style = ParagraphStyle(\n        'CustomTitle',\n        parent=styles['Heading1'],\n        fontSize=24,\n        spaceAfter=30,\n        alignment=1  # 中央揃え\n    )\n    \n    # コンテンツリスト\n    story = []\n    \n    # タイトル\n    title = Paragraph('月次レポート', title_style)\n    story.append(title)\n    \n    # 日付\n    date_text = f'作成日: {datetime.now().strftime(\"%Y年%m月%d日\")}'\n    date_para = Paragraph(date_text, styles['Normal'])\n    story.append(date_para)\n    story.append(Spacer(1, 20))\n    \n    # サマリー\n    summary_title = Paragraph('📊 今月のサマリー', styles['Heading2'])\n    story.append(summary_title)\n    story.append(Spacer(1, 12))\n    \n    summary_data = [\n        ['項目', '金額', '前月比'],\n        ['総売上', '1,250,000円', '+15%'],\n        ['営業利益', '280,000円', '+12%'],\n        ['新規顧客数', '45名', '+8%'],\n        ['既存顧客数', '320名', '+3%']\n    ]\n    \n    summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1*inch])\n    summary_table.setStyle(TableStyle([\n        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),\n        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),\n        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n        ('FONTSIZE', (0, 0), (-1, 0), 12),\n        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),\n        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),\n        ('GRID', (0, 0), (-1, -1), 1, colors.black)\n    ]))\n    story.append(summary_table)\n    story.append(Spacer(1, 20))\n    \n    # 詳細分析\n    detail_title = Paragraph('📈 詳細分析', styles['Heading2'])\n    story.append(detail_title)\n    story.append(Spacer(1, 12))\n    \n    detail_text = '''\n    <b>売上分析:</b><br/>\n    • 今月の売上は前月比15%増加し、好調を維持しています<br/>\n    • 新商品の売上が全体の30%を占め、成長の原動力となっています<br/>\n    • オンライン販売が全体の60%を占め、デジタル化が進んでいます<br/><br/>\n    \n    <b>顧客分析:</b><br/>\n    • 新規顧客の獲得数が前月比8%増加<br/>\n    • 既存顧客のリピート率が85%と高水準を維持<br/>\n    • 顧客満足度調査で4.5/5.0の評価を獲得<br/><br/>\n    \n    <b>今後の方針:</b><br/>\n    • 新商品の販売強化を継続<br/>\n    • オンライン販売チャネルの拡大<br/>\n    • 顧客サポート体制の強化\n    '''\n    \n    detail_para = Paragraph(detail_text, styles['Normal'])\n    story.append(detail_para)\n    story.append(Spacer(1, 20))\n    \n    # ドキュメントをビルド\n    doc.build(story)\n    \n    print(f'✅ PDFファイルを作成しました: {filename}')\n    print('\\n📄 作成された内容:')\n    print('• 月次レポートタイトル')\n    print('• 作成日')\n    print('• 今月のサマリー（表形式）')\n    print('• 詳細分析（売上・顧客・今後の方針）')\n    \nexcept Exception as e:\n    print(f'エラーが発生しました: {e}')\n    print('PDFの作成に失敗しました。')\n\nprint('\\n=== PDF作成完了 ===')\nprint('💡 実際の使用時は、実際のデータを使用してレポートを作成できます。')",
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
        "sample_code": "import requests\nfrom bs4 import BeautifulSoup\nimport pandas as pd\nimport time\nfrom datetime import datetime\n\nprint('=== Webスクレイピング（デモ版） ===')\nprint('実際のWebサイトからデータを取得するデモを実行します。')\nprint('\\n⚠️ 注意事項:')\nprint('• 利用規約を必ず確認してください')\nprint('• 過度なアクセスは避けてください')\nprint('• robots.txtを確認してください')\nprint('• 取得したデータの使用目的を明確にしてください')\n\n# デモ用のサンプルデータ（実際のWebサイトの代わり）\ntry:\n    print('\\n🌐 サンプルWebサイトからデータを取得中...')\n    \n    # サンプルHTMLデータ（実際のWebサイトの代わり）\n    sample_html = '''\n    <html>\n        <body>\n            <div class=\"product\">\n                <h3>ノートパソコン</h3>\n                <span class=\"price\">89,800円</span>\n                <p class=\"description\">高性能なビジネスノート</p>\n            </div>\n            <div class=\"product\">\n                <h3>ワイヤレスマウス</h3>\n                <span class=\"price\">2,980円</span>\n                <p class=\"description\">静音設計のマウス</p>\n            </div>\n            <div class=\"product\">\n                <h3>USBメモリ 32GB</h3>\n                <span class=\"price\">1,580円</span>\n                <p class=\"description\">高速転送対応</p>\n            </div>\n            <div class=\"product\">\n                <h3>ワイヤレスキーボード</h3>\n                <span class=\"price\">4,980円</span>\n                <p class=\"description\">薄型軽量設計</p>\n            </div>\n            <div class=\"product\">\n                <h3>モニター 24インチ</h3>\n                <span class=\"price\">15,800円</span>\n                <p class=\"description\">フルHD対応</p>\n            </div>\n        </body>\n    </html>\n    '''\n    \n    # BeautifulSoupでHTMLを解析\n    soup = BeautifulSoup(sample_html, 'html.parser')\n    \n    # 商品情報を抽出\n    products = []\n    for item in soup.find_all('div', class_='product'):\n        try:\n            name = item.find('h3').text.strip()\n            price = item.find('span', class_='price').text.strip()\n            description = item.find('p', class_='description').text.strip()\n            \n            products.append({\n                '商品名': name,\n                '価格': price,\n                '説明': description,\n                '取得日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n            })\n            \n            print(f'✓ {name}: {price}')\n            \n        except Exception as e:\n            print(f'⚠️ 商品情報の抽出でエラー: {e}')\n            continue\n    \n    if products:\n        # DataFrameに変換\n        df = pd.DataFrame(products)\n        \n        # CSVファイルに保存\n        filename = f'products_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.csv'\n        df.to_csv(filename, index=False, encoding='utf-8-sig')\n        \n        print(f'\\n✅ スクレイピング完了！')\n        print(f'取得件数: {len(products)}件')\n        print(f'保存ファイル: {filename}')\n        \n        print('\\n📊 取得したデータ:')\n        print(df.to_string(index=False))\n        \n        # 統計情報\n        print('\\n📈 統計情報:')\n        print(f'• 商品数: {len(products)}件')\n        print(f'• 平均価格: {sum([int(p[\"価格\"].replace(\"円\", \"\").replace(\",\", \"\")) for p in products]) / len(products):,.0f}円')\n        print(f'• 最高価格: {max([int(p[\"価格\"].replace(\"円\", \"\").replace(\",\", \"\")) for p in products]):,}円')\n        print(f'• 最低価格: {min([int(p[\"価格\"].replace(\"円\", \"\").replace(\",\", \"\")) for p in products]):,}円')\n        \n    else:\n        print('\\n❌ 商品情報を取得できませんでした。')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 対象サイトの利用規約を確認してください')\n    print('• 適切な間隔でアクセスしてください（time.sleep()を使用）')\n    print('• エラーハンドリングを適切に行ってください')\n    print('• 取得したデータの使用目的を明確にしてください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• インターネット接続を確認してください')\n    print('• 対象サイトがアクセス可能か確認してください')\n    print('• 必要なライブラリがインストールされているか確認してください')\n\nprint('\\n=== Webスクレイピング完了 ===')",
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
        "sample_code": "import matplotlib\nmatplotlib.use('Agg')  # Web環境用のバックエンド\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nprint('=== データ可視化グラフ作成 ===')\nprint('サンプルデータを使用してグラフを作成します...')\n\n# サンプルデータを作成（実際の環境で動作する）\ntry:\n    # 月次売上データ\n    months = ['1月', '2月', '3月', '4月', '5月', '6月']\n    sales = [120, 180, 220, 190, 280, 320]\n    \n    # データフレーム作成\n    df = pd.DataFrame({\n        '月': months,\n        '売上': sales\n    })\n    \n    print(f'データ件数: {len(df)}件')\n    print(f'売上合計: {df[\"売上\"].sum():,}万円')\n    print(f'平均売上: {df[\"売上\"].mean():.1f}万円')\n    print(f'最大売上: {df[\"売上\"].max():,}万円（{df.loc[df[\"売上\"].idxmax(), \"月\"]}）')\n    print(f'最小売上: {df[\"売上\"].min():,}万円（{df.loc[df[\"売上\"].idxmin(), \"月\"]}）')\n    \n    # グラフ作成\n    plt.figure(figsize=(12, 8))\n    \n    # メインの折れ線グラフ\n    plt.subplot(2, 2, 1)\n    plt.plot(df['月'], df['売上'], marker='o', linewidth=3, markersize=10, color='#2E86AB')\n    plt.title('月次売上推移', fontsize=14, fontweight='bold', pad=20)\n    plt.xlabel('月', fontsize=12)\n    plt.ylabel('売上（万円）', fontsize=12)\n    plt.grid(True, alpha=0.3)\n    \n    # データラベルを追加\n    for i, v in enumerate(df['売上']):\n        plt.text(i, v + 15, f'{v:,}', ha='center', va='bottom', fontweight='bold', fontsize=10)\n    \n    # 棒グラフ\n    plt.subplot(2, 2, 2)\n    bars = plt.bar(df['月'], df['売上'], color='#A23B72', alpha=0.7)\n    plt.title('月別売上（棒グラフ）', fontsize=14, fontweight='bold', pad=20)\n    plt.xlabel('月', fontsize=12)\n    plt.ylabel('売上（万円）', fontsize=12)\n    plt.grid(True, alpha=0.3, axis='y')\n    \n    # 棒グラフに数値を表示\n    for bar, v in zip(bars, df['売上']):\n        height = bar.get_height()\n        plt.text(bar.get_x() + bar.get_width()/2., height + 10,\n                f'{v:,}', ha='center', va='bottom', fontweight='bold')\n    \n    # 円グラフ（売上比率）\n    plt.subplot(2, 2, 3)\n    total_sales = df['売上'].sum()\n    percentages = [s/total_sales*100 for s in df['売上']]\n    colors = plt.cm.Set3(np.linspace(0, 1, len(df)))\n    \n    wedges, texts, autotexts = plt.pie(percentages, labels=df['月'], autopct='%1.1f%%',\n                                       colors=colors, startangle=90)\n    plt.title('月別売上比率', fontsize=14, fontweight='bold', pad=20)\n    \n    # 統計情報\n    plt.subplot(2, 2, 4)\n    plt.axis('off')\n    stats_text = f'''\n統計情報:\n\n• 総売上: {total_sales:,}万円\n• 平均売上: {df['売上'].mean():.1f}万円\n• 最大売上: {df['売上'].max():,}万円\n• 最小売上: {df['売上'].min():,}万円\n• 成長率: {((df['売上'].iloc[-1] / df['売上'].iloc[0] - 1) * 100):.1f}%\n    '''\n    plt.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',\n             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))\n    \n    # レイアウト調整\n    plt.tight_layout()\n    \n    # グラフ保存\n    plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')\n    print('\\n✅ グラフを保存しました: sales_analysis.png')\n    print('\\n=== グラフ作成完了 ===')\n    print('\\n📊 作成されたグラフ:')\n    print('• 月次売上推移（折れ線グラフ）')\n    print('• 月別売上（棒グラフ）')\n    print('• 月別売上比率（円グラフ）')\n    print('• 統計情報サマリー')\n    \nexcept Exception as e:\n    print(f'エラーが発生しました: {e}')\n    print('グラフの作成に失敗しました。')\n\nprint('\\n💡 実際の使用時は、CSVファイルをアップロードして同じ処理を実行できます。')",
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
        "sample_code": "import os\nimport shutil\nfrom pathlib import Path\nfrom datetime import datetime\n\nprint('=== ファイル自動整理（デモ版） ===')\nprint('実際のフォルダ整理には、対象フォルダのパスを指定してください。')\nprint('\\n📁 対象フォルダ:')\nprint('• デスクトップ: C:\\\\Users\\\\YourName\\\\Desktop')\nprint('• ダウンロード: C:\\\\Users\\\\YourName\\\\Downloads')\nprint('• ドキュメント: C:\\\\Users\\\\YourName\\\\Documents')\nprint('\\n⚠️ 注意事項:')\nprint('• 重要なファイルは事前にバックアップしてください')\nprint('• システムファイルは移動しないでください')\nprint('• 移動先のフォルダが存在しない場合は自動作成されます')\n\ntry:\n    # デモ用のサンプルフォルダ構造を作成\n    print('\\n📂 デモ用のサンプルファイルを作成中...')\n    \n    # サンプルファイルリスト\n    sample_files = [\n        'document1.pdf',\n        'photo1.jpg',\n        'video1.mp4',\n        'music1.mp3',\n        'report.docx',\n        'image.png',\n        'presentation.pptx',\n        'song.wav',\n        'data.xlsx',\n        'picture.gif'\n    ]\n    \n    # ファイル種類の定義\n    file_types = {\n        '📷 画像': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],\n        '📄 文書': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt'],\n        '🎬 動画': ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm'],\n        '🎵 音楽': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],\n        '📦 圧縮': ['.zip', '.rar', '.7z', '.tar', '.gz'],\n        '💻 プログラム': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']\n    }\n    \n    print(f'\\n📊 整理対象ファイル数: {len(sample_files)}件')\n    print('\\n🔍 ファイル分析中...')\n    \n    # ファイル分析\n    file_stats = {}\n    organized_files = []\n    \n    for filename in sample_files:\n        file_ext = Path(filename).suffix.lower()\n        file_size = len(filename) * 100  # デモ用のサイズ\n        \n        # ファイル種類を判定\n        category = '📁 その他'\n        for folder_name, extensions in file_types.items():\n            if file_ext in extensions:\n                category = folder_name\n                break\n        \n        file_stats[category] = file_stats.get(category, 0) + 1\n        organized_files.append({\n            'ファイル名': filename,\n            '拡張子': file_ext,\n            'サイズ': f'{file_size:,} bytes',\n            '分類': category,\n            '移動先': f'{category}/'\n        })\n        \n        print(f'✓ {filename} → {category}')\n    \n    # 整理結果の表示\n    print(f'\\n✅ ファイル整理完了！')\n    print(f'処理ファイル数: {len(organized_files)}件')\n    \n    print('\\n📈 整理結果:')\n    for category, count in file_stats.items():\n        print(f'• {category}: {count}件')\n    \n    print('\\n📋 詳細リスト:')\n    for file_info in organized_files:\n        print(f'• {file_info[\"ファイル名\"]} → {file_info[\"分類\"]}')\n    \n    # 統計情報\n    total_files = len(organized_files)\n    print(f'\\n📊 統計情報:')\n    print(f'• 総ファイル数: {total_files}件')\n    print(f'• 分類カテゴリ数: {len(file_stats)}種類')\n    print(f'• 最も多い種類: {max(file_stats, key=file_stats.get)} ({max(file_stats.values())}件)')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 対象フォルダのパスを正しく設定してください')\n    print('• 重要なファイルは事前にバックアップしてください')\n    print('• システムファイルは移動しないでください')\n    print('• 移動先のフォルダが存在しない場合は自動作成されます')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• フォルダパスが正しいか確認してください')\n    print('• ファイルのアクセス権限を確認してください')\n    print('• ディスク容量が十分か確認してください')\n\nprint('\\n=== ファイル自動整理完了 ===')",
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
        "sample_code": "import random\nfrom datetime import datetime\n\nprint('=== チャットボット作成（デモ版） ===')\nprint('簡単な自動応答チャットボットを作成します。')\nprint('\\n🤖 機能:')\nprint('• 基本的な挨拶への応答')\nprint('• 天気・時間の情報提供')\nprint('• ビジネス関連の質問への回答')\nprint('• 感情に応じた応答')\n\ntry:\n    # 応答パターンの定義\n    responses = {\n        # 基本的な挨拶\n        'こんにちは': ['こんにちは！お疲れ様です。', 'こんにちは！何かお手伝いできることはありますか？', 'こんにちは！今日も頑張りましょう！'],\n        'おはよう': ['おはようございます！今日も一日頑張りましょう！', 'おはようございます！素敵な一日になりますように。', 'おはようございます！何かお手伝いできることはありますか？'],\n        'こんばんは': ['こんばんは！お疲れ様でした。', 'こんばんは！今日も一日お疲れ様でした。', 'こんばんは！明日も頑張りましょう！'],\n        \n        # 天気・時間\n        '天気': ['今日は晴れの予定です。', '今日は曇りの予定です。', '今日は雨の予定です。傘をお忘れなく！'],\n        '時間': [f'現在の時刻は {datetime.now().strftime(\"%H:%M\")} です。', f'現在の時刻は {datetime.now().strftime(\"%H時%M分\")} です。'],\n        \n        # ビジネス関連\n        '売上': ['売上についてお聞きですね。詳細な分析が必要でしたら、データ分析ツールをご利用ください。', '売上データの分析は、Excel自動処理ツールがおすすめです。'],\n        '顧客': ['顧客管理についてですね。顧客データの整理や分析ができます。', '顧客フォローアップの自動化も可能です。'],\n        'レポート': ['レポート作成の自動化ができます。PDF自動生成ツールをご利用ください。', '月次レポートの自動作成が可能です。'],\n        \n        # 感情・感謝\n        'ありがとう': ['どういたしまして！', 'お役に立てて嬉しいです！', 'いつでもお手伝いします！'],\n        '助かった': ['良かったです！', 'お役に立てて嬉しいです！', 'また何かありましたらお声がけください！'],\n        \n        # 終了\n        'さようなら': ['お疲れ様でした！またお話ししましょう！', 'さようなら！またいつでもお声がけください！', 'お疲れ様でした！良い一日をお過ごしください！'],\n        '終了': ['お疲れ様でした！', 'またお話ししましょう！', 'さようなら！']\n    }\n    \n    # チャットボットの開始\n    print('\\n🤖 チャットボット: こんにちは！何かお手伝いできることはありますか？')\n    print('\\n=== デモンストレーション ===')\n    \n    # サンプル会話を実行\n    sample_inputs = ['こんにちは', '天気', '売上', 'ありがとう', 'さようなら']\n    \n    for user_input in sample_inputs:\n        print(f'\\n👤 あなた: {user_input}')\n        \n        # 終了条件のチェック\n        if user_input.lower() in ['終了', 'さようなら', 'bye', 'exit']:\n            response = random.choice(responses.get('さようなら', ['お疲れ様でした！']))\n            print(f'🤖 チャットボット: {response}')\n            break\n        \n        # 応答を探す（部分一致も含む）\n        response = None\n        for key, replies in responses.items():\n            if key in user_input or user_input in key:\n                response = random.choice(replies)\n                break\n        \n        if response is None:\n            # デフォルト応答\n            default_responses = [\n                'すみません、その質問にはお答えできません。',\n                '申し訳ございませんが、その内容については詳しくありません。',\n                'その質問については、別の方法でお調べいただけますでしょうか？',\n                'すみません、その内容は私の知識の範囲外です。'\n            ]\n            response = random.choice(default_responses)\n        \n        print(f'🤖 チャットボット: {response}')\n    \n    print('\\n=== チャットボットの動作確認完了 ===')\n    \n    # 統計情報\n    print('\\n📊 チャットボット統計:')\n    print(f'• 応答パターン数: {len(responses)}種類')\n    print(f'• 総応答数: {sum(len(replies) for replies in responses.values())}個')\n    print(f'• デモ会話数: {len(sample_inputs)}回')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• input()関数を使って対話形式で実行できます')\n    print('• 応答パターンを追加して機能を拡張できます')\n    print('• 自然言語処理ライブラリを使うとより高度な応答が可能です')\n    print('• データベースと連携して学習機能を追加できます')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• コードの構文を確認してください')\n    print('• 必要なライブラリがインストールされているか確認してください')\n\nprint('\\n=== チャットボット作成完了 ===')",
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
        "sample_code": "from PIL import Image\nimport os\nfrom datetime import datetime\n\nprint('=== 画像自動リサイズ（デモ版） ===')\nprint('画像ファイルを一括でリサイズします。')\nprint('\\n📁 対象フォルダ:')\nprint('• ピクチャー: C:\\\\Users\\\\YourName\\\\Pictures')\nprint('• デスクトップ: C:\\\\Users\\\\YourName\\\\Desktop')\nprint('• ダウンロード: C:\\\\Users\\\\YourName\\\\Downloads')\nprint('\\n⚠️ 注意事項:')\nprint('• 元の画像ファイルは保持されます')\nprint('• リサイズ後の画像は新しいファイル名で保存されます')\nprint('• 対応形式: JPG、PNG、GIF、BMP、TIFF')\n\ntry:\n    # デモ用のサンプル画像情報\n    print('\\n📂 デモ用のサンプル画像を処理中...')\n    \n    # サンプル画像リスト\n    sample_images = [\n        {'name': 'photo1.jpg', 'width': 1920, 'height': 1080, 'size': 2048576},\n        {'name': 'image2.png', 'width': 2560, 'height': 1440, 'size': 3145728},\n        {'name': 'picture3.gif', 'width': 1280, 'height': 720, 'size': 1048576},\n        {'name': 'screenshot4.png', 'width': 3840, 'height': 2160, 'size': 5242880},\n        {'name': 'photo5.jpg', 'width': 1600, 'height': 900, 'size': 1572864}\n    ]\n    \n    # リサイズ設定\n    new_width = 800  # 新しい幅\n    quality = 85     # JPEG品質\n    \n    print(f'\\n⚙️ リサイズ設定:')\n    print(f'• 新しい幅: {new_width}px')\n    print(f'• JPEG品質: {quality}%')\n    print(f'• 処理対象: {len(sample_images)}件')\n    \n    # 対応する画像形式\n    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']\n    \n    # 処理結果を記録\n    processed_images = []\n    total_original_size = 0\n    total_resized_size = 0\n    \n    print('\\n🔄 画像処理中...')\n    \n    for img_info in sample_images:\n        filename = img_info['name']\n        original_width = img_info['width']\n        original_height = img_info['height']\n        original_size = img_info['size']\n        \n        # ファイル拡張子をチェック\n        if any(filename.lower().endswith(ext) for ext in image_extensions):\n            try:\n                # アスペクト比を保ってリサイズ\n                ratio = new_width / original_width\n                new_height = int(original_height * ratio)\n                \n                # リサイズ後のサイズを計算（概算）\n                resized_size = int(original_size * (new_width * new_height) / (original_width * original_height))\n                \n                # 新しいファイル名\n                name, ext = os.path.splitext(filename)\n                new_filename = f'{name}_resized_{new_width}px{ext}'\n                \n                # 処理結果を記録\n                processed_images.append({\n                    '元ファイル': filename,\n                    '新ファイル': new_filename,\n                    '元サイズ': f'{original_width}x{original_height}px',\n                    '新サイズ': f'{new_width}x{new_height}px',\n                    '元容量': f'{original_size / 1024 / 1024:.1f}MB',\n                    '新容量': f'{resized_size / 1024 / 1024:.1f}MB',\n                    '圧縮率': f'{(1 - resized_size / original_size) * 100:.1f}%'\n                })\n                \n                total_original_size += original_size\n                total_resized_size += resized_size\n                \n                print(f'✓ {filename} → {new_filename} ({new_width}x{new_height}px)')\n                \n            except Exception as e:\n                print(f'⚠️ {filename} の処理でエラー: {e}')\n                continue\n        else:\n            print(f'⚠️ {filename} は対応していない形式です')\n    \n    if processed_images:\n        print(f'\\n✅ 画像リサイズ完了！')\n        print(f'処理件数: {len(processed_images)}件')\n        \n        print('\\n📊 処理結果:')\n        for result in processed_images:\n            print(f'• {result[\"元ファイル\"]} → {result[\"新ファイル\"]}')\n            print(f'  サイズ: {result[\"元サイズ\"]} → {result[\"新サイズ\"]}')\n            print(f'  容量: {result[\"元容量\"]} → {result[\"新容量\"]} (圧縮率: {result[\"圧縮率\"]})')\n        \n        # 統計情報\n        print(f'\\n📈 統計情報:')\n        print(f'• 総処理件数: {len(processed_images)}件')\n        print(f'• 総容量削減: {(total_original_size - total_resized_size) / 1024 / 1024:.1f}MB')\n        print(f'• 平均圧縮率: {(1 - total_resized_size / total_original_size) * 100:.1f}%')\n        print(f'• 処理日時: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')\n        \n    else:\n        print('\\n❌ 処理可能な画像が見つかりませんでした。')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 対象フォルダのパスを正しく設定してください')\n    print('• 元の画像ファイルは保持されます')\n    print('• 大量の画像を処理する場合は時間がかかります')\n    print('• ディスク容量が十分か確認してください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• Pillowライブラリがインストールされているか確認してください')\n    print('• フォルダパスが正しいか確認してください')\n    print('• ファイルのアクセス権限を確認してください')\n\nprint('\\n=== 画像自動リサイズ完了 ===')",
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
        "sample_code": "import tweepy\nimport schedule\nimport time\nfrom datetime import datetime\nimport random\n\nprint('=== SNS自動投稿（デモ版） ===')\nprint('Twitter（X）への自動投稿機能をデモンストレーションします。')\nprint('\\n📱 必要な設定:')\nprint('1. Twitter Developer Accountの取得')\nprint('2. APIキーとアクセストークンの取得')\nprint('3. アプリケーションの作成')\nprint('\\n🔒 セキュリティ注意:')\nprint('• APIキーは絶対に他人に見せないでください')\nprint('• 環境変数に保存することを推奨します')\nprint('• 投稿内容は事前に確認してください')\n\ntry:\n    # デモ用の設定（実際の使用時は変更してください）\n    consumer_key = 'your_consumer_key'  # ← ここにあなたのConsumer Keyを入力\n    consumer_secret = 'your_consumer_secret'  # ← ここにあなたのConsumer Secretを入力\n    access_token = 'your_access_token'  # ← ここにあなたのAccess Tokenを入力\n    access_token_secret = 'your_access_token_secret'  # ← ここにあなたのAccess Token Secretを入力\n    \n    # ビジネスTipsのリスト\n    business_tips = [\n        '💡 今日のビジネスTips: 朝一番に重要なタスクから始めましょう！優先順位を明確にすることが成功の鍵です。',\n        '🚀 効率化のコツ: 同じ作業を3回以上やったら自動化を検討してください。時間は最も貴重な資源です。',\n        '🤝 コミュニケーション: 相手の立場に立って考えることが大切です。共感力が信頼関係を築きます。',\n        '⏰ 時間管理: 15分単位でタスクを区切ると集中力が続きます。ポモドーロテクニックを試してみてください。',\n        '📈 成長の秘訣: 毎日少しずつでも改善を続けることが、大きな成果につながります。',\n        '🎯 目標設定: SMART原則（具体的、測定可能、達成可能、関連性、期限）で目標を立てましょう。',\n        '💪 リーダーシップ: チームの強みを活かし、弱みを補完する環境を作ることが重要です。',\n        '📊 データ活用: 感情ではなく、データに基づいて意思決定を行いましょう。'\n    ]\n    \n    # 今日のTipsを選択\n    today = datetime.now().day\n    selected_tip = business_tips[today % len(business_tips)]\n    \n    # 投稿内容を作成\n    current_time = datetime.now().strftime('%H:%M')\n    message = f'''{selected_tip}\n\n📅 {datetime.now().strftime('%Y年%m月%d日')} {current_time}\n🤖 Python自動投稿\n\n#ビジネス #効率化 #自動化 #Python'''\n    \n    print('\\n📝 投稿内容:')\n    print('-' * 50)\n    print(message)\n    print('-' * 50)\n    print(f'文字数: {len(message)}文字')\n    \n    # 文字数チェック（Twitter制限: 280文字）\n    if len(message) > 280:\n        print('\\n⚠️ 警告: 投稿内容が280文字を超えています')\n        print('投稿内容を短くしてください')\n    else:\n        print('\\n✅ 文字数チェック: OK')\n    \n    # 実際の投稿（設定が正しい場合のみ実行）\n    if (consumer_key != 'your_consumer_key' and \n        consumer_secret != 'your_consumer_secret' and \n        access_token != 'your_access_token' and \n        access_token_secret != 'your_access_token_secret'):\n        \n        print('\\n🚀 Twitter APIに接続中...')\n        \n        try:\n            # 認証\n            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)\n            auth.set_access_token(access_token, access_token_secret)\n            api = tweepy.API(auth)\n            \n            # アカウント情報を取得\n            user = api.verify_credentials()\n            print(f'✓ 認証成功: @{user.screen_name}')\n            \n            # 投稿\n            print('\\n📤 投稿を実行中...')\n            status = api.update_status(message)\n            \n            print('✅ 投稿完了！')\n            print(f'投稿ID: {status.id}')\n            print(f'投稿URL: https://twitter.com/{user.screen_name}/status/{status.id}')\n            \n        except tweepy.TweepError as e:\n            print(f'\\n❌ Twitter API エラー: {e}')\n            print('\\n🔧 トラブルシューティング:')\n            print('• APIキーが正しいか確認してください')\n            print('• アプリケーションの権限設定を確認してください')\n            print('• 投稿内容が重複していないか確認してください')\n            \n    else:\n        print('\\n⚠️ デモモード: 実際の投稿はスキップされました')\n        print('実際に投稿するには、上記の設定値を変更してください')\n    \n    # スケジュール機能のデモ\n    print('\\n📅 自動投稿スケジュール機能:')\n    print('• 毎日9時にビジネスTipsを投稿')\n    print('• 毎週月曜日に週間振り返りを投稿')\n    print('• 毎月1日に月間目標を投稿')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• Twitter Developer Accountが必要です')\n    print('• APIキーは環境変数に保存してください')\n    print('• 投稿内容は事前に確認してください')\n    print('• 利用規約を遵守してください')\n    print('• 過度な投稿は避けてください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• tweepyライブラリがインストールされているか確認してください')\n    print('• インターネット接続を確認してください')\n    print('• APIキーが正しいか確認してください')\n\nprint('\\n=== SNS自動投稿完了 ===')",
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
        "sample_code": "from google.oauth2.credentials import Credentials\nfrom googleapiclient.discovery import build\nfrom datetime import datetime, timedelta\nimport os\n\nprint('=== Googleカレンダー自動登録（デモ版） ===')\nprint('Googleカレンダーに予定を自動登録する機能をデモンストレーションします。')\nprint('\\n📅 必要な設定:')\nprint('1. Google Cloud Consoleでプロジェクトを作成')\nprint('2. Google Calendar APIを有効化')\nprint('3. 認証情報（OAuth 2.0）を作成')\nprint('4. token.jsonファイルを取得')\nprint('\\n🔒 セキュリティ注意:')\nprint('• 認証情報は絶対に他人に見せないでください')\nprint('• token.jsonファイルは安全に保管してください')\nprint('• 予定の内容は事前に確認してください')\n\ntry:\n    # デモ用の設定（実際の使用時は変更してください）\n    SCOPES = ['https://www.googleapis.com/auth/calendar']\n    \n    # 予定の情報\n    event_title = 'プロジェクト会議'  # ← ここに予定のタイトルを入力\n    event_description = '新プロジェクトのキックオフ会議'  # ← ここに予定の説明を入力\n    event_date = '2024-01-15'  # ← ここに予定の日付を入力（YYYY-MM-DD形式）\n    event_start_time = '10:00'  # ← ここに開始時刻を入力（HH:MM形式）\n    event_end_time = '11:00'    # ← ここに終了時刻を入力（HH:MM形式）\n    \n    print('\\n📝 登録予定の情報:')\n    print(f'• タイトル: {event_title}')\n    print(f'• 説明: {event_description}')\n    print(f'• 日付: {event_date}')\n    print(f'• 時間: {event_start_time} - {event_end_time}')\n    \n    # 日時形式の作成\n    start_datetime = f'{event_date}T{event_start_time}:00+09:00'\n    end_datetime = f'{event_date}T{event_end_time}:00+09:00'\n    \n    # 予定オブジェクトの作成\n    event = {\n        'summary': event_title,\n        'description': event_description,\n        'start': {\n            'dateTime': start_datetime,\n            'timeZone': 'Asia/Tokyo',\n        },\n        'end': {\n            'dateTime': end_datetime,\n            'timeZone': 'Asia/Tokyo',\n        },\n        'reminders': {\n            'useDefault': False,\n            'overrides': [\n                {'method': 'email', 'minutes': 24 * 60},  # 1日前\n                {'method': 'popup', 'minutes': 30},       # 30分前\n            ],\n        },\n    }\n    \n    print('\\n✅ 予定オブジェクトを作成しました')\n    print(f'開始時刻: {start_datetime}')\n    print(f'終了時刻: {end_datetime}')\n    \n    # 実際の登録（認証ファイルが存在する場合のみ実行）\n    if os.path.exists('token.json'):\n        print('\\n🚀 Google Calendar APIに接続中...')\n        \n        try:\n            # 認証\n            creds = Credentials.from_authorized_user_file('token.json', SCOPES)\n            service = build('calendar', 'v3', credentials=creds)\n            \n            # カレンダー情報を取得\n            calendar_list = service.calendarList().list().execute()\n            primary_calendar = next((cal for cal in calendar_list['items'] if cal['primary']), None)\n            \n            if primary_calendar:\n                print(f'✓ カレンダーに接続: {primary_calendar[\"summary\"]}')\n                \n                # 予定を登録\n                print('\\n📅 予定を登録中...')\n                created_event = service.events().insert(\n                    calendarId='primary', \n                    body=event\n                ).execute()\n                \n                print('✅ 予定の登録が完了しました！')\n                print(f'予定ID: {created_event[\"id\"]}')\n                print(f'カレンダーURL: {created_event.get(\"htmlLink\")}')\n                print(f'作成日時: {created_event[\"created\"]}')\n                \n            else:\n                print('❌ プライマリカレンダーが見つかりませんでした')\n                \n        except Exception as e:\n            print(f'\\n❌ Google Calendar API エラー: {e}')\n            print('\\n🔧 トラブルシューティング:')\n            print('• token.jsonファイルが正しいか確認してください')\n            print('• Google Calendar APIが有効化されているか確認してください')\n            print('• インターネット接続を確認してください')\n            \n    else:\n        print('\\n⚠️ デモモード: 実際の登録はスキップされました')\n        print('実際に登録するには、token.jsonファイルが必要です')\n    \n    # 複数予定の一括登録機能のデモ\n    print('\\n📋 一括登録機能のデモ:')\n    sample_events = [\n        {'title': '朝会', 'date': '2024-01-16', 'start': '09:00', 'end': '09:30'},\n        {'title': 'クライアントMTG', 'date': '2024-01-16', 'start': '14:00', 'end': '15:00'},\n        {'title': '週次報告', 'date': '2024-01-17', 'start': '17:00', 'end': '17:30'}\n    ]\n    \n    print('\\n予定リスト:')\n    for i, event_info in enumerate(sample_events, 1):\n        print(f'{i}. {event_info[\"title\"]} - {event_info[\"date\"]} {event_info[\"start\"]}-{event_info[\"end\"]}')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• Google Cloud Consoleでプロジェクトを作成してください')\n    print('• Google Calendar APIを有効化してください')\n    print('• OAuth 2.0認証情報を作成してください')\n    print('• token.jsonファイルを安全に保管してください')\n    print('• 予定の重複を避けてください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• google-authとgoogle-api-python-clientライブラリがインストールされているか確認してください')\n    print('• インターネット接続を確認してください')\n    print('• 認証情報が正しいか確認してください')\n\nprint('\\n=== Googleカレンダー自動登録完了 ===')",
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
        "sample_code": "import cv2\nimport pytesseract\nimport re\nimport pandas as pd\nfrom datetime import datetime\nimport os\n\nprint('=== 名刺データ自動整理（デモ版） ===')\nprint('名刺画像から連絡先情報を自動抽出する機能をデモンストレーションします。')\nprint('\\n📷 必要な設定:')\nprint('1. Tesseract OCRのインストール')\nprint('2. 日本語言語パックのインストール')\nprint('3. OpenCVとpytesseractライブラリのインストール')\nprint('\\n⚠️ 注意事項:')\nprint('• 名刺画像は鮮明で読みやすいものを使用してください')\nprint('• 文字が小さすぎたり、傾いていると認識精度が下がります')\nprint('• 個人情報の取り扱いには十分注意してください')\n\ntry:\n    # デモ用のサンプル名刺データ（実際の画像の代わり）\n    print('\\n📂 デモ用のサンプル名刺を処理中...')\n    \n    # サンプル名刺リスト\n    sample_cards = [\n        {\n            'filename': 'card1.jpg',\n            'extracted_text': '''\n            株式会社サンプル\n            田中 太郎\n            営業部 部長\n            \n            〒100-0001\n            東京都千代田区千代田1-1-1\n            \n            TEL: 03-1234-5678\n            FAX: 03-1234-5679\n            \n            Email: tanaka@sample.co.jp\n            URL: https://www.sample.co.jp\n            '''\n        },\n        {\n            'filename': 'card2.jpg',\n            'extracted_text': '''\n            佐藤 花子\n            マーケティング部\n            \n            〒530-0001\n            大阪府大阪市北区梅田1-1-1\n            \n            Tel: 06-1234-5678\n            Mobile: 090-1234-5678\n            \n            sato@example.com\n            '''\n        },\n        {\n            'filename': 'card3.jpg',\n            'extracted_text': '''\n            鈴木 一郎\n            システム開発部 課長\n            \n            〒460-0001\n            愛知県名古屋市中区栄1-1-1\n            \n            電話: 052-123-4567\n            携帯: 080-1234-5678\n            \n            suzuki@tech.co.jp\n            '''\n        }\n    ]\n    \n    def extract_business_card_info(extracted_text):\n        \"\"\"名刺のテキストから情報を抽出する関数\"\"\"\n        \n        # 正規表現パターンの定義\n        patterns = {\n            'name': [\n                r'([\\u4e00-\\u9fa5]{2,4})\\s*[\\u4e00-\\u9fa5]{2,4}',  # 姓名\n                r'([\\u4e00-\\u9fa5]{2,4})',  # 名前のみ\n            ],\n            'company': [\n                r'([\\u4e00-\\u9fa5]+株式会社)',\n                r'([\\u4e00-\\u9fa5]+有限会社)',\n                r'([\\u4e00-\\u9fa5]+合同会社)',\n            ],\n            'department': [\n                r'([\\u4e00-\\u9fa5]+部)',\n                r'([\\u4e00-\\u9fa5]+課)',\n            ],\n            'position': [\n                r'([\\u4e00-\\u9fa5]+長)',\n                r'([\\u4e00-\\u9fa5]+員)',\n            ],\n            'phone': [\n                r'(\\d{2,4}-\\d{2,4}-\\d{4})',  # 固定電話\n                r'(TEL|Tel|電話)[:\\s]*(\\d{2,4}-\\d{2,4}-\\d{4})',\n            ],\n            'mobile': [\n                r'(\\d{3}-\\d{4}-\\d{4})',  # 携帯電話\n                r'(Mobile|携帯)[:\\s]*(\\d{3}-\\d{4}-\\d{4})',\n            ],\n            'email': [\n                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})',\n            ],\n            'address': [\n                r'〒\\d{3}-\\d{4}\\s*([\\u4e00-\\u9fa5]+)',\n            ],\n            'website': [\n                r'(https?://[\\w\\-./]+)',\n                r'(URL|Web)[:\\s]*(https?://[\\w\\-./]+)',\n            ]\n        }\n        \n        # 情報を抽出\n        extracted_info = {}\n        \n        for field, pattern_list in patterns.items():\n            for pattern in pattern_list:\n                match = re.search(pattern, extracted_text)\n                if match:\n                    # グループが複数ある場合は適切なものを選択\n                    if len(match.groups()) > 1:\n                        extracted_info[field] = match.group(2) if match.group(2) else match.group(1)\n                    else:\n                        extracted_info[field] = match.group(1)\n                    break\n        \n        return extracted_info\n    \n    # 名刺情報を処理\n    processed_cards = []\n    \n    print('\\n🔍 名刺情報を抽出中...')\n    \n    for card in sample_cards:\n        print(f'\\n📄 処理中: {card[\"filename\"]}')\n        \n        # 情報を抽出\n        info = extract_business_card_info(card['extracted_text'])\n        \n        # 処理結果を記録\n        card_info = {\n            'ファイル名': card['filename'],\n            '会社名': info.get('company', ''),\n            '氏名': info.get('name', ''),\n            '部署': info.get('department', ''),\n            '役職': info.get('position', ''),\n            '電話番号': info.get('phone', ''),\n            '携帯電話': info.get('mobile', ''),\n            'メールアドレス': info.get('email', ''),\n            '住所': info.get('address', ''),\n            'Webサイト': info.get('website', ''),\n            '処理日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n        }\n        \n        processed_cards.append(card_info)\n        \n        # 抽出結果を表示\n        print(f'✓ 会社名: {card_info[\"会社名\"]}')\n        print(f'✓ 氏名: {card_info[\"氏名\"]}')\n        print(f'✓ 部署: {card_info[\"部署\"]}')\n        print(f'✓ 電話番号: {card_info[\"電話番号\"]}')\n        print(f'✓ メールアドレス: {card_info[\"メールアドレス\"]}')\n    \n    if processed_cards:\n        # DataFrameに変換\n        df = pd.DataFrame(processed_cards)\n        \n        # CSVファイルに保存\n        filename = f'business_cards_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.csv'\n        df.to_csv(filename, index=False, encoding='utf-8-sig')\n        \n        print(f'\\n✅ 名刺データ整理完了！')\n        print(f'処理件数: {len(processed_cards)}件')\n        print(f'保存ファイル: {filename}')\n        \n        print('\\n📊 抽出結果:')\n        print(df.to_string(index=False))\n        \n        # 統計情報\n        print('\\n📈 統計情報:')\n        print(f'• 総処理件数: {len(processed_cards)}件')\n        print(f'• 会社名抽出率: {sum(1 for c in processed_cards if c[\"会社名\"]) / len(processed_cards) * 100:.1f}%')\n        print(f'• 電話番号抽出率: {sum(1 for c in processed_cards if c[\"電話番号\"]) / len(processed_cards) * 100:.1f}%')\n        print(f'• メールアドレス抽出率: {sum(1 for c in processed_cards if c[\"メールアドレス\"]) / len(processed_cards) * 100:.1f}%')\n        \n    else:\n        print('\\n❌ 処理可能な名刺が見つかりませんでした。')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 名刺画像は鮮明で読みやすいものを使用してください')\n    print('• 文字が小さすぎたり、傾いていると認識精度が下がります')\n    print('• 個人情報の取り扱いには十分注意してください')\n    print('• 抽出結果は必ず確認してから使用してください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• Tesseract OCRがインストールされているか確認してください')\n    print('• 日本語言語パックがインストールされているか確認してください')\n    print('• OpenCVとpytesseractライブラリがインストールされているか確認してください')\n    print('• 画像ファイルが正しい形式か確認してください')\n\nprint('\\n=== 名刺データ自動整理完了 ===')",
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
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom reportlab.lib import colors\nfrom reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle\nfrom reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle\nfrom reportlab.lib.units import inch\nfrom datetime import datetime\nimport os\n\nprint('=== 請求書自動作成（デモ版） ===')\nprint('プロフェッショナルな請求書を自動生成します。')\nprint('\\n📄 機能:')\nprint('• 見やすいレイアウト')\nprint('• 自動計算機能')\nprint('• 税額計算')\nprint('• 支払い条件の設定')\nprint('\\n⚠️ 注意事項:')\nprint('• 請求書の内容は必ず確認してください')\nprint('• 法的要件に従って作成してください')\nprint('• 税務署の要件を確認してください')\n\ntry:\n    # 請求書の基本情報\n    invoice_info = {\n        'invoice_number': 'INV-2024-001',  # ← ここに請求書番号を入力\n        'issue_date': datetime.now().strftime('%Y年%m月%d日'),\n        'due_date': '2024年2月15日',  # ← ここに支払期限を入力\n        'company_name': '株式会社サンプル',  # ← ここに会社名を入力\n        'company_address': '〒100-0001 東京都千代田区千代田1-1-1',\n        'company_phone': '03-1234-5678',\n        'company_email': 'info@sample.co.jp',\n        'client_name': '株式会社クライアント',  # ← ここに顧客名を入力\n        'client_address': '〒530-0001 大阪府大阪市北区梅田1-1-1',\n        'payment_terms': '月末締め翌月末払い',\n        'tax_rate': 0.10  # 消費税率（10%）\n    }\n    \n    # 明細項目\n    items = [\n        {'description': 'Webサイト制作費', 'quantity': 1, 'unit_price': 150000, 'remarks': 'レスポンシブ対応'},\n        {'description': 'システム開発費', 'quantity': 1, 'unit_price': 300000, 'remarks': '管理画面付き'},\n        {'description': '保守・運用費（月額）', 'quantity': 12, 'unit_price': 25000, 'remarks': '年間契約'}\n    ]\n    \n    print('\\n📝 請求書情報:')\n    print(f'• 請求書番号: {invoice_info[\"invoice_number\"]}')\n    print(f'• 発行日: {invoice_info[\"issue_date\"]}')\n    print(f'• 支払期限: {invoice_info[\"due_date\"]}')\n    print(f'• 顧客名: {invoice_info[\"client_name\"]}')\n    \n    # 金額計算\n    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)\n    tax_amount = int(subtotal * invoice_info['tax_rate'])\n    total_amount = subtotal + tax_amount\n    \n    print(f'\\n💰 金額計算:')\n    print(f'• 小計: {subtotal:,}円')\n    print(f'• 消費税（{invoice_info[\"tax_rate\"]*100}%）: {tax_amount:,}円')\n    print(f'• 合計: {total_amount:,}円')\n    \n    # PDFファイル名\n    filename = f'invoice_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.pdf'\n    \n    # PDF作成\n    print('\\n📄 PDFを作成中...')\n    doc = SimpleDocTemplate(filename, pagesize=A4)\n    story = []\n    \n    # スタイル設定\n    styles = getSampleStyleSheet()\n    title_style = ParagraphStyle(\n        'CustomTitle',\n        parent=styles['Heading1'],\n        fontSize=18,\n        spaceAfter=30,\n        alignment=1  # 中央揃え\n    )\n    \n    # タイトル\n    story.append(Paragraph('請求書', title_style))\n    story.append(Spacer(1, 20))\n    \n    # 請求書情報テーブル\n    invoice_data = [\n        ['請求書番号', invoice_info['invoice_number'], '発行日', invoice_info['issue_date']],\n        ['支払期限', invoice_info['due_date'], '支払条件', invoice_info['payment_terms']],\n    ]\n    \n    invoice_table = Table(invoice_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])\n    invoice_table.setStyle(TableStyle([\n        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),\n        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),\n        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),\n        ('FONTSIZE', (0, 0), (-1, -1), 10),\n        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),\n        ('GRID', (0, 0), (-1, -1), 1, colors.black)\n    ]))\n    story.append(invoice_table)\n    story.append(Spacer(1, 20))\n    \n    # 会社情報と顧客情報\n    company_client_data = [\n        ['請求元', '請求先'],\n        [f\"{invoice_info['company_name']}\\n{invoice_info['company_address']}\\nTEL: {invoice_info['company_phone']}\\nEmail: {invoice_info['company_email']}\", \n         f\"{invoice_info['client_name']}\\n{invoice_info['client_address']}\"]\n    ]\n    \n    company_client_table = Table(company_client_data, colWidths=[3*inch, 3*inch])\n    company_client_table.setStyle(TableStyle([\n        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),\n        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n        ('FONTSIZE', (0, 0), (-1, -1), 10),\n        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),\n        ('GRID', (0, 0), (-1, -1), 1, colors.black)\n    ]))\n    story.append(company_client_table)\n    story.append(Spacer(1, 20))\n    \n    # 明細テーブル\n    table_data = [['項目', '数量', '単価', '金額', '備考']]\n    for item in items:\n        amount = item['quantity'] * item['unit_price']\n        table_data.append([\n            item['description'],\n            str(item['quantity']),\n            f\"{item['unit_price']:,}円\",\n            f\"{amount:,}円\",\n            item['remarks']\n        ])\n    \n    # 合計行\n    table_data.append(['', '', '小計', f\"{subtotal:,}円\", ''])\n    table_data.append(['', '', f'消費税（{invoice_info[\"tax_rate\"]*100}%）', f\"{tax_amount:,}円\", ''])\n    table_data.append(['', '', '合計', f\"{total_amount:,}円\", ''])\n    \n    table = Table(table_data, colWidths=[2.5*inch, 0.8*inch, 1*inch, 1.2*inch, 1.5*inch])\n    table.setStyle(TableStyle([\n        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),\n        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n        ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # 数量を中央揃え\n        ('ALIGN', (2, 1), (3, -1), 'RIGHT'),   # 金額を右揃え\n        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n        ('FONTSIZE', (0, 0), (-1, -1), 9),\n        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),\n        ('GRID', (0, 0), (-1, -1), 1, colors.black),\n        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),  # 合計行をハイライト\n    ]))\n    story.append(table)\n    \n    # 備考\n    story.append(Spacer(1, 20))\n    story.append(Paragraph('<b>備考:</b>', styles['Normal']))\n    story.append(Paragraph('• 支払いは銀行振込にてお願いいたします。', styles['Normal']))\n    story.append(Paragraph('• 振込手数料はお客様負担となります。', styles['Normal']))\n    story.append(Paragraph('• ご不明な点がございましたら、お気軽にお問い合わせください。', styles['Normal']))\n    \n    # PDFを生成\n    doc.build(story)\n    \n    print(f'✅ 請求書作成完了！')\n    print(f'ファイル名: {filename}')\n    print(f'ファイルサイズ: {os.path.getsize(filename) / 1024:.1f}KB')\n    \n    print('\\n📊 請求書詳細:')\n    print(f'• 明細項目数: {len(items)}件')\n    print(f'• 請求金額: {total_amount:,}円')\n    print(f'• 消費税額: {tax_amount:,}円')\n    print(f'• 支払期限: {invoice_info[\"due_date\"]}')\n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 請求書の内容は必ず確認してください')\n    print('• 法的要件に従って作成してください')\n    print('• 税務署の要件を確認してください')\n    print('• 顧客情報は正確に入力してください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• reportlabライブラリがインストールされているか確認してください')\n    print('• ファイルの書き込み権限を確認してください')\n    print('• ディスク容量が十分か確認してください')\n\nprint('\\n=== 請求書自動作成完了 ===')",
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
        "sample_code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\nfrom datetime import datetime\nimport seaborn as sns\n\nprint('=== アンケート自動集計（デモ版） ===')\nprint('アンケート結果を自動で集計・分析します。')\nprint('\\n📊 機能:')\nprint('• 基本統計の計算')\nprint('• クロス集計分析')\nprint('• グラフ作成')\nprint('• レポート生成')\nprint('\\n⚠️ 注意事項:')\nprint('• 個人情報の取り扱いには十分注意してください')\nprint('• 統計結果は適切に解釈してください')\nprint('• サンプルサイズが小さい場合は注意が必要です')\n\ntry:\n    # デモ用のサンプルアンケートデータ\n    print('\\n📂 デモ用のサンプルアンケートデータを作成中...')\n    \n    # サンプルデータの作成\n    np.random.seed(42)  # 再現性のため\n    n_responses = 100\n    \n    # 年齢データ（20-60歳の正規分布）\n    ages = np.random.normal(35, 10, n_responses).astype(int)\n    ages = np.clip(ages, 20, 60)\n    \n    # 性別データ\n    genders = np.random.choice(['男性', '女性'], n_responses, p=[0.6, 0.4])\n    \n    # 満足度データ（1-5段階評価）\n    satisfaction = np.random.choice([1, 2, 3, 4, 5], n_responses, p=[0.05, 0.1, 0.2, 0.4, 0.25])\n    \n    # 利用頻度データ\n    usage_frequency = np.random.choice(['毎日', '週1-2回', '月1-2回', '半年に1回', '初回'], n_responses, p=[0.3, 0.4, 0.2, 0.08, 0.02])\n    \n    # 改善要望データ\n    improvement_requests = np.random.choice([\n        '使いやすさの向上', '機能の追加', '価格の見直し', 'サポートの充実', '特にない'\n    ], n_responses, p=[0.3, 0.25, 0.2, 0.15, 0.1])\n    \n    # データフレーム作成\n    survey_data = pd.DataFrame({\n        '回答ID': range(1, n_responses + 1),\n        '年齢': ages,\n        '性別': genders,\n        '満足度': satisfaction,\n        '利用頻度': usage_frequency,\n        '改善要望': improvement_requests,\n        '回答日時': pd.date_range('2024-01-01', periods=n_responses, freq='D')\n    })\n    \n    print(f'\\n📊 サンプルデータ作成完了: {len(survey_data)}件')\n    \n    # 基本統計\n    print('\\n=== 📈 基本統計 ===')\n    print(f'• 回答者数: {len(survey_data):,}人')\n    print(f'• 平均年齢: {survey_data[\"年齢\"].mean():.1f}歳')\n    print(f'• 年齢範囲: {survey_data[\"年齢\"].min()}歳 - {survey_data[\"年齢\"].max()}歳')\n    print(f'• 標準偏差: {survey_data[\"年齢\"].std():.1f}歳')\n    \n    # 性別集計\n    print('\\n=== 👥 性別集計 ===')\n    gender_counts = survey_data['性別'].value_counts()\n    gender_percentages = survey_data['性別'].value_counts(normalize=True) * 100\n    \n    for gender, count in gender_counts.items():\n        percentage = gender_percentages[gender]\n        print(f'• {gender}: {count}人 ({percentage:.1f}%)')\n    \n    # 満足度集計\n    print('\\n=== 😊 満足度集計 ===')\n    satisfaction_counts = survey_data['満足度'].value_counts().sort_index()\n    satisfaction_percentages = survey_data['満足度'].value_counts(normalize=True).sort_index() * 100\n    \n    satisfaction_labels = {1: '非常に不満', 2: '不満', 3: '普通', 4: '満足', 5: '非常に満足'}\n    \n    for score, count in satisfaction_counts.items():\n        percentage = satisfaction_percentages[score]\n        label = satisfaction_labels[score]\n        print(f'• {score}点（{label}）: {count}人 ({percentage:.1f}%)')\n    \n    # 平均満足度\n    avg_satisfaction = survey_data['満足度'].mean()\n    print(f'• 平均満足度: {avg_satisfaction:.2f}点')\n    \n    # 利用頻度集計\n    print('\\n=== 📅 利用頻度集計 ===')\n    usage_counts = survey_data['利用頻度'].value_counts()\n    for usage, count in usage_counts.items():\n        percentage = (count / len(survey_data)) * 100\n        print(f'• {usage}: {count}人 ({percentage:.1f}%)')\n    \n    # 改善要望集計\n    print('\\n=== 💡 改善要望集計 ===')\n    improvement_counts = survey_data['改善要望'].value_counts()\n    for request, count in improvement_counts.items():\n        percentage = (count / len(survey_data)) * 100\n        print(f'• {request}: {count}人 ({percentage:.1f}%)')\n    \n    # クロス集計分析\n    print('\\n=== 🔍 クロス集計分析 ===')\n    \n    # 性別×満足度\n    print('\\n【性別×満足度】')\n    gender_satisfaction = pd.crosstab(survey_data['性別'], survey_data['満足度'], margins=True)\n    print(gender_satisfaction)\n    \n    # 利用頻度×満足度\n    print('\\n【利用頻度×満足度】')\n    usage_satisfaction = pd.crosstab(survey_data['利用頻度'], survey_data['満足度'], margins=True)\n    print(usage_satisfaction)\n    \n    # 年齢層別分析\n    print('\\n=== 📊 年齢層別分析 ===')\n    survey_data['年齢層'] = pd.cut(survey_data['年齢'], \n                                bins=[0, 30, 40, 50, 100], \n                                labels=['20-30代', '30-40代', '40-50代', '50代以上'])\n    \n    age_satisfaction = survey_data.groupby('年齢層')['満足度'].agg(['count', 'mean', 'std']).round(2)\n    print(age_satisfaction)\n    \n    # 統計情報の保存\n    print('\\n=== 💾 結果の保存 ===')\n    \n    # 集計結果をDataFrameにまとめる\n    summary_data = {\n        '項目': ['回答者数', '平均年齢', '平均満足度', '男性比率', '女性比率', '満足度4-5点比率'],\n        '値': [\n            len(survey_data),\n            f\"{survey_data['年齢'].mean():.1f}歳\",\n            f\"{survey_data['満足度'].mean():.2f}点\",\n            f\"{gender_percentages['男性']:.1f}%\",\n            f\"{gender_percentages['女性']:.1f}%\",\n            f\"{(satisfaction_counts[4:].sum() / len(survey_data)) * 100:.1f}%\"\n        ]\n    }\n    \n    summary_df = pd.DataFrame(summary_data)\n    \n    # ファイル保存\n    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n    \n    # 詳細データの保存\n    survey_data.to_csv(f'survey_data_{timestamp}.csv', index=False, encoding='utf-8-sig')\n    \n    # 集計結果の保存\n    summary_df.to_csv(f'survey_summary_{timestamp}.csv', index=False, encoding='utf-8-sig')\n    \n    print(f'✅ 集計完了！')\n    print(f'• 詳細データ: survey_data_{timestamp}.csv')\n    print(f'• 集計結果: survey_summary_{timestamp}.csv')\n    \n    # 主要な発見\n    print('\\n=== 🔍 主要な発見 ===')\n    print(f'• 最も多い年齢層: {survey_data[\"年齢層\"].mode().iloc[0]}') \n    print(f'• 最も多い改善要望: {improvement_counts.index[0]}') \n    print(f'• 最も多い利用頻度: {usage_counts.index[0]}') \n    \n    if avg_satisfaction >= 4.0:\n        print('• 満足度は高い水準です') \n    elif avg_satisfaction >= 3.0:\n        print('• 満足度は普通の水準です') \n    else:\n        print('• 満足度は改善が必要です') \n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 個人情報の取り扱いには十分注意してください')\n    print('• 統計結果は適切に解釈してください')\n    print('• サンプルサイズが小さい場合は注意が必要です')\n    print('• グラフ作成機能も利用できます')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• pandas、matplotlib、numpyライブラリがインストールされているか確認してください')\n    print('• CSVファイルの形式を確認してください')\n    print('• データの文字エンコーディングを確認してください')\n\nprint('\\n=== アンケート自動集計完了 ===')",
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
        "sample_code": "import speech_recognition as sr\nimport os\nfrom datetime import datetime\nimport wave\nimport contextlib\n\nprint('=== 音声データ自動文字起こし（デモ版） ===')\nprint('音声ファイルを自動でテキストに変換します。')\nprint('\\n🎤 対応形式:')\nprint('• WAV、MP3、M4A、FLAC、OGG')\nprint('• 日本語、英語、その他言語')\nprint('\\n⚠️ 注意事項:')\nprint('• 音声の品質が文字起こし精度に影響します')\nprint('• インターネット接続が必要です')\nprint('• 長時間の音声は分割して処理することを推奨します')\nprint('• 個人情報が含まれる場合は注意してください')\n\ntry:\n    # デモ用のサンプル音声情報（実際の音声ファイルの代わり）\n    print('\\n📂 デモ用のサンプル音声を処理中...')\n    \n    # サンプル音声データ\n    sample_audio_info = {\n        'filename': 'meeting_recording.wav',\n        'duration': 120,  # 秒\n        'sample_rate': 16000,\n        'channels': 1,\n        'transcribed_text': '''\n        お疲れ様です。今日の会議の議題について話し合いましょう。\n        まず、新プロジェクトの進捗状況について報告をお願いします。\n        田中さん、お願いします。\n        \n        はい、新プロジェクトについて報告いたします。\n        現在、開発フェーズが70%完了しており、\n        予定通り来月末のリリースに向けて順調に進んでいます。\n        ただし、いくつかの課題があります。\n        \n        一つ目は、ユーザーインターフェースの改善が必要です。\n        二つ目は、パフォーマンスの最適化です。\n        三つ目は、セキュリティテストの実施です。\n        \n        これらの課題について、どのように対応していくか\n        皆さんのご意見をお聞かせください。\n        '''\n    }\n    \n    def analyze_audio_file(audio_info):\n        \"\"\"音声ファイルの情報を分析する関数\"\"\"\n        \n        # 音声ファイルの基本情報をシミュレート\n        file_size = audio_info['duration'] * audio_info['sample_rate'] * audio_info['channels'] * 2 / 1024 / 1024  # MB\n        \n        analysis = {\n            'ファイル名': audio_info['filename'],\n            '再生時間': f\"{audio_info['duration'] // 60}分{audio_info['duration'] % 60}秒\",\n            'サンプリングレート': f\"{audio_info['sample_rate']}Hz\",\n            'チャンネル数': audio_info['channels'],\n            '推定ファイルサイズ': f\"{file_size:.1f}MB\",\n            '処理日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n        }\n        \n        return analysis\n    \n    def transcribe_audio_segments(text, segment_duration=30):\n        \"\"\"音声をセグメントに分割して文字起こしする関数\"\"\"\n        \n        # テキストをセグメントに分割（実際の音声処理のシミュレート）\n        sentences = text.strip().split('。')\n        segments = []\n        current_segment = \"\"\n        \n        for sentence in sentences:\n            if sentence.strip():\n                if len(current_segment) + len(sentence) < 200:  # 文字数制限\n                    current_segment += sentence + \"。\"\n                else:\n                    if current_segment:\n                        segments.append(current_segment.strip())\n                    current_segment = sentence + \"。\"\n        \n        if current_segment:\n            segments.append(current_segment.strip())\n        \n        return segments\n    \n    # 音声ファイルの分析\n    print('\\n🔍 音声ファイルを分析中...')\n    audio_analysis = analyze_audio_file(sample_audio_info)\n    \n    print('\\n📊 音声ファイル情報:') \n    for key, value in audio_analysis.items():\n        print(f'• {key}: {value}')\n    \n    # 文字起こし処理\n    print('\\n🎤 文字起こしを実行中...')\n    \n    # セグメント分割\n    segments = transcribe_audio_segments(sample_audio_info['transcribed_text'])\n    \n    print(f'\\n📝 セグメント数: {len(segments)}個')\n    \n    # 各セグメントの文字起こし結果を記録\n    transcription_results = []\n    total_words = 0\n    \n    for i, segment in enumerate(segments, 1):\n        print(f'\\nセグメント {i}/{len(segments)}:')\n        print(f'内容: {segment[:100]}{\"...\" if len(segment) > 100 else \"\"}')\n        \n        # 文字数と単語数の計算\n        char_count = len(segment)\n        word_count = len(segment.split())\n        total_words += word_count\n        \n        # 信頼度スコア（デモ用）\n        confidence_score = 0.85 + (i * 0.02)  # セグメントごとに少しずつ変化\n        confidence_score = min(confidence_score, 0.98)\n        \n        result = {\n            'セグメント': i,\n            '開始時間': f\"{(i-1)*30:02d}:00\",\n            '終了時間': f\"{i*30:02d}:00\",\n            '文字数': char_count,\n            '単語数': word_count,\n            '信頼度': f\"{confidence_score:.1%}\",\n            'テキスト': segment\n        }\n        \n        transcription_results.append(result)\n        \n        print(f'✓ 文字数: {char_count}文字')\n        print(f'✓ 単語数: {word_count}語')\n        print(f'✓ 信頼度: {confidence_score:.1%}')\n    \n    # 全体の統計\n    total_chars = sum(r['文字数'] for r in transcription_results)\n    avg_confidence = sum(float(r['信頼度'].rstrip('%')) for r in transcription_results) / len(transcription_results)\n    \n    print(f'\\n✅ 文字起こし完了！')\n    print(f'• 総文字数: {total_chars:,}文字')\n    print(f'• 総単語数: {total_words:,}語')\n    print(f'• 平均信頼度: {avg_confidence:.1%}')\n    print(f'• 処理時間: 約{len(segments) * 5}秒（推定）')\n    \n    # 結果の保存\n    print('\\n💾 結果を保存中...')\n    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n    \n    # 詳細結果の保存\n    detailed_filename = f'transcription_detailed_{timestamp}.txt'\n    with open(detailed_filename, 'w', encoding='utf-8') as f:\n        f.write(f'音声文字起こし結果\\n')\n        f.write(f'ファイル: {sample_audio_info[\"filename\"]}\\n')\n        f.write(f'処理日時: {datetime.now().strftime(\"%Y年%m月%d日 %H:%M:%S\")}\\n')\n        f.write(f'総文字数: {total_chars:,}文字\\n')\n        f.write(f'平均信頼度: {avg_confidence:.1%}\\n')\n        f.write('\\n' + '='*50 + '\\n\\n')\n        \n        for result in transcription_results:\n            f.write(f'[セグメント {result[\"セグメント\"]}] {result[\"開始時間\"]}-{result[\"終了時間\"]}\\n')\n            f.write(f'信頼度: {result[\"信頼度\"]}\\n')\n            f.write(f'{result[\"テキスト\"]}\\n\\n')\n    \n    # 簡潔版の保存\n    simple_filename = f'transcription_simple_{timestamp}.txt'\n    with open(simple_filename, 'w', encoding='utf-8') as f:\n        f.write('\\n'.join(r['テキスト'] for r in transcription_results))\n    \n    print(f'• 詳細版: {detailed_filename}')\n    print(f'• 簡潔版: {simple_filename}')\n    \n    # 品質評価\n    print('\\n📈 品質評価:') \n    if avg_confidence >= 0.9:\n        print('• 信頼度: 非常に高い（90%以上）') \n    elif avg_confidence >= 0.8:\n        print('• 信頼度: 高い（80-90%）') \n    elif avg_confidence >= 0.7:\n        print('• 信頼度: 普通（70-80%）') \n    else:\n        print('• 信頼度: 低い（70%未満）- 手動確認を推奨') \n    \n    print('\\n💡 実際の使用時の注意点:')\n    print('• 音声の品質が文字起こし精度に影響します')\n    print('• インターネット接続が必要です')\n    print('• 長時間の音声は分割して処理することを推奨します')\n    print('• 個人情報が含まれる場合は注意してください')\n    print('• 結果は必ず確認してから使用してください')\n    \nexcept Exception as e:\n    print(f'\\n❌ エラーが発生しました: {e}')\n    print('\\n🔧 トラブルシューティング:')\n    print('• SpeechRecognitionライブラリがインストールされているか確認してください')\n    print('• 音声ファイルの形式を確認してください')\n    print('• インターネット接続を確認してください')\n    print('• 音声ファイルが破損していないか確認してください')\n\nprint('\\n=== 音声データ自動文字起こし完了 ===')",
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

# エラーメッセージの日本語翻訳辞書
ERROR_TRANSLATIONS = {
    # 一般的なエラー
    'No code provided': 'コードが入力されていません',
    'Code execution timed out': 'コードの実行がタイムアウトしました（60秒を超過）',
    'Tool not found': 'ツールが見つかりません',
    'Security: os.system is not allowed in web execution': 'セキュリティ上の理由で、os.systemはWeb実行では使用できません',
    'Security: subprocess.call is not allowed in web execution': 'セキュリティ上の理由で、subprocess.callはWeb実行では使用できません',
    'Security: subprocess.run is not allowed in web execution': 'セキュリティ上の理由で、subprocess.runはWeb実行では使用できません',
    'Security: eval is not allowed in web execution': 'セキュリティ上の理由で、evalはWeb実行では使用できません',
    'Security: exec is not allowed in web execution': 'セキュリティ上の理由で、execはWeb実行では使用できません',
    'Security: __import__ is not allowed in web execution': 'セキュリティ上の理由で、__import__はWeb実行では使用できません',
    'Security: input( is not allowed in web execution': 'Web実行では対話的な入力（input）は使用できません',
    'Security: while True: is not allowed in web execution': '無限ループ（while True）はWeb実行では使用できません',
    'Security: schedule.run_pending() is not allowed in web execution': 'スケジュール実行はWeb実行では使用できません',
    'Security: time.sleep( is not allowed in web execution': 'time.sleepはWeb実行では使用できません',
    'Security: open( is not allowed in web execution': 'ファイル操作（open）はWeb実行では使用できません',
    'Security: file( is not allowed in web execution': 'ファイル操作（file）はWeb実行では使用できません',
    'Security: import os is not allowed in web execution': 'セキュリティ上の理由で、osモジュールのインポートはWeb実行では使用できません',
    'Security: import subprocess is not allowed in web execution': 'セキュリティ上の理由で、subprocessモジュールのインポートはWeb実行では使用できません',
    
    # ファイル関連エラー
    'ファイルが選択されていません': 'ファイルが選択されていません',
    '許可されていないファイル形式です': '許可されていないファイル形式です。CSV、Excel、テキスト、画像、PDFファイルのみアップロード可能です',
    'ファイルのアップロードに失敗しました': 'ファイルのアップロードに失敗しました',
    'ファイルが見つかりません': 'ファイルが見つかりません',
    'ファイルの削除に失敗しました': 'ファイルの削除に失敗しました',
    
    # Python実行エラー
    'SyntaxError': 'コードの文法エラーがあります',
    'IndentationError': 'インデント（字下げ）のエラーがあります',
    'NameError': '未定義の変数や関数を使用しています',
    'ImportError': '存在しないモジュールをインポートしようとしています',
    'ModuleNotFoundError': '指定されたモジュールが見つかりません',
    'AttributeError': '存在しない属性やメソッドにアクセスしようとしています',
    'TypeError': 'データ型のエラーがあります',
    'ValueError': '値のエラーがあります',
    'FileNotFoundError': '指定されたファイルが見つかりません',
    'PermissionError': 'ファイルやディレクトリへのアクセス権限がありません',
    'ZeroDivisionError': 'ゼロで割り算しようとしています',
    'IndexError': 'リストや配列の範囲外のインデックスにアクセスしています',
    'KeyError': '辞書に存在しないキーにアクセスしています',
    'RuntimeError': '実行時エラーが発生しました',
    'MemoryError': 'メモリ不足です',
    'OverflowError': '数値が大きすぎます',
    'RecursionError': '再帰が深すぎます',
    'TimeoutError': '処理がタイムアウトしました',
    'ConnectionError': 'ネットワーク接続エラーが発生しました',
    'OSError': 'オペレーティングシステムエラーが発生しました',
    'IOError': '入出力エラーが発生しました',
    
    # ライブラリ固有のエラー
    'pandas': 'pandasライブラリがインストールされていません',
    'matplotlib': 'matplotlibライブラリがインストールされていません',
    'openpyxl': 'openpyxlライブラリがインストールされていません',
    'requests': 'requestsライブラリがインストールされていません',
    'beautifulsoup4': 'beautifulsoup4ライブラリがインストールされていません',
    'pillow': 'Pillowライブラリがインストールされていません',
    'reportlab': 'reportlabライブラリがインストールされていません',
    'schedule': 'scheduleライブラリがインストールされていません',
    'tweepy': 'tweepyライブラリがインストールされていません',
    'opencv-python': 'opencv-pythonライブラリがインストールされていません',
    'pytesseract': 'pytesseractライブラリがインストールされていません',
    'google-auth': 'google-authライブラリがインストールされていません',
    'google-api-python-client': 'google-api-python-clientライブラリがインストールされていません',
    
    # データ処理関連エラー
    'No numeric data': '数値データが見つかりません',
    'Empty DataFrame': 'データフレームが空です',
    'Column not found': '指定された列が見つかりません',
    'Invalid file format': 'ファイル形式が正しくありません',
    'File is corrupted': 'ファイルが破損しています',
    'Encoding error': '文字エンコーディングエラーが発生しました',
    
    # メール関連エラー
    'SMTPAuthenticationError': 'メール認証に失敗しました。メールアドレスとパスワードを確認してください',
    'SMTPConnectError': 'メールサーバーに接続できません',
    'SMTPRecipientsRefused': '受信者のメールアドレスが拒否されました',
    'SMTPSenderRefused': '送信者のメールアドレスが拒否されました',
    'SMTPDataError': 'メールデータエラーが発生しました',
    'SMTPNotSupportedError': 'このメールサーバーはサポートされていません',
    
    # Webスクレイピング関連エラー
    'Connection timeout': 'Webサイトへの接続がタイムアウトしました',
    'HTTP Error': 'HTTPエラーが発生しました',
    'SSL Certificate Error': 'SSL証明書エラーが発生しました',
    'Robot.txt violation': 'Webサイトの利用規約に違反しています',
    'Rate limit exceeded': 'アクセス頻度が制限を超えました',
    
    # 画像処理関連エラー
    'Image file is corrupted': '画像ファイルが破損しています',
    'Unsupported image format': 'サポートされていない画像形式です',
    'Image size too large': '画像サイズが大きすぎます',
    'OCR failed': '文字認識に失敗しました',
    
    # データベース関連エラー
    'Database connection failed': 'データベース接続に失敗しました',
    'Table not found': 'テーブルが見つかりません',
    'Column not found': '列が見つかりません',
    'Duplicate entry': '重複するエントリがあります',
    'Foreign key constraint': '外部キー制約エラーが発生しました',
    
    # API関連エラー
    'API key is invalid': 'APIキーが無効です',
    'API rate limit exceeded': 'API利用制限を超えました',
    'API endpoint not found': 'APIエンドポイントが見つかりません',
    'API authentication failed': 'API認証に失敗しました',
    'API request failed': 'APIリクエストに失敗しました',
    
    # 設定関連エラー
    'Configuration file not found': '設定ファイルが見つかりません',
    'Invalid configuration': '設定が無効です',
    'Missing required parameter': '必要なパラメータが不足しています',
    'Invalid parameter value': 'パラメータの値が無効です',
    
    # 権限関連エラー
    'Permission denied': 'アクセス権限がありません',
    'Read-only file system': 'ファイルシステムが読み取り専用です',
    'Insufficient privileges': '権限が不足しています',
    'Access denied': 'アクセスが拒否されました',
    
    # ネットワーク関連エラー
    'Network unreachable': 'ネットワークに到達できません',
    'DNS resolution failed': 'DNS解決に失敗しました',
    'Connection refused': '接続が拒否されました',
    'Host unreachable': 'ホストに到達できません',
    'Port not available': 'ポートが利用できません',
    
    # システム関連エラー
    'Out of memory': 'メモリ不足です',
    'Disk space full': 'ディスク容量が不足しています',
    'Process limit exceeded': 'プロセス数の制限を超えました',
    'File descriptor limit': 'ファイルディスクリプタの制限に達しました',
    'System resource exhausted': 'システムリソースが不足しています'
}

def translate_error_message(error_msg):
    """
    英語のエラーメッセージを日本語に翻訳する
    """
    # 完全一致をチェック
    if error_msg in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[error_msg]
    
    # 部分一致をチェック（エラータイプの検出）
    for english_pattern, japanese_msg in ERROR_TRANSLATIONS.items():
        if english_pattern in error_msg:
            return japanese_msg
    
    # 一般的なPythonエラーの検出
    if 'SyntaxError' in error_msg:
        return 'コードの文法エラーがあります。括弧の対応やインデントを確認してください'
    elif 'IndentationError' in error_msg:
        return 'インデント（字下げ）のエラーがあります。タブとスペースの混在を確認してください'
    elif 'NameError' in error_msg:
        return '未定義の変数や関数を使用しています。変数名や関数名のスペルを確認してください'
    elif 'ImportError' in error_msg or 'ModuleNotFoundError' in error_msg:
        return '存在しないモジュールをインポートしようとしています。ライブラリ名を確認してください'
    elif 'AttributeError' in error_msg:
        return '存在しない属性やメソッドにアクセスしようとしています'
    elif 'TypeError' in error_msg:
        return 'データ型のエラーがあります。文字列と数値の演算などを確認してください'
    elif 'ValueError' in error_msg:
        return '値のエラーがあります。入力値の形式を確認してください'
    elif 'FileNotFoundError' in error_msg:
        return '指定されたファイルが見つかりません。ファイルパスを確認してください'
    elif 'PermissionError' in error_msg:
        return 'ファイルやディレクトリへのアクセス権限がありません'
    elif 'ZeroDivisionError' in error_msg:
        return 'ゼロで割り算しようとしています。分母が0になっていないか確認してください'
    elif 'IndexError' in error_msg:
        return 'リストや配列の範囲外のインデックスにアクセスしています'
    elif 'KeyError' in error_msg:
        return '辞書に存在しないキーにアクセスしています'
    elif 'TimeoutError' in error_msg:
        return '処理がタイムアウトしました。処理時間を短縮するか、タイムアウト時間を延長してください'
    
    # デフォルトメッセージ
    return f'エラーが発生しました: {error_msg}'

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
            return jsonify({'error': translate_error_message('Tool not found')}), 404
        
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
        return jsonify({'error': translate_error_message(str(e))}), 500

# コードを実行するAPI
@app.route('/api/execute-code', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        tool_id = data.get('tool_id')
        
        if not code:
            return jsonify({'error': translate_error_message('No code provided')}), 400
        
        # セキュリティチェック（危険なコードを実行しない）
        dangerous_patterns = [
            'os.system', 'subprocess.call', 'subprocess.run', 'eval', 'exec', '__import__',
            'input(', 'while True:', 'schedule.run_pending()', 'time.sleep(',
            'open(', 'file(', 'import os', 'import subprocess'
        ]
        for pattern in dangerous_patterns:
            if pattern in code:
                error_msg = f'Security: {pattern} is not allowed in web execution'
                return jsonify({'error': translate_error_message(error_msg)}), 403
        
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
        return jsonify({'error': translate_error_message('Code execution timed out')}), 408
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return jsonify({'error': translate_error_message(str(e))}), 500

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
        return jsonify({'error': translate_error_message(str(e))}), 500

# ファイルアップロード機能を追加
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': translate_error_message('ファイルが選択されていません')}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': translate_error_message('ファイルが選択されていません')}), 400
        
        # ファイルの拡張子をチェック
        allowed_extensions = {'csv', 'xlsx', 'xls', 'txt', 'json', 'jpg', 'jpeg', 'png', 'gif', 'pdf'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({'error': translate_error_message('許可されていないファイル形式です')}), 400
        
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
        return jsonify({'error': translate_error_message('ファイルのアップロードに失敗しました')}), 500

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
            return jsonify({'error': translate_error_message('ファイルが見つかりません')}), 404
            
    except Exception as e:
        logger.error(f"File deletion error: {e}")
        return jsonify({'error': translate_error_message('ファイルの削除に失敗しました')}), 500

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
