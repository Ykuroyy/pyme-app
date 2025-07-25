import pandas as pd
import os
import shutil
from datetime import datetime, timedelta
import numpy as np

EXTRA_TOOLS = [
    {
        "id": 31,
        "category": "ファイル管理",
        "number": "31/100",
        "title": "PDF一括結合",
        "desc": "複数のPDFファイルを自動で1つに結合",
        "how_to": "PyPDF2ライブラリを使って、複数のPDFファイルを1つのファイルにまとめます。",
        "sample_code": "import os\\nfrom PyPDF2 import PdfMerger\\n\\nprint('=== PDF一括結合システム ===')\\n\\npdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']\\noutput_pdf = 'merged_output.pdf'\\n\\ntry:\\n    merger = PdfMerger()\\n    for pdf in pdf_files:\\n        if os.path.exists(pdf):\\n            merger.append(pdf)\\n            print(f'{pdf}を追加しました')\\n    \\n    merger.write(output_pdf)\\n    merger.close()\\n    print(f'PDF結合完了！出力ファイル: {output_pdf}')\\nexcept Exception as e:\\n    print(f'エラーが発生しました: {e}')",
        "libraries": "PyPDF2、os（標準ライブラリ）",
        "explanation": "複数のPDFを一括で結合することで、資料整理や提出が効率化できます。",
        "benefits": ["手作業が不要", "一括結合", "資料整理が簡単"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでPDF一括結合のコードを作成してください。PyPDF2ライブラリを使って複数のPDFファイルを1つにまとめるコードを書いてください。初心者でも理解できるようにコメントを詳しく書いてください。"
    },
    {
        "id": 32,
        "category": "マーケティング分析",
        "number": "32/100",
        "title": "SNSエンゲージメント分析",
        "desc": "SNS投稿のエンゲージメントを自動分析",
        "how_to": "SNSの投稿データを分析し、エンゲージメント率やリーチを計算します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== SNSエンゲージメント分析システム ===')\\n\\n# SNS投稿データ（サンプル）\\nsns_posts = pd.DataFrame({\\n    '投稿ID': ['POST001', 'POST002', 'POST003', 'POST004'],\\n    '投稿日': ['2024-07-20', '2024-07-21', '2024-07-22', '2024-07-23'],\\n    'プラットフォーム': ['Twitter', 'Instagram', 'Facebook', 'Twitter'],\\n    '投稿タイプ': ['テキスト', '画像', '動画', 'テキスト'],\\n    'フォロワー数': [12500, 8200, 15800, 12800],\\n    'インプレッション': [15600, 12400, 22100, 9800],\\n    'エンゲージメント': [892, 654, 1245, 445],\\n    'クリック': [156, 89, 287, 67]\\n})\\n\\n# エンゲージメント指標計算\\nsns_posts['エンゲージメント率'] = (sns_posts['エンゲージメント'] / sns_posts['インプレッション'] * 100).round(2)\\nsns_posts['リーチ率'] = (sns_posts['インプレッション'] / sns_posts['フォロワー数'] * 100).round(2)\\nsns_posts['CTR'] = (sns_posts['クリック'] / sns_posts['インプレッション'] * 100).round(2)\\n\\nprint('投稿パフォーマンスサマリー:')\\nprint(sns_posts.to_string(index=False))\\n\\nprint('\\n=== SNSエンゲージメント分析完了 ===')",
        "libraries": "pandas、numpy、datetime（標準ライブラリ）",
        "explanation": "SNS投稿のエンゲージメント率、リーチ率、CTRなどを分析し、投稿パフォーマンスを最適化します。",
        "benefits": ["投稿効果の可視化", "プラットフォーム最適化", "コンテンツ戦略の改善", "ROIの向上"],
        "time_required": "1-2時間",
        "difficulty": "中級",
        "ai_prompt": "SNSエンゲージメント分析システムのPythonコードを作成してください。エンゲージメント率計算、プラットフォーム別分析、コンテンツタイプ別分析、パフォーマンス最適化提案を含めてください。"
    }
]

# 残りの68ツールを具体的な名前で追加
tool_definitions = [
    # ビジネス分析（8ツール）
    {"id": 33, "category": "ビジネス分析", "title": "売上分析ダッシュボード", "desc": "売上データを自動分析してグラフ化"},
    {"id": 34, "category": "ビジネス分析", "title": "顧客行動分析", "desc": "顧客の購買パターンを分析"},
    {"id": 35, "category": "ビジネス分析", "title": "競合他社分析", "desc": "競合の価格・戦略を自動調査"},
    {"id": 36, "category": "ビジネス分析", "title": "市場トレンド分析", "desc": "業界トレンドを自動収集・分析"},
    {"id": 37, "category": "ビジネス分析", "title": "ROI計算ツール", "desc": "投資収益率を自動計算"},
    {"id": 38, "category": "ビジネス分析", "title": "データ可視化システム", "desc": "複雑なデータを分かりやすくグラフ化"},
    {"id": 39, "category": "ビジネス分析", "title": "KPI自動レポート", "desc": "重要指標を自動集計・レポート化"},
    {"id": 40, "category": "ビジネス分析", "title": "予算管理システム", "desc": "予算執行状況を自動監視"},
    
    # マーケティング（9ツール）
    {"id": 41, "category": "マーケティング", "title": "顧客セグメンテーション", "desc": "顧客を属性別に自動分類"},
    {"id": 42, "category": "マーケティング", "title": "キャンペーン効果測定", "desc": "広告効果を自動測定・分析"},
    {"id": 43, "category": "マーケティング", "title": "リード管理システム", "desc": "見込み客情報を自動管理"},
    {"id": 44, "category": "マーケティング", "title": "コンテンツ管理システム", "desc": "マーケティング素材を自動整理"},
    {"id": 45, "category": "マーケティング", "title": "A/Bテスト自動化", "desc": "マーケティング施策の効果を自動比較"},
    {"id": 46, "category": "マーケティング", "title": "アフィリエイト管理", "desc": "アフィリエイト成果を自動追跡"},
    {"id": 47, "category": "マーケティング", "title": "広告効果分析", "desc": "広告のROASを自動計算"},
    {"id": 48, "category": "マーケティング", "title": "ソーシャルメディア監視", "desc": "SNS上の評判を自動監視"},
    {"id": 49, "category": "マーケティング", "title": "マーケティングROI分析", "desc": "マーケティング投資の効果測定"},
    
    # 営業・顧客管理（8ツール）
    {"id": 50, "category": "営業・顧客管理", "title": "商談進捗管理", "desc": "営業案件の進捗を自動追跡"},
    {"id": 51, "category": "営業・顧客管理", "title": "見積書自動生成", "desc": "顧客情報から見積書を自動作成"},
    {"id": 52, "category": "営業・顧客管理", "title": "契約管理システム", "desc": "契約書の期限・更新を自動管理"},
    {"id": 53, "category": "営業・顧客管理", "title": "顧客満足度調査", "desc": "アンケート結果を自動集計・分析"},
    {"id": 54, "category": "営業・顧客管理", "title": "セールスレポート", "desc": "営業実績を自動レポート化"},
    {"id": 55, "category": "営業・顧客管理", "title": "営業活動追跡", "desc": "営業担当者の活動を自動記録"},
    {"id": 56, "category": "営業・顧客管理", "title": "顧客対応履歴管理", "desc": "問い合わせ対応履歴を自動整理"},
    {"id": 57, "category": "営業・顧客管理", "title": "価格管理システム", "desc": "商品価格の変動を自動監視"},
    
    # 人事・労務（8ツール）
    {"id": 58, "category": "人事・労務", "title": "勤怠管理システム", "desc": "出退勤時間を自動集計"},
    {"id": 59, "category": "人事・労務", "title": "給与計算自動化", "desc": "給与明細を自動計算・作成"},
    {"id": 60, "category": "人事・労務", "title": "採用管理システム", "desc": "応募者情報を自動整理・管理"},
    {"id": 61, "category": "人事・労務", "title": "人事評価システム", "desc": "従業員評価を自動集計"},
    {"id": 62, "category": "人事・労務", "title": "従業員データ管理", "desc": "人事情報を一元管理"},
    {"id": 63, "category": "人事・労務", "title": "研修管理システム", "desc": "研修履歴・進捗を自動追跡"},
    {"id": 64, "category": "人事・労務", "title": "休暇管理システム", "desc": "有給休暇の取得状況を自動管理"},
    {"id": 65, "category": "人事・労務", "title": "人材配置最適化", "desc": "スキルマッチングで最適配置提案"},
    
    # データ処理・分析（9ツール）
    {"id": 66, "category": "データ処理・分析", "title": "統計分析システム", "desc": "データの統計解析を自動実行"},
    {"id": 67, "category": "データ処理・分析", "title": "データクレンジング", "desc": "データの重複・欠損を自動修正"},
    {"id": 68, "category": "データ処理・分析", "title": "レポート自動生成", "desc": "定期レポートを自動作成・配信"},
    {"id": 69, "category": "データ処理・分析", "title": "データベース管理", "desc": "DB の保守・最適化を自動実行"},
    {"id": 70, "category": "データ処理・分析", "title": "機械学習予測モデル", "desc": "AIを使った需要予測システム"},
    {"id": 71, "category": "データ処理・分析", "title": "テキスト分析システム", "desc": "レビュー・感想を自動分析"},
    {"id": 72, "category": "データ処理・分析", "title": "画像認識システム", "desc": "商品画像を自動分類・検索"},
    {"id": 73, "category": "データ処理・分析", "title": "自然言語処理システム", "desc": "文書の自動要約・翻訳"},
    {"id": 74, "category": "データ処理・分析", "title": "予測分析プラットフォーム", "desc": "ビジネス予測を自動実行"},
    
    # ファイル・文書管理（8ツール）
    {"id": 75, "category": "ファイル・文書管理", "title": "文書管理システム", "desc": "文書の版数・承認を自動管理"},
    {"id": 76, "category": "ファイル・文書管理", "title": "バージョン管理システム", "desc": "ファイルの変更履歴を自動追跡"},
    {"id": 77, "category": "ファイル・文書管理", "title": "ファイル暗号化", "desc": "重要ファイルを自動暗号化"},
    {"id": 78, "category": "ファイル・文書管理", "title": "自動アーカイブ", "desc": "古いファイルを自動圧縮・保管"},
    {"id": 79, "category": "ファイル・文書管理", "title": "文書検索システム", "desc": "大量文書から目的の情報を自動検索"},
    {"id": 80, "category": "ファイル・文書管理", "title": "OCR文字認識", "desc": "画像・PDFから文字を自動抽出"},
    {"id": 81, "category": "ファイル・文書管理", "title": "電子署名システム", "desc": "契約書に電子署名を自動付与"},
    {"id": 82, "category": "ファイル・文書管理", "title": "文書自動生成", "desc": "テンプレートから文書を自動作成"},
    
    # 自動化・効率化（9ツール）
    {"id": 83, "category": "自動化・効率化", "title": "ワークフロー自動化", "desc": "業務プロセスを自動化"},
    {"id": 84, "category": "自動化・効率化", "title": "在庫管理システム", "desc": "在庫数・発注を自動管理"},
    {"id": 85, "category": "自動化・効率化", "title": "品質管理システム", "desc": "製品品質を自動チェック"},
    {"id": 86, "category": "自動化・効率化", "title": "プロジェクト管理", "desc": "プロジェクトの進捗を自動追跡"},
    {"id": 87, "category": "自動化・効率化", "title": "業務プロセス最適化AI", "desc": "AIが業務改善案を自動提案"},
    {"id": 88, "category": "自動化・効率化", "title": "経費精算自動化システム", "desc": "領収書から経費を自動計算"},
    {"id": 89, "category": "自動化・効率化", "title": "業務フロー自動化", "desc": "定型業務を完全自動化"},
    {"id": 90, "category": "自動化・効率化", "title": "設備保守管理", "desc": "機器のメンテナンス時期を自動通知"},
    {"id": 91, "category": "自動化・効率化", "title": "IoTデータ収集", "desc": "センサーデータを自動収集・分析"},
    
    # リスク・品質管理（9ツール）
    {"id": 92, "category": "リスク・品質管理", "title": "セキュリティ監視", "desc": "不正アクセスを自動検知・通知"},
    {"id": 93, "category": "リスク・品質管理", "title": "リスク評価システム", "desc": "事業リスクを自動評価・警告"},
    {"id": 94, "category": "リスク・品質管理", "title": "コンプライアンス管理", "desc": "法令遵守状況を自動チェック"},
    {"id": 95, "category": "リスク・品質管理", "title": "監査支援システム", "desc": "監査資料を自動収集・整理"},
    {"id": 96, "category": "リスク・品質管理", "title": "品質検査システム", "desc": "製品の品質基準を自動判定"},
    {"id": 97, "category": "リスク・品質管理", "title": "インシデント管理", "desc": "問題発生時の対応を自動化"},
    {"id": 98, "category": "リスク・品質管理", "title": "災害対策システム", "desc": "緊急時のBCP対応を自動実行"},
    {"id": 99, "category": "リスク・品質管理", "title": "情報漏洩対策", "desc": "機密情報の流出を自動防止"},
    {"id": 100, "category": "リスク・品質管理", "title": "統合リスク管理システム", "desc": "全社的リスクを一元管理"}
]

# 具体的なツール実装マッピング
tool_implementations = {
    "売上分析ダッシュボード": {
        "how_to": "pandas、matplotlib、seabornを使って売上データを読み込み、月別・商品別・地域別の売上推移をグラフ化します。",
        "sample_code": "import pandas as pd\\nimport matplotlib.pyplot as plt\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== 売上分析ダッシュボード ===')\\n\\n# 売上データ（サンプル）\\nsales_data = pd.DataFrame({\\n    '月': pd.date_range('2024-01-01', periods=12, freq='M'),\\n    '売上': [1000000, 1200000, 950000, 1300000, 1100000, 1450000, 1600000, 1380000, 1220000, 1500000, 1750000, 1900000],\\n    '商品': ['電子機器', '家具', '衣類', '電子機器', '家具', '衣類', '電子機器', '家具', '衣類', '電子機器', '家具', '衣類']\\n})\\n\\n# 月別売上推移グラフ\\nplt.figure(figsize=(10, 6))\\nplt.plot(sales_data['月'], sales_data['売上'], marker='o')\\nplt.title('月別売上推移')\\nplt.ylabel('売上（円）')\\nplt.xticks(rotation=45)\\nplt.show()\\n\\nprint(f'総売上: {sales_data[\"売上\"].sum():,}円')\\nprint('=== 売上分析完了 ===')",
        "libraries": "pandas、matplotlib、numpy、datetime"
    },
    "顧客行動分析": {
        "how_to": "RFM分析（最新購入日、購入頻度、購入金額）を使って顧客をセグメント化し、購買行動パターンを分析します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== 顧客行動分析システム ===')\\n\\n# 顧客データ（サンプル）\\ncustomer_data = pd.DataFrame({\\n    '顧客ID': ['C001', 'C002', 'C003', 'C004'],\\n    '最終購入日': ['2024-07-20', '2024-06-15', '2024-07-22', '2024-05-10'],\\n    '購入回数': [5, 2, 8, 1],\\n    '総購入金額': [50000, 15000, 120000, 8000]\\n})\\n\\n# RFM分析\\nbase_date = datetime(2024, 7, 25)\\ncustomer_data['最終購入日'] = pd.to_datetime(customer_data['最終購入日'])\\ncustomer_data['Recency'] = (base_date - customer_data['最終購入日']).dt.days\\n\\nprint('顧客セグメント分析:')\\nprint(customer_data)\\nprint('=== 顧客行動分析完了 ===')",
        "libraries": "pandas、numpy、datetime"
    },
    "見積書自動生成": {
        "how_to": "顧客情報と商品データを基に、PDFまたはExcel形式の見積書を自動生成します。",
        "sample_code": "import pandas as pd\\nfrom datetime import datetime\\n\\nprint('=== 見積書自動生成システム ===')\\n\\n# 見積データ（サンプル）\\nquote_data = pd.DataFrame({\\n    '商品名': ['ノートPC', 'マウス', 'キーボード'],\\n    '数量': [2, 2, 2],\\n    '単価': [80000, 3000, 5000],\\n})\\n\\nquote_data['金額'] = quote_data['数量'] * quote_data['単価']\\ntotal_amount = quote_data['金額'].sum()\\ntax = int(total_amount * 0.1)\\ntotal_with_tax = total_amount + tax\\n\\nprint('見積書')\\nprint('-' * 40)\\nprint(f'作成日: {datetime.now().strftime(\"%Y年%m月%d日\")}')\\nprint()\\nprint(quote_data.to_string(index=False))\\nprint('-' * 40)\\nprint(f'小計: {total_amount:,}円')\\nprint(f'消費税: {tax:,}円')\\nprint(f'合計: {total_with_tax:,}円')\\nprint('=== 見積書生成完了 ===')",
        "libraries": "pandas、datetime"
    },
    "給与計算自動化": {
        "how_to": "従業員の勤怠データから基本給、残業代、各種手当、社会保険料を自動計算し、給与明細を生成します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\n\\nprint('=== 給与計算自動化システム ===')\\n\\n# 従業員データ（サンプル）\\nemployee_data = pd.DataFrame({\\n    '従業員ID': ['E001', 'E002', 'E003', 'E004'],\\n    '氏名': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲'],\\n    '基本給': [300000, 280000, 350000, 320000],\\n    '勤務時間': [160, 170, 180, 165],\\n    '残業時間': [20, 15, 30, 10]\\n})\\n\\n# 給与計算\\nemployee_data['時給'] = employee_data['基本給'] / 160\\nemployee_data['残業代'] = employee_data['時給'] * employee_data['残業時間'] * 1.25\\nemployee_data['支給額'] = employee_data['基本給'] + employee_data['残業代']\\nemployee_data['社会保険料'] = (employee_data['支給額'] * 0.15).astype(int)\\nemployee_data['所得税'] = (employee_data['支給額'] * 0.08).astype(int)\\nemployee_data['手取額'] = employee_data['支給額'] - employee_data['社会保険料'] - employee_data['所得税']\\n\\nprint('給与計算結果:')\\nprint(employee_data[['氏名', '基本給', '残業代', '支給額', '手取額']].to_string(index=False))\\nprint('=== 給与計算完了 ===')",
        "libraries": "pandas、numpy"
    },
    "在庫管理システム": {
        "how_to": "商品の入出庫を記録し、在庫数量を自動更新、安全在庫を下回った商品に発注アラートを出します。",
        "sample_code": "import pandas as pd\\nfrom datetime import datetime\\n\\nprint('=== 在庫管理システム ===')\\n\\n# 在庫データ（サンプル）\\ninventory_data = pd.DataFrame({\\n    '商品コード': ['P001', 'P002', 'P003', 'P004', 'P005'],\\n    '商品名': ['ノートPC', 'マウス', 'キーボード', 'モニター', 'プリンター'],\\n    '現在在庫': [15, 50, 30, 8, 12],\\n    '安全在庫': [10, 20, 15, 5, 8],\\n    '最大在庫': [50, 100, 60, 30, 40]\\n})\\n\\n# 在庫状況判定\\ndef get_stock_status(current, safety, maximum):\\n    if current <= safety:\\n        return '要発注 🚨'\\n    elif current >= maximum * 0.8:\\n        return '過剰在庫 ⚠️'\\n    else:\\n        return '適正 ✅'\\n\\ninventory_data['在庫状況'] = inventory_data.apply(\\n    lambda x: get_stock_status(x['現在在庫'], x['安全在庫'], x['最大在庫']), axis=1\\n)\\n\\n# 発注推奨数量\\ninventory_data['発注推奨'] = (inventory_data['最大在庫'] - inventory_data['現在在庫']).clip(lower=0)\\n\\nprint('在庫管理レポート:')\\nprint(inventory_data.to_string(index=False))\\n\\n# アラート\\nlow_stock = inventory_data[inventory_data['現在在庫'] <= inventory_data['安全在庫']]\\nif not low_stock.empty:\\n    print('\\n🚨 発注アラート:')\\n    for _, item in low_stock.iterrows():\\n        print(f'  {item[\"商品名\"]}: 残り{item[\"現在在庫\"]}個 (推奨発注: {item[\"発注推奨\"]}個)')\\n\\nprint('=== 在庫管理完了 ===')",
        "libraries": "pandas、datetime"
    },
    "セキュリティ監視": {
        "how_to": "システムログを解析し、不正アクセスの兆候や異常なアクティビティを検知してアラートを発報します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime, timedelta\\n\\nprint('=== セキュリティ監視システム ===')\\n\\n# アクセスログ（サンプル）\\naccess_log = pd.DataFrame({\\n    'タイムスタンプ': pd.date_range(end=datetime.now(), periods=100, freq='1min'),\\n    'IPアドレス': np.random.choice(['192.168.1.10', '192.168.1.20', '10.0.0.5', '203.0.113.1'], 100),\\n    'ユーザー': np.random.choice(['user1', 'user2', 'admin', 'guest', 'unknown'], 100),\\n    'アクション': np.random.choice(['login', 'logout', 'file_access', 'admin_action', 'failed_login'], 100),\\n    'ステータス': np.random.choice(['success', 'failed'], 100, p=[0.8, 0.2])\\n})\\n\\n# 異常検知\\nfailed_logins = access_log[(access_log['アクション'] == 'failed_login')]\\nsuspicious_ips = failed_logins.groupby('IPアドレス').size()\\nsuspicious_ips = suspicious_ips[suspicious_ips >= 3]\\n\\nunknown_users = access_log[access_log['ユーザー'] == 'unknown']\\n\\nprint('セキュリティ監視レポート:')\\nprint(f'総アクセス数: {len(access_log)}')\\nprint(f'失敗ログイン: {len(failed_logins)}件')\\nprint(f'不明ユーザー: {len(unknown_users)}件')\\n\\nif not suspicious_ips.empty:\\n    print('\\n🚨 セキュリティアラート:')\\n    for ip, count in suspicious_ips.items():\\n        print(f'  IP {ip}: {count}回の失敗ログイン')\\n\\nif not unknown_users.empty:\\n    print(f'\\n⚠️  不明ユーザーアクセス: {len(unknown_users)}件検出')\\n\\nprint('=== セキュリティ監視完了 ===')",
        "libraries": "pandas、numpy、datetime"
    },
    "競合他社分析": {
        "how_to": "競合企業の価格、市場シェア、顧客満足度を比較分析し、自社のポジションを評価します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\n\\nprint('=== 競合他社分析システム ===')\\n\\n# 競合データ（サンプル）\\ncompetitor_data = pd.DataFrame({\\n    '企業名': ['競合A', '競合B', '競合C', '自社'],\\n    '商品価格': [9800, 10500, 8900, 9500],\\n    '市場シェア': [25.5, 18.2, 15.8, 20.3],\\n    '顧客満足度': [4.2, 3.8, 4.5, 4.1]\\n})\\n\\n# 競争力スコア計算\\ncompetitor_data['価格競争力'] = (competitor_data['商品価格'].max() - competitor_data['商品価格']) / competitor_data['商品価格'].max() * 100\\ncompetitor_data['総合スコア'] = (competitor_data['市場シェア'] * 0.4 + competitor_data['顧客満足度'] * 20 * 0.3 + competitor_data['価格競争力'] * 0.3).round(1)\\n\\nprint('競合他社分析結果:')\\nprint(competitor_data)\\n\\n# 自社ポジション\\nown_rank = (competitor_data['総合スコア'] > competitor_data[competitor_data['企業名'] == '自社']['総合スコア'].iloc[0]).sum() + 1\\nprint(f'\\n自社順位: {own_rank}位/{len(competitor_data)}社中')\\nprint('=== 競合他社分析完了 ===')",
        "libraries": "pandas、numpy"
    },
    "キャンペーン効果測定": {
        "how_to": "マーケティングキャンペーンのKPIを自動計測し、ROI、CVR、CPAなどの効果指標を算出します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== キャンペーン効果測定システム ===')\\n\\n# キャンペーンデータ（サンプル）\\ncampaign_data = pd.DataFrame({\\n    'キャンペーン名': ['夏セール', 'SNS広告A', 'メルマガ', 'リターゲティング'],\\n    '投資額': [500000, 300000, 100000, 200000],\\n    'インプレッション': [100000, 80000, 15000, 50000],\\n    'クリック': [2500, 1600, 450, 1000],\\n    'コンバージョン': [125, 80, 30, 60],\\n    '売上': [2500000, 1600000, 600000, 1200000]\\n})\\n\\n# 効果指標計算\\ncampaign_data['CTR'] = (campaign_data['クリック'] / campaign_data['インプレッション'] * 100).round(2)\\ncampaign_data['CVR'] = (campaign_data['コンバージョン'] / campaign_data['クリック'] * 100).round(2)\\ncampaign_data['CPA'] = (campaign_data['投資額'] / campaign_data['コンバージョン']).round(0)\\ncampaign_data['ROI'] = ((campaign_data['売上'] - campaign_data['投資額']) / campaign_data['投資額'] * 100).round(1)\\n\\nprint('キャンペーン効果測定結果:')\\nprint(campaign_data[['キャンペーン名', 'CTR', 'CVR', 'CPA', 'ROI']].to_string(index=False))\\n\\n# ベストキャンペーン\\nbest_campaign = campaign_data.loc[campaign_data['ROI'].idxmax()]\\nprint(f'\\n🏆 最高ROIキャンペーン: {best_campaign[\"キャンペーン名\"]} (ROI: {best_campaign[\"ROI\"]}%)')\\nprint('=== キャンペーン効果測定完了 ===')",
        "libraries": "pandas、numpy、datetime"
    },
    "勤怠管理システム": {
        "how_to": "従業員の出退勤時間を記録し、労働時間、残業時間、有給取得状況を自動集計します。",
        "sample_code": "import pandas as pd\\nfrom datetime import datetime, timedelta\\n\\nprint('=== 勤怠管理システム ===')\\n\\n# 勤怠データ（サンプル）\\nattendance_data = pd.DataFrame({\\n    '従業員ID': ['E001', 'E002', 'E003', 'E004'],\\n    '氏名': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲'],\\n    '出勤時刻': ['09:00', '08:45', '09:15', '08:30'],\\n    '退勤時刻': ['18:30', '17:45', '19:30', '18:00'],\\n    '休憩時間': [60, 60, 60, 60],\\n    '有給残日数': [15, 12, 8, 20]\\n})\\n\\n# 労働時間計算\\nfor i, row in attendance_data.iterrows():\\n    start = datetime.strptime(row['出勤時刻'], '%H:%M')\\n    end = datetime.strptime(row['退勤時刻'], '%H:%M')\\n    work_hours = (end - start).total_seconds() / 3600 - row['休憩時間'] / 60\\n    overtime = max(0, work_hours - 8)\\n    \\n    attendance_data.loc[i, '労働時間'] = round(work_hours, 1)\\n    attendance_data.loc[i, '残業時間'] = round(overtime, 1)\\n\\nprint('勤怠管理レポート:')\\nprint(attendance_data[['氏名', '出勤時刻', '退勤時刻', '労働時間', '残業時間', '有給残日数']].to_string(index=False))\\n\\n# 残業時間アラート\\novertime_employees = attendance_data[attendance_data['残業時間'] > 2]\\nif not overtime_employees.empty:\\n    print('\\n⚠️  残業時間注意:')\\n    for _, emp in overtime_employees.iterrows():\\n        print(f'  {emp[\"氏名\"]}: {emp[\"残業時間\"]}時間')\\n\\nprint('=== 勤怠管理完了 ===')",
        "libraries": "pandas、datetime"
    },
    "機械学習予測モデル": {
        "how_to": "過去のデータを基に機械学習モデルを構築し、売上や需要の予測を自動化します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom sklearn.linear_model import LinearRegression\\nfrom sklearn.model_selection import train_test_split\\nimport matplotlib.pyplot as plt\\n\\nprint('=== 機械学習予測モデル ===')\\n\\n# 予測用データ（サンプル）\\nnp.random.seed(42)\\nprediction_data = pd.DataFrame({\\n    '月': range(1, 25),\\n    '広告費': np.random.normal(100, 20, 24),\\n    '気温': np.random.normal(20, 10, 24),\\n    '売上': np.random.normal(1000, 200, 24)\\n})\\n\\n# 特徴量とターゲットを分離\\nX = prediction_data[['月', '広告費', '気温']]\\ny = prediction_data['売上']\\n\\n# 訓練・テストデータに分割\\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\\n\\n# 線形回帰モデルを訓練\\nmodel = LinearRegression()\\nmodel.fit(X_train, y_train)\\n\\n# 予測\\ny_pred = model.predict(X_test)\\n\\n# 精度評価\\nfrom sklearn.metrics import mean_squared_error, r2_score\\nmse = mean_squared_error(y_test, y_pred)\\nr2 = r2_score(y_test, y_pred)\\n\\nprint('機械学習予測結果:')\\nprint(f'平均二乗誤差: {mse:.2f}')\\nprint(f'決定係数 (R²): {r2:.3f}')\\n\\n# 来月の予測\\nnext_month_data = [[25, 120, 25]]  # 25月目、広告費120、気温25度\\nnext_month_pred = model.predict(next_month_data)[0]\\nprint(f'\\n来月の売上予測: {next_month_pred:.0f}')\\n\\n# 特徴量の重要度\\nfeature_importance = pd.DataFrame({\\n    '特徴量': ['月', '広告費', '気温'],\\n    '係数': model.coef_\\n})\\nprint('\\n特徴量の影響度:')\\nprint(feature_importance)\\nprint('=== 機械学習予測完了 ===')",
        "libraries": "pandas、numpy、scikit-learn、matplotlib"
    },
    "OCR文字認識": {
        "how_to": "画像やPDFファイルから文字を自動認識し、テキストデータとして抽出・保存します。",
        "sample_code": "import pandas as pd\\nfrom datetime import datetime\\nimport os\\n\\nprint('=== OCR文字認識システム ===')\\n\\n# OCR処理のサンプル（実際にはPyTesseractなどを使用）\\ndef extract_text_from_image(image_path):\\n    # 実際のOCR処理はここで行う\\n    # return pytesseract.image_to_string(Image.open(image_path), lang='jpn')\\n    return 'これはサンプルの認識結果です。\\n請求書番号: INV-2024-001\\n金額: 100,000円\\n日付: 2024/07/25'\\n\\n# 処理対象ファイル\\nimage_files = ['invoice1.jpg', 'receipt1.png', 'document1.pdf']\\n\\n# OCR結果を格納\\nocr_results = []\\n\\nfor file in image_files:\\n    print(f'処理中: {file}')\\n    \\n    # OCR実行（サンプル）\\n    extracted_text = extract_text_from_image(file)\\n    \\n    # 結果を保存\\n    ocr_results.append({\\n        'ファイル名': file,\\n        '処理日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),\\n        '抽出テキスト': extracted_text,\\n        '文字数': len(extracted_text)\\n    })\\n    \\n    # テキストファイルとして保存\\n    output_file = f'{file}_extracted.txt'\\n    with open(output_file, 'w', encoding='utf-8') as f:\\n        f.write(extracted_text)\\n    \\n    print(f'  → {output_file} に保存')\\n\\n# 結果サマリー\\nresult_df = pd.DataFrame(ocr_results)\\nprint('\\nOCR処理結果サマリー:')\\nprint(result_df[['ファイル名', '文字数', '処理日時']].to_string(index=False))\\n\\nprint(f'\\n処理完了: {len(image_files)}ファイル')\\nprint(f'総抽出文字数: {result_df[\"文字数\"].sum()}文字')\\nprint('=== OCR文字認識完了 ===')",
        "libraries": "pandas、datetime、os、PIL（画像処理）、pytesseract（OCR）"
    },
    "業務プロセス最適化AI": {
        "how_to": "業務フローを分析し、ボトルネックや非効率な工程を特定、改善案を自動提案します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== 業務プロセス最適化AIシステム ===')\\n\\n# 業務プロセスデータ（サンプル）\\nprocess_data = pd.DataFrame({\\n    '工程名': ['受注', '在庫確認', '商品準備', '梱包', '発送', '請求書発行'],\\n    '平均処理時間': [15, 30, 45, 20, 10, 25],  # 分\\n    '担当者数': [2, 1, 3, 2, 1, 1],\\n    '一日処理件数': [50, 50, 45, 45, 45, 45],\\n    'エラー発生率': [2, 5, 8, 3, 1, 2],  # %\\n    '自動化可能度': [80, 90, 30, 60, 70, 95]  # %\\n})\\n\\n# 効率性指標計算\\nprocess_data['工程効率'] = (60 / process_data['平均処理時間'] * process_data['担当者数']).round(1)\\nprocess_data['品質スコア'] = (100 - process_data['エラー発生率'])\\nprocess_data['改善ポテンシャル'] = (process_data['平均処理時間'] * process_data['エラー発生率'] / 100 * process_data['自動化可能度'] / 100).round(1)\\n\\nprint('業務プロセス分析結果:')\\nprint(process_data[['工程名', '平均処理時間', 'エラー発生率', '改善ポテンシャル']].to_string(index=False))\\n\\n# ボトルネック特定\\nbottleneck = process_data.loc[process_data['平均処理時間'].idxmax()]\\nprint(f'\\n🚨 ボトルネック工程: {bottleneck[\"工程名\"]} ({bottleneck[\"平均処理時間\"]}分)')\\n\\n# 改善提案\\nprint('\\n💡 改善提案:')\\nhigh_potential = process_data[process_data['改善ポテンシャル'] > 5]\\nif not high_potential.empty:\\n    for _, process in high_potential.iterrows():\\n        if process['自動化可能度'] > 80:\\n            suggestion = 'システム自動化を推奨'\\n        elif process['エラー発生率'] > 5:\\n            suggestion = '品質管理体制の見直し'\\n        else:\\n            suggestion = '作業手順の標準化'\\n        \\n        print(f'  {process[\"工程名\"]}: {suggestion} (改善効果: {process[\"改善ポテンシャル\"]}点)')\\n\\n# 自動化ROI試算\\ntotal_automation_potential = (process_data['平均処理時間'] * process_data['自動化可能度'] / 100 * process_data['一日処理件数']).sum()\\nprint(f'\\n📈 自動化による時間削減見込み: {total_automation_potential:.0f}分/日')\\nprint(f'月間削減時間: {total_automation_potential * 22 / 60:.1f}時間')\\nprint('=== 業務プロセス最適化完了 ===')",
        "libraries": "pandas、numpy、datetime"
    }
}

for tool_def in tool_definitions:
    # 具体的な実装があるかチェック
    if tool_def["title"] in tool_implementations:
        impl = tool_implementations[tool_def["title"]]
        how_to = impl["how_to"]
        sample_code = impl["sample_code"]
        libraries = impl["libraries"]
    else:
        # デフォルトの実装
        how_to = f"{tool_def['desc']}を実現するシステムです。データの収集、処理、分析、結果出力を自動化します。"
        sample_code = "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== " + tool_def['title'] + " ===')\\n\\n# " + tool_def['desc'] + "のサンプル処理\\ndata = pd.DataFrame({'項目': ['A', 'B', 'C'], '値': [100, 200, 300]})\\nresult = data['値'].sum()\\n\\nprint('処理結果:')\\nprint(data)\\nprint(f'合計: {result}')\\nprint('=== " + tool_def['title'] + "完了 ===')"
        libraries = "pandas、numpy、datetime（標準ライブラリ）"
    
    tool = {
        "id": tool_def["id"],
        "category": tool_def["category"],
        "number": f"{tool_def['id']}/100",
        "title": tool_def["title"],
        "desc": tool_def["desc"],
        "how_to": how_to,
        "sample_code": sample_code,
        "libraries": libraries,
        "explanation": f"{tool_def['desc']}により業務効率を向上させます。",
        "benefits": ["業務効率化", "時間短縮", "正確性向上", "コスト削減"],
        "time_required": "1-3時間",
        "difficulty": "中級",
        "ai_prompt": f"{tool_def['title']}のPythonコードを作成してください。{tool_def['desc']}を実現するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    }
    EXTRA_TOOLS.append(tool)