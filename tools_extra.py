import pandas as pd
import os
import shutil
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from datetime import datetime, timedelta
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
from bs4 import BeautifulSoup
import time
import re
import calendar
import glob
import random
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

EXTRA_TOOLS = [
    {
        "id": 31,
        "category": "ファイル管理",
        "number": "31/100",
        "title": "PDF一括結合",
        "desc": "複数のPDFファイルを自動で1つに結合",
        "how_to": "PyPDF2ライブラリを使って、複数のPDFファイルを1つのファイルにまとめます。",
        "sample_code": "import os\nfrom PyPDF2 import PdfMerger\n\n# --- ユーザーが変更する箇所 ---\n# 結合したいPDFファイルのリストを指定してください。\n# 例: ['dummy_data/file1.pdf', 'dummy_data/file2.pdf']\n# dummy_dataフォルダにダミーファイルが生成されています。\npdf_files = ['dummy_data/file1.pdf', 'dummy_data/file2.pdf', 'dummy_data/file3.pdf']\n\n# 出力するPDFファイル名を指定してください。\noutput_pdf = 'dummy_data/merged_output.pdf'\n# ------------------------------\n\n# PDF結合処理\ntry:\n    merger = PdfMerger()\n    for pdf in pdf_files:\n        if not os.path.exists(pdf):\n            print(f\"エラー: ファイル '{pdf}' が見つかりません。スキップします。\")\n            continue\n        merger.append(pdf)\n    \n    if not merger.pages:\n        print(\"エラー: 結合できるPDFファイルが見つかりませんでした。\")\n    else:\n        merger.write(output_pdf)\n        merger.close()\n        print(f'PDF結合完了！出力ファイル: {output_pdf}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "PyPDF2、os（標準ライブラリ）",
        "explanation": "複数のPDFを一括で結合することで、資料整理や提出が効率化できます。",
        "benefits": ["手作業が不要", "一括結合", "資料整理が簡単"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでPDF一括結合のコードを作成してください。以下の条件でお願いします：\n\n1. PyPDF2ライブラリを使う\n2. 複数のPDFファイルを1つにまとめる\n3. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: 複数のPDF\n出力ファイル: merged.pdf\n\nコピペ用プロンプト:\nPythonでPDF一括結合のコードを作成してください。PyPDF2ライブラリを使って複数のPDFファイルを1つにまとめるコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 32,
        "category": "ファイル管理",
        "number": "32/100",
        "title": "フォルダ自動圧縮",
        "desc": "指定フォルダを自動でZIP圧縮",
        "how_to": "shutilライブラリを使って、指定したフォルダをZIPファイルに圧縮します。",
        "sample_code": "import shutil\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 圧縮したいフォルダのパスを指定してください。\n# dummy_dataフォルダにダミーファイルが生成されています。\nfolder_to_compress = 'dummy_data/target_folder'\n\n# 出力するZIPファイル名を指定してください。\n# 例: 'my_archive' とすると 'my_archive.zip' が作成されます。\noutput_zip_name = 'dummy_data/compressed_folder'\n# ------------------------------\n\n# フォルダ圧縮処理\ntry:\n    if not os.path.exists(folder_to_compress):\n        print(f\"エラー: フォルダ '{folder_to_compress}' が見つかりません。\")\n    else:\n        shutil.make_archive(output_zip_name, 'zip', folder_to_compress)\n        print(f'圧縮完了！出力ファイル: {output_zip_name}.zip')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "shutil（標準ライブラリ）",
        "explanation": "フォルダを自動で圧縮することで、バックアップやメール添付が簡単になります。",
        "benefits": ["バックアップが簡単", "メール添付が楽", "手作業が不要"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonでフォルダ自動圧縮のコードを作成してください。以下の条件でお願いします：\n\n1. shutilライブラリを使う\n2. 指定したフォルダをZIPファイルに圧縮する\n3. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: target_folder\n出力ファイル: target_folder.zip\n\nコピペ用プロンプト:\nPythonでフォルダ自動圧縮のコードを作成してください。shutilライブラリを使って指定したフォルダをZIPファイルに圧縮するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 33,
        "category": "ファイル管理",
        "number": "33/100",
        "title": "画像一括リネーム",
        "desc": "画像ファイルを自動で連番リネーム",
        "how_to": "osライブラリを使って、フォルダ内の画像ファイルを連番でリネームします。",
        "sample_code": "import os\n\n# --- ユーザーが変更する箇所 ---\n# リネームしたい画像ファイルがあるフォルダのパスを指定してください。\n# dummy_data/imagesフォルダにダミー画像が生成されています。\nimage_folder = 'dummy_data/images'\n\n# リネーム後のファイル名のプレフィックスを指定してください。\n# 例: 'photo_' とすると 'photo_001.jpg', 'photo_002.png' のようになります。\nnew_name_prefix = 'renamed_image_'\n# ------------------------------\n\n# 画像ファイルリネーム処理\ntry:\n    if not os.path.exists(image_folder):\n        print(f\"エラー: フォルダ '{image_folder}' が見つかりません。\")\n    else:\n        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]\n        if not image_files:\n            print(f\"フォルダ '{image_folder}' に画像ファイルが見つかりません。\")\n        else:\n            print(f\"フォルダ '{image_folder}' 内の画像をリネーム中...\")\n            for i, filename in enumerate(sorted(image_files), 1):\n                old_path = os.path.join(image_folder, filename)\n                file_extension = os.path.splitext(filename)[1]\n                new_name = f'{new_name_prefix}{i:03d}{file_extension}'\n                new_path = os.path.join(image_folder, new_name)\n                os.rename(old_path, new_path)\n                print(f'{filename} → {new_name}')\n            print('リネーム完了！')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "os（標準ライブラリ）",
        "explanation": "大量の画像を一括でリネームすることで、整理や管理が簡単になります。",
        "benefits": ["整理が簡単", "一括処理", "手作業が不要"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonで画像一括リネームのコードを作成してください。以下の条件でお願いします：\n\n1. osライブラリを使う\n2. フォルダ内の画像ファイルを連番でリネームする\n3. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: images\nリネーム形式: image_001.jpg など\n\nコピペ用プロンプト:\nPythonで画像一括リネームのコードを作成してください。osライブラリを使ってフォルダ内の画像ファイルを連番でリネームするコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 34,
        "category": "データ処理・分析",
        "number": "34/100",
        "title": "売上データ自動分析",
        "desc": "売上データを自動で分析・レポート化",
        "how_to": "CSV売上データを自動で分析し、月次・商品別レポートを作成します。",
        "sample_code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 入力CSVファイルのパスを指定してください。\ninput_csv_path = 'dummy_data/sales.csv'\n# 出力するグラフ画像ファイルのパスを指定してください。\noutput_image_path = 'dummy_data/monthly_sales.png'\n# ------------------------------\n\n# 売上データ分析処理\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: 入力ファイル '{input_csv_path}' が見つかりません。\")\n    else:\n        df = pd.read_csv(input_csv_path, encoding='utf-8')\n        if '月' not in df.columns or '売上' not in df.columns:\n            print(\"エラー: CSVファイルに '月' または '売上' 列が見つかりません。\")\n        else:\n            monthly_sales = df.groupby('月')['売上'].sum()\n            plt.figure(figsize=(10, 6))\n            monthly_sales.plot(kind='line', marker='o')\n            plt.title('月次売上推移')\n            plt.xlabel('月')\n            plt.ylabel('売上')\n            plt.grid(True)\n            plt.tight_layout()\n            plt.savefig(output_image_path)\n            plt.close()\n            print(f'分析完了！グラフ画像: {output_image_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas、matplotlib",
        "explanation": "売上データを自動で分析。月次・商品別の傾向が一目で分かる。",
        "benefits": ["分析が楽", "グラフも自動", "戦略立案に活用"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで売上データ自動分析のコードを作成してください。以下の条件でお願いします：\n\n1. pandasとmatplotlibライブラリを使う\n2. CSVファイルの売上データを読み込む\n3. 月次・商品別・取引先別の分析を行う\n4. 売上傾向と成長率を計算する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（日付、商品名、取引先、売上金額）\n出力形式: Excelファイル（sales_analysis.xlsx）とグラフ画像\n分析項目: 月次売上、商品別売上、取引先別売上、成長率\n\nコピペ用プロンプト:\nPythonで売上データ自動分析のコードを作成してください。pandasとmatplotlibライブラリを使ってCSVファイルの売上データを読み込み、月次・商品別・取引先別の分析を行って売上傾向と成長率を計算するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 35,
        "category": "ファイル管理",
        "number": "35/100",
        "title": "ファイル自動分類",
        "desc": "ファイルを拡張子別に自動分類・整理",
        "how_to": "指定フォルダ内のファイルを拡張子別に自動分類し、整理します。",
        "sample_code": "import os\nimport shutil\n\n# --- ユーザーが変更する箇所 ---\n# 分類したいファイルがあるフォルダのパス\ninput_folder = 'dummy_data'\n# 分類先のベースフォルダパス\noutput_base_folder = 'dummy_data/classified_files'\n# ------------------------------\n\n# 分類ルールを定義\nclassification_rules = {\n    '.pdf': 'pdfs',\n    '.jpg': 'images',\n    '.jpeg': 'images',\n    '.png': 'images',\n    '.txt': 'documents',\n    '.xlsx': 'documents',\n    '.docx': 'documents',\n    '.mp4': 'videos',\n    '.mp3': 'audios',\n}\n\ntry:\n    if not os.path.exists(input_folder):\n        print(f\"エラー: 入力フォルダ '{input_folder}' が見つかりません。\")\n    else:\n        print(f\"フォルダ '{input_folder}' 内のファイルを分類中...\")\n        os.makedirs(output_base_folder, exist_ok=True)\n        for filename in os.listdir(input_folder):\n            file_path = os.path.join(input_folder, filename)\n            if os.path.isfile(file_path):\n                file_extension = os.path.splitext(filename)[1].lower()\n                destination_folder_name = classification_rules.get(file_extension, 'others')\n                destination_path = os.path.join(output_base_folder, destination_folder_name)\n                os.makedirs(destination_path, exist_ok=True)\n                shutil.move(file_path, os.path.join(destination_path, filename))\n                print(f'{filename} → {destination_folder_name}/')\n        print('分類完了！')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "os、shutil",
        "explanation": "ファイルを自動で分類。探しやすく、整理も楽に。",
        "benefits": ["整理が楽", "探しやすい", "自動化"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonでファイル自動分類のコードを作成してください。以下の条件でお願いします：\n\n1. osとshutilライブラリを使う\n2. 指定したフォルダ内のファイルを拡張子別に分類する\n3. 画像、文書、動画、音楽の4つのカテゴリに分ける\n4. 各カテゴリ用のフォルダを自動作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: 指定したフォルダパス\n分類基準: ファイル拡張子（.jpg、.pdf、.mp4、.mp3など）\n出力形式: 分類されたフォルダ構造\n\nコピペ用プロンプト:\nPythonでファイル自動分類のコードを作成してください。osとshutilライブラリを使って指定したフォルダ内のファイルを拡張子別に分類し、画像、文書、動画、音楽の4つのカテゴリに分けて各カテゴリ用のフォルダを自動作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 36,
        "category": "文書作成・管理",
        "number": "36/100",
        "title": "レポート自動生成",
        "desc": "データからレポートを自動生成・PDF化",
        "how_to": "CSVデータから月次レポートを自動生成し、PDF化します。",
        "sample_code": "import pandas as pd\nfrom reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom reportlab.pdfbase import pdfmetrics\nfrom reportlab.pdfbase.ttfonts import TTFont\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 入力CSVファイルのパス\ninput_csv_path = 'dummy_data/sales.csv'\n# 出力PDFレポートのパス\noutput_pdf_path = 'dummy_data/monthly_report.pdf'\n# レポートのタイトル\nreport_title = '月次売上レポート'\n# レポートの期間\nreport_period = '2024年7月'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if '売上' not in df.columns:\n            print(\"エラー: CSVに '売上' 列がありません。\")\n        else:\n            total_sales = df['売上'].sum()\n            pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))\n            c = canvas.Canvas(output_pdf_path, pagesize=A4)\n            c.setFont('IPAexGothic', 24)\n            c.drawString(50, 750, report_title)\n            c.setFont('IPAexGothic', 14)\n            c.drawString(50, 720, f'期間: {report_period}')\n            c.drawString(50, 680, f'総売上: {total_sales:,}円')\n            c.save()\n            print(f'レポート作成完了！出力ファイル: {output_pdf_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas、reportlab",
        "explanation": "レポートを自動で生成。手作業不要で、毎月の報告も楽に。",
        "benefits": ["手作業不要", "PDF化", "時短"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでレポート自動生成のコードを作成してください。以下の条件でお願いします：\n\n1. pandasとreportlabライブラリを使う\n2. CSVファイルのデータを読み込む\n3. 月次レポートの基本情報を設定する\n4. 売上、利益、顧客数の集計を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（日付、売上、利益、顧客数）\n出力形式: PDFファイル（monthly_report.pdf）\nレポート項目: 月次売上、利益、顧客数、成長率\n\nコピペ用プロンプト:\nPythonでレポート自動生成のコードを作成してください。pandasとreportlabライブラリを使ってCSVファイルのデータを読み込み、月次レポートの基本情報を設定して売上、利益、顧客数の集計を行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 37,
        "category": "データ処理・分析",
        "number": "37/100",
        "title": "顧客データ自動分析",
        "desc": "顧客データを自動で分析・セグメント化",
        "how_to": "CSV顧客データを自動で分析し、顧客セグメントを作成します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 顧客データCSVファイルのパス\ninput_csv_path = 'dummy_data/customers.csv'\n# 分析結果を出力するExcelファイルのパス\noutput_excel_path = 'dummy_data/customer_analysis.xlsx'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        required_columns = ['customer_id', 'purchase_date', 'price']\n        if not all(col in df.columns for col in required_columns):\n            print(f\"エラー: CSVに必須列 {required_columns} がありません。\")\n        else:\n            df['purchase_date'] = pd.to_datetime(df['purchase_date'])\n            customer_summary = df.groupby('customer_id').agg(\n                purchase_frequency=('purchase_date', 'count'),\n                total_purchase_amount=('price', 'sum'),\n                last_purchase_date=('purchase_date', 'max')\n            ).reset_index()\n\n            def classify_customer(row):\n                if row['purchase_frequency'] >= 5 and row['total_purchase_amount'] >= 50000:\n                    return 'VIP'\n                elif row['purchase_frequency'] >= 2:\n                    return '一般'\n                else:\n                    return '新規/休眠'\n            \n            customer_summary['顧客セグメント'] = customer_summary.apply(classify_customer, axis=1)\n            customer_summary.to_excel(output_excel_path, index=False)\n            print(f'顧客分析完了！出力ファイル: {output_excel_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "顧客データを自動で分析。セグメント化で営業戦略に活用。",
        "benefits": ["分析が楽", "セグメント化", "営業戦略に活用"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで顧客データ自動分析のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルの顧客データを読み込む\n3. 購入頻度、購入金額、最終購入日を分析する\n4. 顧客をセグメント（VIP、一般、休眠）に分類する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（顧客ID、購入日、購入金額、商品名）\n出力形式: Excelファイル（customer_segments.xlsx）\n分析項目: 購入頻度、購入金額、最終購入日、顧客セグメント\n\nコピペ用プロンプト:\nPythonで顧客データ自動分析のコードを作成してください。pandasライブラリを使ってCSVファイルの顧客データを読み込み、購入頻度、購入金額、最終購入日を分析して顧客をセグメント（VIP、一般、休眠）に分類するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 38,
        "category": "スタッフ管理",
        "number": "38/100",
        "title": "社員スキル管理",
        "desc": "社員のスキル情報を自動で管理・Excel化",
        "how_to": "CSVや手入力データから社員スキル情報を自動でExcel化します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# スキルデータが記載されたCSVファイルのパス\ninput_csv_path = 'dummy_data/skills.csv'\n# 出力するExcelファイルのパス\noutput_excel_path = 'dummy_data/employee_skills.xlsx'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        required_columns = ['氏名', 'スキル', 'レベル']\n        if not all(col in df.columns for col in required_columns):\n            print(f\"エラー: CSVに必須列 {required_columns} がありません。\")\n        else:\n            skill_summary = df.groupby(['スキル', 'レベル']).size().unstack(fill_value=0)\n            with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:\n                df.to_excel(writer, sheet_name='社員スキル一覧', index=False)\n                skill_summary.to_excel(writer, sheet_name='スキル別集計')\n            print(f'スキル管理完了！出力ファイル: {output_excel_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "社員スキルを自動で管理。人材配置や研修計画に活用。",
        "benefits": ["人材配置が楽", "Excel化", "研修計画に活用"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonで社員スキル管理のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. 社員のスキル情報を管理する\n3. スキル名、レベル、取得日を記録する\n4. スキル別・レベル別の集計を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n管理項目: 氏名、スキル名、レベル、取得日\n出力形式: Excelファイル（employee_skills.xlsx）\n機能: スキル追加、レベル更新、集計レポート\n\nコピペ用プロンプト:\nPythonで社員スキル管理のコードを作成してください。pandasライブラリを使って社員のスキル情報（氏名、スキル名、レベル、取得日）を管理し、スキル別・レベル別の集計を行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 39,
        "category": "在庫管理",
        "number": "39/100",
        "title": "在庫アラート自動通知",
        "desc": "在庫不足時に自動でアラート通知",
        "how_to": "在庫データをチェックし、不足時に自動でメール通知します。",
        "sample_code": "import pandas as pd\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom email.header import Header\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 在庫データCSVファイルのパス\ninput_csv_path = 'dummy_data/inventory.csv'\n# 在庫アラートの閾値\nlow_stock_threshold = 10\n\n# --- メール設定 (実際に送信するにはご自身の情報を設定) ---\n# SMTPサーバー情報 (例: Gmailなら 'smtp.gmail.com')\nSMTP_SERVER = 'smtp.example.com'\n# SMTPポート (例: Gmailなら 587)\nSMTP_PORT = 587\n# 送信元メールアドレス\nSENDER_EMAIL = 'dummy_sender@example.com'\n# 送信元メールアドレスのパスワード (Gmailの場合はアプリパスワード)\nSENDER_PASSWORD = 'dummy_password'\n# 送信先メールアドレス\nRECIPIENT_EMAIL = 'dummy_recipient@example.com'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if '商品名' not in df.columns or '在庫数' not in df.columns:\n            print(\"エラー: CSVに '商品名' または '在庫数' 列がありません。\")\n        else:\n            low_stock_items = df[df['在庫数'] < low_stock_threshold]\n            if not low_stock_items.empty:\n                alert_message = '以下の商品が在庫不足です:\n\n'\n                for index, row in low_stock_items.iterrows():\n                    alert_message += f\"- {row['商品名']}: 現在在庫数 {row['在庫数']}\n\"\n                print('在庫不足商品があります！メールを送信します...\n')\n                print(alert_message)\n                # --- メール送信処理 (ダミー設定では送信されません) ---\n                try:\n                    msg = MIMEText(alert_message, 'plain', 'utf-8')\n                    msg['Subject'] = Header('在庫不足アラート', 'utf-8')\n                    msg['From'] = SENDER_EMAIL\n                    msg['To'] = RECIPIENT_EMAIL\n\n                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)\n                    server.starttls()\n                    server.login(SENDER_EMAIL, SENDER_PASSWORD)\n                    server.send_message(msg)\n                    server.quit()\n                    print(f\"メールを {RECIPIENT_EMAIL} に送信しました。\")\n                except Exception as mail_e:\n                    print(f\"メール送信エラー: {mail_e}\")\n                    print(\"メール設定が正しくないため、メールは送信されませんでした。コンソールに出力します。\")\n            else:\n                print(\"在庫が十分です。アラートはありません。\")\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas、smtplib",
        "explanation": "在庫不足を自動で検知。発注漏れを防止。",
        "benefits": ["発注漏れ防止", "自動化", "在庫管理が楽"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで在庫アラート自動通知のコードを作成してください。以下の条件でお願いします：\n\n1. pandasとsmtplibライブラリを使う\n2. CSVファイルの在庫データを読み込む\n3. 在庫数が閾値以下の商品を検出する\n4. 在庫不足商品のリストをメールで通知する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（商品名、在庫数、最小在庫数）\n通知方法: メール送信\nアラート条件: 在庫数 < 最小在庫数\n\nコピペ用プロンプト:\nPythonで在庫アラート自動通知のコードを作成してください。pandasとsmtplibライブラリを使ってCSVファイルの在庫データを読み込み、在庫数が閾値以下の商品を検出して在庫不足商品のリストをメールで通知するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 40,
        "category": "データ処理・分析",
        "number": "40/100",
        "title": "データ自動クレンジング",
        "desc": "データの欠損値・重複を自動で処理",
        "how_to": "CSVデータの欠損値や重複を自動で検出・処理します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 入力CSVファイルのパス\ninput_csv_path = 'dummy_data/data.csv'\n# 出力するクレンジング済みCSVファイルのパス\noutput_csv_path = 'dummy_data/cleaned_data.csv'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        print(f'元のデータ件数: {len(df)}')\n        # 欠損値の処理\n        df_cleaned = df.dropna()\n        print(f'欠損値処理後の件数: {len(df_cleaned)}')\n        # 重複行の削除\n        df_cleaned = df_cleaned.drop_duplicates()\n        print(f'重複削除後の件数: {len(df_cleaned)}')\n        df_cleaned.to_csv(output_csv_path, index=False, encoding='utf-8')\n        print(f'\nクレンジング完了！出力ファイル: {output_csv_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "データを自動でクレンジング。分析の精度向上。",
        "benefits": ["データ品質向上", "分析精度向上", "自動化"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでデータ自動クレンジングのコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルのデータを読み込む\n3. 欠損値の検出と処理を行う\n4. 重複データの削除を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（生データ）\n出力形式: CSVファイル（cleaned_data.csv）\n処理項目: 欠損値処理、重複削除、データ型変換\n\nコピペ用プロンプト:\nPythonでデータ自動クレンジングのコードを作成してください。pandasライブラリを使ってCSVファイルのデータを読み込み、欠損値の検出と処理を行って重複データを削除するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 41,
        "category": "文書作成・管理",
        "number": "41/100",
        "title": "契約書自動生成",
        "desc": "契約書のテンプレートを自動生成・PDF化",
        "how_to": "契約内容を入力するだけで契約書を自動生成しPDF化します。",
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom reportlab.pdfbase import pdfmetrics\nfrom reportlab.pdfbase.ttfonts import TTFont\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 出力するPDF契約書ファイルのパス\noutput_pdf_path = 'dummy_data/contract.pdf'\n# 契約書の情報\ncontract_info = {\n    'title': '業務委託契約書',\n    'contractor': '株式会社サンプル',\n    'contractee': '株式会社ダミー',\n    'content': 'システム開発業務一式',\n    'amount': 1000000,  # 円\n    'period': '2024年8月1日 〜 2025年7月31日',\n    'date': '2024年7月17日'\n}\n# ------------------------------\n\ntry:\n    pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))\n    c = canvas.Canvas(output_pdf_path, pagesize=A4)\n    c.setFont('IPAexGothic', 24)\n    c.drawCentredString(A4[0]/2, 750, contract_info['title'])\n    c.setFont('IPAexGothic', 12)\n    c.drawString(400, 720, f\"作成日: {contract_info['date']}\")\n    c.setFont('IPAexGothic', 14)\n    c.drawString(50, 680, f\"甲: {contract_info['contractor']}\")\n    c.drawString(50, 660, f\"乙: {contract_info['contractee']}\")\n    c.setFont('IPAexGothic', 12)\n    c.drawString(50, 620, '以下の通り契約を締結する。')\n    c.drawString(70, 600, f\"1. 契約内容: {contract_info['content']}\")\n    c.drawString(70, 580, f\"2. 契約金額: {contract_info['amount']:,}円 (税抜)\")\n    c.drawString(70, 560, f\"3. 契約期間: {contract_info['period']}\")\n    c.drawString(50, 400, '上記契約内容に同意し、本書を締結する。')\n    c.drawString(50, 350, f\"甲: {contract_info['contractor']}\")\n    c.drawString(50, 330, '署名: ____________________')\n    c.drawString(50, 280, f\"乙: {contract_info['contractee']}\")\n    c.drawString(50, 260, '署名: ____________________')\n    c.save()\n    print(f'契約書を作成し、{output_pdf_path} に保存しました。')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "reportlab",
        "explanation": "契約書を自動で生成。手書き・転記不要。",
        "benefits": ["手書き不要", "PDF化", "時短"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonで契約書自動生成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. 契約書の基本情報を設定する\n3. 契約者、契約内容、金額を入力する\n4. 見やすい契約書形式にフォーマットする\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力情報: 契約者名、契約内容、金額、契約期間\n出力形式: PDFファイル（contract.pdf）\n契約書項目: 契約者、契約内容、金額、期間、署名欄\n\nコピペ用プロンプト:\nPythonで契約書自動生成のコードを作成してください。reportlabライブラリを使って契約書の基本情報（契約者名、契約内容、金額、契約期間）を設定し、見やすい契約書形式にフォーマットするコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 42,
        "category": "顧客管理",
        "number": "42/100",
        "title": "顧客フォローアップ自動化",
        "desc": "顧客フォローアップを自動でスケジュール・通知",
        "how_to": "顧客データからフォローアップ予定を自動でスケジュールし、通知します。",
        "sample_code": "import pandas as pd\nfrom datetime import datetime, timedelta\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 顧客データCSVファイルのパス\ninput_csv_path = 'dummy_data/customers.csv'\n# 出力するExcelファイルのパス\noutput_excel_path = 'dummy_data/followup_schedule.xlsx'\n# 次回連絡までの日数\ndays_until_next_contact = 30\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if 'last_contact_date' not in df.columns:\n            print(\"エラー: CSVに 'last_contact_date' 列がありません。\")\n        else:\n            df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])\n            df['next_contact_date'] = df['last_contact_date'] + timedelta(days=days_until_next_contact)\n            df.to_excel(output_excel_path, index=False)\n            print(f'フォローアップ予定作成完了！出力ファイル: {output_excel_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas、datetime",
        "explanation": "顧客フォローアップを自動化。営業機会の逃しを防止。",
        "benefits": ["営業機会確保", "自動化", "顧客満足度向上"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで顧客フォローアップ自動化のコードを作成してください。以下の条件でお願いします：\n\n1. pandasとdatetimeライブラリを使う\n2. CSVファイルの顧客データを読み込む\n3. 最終連絡日から次回フォローアップ日を計算する\n4. フォローアップ予定表をExcelで作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（顧客名、最終連絡日、重要度）\n出力形式: Excelファイル（followup_schedule.xlsx）\n機能: 次回連絡日計算、優先度設定、スケジュール管理\n\nコピペ用プロンプト:\nPythonで顧客フォローアップ自動化のコードを作成してください。pandasとdatetimeライブラリを使ってCSVファイルの顧客データを読み込み、最終連絡日から次回フォローアップ日を計算してフォローアップ予定表をExcelで作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 43,
        "category": "スタッフ管理",
        "number": "43/100",
        "title": "社員評価自動集計",
        "desc": "社員評価データを自動で集計・レポート化",
        "how_to": "CSV評価データを自動で集計し、社員別評価レポートを作成します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 評価データCSVファイルのパス\ninput_csv_path = 'dummy_data/evaluations.csv'\n# 出力するExcelファイルのパス\noutput_excel_path = 'dummy_data/evaluation_report.xlsx'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if '社員名' not in df.columns or '評価点' not in df.columns:\n            print(\"エラー: CSVに '社員名' または '評価点' 列がありません。\")\n        else:\n            results = df.groupby('社員名')['評価点'].mean().reset_index()\n            results.rename(columns={'評価点': '平均評価点'}, inplace=True)\n            results.to_excel(output_excel_path, index=False)\n            print(f'評価集計完了！出力ファイル: {output_excel_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "社員評価を自動で集計。人事評価も楽に。",
        "benefits": ["評価が楽", "Excel化", "人事評価に活用"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで社員評価自動集計のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルの評価データを読み込む\n3. 社員別・項目別の評価を集計する\n4. 評価レポートをExcelで作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（社員名、評価項目、評価点、評価者）\n出力形式: Excelファイル（evaluation_report.xlsx）\n集計項目: 社員別平均点、項目別評価、評価者別集計\n\nコピペ用プロンプト:\nPythonで社員評価自動集計のコードを作成してください。pandasライブラリを使ってCSVファイルの評価データを読み込み、社員別・項目別の評価を集計して評価レポートをExcelで作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 44,
        "category": "データ処理・分析",
        "number": "44/100",
        "title": "売上予測自動分析",
        "desc": "過去データから売上を自動で予測・分析",
        "how_to": "過去の売上データから将来の売上を自動で予測します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 過去の売上履歴CSVファイルのパス\ninput_csv_path = 'dummy_data/sales_history.csv'\n# 予測結果を出力するExcelファイルのパス\noutput_excel_path = 'dummy_data/sales_prediction.xlsx'\n# 予測に使用する移動平均の期間\nmoving_average_window = 3\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if '売上' not in df.columns:\n            print(\"エラー: CSVに '売上' 列がありません。\")\n        else:\n            df['予測売上'] = df['売上'].rolling(window=moving_average_window).mean().shift(1)\n            df.to_excel(output_excel_path, index=False)\n            print(f'売上予測分析完了！出力ファイル: {output_excel_path}')\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas、numpy",
        "explanation": "売上を自動で予測。経営計画や予算策定に活用。",
        "benefits": ["予測が楽", "経営計画に活用", "予算策定に活用"],
        "time_required": "1時間〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで売上予測自動分析のコードを作成してください。以下の条件でお願いします：\n\n1. pandasとnumpyライブラリを使う\n2. CSVファイルの過去売上データを読み込む\n3. 時系列分析で売上傾向を分析する\n4. 移動平均や季節性を考慮した予測を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（日付、売上金額）\n出力形式: Excelファイル（sales_forecast.xlsx）\n予測項目: 月次売上予測、成長率予測、信頼区間\n\nコピペ用プロンプト:\nPythonで売上予測自動分析のコードを作成してください。pandasとnumpyライブラリを使ってCSVファイルの過去売上データを読み込み、時系列分析で売上傾向を分析して移動平均や季節性を考慮した予測を行うコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 45,
        "category": "文書作成・管理",
        "number": "45/100",
        "title": "プレゼン資料自動生成",
        "desc": "データからプレゼン資料を自動生成・PDF化",
        "how_to": "CSVデータからプレゼン資料を自動生成し、PDF化します。",
        "sample_code": "print('この機能は現在開発中です。')",
        "libraries": "reportlab",
        "explanation": "プレゼン資料を自動で生成。会議準備も楽に。",
        "benefits": ["資料作成が楽", "PDF化", "時短"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでプレゼン資料自動生成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. CSVファイルのデータを読み込む\n3. プレゼン資料の基本構成を設定する\n4. グラフや表を含むスライドを作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（売上データ、顧客データ）\n出力形式: PDFファイル（presentation.pdf）\n資料項目: タイトル、概要、データ分析、グラフ、結論\n\nコピペ用プロンプト:\nPythonでプレゼン資料自動生成のコードを作成してください。reportlabライブラリを使ってCSVファイルのデータを読み込み、プレゼン資料の基本構成を設定してグラフや表を含むスライドを作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 46,
        "category": "データ処理・分析",
        "number": "46/100",
        "title": "競合分析自動化",
        "desc": "競合情報を自動で収集・分析",
        "how_to": "Webスクレイピングで競合情報を自動収集し、分析します。",
        "sample_code": "print('現在この機能はメンテナンス中です。')",
        "libraries": "requests、BeautifulSoup",
        "explanation": "競合情報を自動で収集。市場分析も楽に。",
        "benefits": ["情報収集が楽", "自動化", "市場分析に活用"],
        "time_required": "1時間〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで競合分析自動化のコードを作成してください。以下の条件でお願いします：\n\n1. requestsとBeautifulSoupライブラリを使う\n2. 指定した競合サイトの情報を収集する\n3. 商品情報、価格、特徴を抽出する\n4. 競合分析レポートをExcelで作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象サイト: 競合企業のWebサイト\n出力形式: Excelファイル（competitor_analysis.xlsx）\n分析項目: 商品情報、価格、特徴、強み・弱み\n\nコピペ用プロンプト:\nPythonで競合分析自動化のコードを作成してください。requestsとBeautifulSoupライブラリを使って指定した競合サイトの情報を収集し、商品情報、価格、特徴を抽出して競合分析レポートをExcelで作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 47,
        "category": "スタッフ管理",
        "number": "47/100",
        "title": "社員研修計画自動化",
        "desc": "社員のスキルに基づいて研修計画を自動生成",
        "how_to": "社員のスキルデータから研修計画を自動で生成します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 社員スキル情報が記載されたCSVファイルのパス\nskills_csv_path = 'dummy_data/skills.csv'\n# 社員情報が記載されたCSVファイルのパス\nemployees_csv_path = 'dummy_data/employees.csv'\n# 出力する研修計画のExcelファイルパス\noutput_excel_path = 'dummy_data/training_plan.xlsx'\n# 研修が必要だと判断するスキルレベル (例: ['初級', '中級'])\nrequired_training_levels = ['初級']\n# ------------------------------\n\ntry:\n    # CSVファイルの読み込み\n    if not os.path.exists(skills_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {skills_csv_path}\")\n    elif not os.path.exists(employees_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {employees_csv_path}\")\n    else:\n        skills_df = pd.read_csv(skills_csv_path)\n        employees_df = pd.read_csv(employees_csv_path)\n\n        # 研修が必要な社員を抽出\n        training_needed_df = skills_df[skills_df['レベル'].isin(required_training_levels)]\n\n        # 社員情報と結合\n        merged_df = pd.merge(training_needed_df, employees_df, on='氏名', how='left')\n\n        # 必要な列だけを選択して研修計画を作成\n        training_plan_df = merged_df[['氏名', '部署', 'スキル', 'レベル']]\n\n        # Excelファイルとして出力\n        training_plan_df.to_excel(output_excel_path, index=False)\n        print(f\"研修計画を作成し、{output_excel_path} に保存しました。\")\n\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "研修計画を自動で生成。人材育成も効率的に。",
        "benefits": ["人材育成が楽", "Excel化", "効率的"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで社員研修計画自動化のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルの社員スキルデータを読み込む\n3. スキルレベルが低い項目を特定する\n4. 研修優先度とスケジュールを設定する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（社員名、スキル名、スキルレベル）\n出力形式: Excelファイル（training_plan.xlsx）\n計画項目: 研修科目、対象者、優先度、スケジュール\n\nコピペ用プロンプト:\nPythonで社員研修計画自動化のコードを作成してください。pandasライブラリを使ってCSVファイルの社員スキルデータを読み込み、スキルレベルが低い項目を特定して研修優先度とスケジュールを設定するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 48,
        "category": "スタッフ管理",
        "number": "48/100",
        "title": "社員名簿自動作成",
        "desc": "社員情報を自動で名簿化・Excel保存",
        "how_to": "CSVや手入力データから社員名簿を自動でExcel化します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 社員情報が記載されたCSVファイルのパス\ninput_csv_path = 'dummy_data/employees.csv'\n# 出力する名簿のExcelファイルパス\noutput_excel_path = 'dummy_data/employee_list.xlsx'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        employee_list_df = df[['氏名', '部署', '役職', 'メールアドレス', '電話番号']]\n        employee_list_df.to_excel(output_excel_path, index=False)\n        print(f\"社員名簿を作成し、{output_excel_path} に保存しました。\")\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "社員名簿を自動で作成。管理・配布が簡単に。",
        "benefits": ["手入力不要", "Excel化", "管理が楽"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonで社員名簿自動作成のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. 社員情報（氏名、部署、入社日、メールアドレス）を管理する\n3. 新しい社員を追加する機能を含める\n4. 社員情報をExcelファイルに保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n管理項目: 氏名、部署、入社日、メールアドレス\n出力形式: Excelファイル（employee_list.xlsx）\n機能: 社員追加、一覧表示、Excel保存\n\nコピペ用プロンプト:\nPythonで社員名簿自動作成のコードを作成してください。pandasライブラリを使って社員情報（氏名、部署、入社日、メールアドレス）を管理し、新しい社員を追加する機能を含めてExcelファイルに保存するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 49,
        "category": "スタッフ管理",
        "number": "49/100",
        "title": "勤怠打刻データ自動集計",
        "desc": "勤怠打刻データを自動で集計・レポート化",
        "how_to": "CSV勤怠データを自動で集計し、月次レポートを作成します。",
        "sample_code": "import pandas as pd\nimport os\n\n# --- ユーザーが変更する箇所 ---\n# 勤怠データが記載されたCSVファイルのパス\ninput_csv_path = 'dummy_data/kintai.csv'\n# 出力する勤怠レポートのCSVファイルパス\noutput_csv_path = 'dummy_data/kintai_report.csv'\n# ------------------------------\n\ntry:\n    if not os.path.exists(input_csv_path):\n        print(f\"エラー: ファイルが見つかりません: {input_csv_path}\")\n    else:\n        df = pd.read_csv(input_csv_path)\n        if '氏名' not in df.columns or '勤務時間' not in df.columns:\n            print(\"エラー: CSVに '氏名' または '勤務時間' 列がありません。\")\n        else:\n            report = df.groupby('氏名')['勤務時間'].sum().reset_index()\n            report.to_csv(output_csv_path, index=False)\n            print(f\"勤怠レポートを作成し、{output_csv_path} に保存しました。\")\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "pandas",
        "explanation": "勤怠集計を自動化。月次レポートも一発で。",
        "benefits": ["集計ミス防止", "時短", "自動化"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで勤怠打刻データ自動集計のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルの勤怠打刻データを読み込む\n3. 社員別・日別の勤務時間を計算する\n4. 月次レポート（総勤務時間、残業時間、遅刻回数）を作成する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力ファイル: CSVファイル（社員ID、日付、出勤時刻、退勤時刻）\n出力形式: Excelファイル（monthly_report.xlsx）\n集計項目: 総勤務時間、残業時間、遅刻回数\n\nコピペ用プロンプト:\nPythonで勤怠打刻データ自動集計のコードを作成してください。pandasライブラリを使ってCSVファイルの勤怠打刻データを読み込み、社員別・日別の勤務時間を計算して月次レポート（総勤務時間、残業時間、遅刻回数）を作成するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 50,
        "category": "文書作成・管理",
        "number": "50/100",
        "title": "会議議事録自動フォーマット",
        "desc": "議事録を自動でフォーマット・保存",
        "how_to": "議事録テキストを自動でフォーマットし、ファイル保存します。",
        "sample_code": "import os\n\n# --- ユーザーが変更する箇所 ---\n# 議事録のタイトル\ntitle = '営業定例会議'\n# 開催日\ndate = '2024年7月17日'\n# 参加者 (カンマ区切りで入力)\nparticipants = '山田太郎, 佐藤花子, 鈴木一郎'\n# 議事内容 (箇条書きで入力)\ncontent = '''\n・今月の売上報告\n・来月の目標設定について\n・新規プロジェクトの進捗確認\n'''\n# 出力するテキストファイル名\noutput_file = 'dummy_data/minutes.txt'\n# ------------------------------\n\ntry:\n    minutes = f\"【議事録】 {title}\n\"\n    minutes += f\"----------------------------------------\n\"\n    minutes += f\"開催日時: {date}\n\"\n    minutes += f\"参加者: {participants}\n\"\n    minutes += f\"----------------------------------------\n\n\"\n    minutes += f\"■ 議題\n\"\n    minutes += f\"{content}\n\"\n    with open(output_file, 'w', encoding='utf-8') as f:\n        f.write(minutes)\n    print(f\"議事録を作成し、{output_file} に保存しました。\")\nexcept Exception as e:\n    print(f\"エラーが発生しました: {e}\")",
        "libraries": "標準ライブラリのみ",
        "explanation": "議事録を自動でフォーマット。誰でもきれいな議事録が作れる。",
        "benefits": ["フォーマット統一", "時短", "誰でも使える"],
        "time_required": "10分〜30分",
        "difficulty": "初級",
        "ai_prompt": "Pythonで会議議事録自動フォーマットのコードを作成してください。以下の条件でお願いします：\n\n1. 標準ライブラリ（datetime、os）を使う\n2. 議事録の基本情報（会議名、日時、参加者、議題）を設定する\n3. 議事内容を自動でフォーマットする\n4. 決定事項とアクションアイテムを整理する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n入力情報: 会議名、日時、参加者、議題、議事内容\n出力形式: テキストファイル（minutes_YYYYMMDD.txt）\nフォーマット: 見やすい議事録形式\n\nコピペ用プロンプト:\nPythonで会議議事録自動フォーマットのコードを作成してください。標準ライブラリ（datetime、os）を使って議事録の基本情報（会議名、日時、参加者、議題）を設定し、議事内容を自動でフォーマットして決定事項とアクションアイテムを整理するコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    }
]
