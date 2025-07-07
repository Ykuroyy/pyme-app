from flask import Flask, render_template
import os

app = Flask(__name__)

# 自動化ツールリスト（シンプル版）
TOOLS = [
    {
        "id": 1, 
        "title": "メール自動送信", 
        "desc": "Pythonでメールを自動送信する方法",
        "how_to": "smtplibライブラリを使ってメールサーバーに接続し、メールを送信します。",
        "sample_code": "import smtplib\nfrom email.mime.text import MIMEText\n\n# メール設定\nsender_email = 'your_email@gmail.com'\nsender_password = 'your_password'\nreceiver_email = 'receiver@example.com'\n\n# メール作成\nmsg = MIMEText('これは自動送信されたメールです。')\nmsg['Subject'] = '自動送信メール'\nmsg['From'] = sender_email\nmsg['To'] = receiver_email\n\n# 送信\nserver = smtplib.SMTP('smtp.gmail.com', 587)\nserver.starttls()\nserver.login(sender_email, sender_password)\nserver.send_message(msg)\nserver.quit()\nprint('メール送信完了！')",
        "libraries": "smtplib（標準ライブラリ）、email（標準ライブラリ）",
        "explanation": "Pythonの標準ライブラリを使って、簡単にメールの自動送信ができます。定期レポートの送信や通知メールの送信に便利です。",
        "benefits": ["時間を節約できる", "ミスを減らせる", "一括送信が可能"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでメール自動送信のコードを作成してください。以下の条件でお願いします：\n\n1. smtplibライブラリを使う\n2. GmailのSMTPサーバーを使用する\n3. 件名、本文、送信者、受信者を設定する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n送信者: 自分のGmailアドレス\n受信者: 指定したメールアドレス\n件名: 自動送信メール\n本文: 簡単なメッセージ"
    },
    {
        "id": 2, 
        "title": "Excel自動処理", 
        "desc": "Excelファイルを自動で編集・集計",
        "how_to": "openpyxlライブラリを使ってExcelファイルを読み込み、データを編集・集計します。",
        "sample_code": "from openpyxl import load_workbook\nimport pandas as pd\n\n# Excelファイル読み込み\nwb = load_workbook('data.xlsx')\nws = wb.active\n\n# データの読み込み\ndata = []\nfor row in ws.iter_rows(min_row=2, values_only=True):\n    data.append(row)\n\n# pandasでデータ分析\ndf = pd.DataFrame(data, columns=['名前', '売上', '日付'])\ntotal_sales = df['売上'].sum()\n\n# 結果を新しいセルに書き込み\nws['D1'] = '合計売上'\nws['D2'] = total_sales\n\n# ファイル保存\nwb.save('result.xlsx')\nprint(f'合計売上: {total_sales:,}円')",
        "libraries": "openpyxl、pandas",
        "explanation": "Excelファイルの自動処理は、ビジネスで最もよく使われる自動化の一つです。売上データの集計やレポートの自動作成に便利です。",
        "benefits": ["手作業の時間を大幅削減", "計算ミスを防げる", "大量データも瞬時に処理"],
        "time_required": "1〜2時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでExcel自動処理のコードを作成してください。以下の条件でお願いします：\n\n1. openpyxlライブラリを使う\n2. Excelファイルを読み込んでデータを取得する\n3. 売上データを集計する\n4. 結果を新しいセルに書き込む\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: data.xlsx\n集計項目: 売上列の合計\n出力先: 新しいセル（D2など）"
    },
    {
        "id": 3, 
        "title": "PDF自動生成", 
        "desc": "PDFファイルを自動で作成",
        "how_to": "reportlabライブラリを使ってPDFドキュメントを作成し、テキストや表を追加します。",
        "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import letter\n\n# PDF作成\nc = canvas.Canvas('report.pdf', pagesize=letter)\n\n# タイトル\nc.setFont('Helvetica-Bold', 16)\nc.drawString(100, 750, '月次レポート')\n\n# 内容\nc.setFont('Helvetica', 12)\nc.drawString(100, 700, '売上: 1,000,000円')\nc.drawString(100, 680, '利益: 200,000円')\n\nc.save()\nprint('PDF作成完了！')",
        "libraries": "reportlab",
        "explanation": "PythonでPDFファイルを自動生成することで、レポートや請求書の作成を自動化できます。",
        "benefits": ["レポート作成が自動化", "フォーマットが統一される", "大量のPDFも一括作成"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでPDF自動生成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. 月次レポートのPDFを作成する\n3. タイトル、売上、利益を表示する\n4. 見やすいレイアウトにする\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nPDF内容: 月次レポート\n表示項目: 売上、利益\nファイル名: report.pdf"
    },
    {
        "id": 4, 
        "title": "Webスクレイピング", 
        "desc": "Webサイトから自動でデータ取得",
        "how_to": "requestsとBeautifulSoupを使ってWebページから情報を取得し、データを整理します。",
        "sample_code": "import requests\nfrom bs4 import BeautifulSoup\nimport pandas as pd\n\n# Webページを取得\nurl = 'https://example.com'\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.content, 'html.parser')\n\n# 商品情報を抽出\nproducts = []\nfor item in soup.find_all('div', class_='product'):\n    name = item.find('h3').text.strip()\n    price = item.find('span', class_='price').text.strip()\n    products.append({'商品名': name, '価格': price})\n\n# DataFrameに変換して保存\ndf = pd.DataFrame(products)\ndf.to_csv('products.csv', index=False)\nprint(f'{len(products)}件の商品情報を取得しました')",
        "libraries": "requests、beautifulsoup4、pandas",
        "explanation": "Webスクレイピングは、Webサイトから自動で情報を収集する技術です。競合調査やデータ収集に便利です。",
        "benefits": ["手作業の時間を大幅削減", "大量データも瞬時に取得", "定期的な情報収集が自動化"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでWebスクレイピングのコードを作成してください。以下の条件でお願いします：\n\n1. requestsとBeautifulSoupを使う\n2. 指定したWebサイトから商品名と価格を取得する\n3. 取得したデータをCSVファイルに保存する\n4. 初心者でも理解できるようにコメントを詳しく書く\n5. エラーハンドリングも含める\n\n対象サイト: [サイトURLを指定]\n取得したい情報: 商品名、価格、説明文"
    },
    {
        "id": 5, 
        "title": "データ可視化グラフ作成", 
        "desc": "データをグラフで見やすく表示",
        "how_to": "matplotlibやplotlyを使ってデータをグラフ化し、見やすい図表を作成します。",
        "sample_code": "import matplotlib.pyplot as plt\nimport pandas as pd\n\n# サンプルデータ\ndata = {\n    '月': ['1月', '2月', '3月', '4月', '5月', '6月'],\n    '売上': [100, 150, 200, 180, 250, 300]\n}\ndf = pd.DataFrame(data)\n\n# グラフ作成\nplt.figure(figsize=(10, 6))\nplt.plot(df['月'], df['売上'], marker='o', linewidth=2, markersize=8)\nplt.title('月次売上推移', fontsize=16)\nplt.xlabel('月')\nplt.ylabel('売上（万円）')\nplt.grid(True, alpha=0.3)\n\n# グラフ保存\nplt.savefig('sales_chart.png', dpi=300, bbox_inches='tight')\nplt.show()\nprint('グラフを保存しました')",
        "libraries": "matplotlib、pandas、plotly（オプション）",
        "explanation": "データをグラフで可視化することで、数字の意味を直感的に理解できます。プレゼンテーションやレポート作成に便利です。",
        "benefits": ["データの傾向が一目で分かる", "プレゼンが分かりやすくなる", "意思決定がスピードアップ"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでデータ可視化のコードを作成してください。以下の条件でお願いします：\n\n1. matplotlibを使う\n2. 月次売上データを折れ線グラフで表示する\n3. グラフのタイトル、軸ラベル、グリッド線を設定する\n4. グラフを画像ファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nデータ形式: CSVファイル（月、売上の列がある）\nグラフの種類: 折れ線グラフ"
    },
    {
        "id": 6, 
        "title": "ファイル自動整理", 
        "desc": "フォルダ内のファイルを自動で整理",
        "how_to": "osライブラリを使ってフォルダ内のファイルを種類別に自動整理します。",
        "sample_code": "import os\nimport shutil\nfrom pathlib import Path\n\n# 整理対象フォルダ\nfolder_path = 'C:/Users/YourName/Downloads'\n\n# ファイル種類の定義\nfile_types = {\n    '画像': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],\n    '文書': ['.pdf', '.doc', '.docx', '.txt', '.xlsx'],\n    '動画': ['.mp4', '.avi', '.mov', '.wmv'],\n    '音楽': ['.mp3', '.wav', '.flac', '.aac']\n}\n\n# フォルダ作成\nfor folder_name in file_types.keys():\n    new_folder = os.path.join(folder_path, folder_name)\n    if not os.path.exists(new_folder):\n        os.makedirs(new_folder)\n\n# ファイル整理\nfor filename in os.listdir(folder_path):\n    file_path = os.path.join(folder_path, filename)\n    if os.path.isfile(file_path):\n        file_ext = Path(filename).suffix.lower()\n        \n        for folder_name, extensions in file_types.items():\n            if file_ext in extensions:\n                destination = os.path.join(folder_path, folder_name, filename)\n                shutil.move(file_path, destination)\n                print(f'{filename} → {folder_name}フォルダに移動')\n                break\n\nprint('ファイル整理完了！')",
        "libraries": "os、shutil、pathlib（全て標準ライブラリ）",
        "explanation": "ダウンロードフォルダやデスクトップが散らかっていませんか？Pythonで自動整理できます。",
        "benefits": ["作業効率が向上", "ファイルが見つけやすくなる", "ストレスが減る"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonでファイル自動整理のコードを作成してください。以下の条件でお願いします：\n\n1. 指定したフォルダ内のファイルを拡張子別に整理する\n2. 画像、文書、動画、音楽の4つのカテゴリに分類する\n3. 各カテゴリ用のフォルダを自動作成する\n4. ファイルを適切なフォルダに移動する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: ダウンロードフォルダ\n分類カテゴリ: 画像、文書、動画、音楽"
    },
    {
        "id": 7, 
        "title": "チャットボット作成", 
        "desc": "簡単な自動応答チャットボット",
        "how_to": "if文や辞書を使って応答パターンを定義し、ユーザーの入力に応じて自動で返答します。",
        "sample_code": "# 簡単なチャットボット\nresponses = {\n    'こんにちは': 'こんにちは！お疲れ様です。',\n    '天気': '今日は晴れの予定です。',\n    '時間': '現在の時刻をお知らせします。',\n    'ありがとう': 'どういたしまして！',\n    'さようなら': 'お疲れ様でした。またお話ししましょう！'\n}\n\nprint('チャットボット: こんにちは！何かお手伝いできることはありますか？')\n\nwhile True:\n    user_input = input('あなた: ').strip()\n    \n    if user_input.lower() in ['終了', 'さようなら', 'bye']:\n        print('チャットボット: お疲れ様でした！')\n        break\n    \n    # 応答を探す\n    response = responses.get(user_input, 'すみません、その質問にはお答えできません。')\n    print(f'チャットボット: {response}')",
        "libraries": "標準ライブラリのみ使用",
        "explanation": "チャットボットは、よくある質問に自動で答えてくれる便利なツールです。カスタマーサポートや社内FAQに活用できます。",
        "benefits": ["24時間対応可能", "人件費を削減", "応答速度が速い"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで簡単なチャットボットのコードを作成してください。以下の条件でお願いします：\n\n1. 辞書を使って質問と回答のパターンを定義する\n2. ユーザーの入力を受け取って適切な回答を返す\n3. 終了コマンドでプログラムを終了できる\n4. 知らない質問には適切なメッセージを返す\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対応したい質問: 挨拶、天気、時間、感謝の言葉\n終了コマンド: さようなら、終了、bye"
    },
    {
        "id": 8, 
        "title": "画像自動リサイズ", 
        "desc": "画像ファイルを自動でリサイズ",
        "how_to": "PIL（Pillow）ライブラリを使って画像ファイルを一括でリサイズします。",
        "sample_code": "from PIL import Image\nimport os\n\ndef resize_images(folder_path, new_width=800):\n    # 対応する画像形式\n    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']\n    \n    for filename in os.listdir(folder_path):\n        if any(filename.lower().endswith(ext) for ext in image_extensions):\n            file_path = os.path.join(folder_path, filename)\n            \n            # 画像を開く\n            with Image.open(file_path) as img:\n                # アスペクト比を保ってリサイズ\n                ratio = new_width / img.width\n                new_height = int(img.height * ratio)\n                \n                # リサイズ\n                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)\n                \n                # 保存（元ファイル名に_resizedを追加）\n                name, ext = os.path.splitext(filename)\n                new_filename = f'{name}_resized{ext}'\n                new_path = os.path.join(folder_path, new_filename)\n                \n                resized_img.save(new_path, quality=85)\n                print(f'{filename} → {new_filename}')\n\n# 使用例\nresize_images('C:/Users/YourName/Pictures', 800)\nprint('画像リサイズ完了！')",
        "libraries": "Pillow (PIL)、os（標準ライブラリ）",
        "explanation": "大量の画像を一括でリサイズすることで、Webサイトやメールでの送信が楽になります。",
        "benefits": ["大量画像も一括処理", "ファイルサイズを削減", "Web表示が高速化"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "Pythonで画像自動リサイズのコードを作成してください。以下の条件でお願いします：\n\n1. Pillowライブラリを使う\n2. 指定したフォルダ内の画像を一括でリサイズする\n3. アスペクト比を保ってリサイズする\n4. 元ファイルは残して、新しいファイル名で保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: 画像フォルダのパス\nリサイズサイズ: 幅800px（高さは自動調整）\n対応形式: JPG、PNG、GIF、BMP"
    },
    {
        "id": 9, 
        "title": "定期レポート自動送信", 
        "desc": "定期的にレポートを自動送信",
        "how_to": "scheduleライブラリで定期実行を設定し、レポート作成とメール送信を自動化します。",
        "sample_code": "import schedule\nimport time\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom datetime import datetime\n\ndef create_daily_report():\n    today = datetime.now().strftime('%Y年%m月%d日')\n    report = f'''\n    日次レポート - {today}\n    \n    - 本日の売上: 150,000円\n    - 新規顧客数: 5名\n    - 処理件数: 25件\n    \n    Thank you for your work.\n    '''\n    return report\n\ndef send_report():\n    report = create_daily_report()\n    \n    # メール設定\n    sender_email = 'your_email@gmail.com'\n    sender_password = 'your_password'\n    receiver_email = 'boss@company.com'\n    \n    # メール作成\n    msg = MIMEText(report, 'plain')\n    msg['Subject'] = f'日次レポート - {datetime.now().strftime(\"%Y/%m/%d\")}'\n    msg['From'] = sender_email\n    msg['To'] = receiver_email\n    \n    # 送信\n    server = smtplib.SMTP('smtp.gmail.com', 587)\n    server.starttls()\n    server.login(sender_email, sender_password)\n    server.send_message(msg)\n    server.quit()\n    \n    print(f'レポート送信完了: {datetime.now()}')\n\n# 毎日18時に実行\nschedule.every().day.at('18:00').do(send_report)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)  # 1分ごとにチェック",
        "libraries": "schedule、smtplib（標準ライブラリ）、datetime（標準ライブラリ）",
        "explanation": "毎日のルーチンワークを自動化することで、時間を節約し、ミスを防げます。",
        "benefits": ["手作業が不要", "忘れることがない", "時間を大幅節約"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで定期レポート自動送信のコードを作成してください。以下の条件でお願いします：\n\n1. scheduleライブラリで毎日18時に実行する\n2. 日次レポートを作成する（売上、顧客数、処理件数を含む）\n3. 作成したレポートをメールで送信する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n送信時間: 毎日18時\nレポート内容: 売上、新規顧客数、処理件数\n送信先: 上司のメールアドレス"
    },
    {
        "id": 10, 
        "title": "SNS自動投稿", 
        "desc": "Twitterなどに自動で投稿",
        "how_to": "tweepyライブラリを使ってTwitter APIに接続し、定期的に投稿を自動化します。",
        "sample_code": "import tweepy\nimport schedule\nimport time\nfrom datetime import datetime\n\n# Twitter API認証\nconsumer_key = 'your_consumer_key'\nconsumer_secret = 'your_consumer_secret'\naccess_token = 'your_access_token'\naccess_token_secret = 'your_access_token_secret'\n\nauth = tweepy.OAuthHandler(consumer_key, consumer_secret)\nauth.set_access_token(access_token, access_token_secret)\napi = tweepy.API(auth)\n\ndef post_daily_tip():\n    # 毎日のTipsを投稿\n    tips = [\n        '今日のビジネスTips: 朝一番に重要なタスクから始めましょう！',\n        '効率化のコツ: 同じ作業は3回以上やったら自動化を検討してください。',\n        'コミュニケーション: 相手の立場に立って考えることが大切です。',\n        '時間管理: 15分単位でタスクを区切ると集中力が続きます。'\n    ]\n    \n    today = datetime.now().day\ntip = tips[today % len(tips)]\n    \n    try:\n        api.update_status(tip)\n        print(f'投稿完了: {tip}')\n    except Exception as e:\n        print(f'投稿エラー: {e}')\n\n# 毎日9時に投稿\nschedule.every().day.at('09:00').do(post_daily_tip)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
        "libraries": "tweepy、schedule、datetime（標準ライブラリ）",
        "explanation": "SNSの投稿を自動化することで、ブランディングや情報発信を効率化できます。",
        "benefits": ["投稿を忘れることがない", "時間を節約", "一貫したブランディング"],
        "time_required": "1〜2時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでSNS自動投稿のコードを作成してください。以下の条件でお願いします：\n\n1. tweepyライブラリを使ってTwitterに投稿する\n2. 毎日9時にビジネスTipsを自動投稿する\n3. 複数のTipsからランダムに選択する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n投稿時間: 毎日9時\n投稿内容: ビジネスTips（複数パターン）\n投稿先: Twitter"
    },
         {
         "id": 11, 
         "title": "カレンダー自動登録", 
         "desc": "予定を自動でGoogleカレンダーに登録",
         "how_to": "Google Calendar APIを使って予定を自動でカレンダーに登録します。",
         "sample_code": "from google.oauth2.credentials import Credentials\nfrom googleapiclient.discovery import build\nfrom datetime import datetime, timedelta\n\n# Google Calendar API設定\ncreds = Credentials.from_authorized_user_file('token.json', SCOPES)\nservice = build('calendar', 'v3', credentials=creds)\n\n# 予定を作成\nevent = {\n    'summary': '会議',\n    'description': 'プロジェクト会議',\n    'start': {\n        'dateTime': '2024-01-15T10:00:00+09:00',\n        'timeZone': 'Asia/Tokyo',\n    },\n    'end': {\n        'dateTime': '2024-01-15T11:00:00+09:00',\n        'timeZone': 'Asia/Tokyo',\n    }\n}\n\nevent = service.events().insert(calendarId='primary', body=event).execute()\nprint(f'予定を作成しました: {event.get(\"htmlLink\")}')",
         "libraries": "google-auth、google-api-python-client",
         "explanation": "Google Calendar APIを使って予定を自動登録することで、スケジュール管理を効率化できます。",
         "benefits": ["手動入力が不要", "ミスを防げる", "一括登録が可能"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "PythonでGoogleカレンダー自動登録のコードを作成してください。以下の条件でお願いします：\n\n1. Google Calendar APIを使う\n2. 指定した日時に予定を登録する\n3. 予定のタイトル、説明、開始・終了時間を設定する\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n予定内容: 会議\n日時: 指定した日時\nカレンダー: プライマリカレンダー"
     },
     {
         "id": 12, 
         "title": "名刺データ自動整理", 
         "desc": "名刺画像から情報を自動抽出",
         "how_to": "OCR技術を使って名刺画像から文字を認識し、連絡先情報を自動抽出します。",
         "sample_code": "import cv2\nimport pytesseract\nimport re\n\n# 名刺画像を読み込み\ndef extract_business_card(image_path):\n    # 画像を読み込み\n    image = cv2.imread(image_path)\n    \n    # OCRで文字認識\n    text = pytesseract.image_to_string(image, lang='jpn')\n    \n    # 正規表現で情報を抽出\n    name_pattern = r'([\\u4e00-\\u9fa5]{2,4})'  # 日本語の名前\n    phone_pattern = r'(\\d{2,4}-\\d{2,4}-\\d{4})'  # 電話番号\n    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})'  # メールアドレス\n    \n    # 情報を抽出\n    name = re.search(name_pattern, text)\n    phone = re.search(phone_pattern, text)\n    email = re.search(email_pattern, text)\n    \n    return {\n        'name': name.group(1) if name else '',\n        'phone': phone.group(1) if phone else '',\n        'email': email.group(1) if email else ''\n    }\n\n# 使用例\nresult = extract_business_card('business_card.jpg')\nprint(f'名前: {result[\"name\"]}')\nprint(f'電話: {result[\"phone\"]}')\nprint(f'メール: {result[\"email\"]}')",
         "libraries": "opencv-python、pytesseract、re（標準ライブラリ）",
         "explanation": "名刺の画像から自動で連絡先情報を抽出することで、手動入力の手間を大幅に削減できます。",
         "benefits": ["手動入力が不要", "大量処理が可能", "データベース化が簡単"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "Pythonで名刺データ自動整理のコードを作成してください。以下の条件でお願いします：\n\n1. OpenCVとTesseract OCRを使う\n2. 名刺画像から文字を認識する\n3. 名前、電話番号、メールアドレスを抽出する\n4. 正規表現で情報を整理する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: 名刺の画像ファイル\n抽出情報: 名前、電話番号、メールアドレス\n出力形式: 辞書形式"
     },
     {
         "id": 13, 
         "title": "請求書自動作成", 
         "desc": "請求書を自動で作成",
         "how_to": "テンプレートを使って請求書を自動生成し、PDFファイルとして保存します。",
         "sample_code": "from reportlab.pdfgen import canvas\nfrom reportlab.lib.pagesizes import A4\nfrom datetime import datetime\n\ndef create_invoice(client_name, items, total_amount):\n    # PDF作成\n    c = canvas.Canvas('invoice.pdf', pagesize=A4)\n    \n    # ヘッダー\n    c.setFont('Helvetica-Bold', 16)\n    c.drawString(100, 750, '請求書')\n    \n    # 日付\n    c.setFont('Helvetica', 12)\n    c.drawString(100, 720, f'発行日: {datetime.now().strftime(\"%Y年%m月%d日\")}')\n    \n    # 顧客名\n    c.drawString(100, 690, f'顧客名: {client_name}')\n    \n    # 明細\n    y = 650\n    for item in items:\n        c.drawString(100, y, f'{item[\"name\"]} - {item[\"price\"]:,}円')\n        y -= 20\n    \n    # 合計\n    c.setFont('Helvetica-Bold', 14)\n    c.drawString(100, y-20, f'合計: {total_amount:,}円')\n    \n    c.save()\n    print('請求書を作成しました')\n\n# 使用例\nitems = [\n    {'name': 'Webサイト制作', 'price': 100000},\n    {'name': '保守費用', 'price': 20000}\n]\ncreate_invoice('株式会社サンプル', items, 120000)",
         "libraries": "reportlab、datetime（標準ライブラリ）",
         "explanation": "請求書を自動生成することで、経理作業を効率化し、ミスを防げます。",
         "benefits": ["手動作成が不要", "フォーマットが統一", "大量作成が可能"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "Pythonで請求書自動作成のコードを作成してください。以下の条件でお願いします：\n\n1. reportlabライブラリを使う\n2. 顧客名、明細、合計金額を含む請求書を作成する\n3. 見やすいレイアウトにする\n4. PDFファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n請求書内容: 顧客名、明細、合計金額\n出力形式: PDFファイル\nファイル名: invoice.pdf"
     },
     {
         "id": 14, 
         "title": "アンケート自動集計", 
         "desc": "アンケート結果を自動で集計",
         "how_to": "ExcelやCSVファイルのアンケート結果を読み込み、自動で集計・分析します。",
         "sample_code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\n# アンケートデータを読み込み\ndf = pd.read_csv('survey_results.csv')\n\n# 基本統計\nprint('=== 基本統計 ===')\nprint(f'回答者数: {len(df)}人')\nprint(f'平均年齢: {df[\"年齢\"].mean():.1f}歳')\n\n# 性別の集計\nprint('\\n=== 性別集計 ===')\ngender_counts = df['性別'].value_counts()\nprint(gender_counts)\n\n# 満足度の集計\nprint('\\n=== 満足度集計 ===')\nsatisfaction_counts = df['満足度'].value_counts().sort_index()\nprint(satisfaction_counts)\n\n# グラフ作成\nplt.figure(figsize=(10, 6))\nsatisfaction_counts.plot(kind='bar')\nplt.title('満足度分布')\nplt.xlabel('満足度')\nplt.ylabel('回答者数')\nplt.savefig('satisfaction_chart.png')\nplt.show()\n\nprint('集計完了！グラフを保存しました。')",
         "libraries": "pandas、matplotlib",
         "explanation": "アンケート結果を自動集計することで、手作業の時間を大幅に削減し、正確な分析が可能になります。",
         "benefits": ["手作業が不要", "正確な集計", "グラフも自動作成"],
         "time_required": "30分〜1時間",
         "difficulty": "初級",
         "ai_prompt": "Pythonでアンケート自動集計のコードを作成してください。以下の条件でお願いします：\n\n1. pandasライブラリを使う\n2. CSVファイルのアンケート結果を読み込む\n3. 基本統計（回答者数、平均年齢など）を計算する\n4. 性別、満足度などの集計を行う\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: survey_results.csv\n集計項目: 性別、年齢、満足度\n出力: 統計結果とグラフ"
     },
     {
         "id": 15, 
         "title": "音声データ自動文字起こし", 
         "desc": "音声ファイルを自動でテキスト化",
         "how_to": "音声認識APIを使って音声ファイルを自動でテキストに変換します。",
         "sample_code": "import speech_recognition as sr\nimport os\n\ndef transcribe_audio(audio_file_path):\n    # 音声認識エンジンを初期化\n    recognizer = sr.Recognizer()\n    \n    # 音声ファイルを読み込み\n    with sr.AudioFile(audio_file_path) as source:\n        # 音声を録音\n        audio = recognizer.record(source)\n        \n        try:\n            # Google Speech Recognitionで文字起こし\n            text = recognizer.recognize_google(audio, language='ja-JP')\n            return text\n        except sr.UnknownValueError:\n            return '音声を認識できませんでした'\n        except sr.RequestError as e:\n            return f'エラーが発生しました: {e}'\n\n# 使用例\nresult = transcribe_audio('meeting_recording.wav')\nprint('文字起こし結果:')\nprint(result)\n\n# 結果をファイルに保存\nwith open('transcription.txt', 'w', encoding='utf-8') as f:\n    f.write(result)\nprint('文字起こし結果をファイルに保存しました')",
         "libraries": "SpeechRecognition、pyaudio",
         "explanation": "会議の録音やインタビュー音声を自動でテキスト化することで、議事録作成の時間を大幅に短縮できます。",
         "benefits": ["手動入力が不要", "時間を大幅節約", "正確な文字起こし"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "Pythonで音声データ自動文字起こしのコードを作成してください。以下の条件でお願いします：\n\n1. SpeechRecognitionライブラリを使う\n2. 音声ファイル（WAV形式）を読み込む\n3. Google Speech Recognitionで文字起こしする\n4. 日本語に対応する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: 音声ファイル（WAV形式）\n言語: 日本語\n出力: テキストファイル"
     },
     {
         "id": 16, 
         "title": "画像から文字抽出", 
         "desc": "画像内の文字を自動で抽出",
         "how_to": "OCR技術を使って画像内の文字を認識し、テキストとして抽出します。",
         "sample_code": "import pytesseract\nfrom PIL import Image\nimport cv2\nimport numpy as np\n\ndef extract_text_from_image(image_path):\n    # 画像を読み込み\n    image = cv2.imread(image_path)\n    \n    # グレースケールに変換\n    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n    \n    # ノイズ除去\n    denoised = cv2.medianBlur(gray, 3)\n    \n    # 二値化\n    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\n    \n    # OCRで文字認識\n    text = pytesseract.image_to_string(binary, lang='jpn')\n    \n    return text.strip()\n\n# 使用例\nresult = extract_text_from_image('document_image.jpg')\nprint('抽出されたテキスト:')\nprint(result)\n\n# 結果をファイルに保存\nwith open('extracted_text.txt', 'w', encoding='utf-8') as f:\n    f.write(result)\nprint('テキストをファイルに保存しました')",
         "libraries": "pytesseract、opencv-python、Pillow",
         "explanation": "画像内の文字を自動で抽出することで、手動入力の手間を大幅に削減できます。",
         "benefits": ["手動入力が不要", "大量処理が可能", "正確な文字認識"],
         "time_required": "30分〜1時間",
         "difficulty": "初級",
         "ai_prompt": "Pythonで画像から文字抽出のコードを作成してください。以下の条件でお願いします：\n\n1. pytesseractライブラリを使う\n2. 画像ファイルを読み込む\n3. 前処理（グレースケール化、ノイズ除去）を行う\n4. 日本語の文字を認識する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象画像: 文字が含まれる画像ファイル\n言語: 日本語\n出力: テキストファイル"
     },
     {
         "id": 17, 
         "title": "ファイル自動バックアップ", 
         "desc": "重要ファイルを自動でバックアップ",
         "how_to": "指定したフォルダのファイルを定期的にバックアップフォルダにコピーします。",
         "sample_code": "import shutil\nimport os\nfrom datetime import datetime\nimport schedule\nimport time\n\ndef backup_files(source_folder, backup_folder):\n    # バックアップフォルダを作成（日付付き）\n    today = datetime.now().strftime('%Y%m%d')\n    backup_path = os.path.join(backup_folder, f'backup_{today}')\n    \n    if not os.path.exists(backup_path):\n        os.makedirs(backup_path)\n    \n    # ファイルをコピー\n    for item in os.listdir(source_folder):\n        source_item = os.path.join(source_folder, item)\n        backup_item = os.path.join(backup_path, item)\n        \n        if os.path.isfile(source_item):\n            shutil.copy2(source_item, backup_item)\n            print(f'バックアップ完了: {item}')\n        elif os.path.isdir(source_item):\n            shutil.copytree(source_item, backup_item)\n            print(f'フォルダバックアップ完了: {item}')\n    \n    print(f'バックアップ完了: {backup_path}')\n\n# 毎日18時にバックアップ\nschedule.every().day.at('18:00').do(\n    backup_files, \n    'C:/Users/YourName/Documents', \n    'C:/Users/YourName/Backups'\n)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
         "libraries": "shutil、os、datetime、schedule（標準ライブラリ）",
         "explanation": "重要ファイルを自動でバックアップすることで、データ損失のリスクを軽減できます。",
         "benefits": ["データ保護", "手動バックアップが不要", "定期的な実行"],
         "time_required": "30分〜1時間",
         "difficulty": "初級",
         "ai_prompt": "Pythonでファイル自動バックアップのコードを作成してください。以下の条件でお願いします：\n\n1. shutilライブラリを使う\n2. 指定したフォルダのファイルをバックアップする\n3. 日付付きのフォルダにコピーする\n4. 毎日指定した時間に自動実行する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象フォルダ: バックアップしたいフォルダ\nバックアップ先: 指定したフォルダ\n実行時間: 毎日18時"
     },
     {
         "id": 18, 
         "title": "会議議事録自動作成", 
         "desc": "会議音声から議事録を自動作成",
         "how_to": "音声認識とAIを使って会議の録音から議事録を自動生成します。",
         "sample_code": "import speech_recognition as sr\nfrom datetime import datetime\nimport re\n\ndef create_meeting_minutes(audio_file_path):\n    # 音声認識\n    recognizer = sr.Recognizer()\n    \n    with sr.AudioFile(audio_file_path) as source:\n        audio = recognizer.record(source)\n        \n        try:\n            # 文字起こし\n            text = recognizer.recognize_google(audio, language='ja-JP')\n            \n            # 議事録の形式に整理\n            minutes = f'''\n会議議事録\n\n日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n参加者: [参加者名を記入]\n\n【議題】\n[議題を記入]\n\n【議事内容】\n{text}\n\n【決定事項】\n[決定事項を記入]\n\n【次回予定】\n[次回予定を記入]\n            '''\n            \n            return minutes\n            \n        except sr.UnknownValueError:\n            return '音声を認識できませんでした'\n\n# 使用例\nminutes = create_meeting_minutes('meeting.wav')\nprint(minutes)\n\n# ファイルに保存\nwith open('meeting_minutes.txt', 'w', encoding='utf-8') as f:\n    f.write(minutes)\nprint('議事録を保存しました')",
         "libraries": "SpeechRecognition、datetime（標準ライブラリ）",
         "explanation": "会議の録音から自動で議事録を作成することで、手動での議事録作成の時間を大幅に短縮できます。",
         "benefits": ["議事録作成が自動化", "時間を大幅節約", "正確な記録"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "Pythonで会議議事録自動作成のコードを作成してください。以下の条件でお願いします：\n\n1. SpeechRecognitionライブラリを使う\n2. 会議の音声ファイルを文字起こしする\n3. 議事録の形式に整理する（日時、参加者、議題、議事内容、決定事項）\n4. テキストファイルとして保存する\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象ファイル: 会議の音声ファイル\n出力形式: 議事録テキストファイル\n内容: 日時、参加者、議題、議事内容、決定事項"
     },
     {
         "id": 19, 
         "title": "翻訳自動化", 
         "desc": "テキストを自動で翻訳",
         "how_to": "Google Translate APIを使ってテキストを自動翻訳します。",
         "sample_code": "from googletrans import Translator\nimport pandas as pd\n\ndef translate_text(text, target_lang='en'):\n    translator = Translator()\n    \n    try:\n        # 翻訳実行\n        result = translator.translate(text, dest=target_lang)\n        return result.text\n    except Exception as e:\n        return f'翻訳エラー: {e}'\n\ndef translate_file(input_file, output_file, target_lang='en'):\n    # ファイルを読み込み\n    with open(input_file, 'r', encoding='utf-8') as f:\n        content = f.read()\n    \n    # 翻訳\n    translated_content = translate_text(content, target_lang)\n    \n    # 結果を保存\n    with open(output_file, 'w', encoding='utf-8') as f:\n        f.write(translated_content)\n    \n    print(f'翻訳完了: {output_file}')\n\n# 使用例\n# 単一テキストの翻訳\ntranslated = translate_text('こんにちは、世界', 'en')\nprint(f'翻訳結果: {translated}')\n\n# ファイルの翻訳\ntranslate_file('japanese_text.txt', 'english_text.txt', 'en')",
         "libraries": "googletrans==4.0.0rc1、pandas",
         "explanation": "テキストを自動翻訳することで、多言語対応や国際的なコミュニケーションを効率化できます。",
         "benefits": ["手動翻訳が不要", "多言語対応", "大量翻訳が可能"],
         "time_required": "30分〜1時間",
         "difficulty": "初級",
         "ai_prompt": "Pythonで翻訳自動化のコードを作成してください。以下の条件でお願いします：\n\n1. googletransライブラリを使う\n2. 日本語のテキストを英語に翻訳する\n3. ファイル全体を翻訳する機能も含める\n4. エラーハンドリングも含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\n対象言語: 日本語→英語\n入力: テキストファイル\n出力: 翻訳されたテキストファイル"
     },
     {
         "id": 20, 
         "title": "タスク自動リマインド", 
         "desc": "タスクを自動でリマインド",
         "how_to": "スケジュール機能を使ってタスクの期限を管理し、自動でリマインドを送信します。",
         "sample_code": "import schedule\nimport time\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom datetime import datetime, timedelta\n\n# タスクリスト\ntasks = [\n    {'title': 'レポート提出', 'deadline': '2024-01-20', 'priority': 'high'},\n    {'title': '会議準備', 'deadline': '2024-01-18', 'priority': 'medium'},\n    {'title': 'メール返信', 'deadline': '2024-01-17', 'priority': 'low'}\n]\n\ndef check_deadlines():\n    today = datetime.now().date()\n    \n    for task in tasks:\n        deadline = datetime.strptime(task['deadline'], '%Y-%m-%d').date()\n        days_left = (deadline - today).days\n        \n        if days_left <= 1 and days_left >= 0:\n            send_reminder(task, days_left)\n\ndef send_reminder(task, days_left):\n    # メール設定\n    sender_email = 'your_email@gmail.com'\n    sender_password = 'your_password'\n    receiver_email = 'your_email@gmail.com'\n    \n    # メール内容\n    subject = f'タスクリマインド: {task[\"title\"]}'\n    body = f'''\n    タスクリマインド\n    \n    タスク: {task['title']}\n    期限: {task['deadline']}\n    優先度: {task['priority']}\n    残り日数: {days_left}日\n    \n    早めに完了させましょう！\n    '''\n    \n    # メール送信\n    msg = MIMEText(body, 'plain')\n    msg['Subject'] = subject\n    msg['From'] = sender_email\n    msg['To'] = receiver_email\n    \n    server = smtplib.SMTP('smtp.gmail.com', 587)\n    server.starttls()\n    server.login(sender_email, sender_password)\n    server.send_message(msg)\n    server.quit()\n    \n    print(f'リマインド送信: {task[\"title\"]}')\n\n# 毎日9時にチェック\nschedule.every().day.at('09:00').do(check_deadlines)\n\n# スケジュール実行\nwhile True:\n    schedule.run_pending()\n    time.sleep(60)",
         "libraries": "schedule、smtplib（標準ライブラリ）、datetime（標準ライブラリ）",
         "explanation": "タスクの期限を自動で管理し、リマインドを送信することで、タスクの見落としを防げます。",
         "benefits": ["タスクの見落としを防ぐ", "時間管理が向上", "自動リマインド"],
         "time_required": "1〜2時間",
         "difficulty": "中級",
         "ai_prompt": "Pythonでタスク自動リマインドのコードを作成してください。以下の条件でお願いします：\n\n1. scheduleライブラリで毎日9時にチェックする\n2. タスクリストから期限が近いものを検出する\n3. 期限が1日前になったらメールでリマインドを送信する\n4. タスクのタイトル、期限、優先度を含める\n5. 初心者でも理解できるようにコメントを詳しく書く\n\nチェック時間: 毎日9時\nリマインド条件: 期限1日前\n送信内容: タスク名、期限、優先度"
     }
]

@app.route('/')
def index():
    return render_template('index.html', tools=TOOLS)

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if tool is None:
        return "ツールが見つかりません", 404
    return render_template('detail.html', tool=tool)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 