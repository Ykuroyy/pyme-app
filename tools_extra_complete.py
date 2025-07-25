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
    },
    # ビジネス分析（8ツール）
    {
        "id": 33,
        "category": "ビジネス分析",
        "number": "33/100",
        "title": "売上分析ダッシュボード",
        "desc": "売上データを自動分析してグラフ化",
        "how_to": "pandas、matplotlib、seabornを使って売上データを読み込み、月別・商品別・地域別の売上推移をグラフ化します。",
        "sample_code": "import pandas as pd\\nimport matplotlib.pyplot as plt\\nimport seaborn as sns\\nfrom datetime import datetime\\n\\nprint('=== 売上分析ダッシュボード ===')\\n\\n# 売上データ（サンプル）\\nsales_data = pd.DataFrame({\\n    '日付': pd.date_range('2024-01-01', periods=12, freq='M'),\\n    '売上': [1000000, 1200000, 950000, 1300000, 1100000, 1450000, 1600000, 1380000, 1220000, 1500000, 1750000, 1900000],\\n    '商品カテゴリ': ['電子機器', '家具', '衣類', '電子機器', '家具', '衣類', '電子機器', '家具', '衣類', '電子機器', '家具', '衣類'],\\n    '地域': ['東京', '大阪', '名古屋', '東京', '大阪', '名古屋', '東京', '大阪', '名古屋', '東京', '大阪', '名古屋']\\n})\\n\\n# 月別売上推移\\nplt.figure(figsize=(12, 6))\\nplt.plot(sales_data['日付'], sales_data['売上'], marker='o')\\nplt.title('月別売上推移')\\nplt.xlabel('月')\\nplt.ylabel('売上（円）')\\nplt.xticks(rotation=45)\\nplt.tight_layout()\\nplt.show()\\n\\n# 売上統計\\nprint('\\n売上統計:')\\nprint(f'総売上: {sales_data[\"売上\"].sum():,}円')\\nprint(f'平均売上: {sales_data[\"売上\"].mean():,.0f}円')\\nprint(f'最高売上: {sales_data[\"売上\"].max():,}円')\\nprint(f'最低売上: {sales_data[\"売上\"].min():,}円')\\n\\nprint('\\n=== 売上分析完了 ===')",
        "libraries": "pandas、matplotlib、seaborn、datetime",
        "explanation": "売上データを視覚化し、トレンドや傾向を把握することで、経営判断をサポートします。",
        "benefits": ["売上トレンドの可視化", "データドリブンな意思決定", "月次レポート自動化", "売上予測の精度向上"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで売上分析ダッシュボードのコードを作成してください。pandas、matplotlib、seabornを使って売上データを読み込み、月別・商品別・地域別の売上推移をグラフ化するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 34,
        "category": "ビジネス分析",
        "number": "34/100",
        "title": "顧客行動分析",
        "desc": "顧客の購買パターンを分析",
        "how_to": "RFM分析（最新購入日、購入頻度、購入金額）を使って顧客をセグメント化し、購買行動パターンを分析します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime, timedelta\\n\\nprint('=== 顧客行動分析システム ===')\\n\\n# 顧客購買データ（サンプル）\\ncustomer_data = pd.DataFrame({\\n    '顧客ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008'],\\n    '最終購入日': ['2024-07-20', '2024-06-15', '2024-07-22', '2024-05-10', '2024-07-18', '2024-04-05', '2024-07-19', '2024-03-20'],\\n    '購入回数': [5, 2, 8, 1, 12, 3, 6, 1],\\n    '総購入金額': [50000, 15000, 120000, 8000, 200000, 25000, 75000, 12000],\\n    '年齢': [35, 42, 28, 55, 31, 48, 39, 52],\\n    '性別': ['男性', '女性', '女性', '男性', '女性', '男性', '女性', '男性']\\n})\\n\\ncustomer_data['最終購入日'] = pd.to_datetime(customer_data['最終購入日'])\\nbase_date = datetime(2024, 7, 25)\\n\\n# RFM分析\\ncustomer_data['Recency'] = (base_date - customer_data['最終購入日']).dt.days\\ncustomer_data['Frequency'] = customer_data['購入回数']\\ncustomer_data['Monetary'] = customer_data['総購入金額']\\n\\n# RFMスコア計算（5段階）\\ncustomer_data['R_Score'] = pd.qcut(customer_data['Recency'], 5, labels=[5,4,3,2,1])\\ncustomer_data['F_Score'] = pd.qcut(customer_data['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])\\ncustomer_data['M_Score'] = pd.qcut(customer_data['Monetary'], 5, labels=[1,2,3,4,5])\\n\\n# 顧客セグメント分類\\ndef classify_customer(row):\\n    if row['R_Score'] >= 4 and row['F_Score'] >= 4:\\n        return 'ロイヤル顧客'\\n    elif row['R_Score'] >= 3 and row['F_Score'] >= 3:\\n        return '優良顧客'\\n    elif row['R_Score'] >= 3:\\n        return '新規顧客'\\n    elif row['F_Score'] >= 3:\\n        return '休眠顧客'\\n    else:\\n        return '要注意顧客'\\n\\ncustomer_data['顧客セグメント'] = customer_data.apply(classify_customer, axis=1)\\n\\nprint('顧客行動分析結果:')\\nprint(customer_data[['顧客ID', 'Recency', 'Frequency', 'Monetary', '顧客セグメント']].to_string(index=False))\\n\\nprint('\\n顧客セグメント別統計:')\\nsegment_stats = customer_data.groupby('顧客セグメント').agg({\\n    '顧客ID': 'count',\\n    '総購入金額': 'mean'\\n}).round(0)\\nprint(segment_stats)\\n\\nprint('\\n=== 顧客行動分析完了 ===')",
        "libraries": "pandas、numpy、datetime",
        "explanation": "RFM分析により顧客を分類し、各セグメントに応じたマーケティング戦略を立案できます。",
        "benefits": ["顧客セグメント化", "ターゲティング精度向上", "マーケティング効率化", "顧客生涯価値向上"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで顧客行動分析のコードを作成してください。RFM分析（最新購入日、購入頻度、購入金額）を使って顧客をセグメント化し、購買行動パターンを分析するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 35,
        "category": "ビジネス分析",
        "number": "35/100",
        "title": "競合他社分析",
        "desc": "競合の価格・戦略を自動調査",
        "how_to": "Webスクレイピングを使って競合他社の価格情報を自動収集し、比較分析を行います。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\nimport requests\\nfrom bs4 import BeautifulSoup\\n\\nprint('=== 競合他社分析システム ===')\\n\\n# 競合他社データ（サンプル）\\ncompetitor_data = pd.DataFrame({\\n    '企業名': ['競合A', '競合B', '競合C', '自社'],\\n    '商品価格': [9800, 10500, 8900, 9500],\\n    '市場シェア': [25.5, 18.2, 15.8, 20.3],\\n    '顧客満足度': [4.2, 3.8, 4.5, 4.1],\\n    'マーケティング費用': [5000000, 3500000, 4200000, 4000000],\\n    'オンライン評価': [4.3, 3.9, 4.6, 4.2]\\n})\\n\\n# 価格競争力分析\\ncompetitor_data['価格競争力'] = (competitor_data['商品価格'].max() - competitor_data['商品価格']) / competitor_data['商品価格'].max() * 100\\ncompetitor_data['価格競争力'] = competitor_data['価格競争力'].round(1)\\n\\n# 総合スコア計算\\ncompetitor_data['総合スコア'] = (\\n    competitor_data['市場シェア'] * 0.3 +\\n    competitor_data['顧客満足度'] * 20 * 0.25 +\\n    competitor_data['価格競争力'] * 0.25 +\\n    competitor_data['オンライン評価'] * 20 * 0.2\\n).round(1)\\n\\nprint('競合他社分析結果:')\\nprint(competitor_data.to_string(index=False))\\n\\n# 自社のポジション分析\\nown_company = competitor_data[competitor_data['企業名'] == '自社'].iloc[0]\\nown_rank = (competitor_data['総合スコア'] > own_company['総合スコア']).sum() + 1\\n\\nprint(f'\\n自社分析:')\\nprint(f'総合順位: {own_rank}位/{len(competitor_data)}社中')\\nprint(f'価格競争力: {own_company[\"価格競争力\"]}%')\\nprint(f'市場シェア: {own_company[\"市場シェア\"]}%')\\n\\n# 改善提案\\nprint('\\n改善提案:')\\nbest_competitor = competitor_data.loc[competitor_data['総合スコア'].idxmax()]\\nif best_competitor['企業名'] != '自社':\\n    print(f'- トップ企業「{best_competitor[\"企業名\"]}」の戦略を参考にする')\\n    if best_competitor['商品価格'] < own_company['商品価格']:\\n        print('- 価格戦略の見直しを検討')\\n    if best_competitor['顧客満足度'] > own_company['顧客満足度']:\\n        print('- 顧客満足度向上施策の実施')\\n\\nprint('\\n=== 競合他社分析完了 ===')",
        "libraries": "pandas、numpy、datetime、requests、beautifulsoup4",
        "explanation": "競合他社の価格や戦略を定期的に分析し、自社の競争優位性を評価します。",
        "benefits": ["市場ポジション把握", "価格戦略最適化", "競争優位性分析", "戦略的意思決定支援"],
        "time_required": "3-4時間",
        "difficulty": "上級",
        "ai_prompt": "Pythonで競合他社分析のコードを作成してください。競合企業の価格、市場シェア、顧客満足度を比較分析し、自社のポジションを評価するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 36,
        "category": "ビジネス分析",
        "number": "36/100",
        "title": "市場トレンド分析",
        "desc": "業界トレンドを自動収集・分析",
        "how_to": "ニュースAPIやソーシャルメディアデータを活用して、業界のトピックやトレンドを自動分析します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime, timedelta\\nimport matplotlib.pyplot as plt\\n\\nprint('=== 市場トレンド分析システム ===')\\n\\n# 市場トレンドデータ（サンプル）\\ntrend_data = pd.DataFrame({\\n    '日付': pd.date_range('2024-01-01', periods=30, freq='D'),\\n    'AI関連': np.random.randint(50, 200, 30),\\n    'リモートワーク': np.random.randint(30, 150, 30),\\n    'サステナビリティ': np.random.randint(20, 120, 30),\\n    'DX': np.random.randint(40, 180, 30),\\n    'データ分析': np.random.randint(35, 160, 30)\\n})\\n\\n# トレンドスコア計算（移動平均）\\nwindow = 7\\nfor column in ['AI関連', 'リモートワーク', 'サステナビリティ', 'DX', 'データ分析']:\\n    trend_data[f'{column}_平均'] = trend_data[column].rolling(window=window).mean()\\n    trend_data[f'{column}_トレンド'] = trend_data[f'{column}_平均'].pct_change() * 100\\n\\n# 最新のトレンド分析\\nlatest_trends = trend_data.tail(1)\\ntrend_summary = []\\n\\nfor keyword in ['AI関連', 'リモートワーク', 'サステナビリティ', 'DX', 'データ分析']:\\n    latest_trend = latest_trends[f'{keyword}_トレンド'].iloc[0]\\n    if pd.notna(latest_trend):\\n        if latest_trend > 5:\\n            status = '急上昇'\\n        elif latest_trend > 0:\\n            status = '上昇'\\n        elif latest_trend > -5:\\n            status = '安定'\\n        else:\\n            status = '下降'\\n        \\n        trend_summary.append({\\n            'キーワード': keyword,\\n            '現在値': latest_trends[keyword].iloc[0],\\n            'トレンド': f'{latest_trend:.1f}%',\\n            'ステータス': status\\n        })\\n\\ntrend_df = pd.DataFrame(trend_summary)\\nprint('市場トレンド分析結果:')\\nprint(trend_df.to_string(index=False))\\n\\n# 注目トレンド\\nhot_trends = trend_df[trend_df['ステータス'].isin(['急上昇', '上昇'])].sort_values('トレンド', ascending=False)\\nif not hot_trends.empty:\\n    print('\\n📈 注目トレンド:')\\n    for _, trend in hot_trends.head(3).iterrows():\\n        print(f'- {trend[\"キーワード\"]}: {trend[\"ステータス\"]} ({trend[\"トレンド\"]})')\\n\\n# グラフ作成\\nplt.figure(figsize=(12, 8))\\nfor column in ['AI関連', 'リモートワーク', 'サステナビリティ', 'DX', 'データ分析']:\\n    plt.plot(trend_data['日付'], trend_data[f'{column}_平均'], label=column, marker='o', markersize=3)\\n\\nplt.title('市場トレンド推移（7日移動平均）')\\nplt.xlabel('日付')\\nplt.ylabel('トレンドスコア')\\nplt.legend()\\nplt.xticks(rotation=45)\\nplt.tight_layout()\\nplt.show()\\n\\nprint('\\n=== 市場トレンド分析完了 ===')",
        "libraries": "pandas、numpy、datetime、matplotlib",
        "explanation": "市場のトレンドを定量的に分析し、ビジネス機会の発見や戦略立案をサポートします。",
        "benefits": ["市場機会の発見", "トレンド予測", "競争戦略立案", "投資判断支援"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで市場トレンド分析のコードを作成してください。業界キーワードのトレンド推移を分析し、上昇・下降トレンドを可視化するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 37,
        "category": "ビジネス分析",
        "number": "37/100",
        "title": "ROI計算ツール",
        "desc": "投資収益率を自動計算",
        "how_to": "投資コストとリターンを入力し、ROI、IRR、NPVなどの投資指標を自動計算します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== ROI計算ツール ===')\\n\\n# 投資プロジェクトデータ（サンプル）\\nprojects = pd.DataFrame({\\n    'プロジェクト名': ['新システム導入', 'マーケティング施策A', '設備投資', '人材育成', 'デジタル化推進'],\\n    '初期投資': [5000000, 2000000, 8000000, 1500000, 3500000],\\n    '年間収益': [1500000, 800000, 2200000, 500000, 1200000],\\n    '年間コスト': [300000, 200000, 400000, 100000, 250000],\\n    '投資期間': [5, 3, 7, 4, 5]\\n})\\n\\n# ROI計算\\nprojects['年間利益'] = projects['年間収益'] - projects['年間コスト']\\nprojects['総利益'] = projects['年間利益'] * projects['投資期間']\\nprojects['ROI(%)'] = ((projects['総利益'] - projects['初期投資']) / projects['初期投資'] * 100).round(2)\\nprojects['回収期間'] = (projects['初期投資'] / projects['年間利益']).round(1)\\n\\n# NPV計算（割引率5%）\\ndiscount_rate = 0.05\\ndef calculate_npv(initial_investment, annual_profit, years, rate):\\n    npv = -initial_investment\\n    for year in range(1, years + 1):\\n        npv += annual_profit / (1 + rate) ** year\\n    return npv\\n\\nprojects['NPV'] = projects.apply(\\n    lambda row: calculate_npv(row['初期投資'], row['年間利益'], row['投資期間'], discount_rate),\\n    axis=1\\n).round(0)\\n\\n# 投資効率スコア\\nprojects['投資効率スコア'] = (\\n    (projects['ROI(%)'] / projects['ROI(%)'].max() * 40) +\\n    (projects['NPV'] / projects['NPV'].max() * 30) +\\n    ((5 - projects['回収期間']) / 5 * 30)\\n).round(1)\\n\\nprint('ROI分析結果:')\\nprint(projects[['プロジェクト名', 'ROI(%)', '回収期間', 'NPV', '投資効率スコア']].to_string(index=False))\\n\\n# 投資推奨度判定\\ndef get_recommendation(row):\\n    if row['ROI(%)'] > 50 and row['NPV'] > 0 and row['回収期間'] < 3:\\n        return '強く推奨'\\n    elif row['ROI(%)'] > 20 and row['NPV'] > 0 and row['回収期間'] < 4:\\n        return '推奨'\\n    elif row['ROI(%)'] > 0 and row['NPV'] > 0:\\n        return '検討可能'\\n    else:\\n        return '非推奨'\\n\\nprojects['推奨度'] = projects.apply(get_recommendation, axis=1)\\n\\nprint('\\n投資推奨度:')\\nfor _, project in projects.iterrows():\\n    print(f'{project[\"プロジェクト名\"]}: {project[\"推奨度\"]} (ROI: {project[\"ROI(%)\"]:.1f}%, 回収: {project[\"回収期間\"]}年)')\\n\\n# ベストプロジェクト\\nbest_project = projects.loc[projects['投資効率スコア'].idxmax()]\\nprint(f'\\n🏆 最優先プロジェクト: {best_project[\"プロジェクト名\"]}')\\nprint(f'   投資効率スコア: {best_project[\"投資効率スコア\"]}点')\\nprint(f'   ROI: {best_project[\"ROI(%)\"]:.1f}%')\\nprint(f'   回収期間: {best_project[\"回収期間\"]}年')\\n\\nprint('\\n=== ROI計算完了 ===')",
        "libraries": "pandas、numpy、datetime",
        "explanation": "投資プロジェクトのROI、NPV、回収期間を計算し、投資判断をサポートします。",
        "benefits": ["投資判断の定量化", "リスク評価", "資源配分最適化", "投資効率向上"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでROI計算ツールのコードを作成してください。投資コストとリターンからROI、NPV、回収期間を計算し、投資判断を支援するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 38,
        "category": "ビジネス分析",
        "number": "38/100",
        "title": "データ可視化システム",
        "desc": "複雑なデータを分かりやすくグラフ化",
        "how_to": "matplotlib、seaborn、plotlyを使って様々なタイプのグラフを自動生成し、データの特徴を視覚化します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nimport matplotlib.pyplot as plt\\nimport seaborn as sns\\nfrom datetime import datetime, timedelta\\n\\nprint('=== データ可視化システム ===')\\n\\n# ビジネスデータ（サンプル）\\nnp.random.seed(42)\\nbusiness_data = pd.DataFrame({\\n    '月': pd.date_range('2024-01-01', periods=12, freq='M'),\\n    '売上': np.random.normal(1000000, 200000, 12).astype(int),\\n    '利益': np.random.normal(200000, 50000, 12).astype(int),\\n    '顧客数': np.random.normal(500, 100, 12).astype(int),\\n    '新規顧客': np.random.normal(50, 15, 12).astype(int)\\n})\\n\\n# 利益率計算\\nbusiness_data['利益率'] = (business_data['利益'] / business_data['売上'] * 100).round(1)\\nbusiness_data['顧客単価'] = (business_data['売上'] / business_data['顧客数']).round(0)\\n\\n# 1. 売上・利益推移グラフ\\nfig, axes = plt.subplots(2, 2, figsize=(15, 12))\\n\\n# 売上推移\\naxes[0,0].plot(business_data['月'], business_data['売上'], marker='o', color='blue', linewidth=2)\\naxes[0,0].set_title('月別売上推移')\\naxes[0,0].set_ylabel('売上（円）')\\naxes[0,0].tick_params(axis='x', rotation=45)\\naxes[0,0].grid(True, alpha=0.3)\\n\\n# 利益率推移\\naxes[0,1].bar(range(len(business_data)), business_data['利益率'], color='green', alpha=0.7)\\naxes[0,1].set_title('月別利益率')\\naxes[0,1].set_ylabel('利益率（%）')\\naxes[0,1].set_xlabel('月')\\naxes[0,1].grid(True, alpha=0.3)\\n\\n# 顧客数推移\\naxes[1,0].fill_between(range(len(business_data)), business_data['顧客数'], alpha=0.6, color='orange')\\naxes[1,0].plot(range(len(business_data)), business_data['顧客数'], marker='s', color='red')\\naxes[1,0].set_title('月別顧客数推移')\\naxes[1,0].set_ylabel('顧客数（人）')\\naxes[1,0].set_xlabel('月')\\naxes[1,0].grid(True, alpha=0.3)\\n\\n# 売上vs利益散布図\\naxes[1,1].scatter(business_data['売上'], business_data['利益'], s=business_data['顧客数']/5, alpha=0.6, color='purple')\\naxes[1,1].set_title('売上vs利益（バブルサイズ=顧客数）')\\naxes[1,1].set_xlabel('売上（円）')\\naxes[1,1].set_ylabel('利益（円）')\\naxes[1,1].grid(True, alpha=0.3)\\n\\nplt.tight_layout()\\nplt.show()\\n\\n# 統計サマリー\\nprint('\\nビジネス指標サマリー:')\\nsummary_stats = business_data[['売上', '利益', '利益率', '顧客数', '顧客単価']].describe().round(0)\\nprint(summary_stats)\\n\\n# トレンド分析\\nprint('\\nトレンド分析:')\\nsales_trend = np.polyfit(range(len(business_data)), business_data['売上'], 1)[0]\\nprofit_trend = np.polyfit(range(len(business_data)), business_data['利益'], 1)[0]\\ncustomer_trend = np.polyfit(range(len(business_data)), business_data['顧客数'], 1)[0]\\n\\nprint(f'売上トレンド: {\"増加\" if sales_trend > 0 else \"減少\"} (月平均 {abs(sales_trend):,.0f}円)')\\nprint(f'利益トレンド: {\"増加\" if profit_trend > 0 else \"減少\"} (月平均 {abs(profit_trend):,.0f}円)')\\nprint(f'顧客数トレンド: {\"増加\" if customer_trend > 0 else \"減少\"} (月平均 {abs(customer_trend):.0f}人)')\\n\\n# パフォーマンス評価\\nbest_month = business_data.loc[business_data['売上'].idxmax(), '月'].strftime('%Y年%m月')\\nworst_month = business_data.loc[business_data['売上'].idxmin(), '月'].strftime('%Y年%m月')\\n\\nprint(f'\\n📈 最高売上月: {best_month} ({business_data[\"売上\"].max():,}円)')\\nprint(f'📉 最低売上月: {worst_month} ({business_data[\"売上\"].min():,}円)')\\n\\nprint('\\n=== データ可視化完了 ===')",
        "libraries": "pandas、numpy、matplotlib、seaborn、datetime",
        "explanation": "複雑なビジネスデータを様々なグラフで視覚化し、データの特徴や傾向を分かりやすく表示します。",
        "benefits": ["データの直感的理解", "意思決定の迅速化", "プレゼンテーション品質向上", "異常値の発見"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonでデータ可視化システムのコードを作成してください。matplotlib、seabornを使って売上、利益、顧客数などのビジネスデータを様々なグラフで視覚化するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 39,
        "category": "ビジネス分析",
        "number": "39/100",
        "title": "KPI自動レポート",
        "desc": "重要指標を自動集計・レポート化",
        "how_to": "各部門のKPIデータを自動集計し、達成率や前月比を計算してレポート形式で出力します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime, timedelta\\nimport matplotlib.pyplot as plt\\n\\nprint('=== KPI自動レポートシステム ===')\\n\\n# KPIデータ（サンプル）\\nkpi_data = pd.DataFrame({\\n    'KPI項目': ['月間売上', '新規顧客獲得', '顧客満足度', 'リピート率', 'コンバージョン率', '営業効率', 'マーケティングROI', 'カスタマーサポート満足度'],\\n    '目標値': [10000000, 100, 4.5, 65, 3.2, 85, 300, 4.3],\\n    '実績値': [11200000, 85, 4.2, 72, 3.8, 78, 280, 4.1],\\n    '前月実績': [9800000, 92, 4.1, 68, 3.1, 82, 250, 4.0],\\n    '単位': ['円', '人', '点', '%', '%', '%', '%', '点'],\\n    '担当部門': ['営業', 'マーケティング', 'CS', '営業', 'マーケティング', '営業', 'マーケティング', 'CS']\\n})\\n\\n# KPI達成率計算\\nkpi_data['達成率'] = (kpi_data['実績値'] / kpi_data['目標値'] * 100).round(1)\\nkpi_data['前月比'] = ((kpi_data['実績値'] - kpi_data['前月実績']) / kpi_data['前月実績'] * 100).round(1)\\n\\n# 達成度判定\\ndef get_achievement_status(rate):\\n    if rate >= 100:\\n        return '達成 ✅'\\n    elif rate >= 90:\\n        return '概ね達成 🟡'\\n    elif rate >= 80:\\n        return '要改善 🟠'\\n    else:\\n        return '未達成 ❌'\\n\\nkpi_data['達成状況'] = kpi_data['達成率'].apply(get_achievement_status)\\n\\n# 前月比トレンド\\ndef get_trend(change):\\n    if change > 5:\\n        return '大幅改善 📈'\\n    elif change > 0:\\n        return '改善 ↗️'\\n    elif change > -5:\\n        return '横ばい ➡️'\\n    else:\\n        return '悪化 📉'\\n\\nkpi_data['トレンド'] = kpi_data['前月比'].apply(get_trend)\\n\\nprint('📊 KPI達成状況レポート')\\nprint('=' * 80)\\nprint(f'レポート作成日時: {datetime.now().strftime(\"%Y年%m月%d日 %H:%M\")}')\\nprint()\\n\\n# 全体サマリー\\ntotal_kpis = len(kpi_data)\\nachieved_kpis = len(kpi_data[kpi_data['達成率'] >= 100])\\nnearly_achieved = len(kpi_data[(kpi_data['達成率'] >= 90) & (kpi_data['達成率'] < 100)])\\nneeds_improvement = total_kpis - achieved_kpis - nearly_achieved\\n\\nprint('🎯 全体サマリー:')\\nprint(f'   達成: {achieved_kpis}項目 ({achieved_kpis/total_kpis*100:.1f}%)')\\nprint(f'   概ね達成: {nearly_achieved}項目 ({nearly_achieved/total_kpis*100:.1f}%)')\\nprint(f'   要改善: {needs_improvement}項目 ({needs_improvement/total_kpis*100:.1f}%)')\\nprint()\\n\\n# 詳細KPIレポート\\nprint('📈 詳細KPI分析:')\\nfor _, kpi in kpi_data.iterrows():\\n    print(f'\\n【{kpi[\"KPI項目\"]}】({kpi[\"担当部門\"]})\\n'\\\n          f'  目標: {kpi[\"目標値\"]:,}{kpi[\"単位\"]} | 実績: {kpi[\"実績値\"]:,}{kpi[\"単位\"]}\\n'\\\n          f'  達成率: {kpi[\"達成率\"]}% ({kpi[\"達成状況\"]})\\n'\\\n          f'  前月比: {kpi[\"前月比\"]:+.1f}% ({kpi[\"トレンド\"]})')\\n\\n# 部門別サマリー\\nprint('\\n🏢 部門別達成状況:')\\ndept_summary = kpi_data.groupby('担当部門').agg({\\n    '達成率': 'mean',\\n    '前月比': 'mean',\\n    'KPI項目': 'count'\\n}).round(1)\\ndept_summary.columns = ['平均達成率', '平均前月比', 'KPI数']\\n\\nfor dept, data in dept_summary.iterrows():\\n    status = get_achievement_status(data['平均達成率'])\\n    trend = get_trend(data['平均前月比'])\\n    print(f'  {dept}: 達成率{data[\"平均達成率\"]}% ({status}) | 前月比{data[\"平均前月比\"]:+.1f}% ({trend})')\\n\\n# 注目ポイント\\nprint('\\n🔍 注目ポイント:')\\n\\n# 最高達成率\\nbest_kpi = kpi_data.loc[kpi_data['達成率'].idxmax()]\\nprint(f'✨ 最高達成率: {best_kpi[\"KPI項目\"]} ({best_kpi[\"達成率\"]}%)')\\n\\n# 最大改善\\nbest_improvement = kpi_data.loc[kpi_data['前月比'].idxmax()]\\nprint(f'📈 最大改善: {best_improvement[\"KPI項目\"]} (前月比+{best_improvement[\"前月比\"]}%)')\\n\\n# 要注意項目\\nworst_kpi = kpi_data.loc[kpi_data['達成率'].idxmin()]\\nif worst_kpi['達成率'] < 90:\\n    print(f'⚠️  要注意: {worst_kpi[\"KPI項目\"]} (達成率{worst_kpi[\"達成率\"]}%)')\\n\\nprint('\\n=== KPI自動レポート完了 ===')",
        "libraries": "pandas、numpy、datetime、matplotlib",
        "explanation": "各部門のKPIを自動集計し、達成状況や前月比を分析してレポート形式で出力します。",
        "benefits": ["KPI管理の自動化", "経営状況の可視化", "部門別パフォーマンス比較", "意思決定の迅速化"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "PythonでKPI自動レポートのコードを作成してください。各部門のKPIデータを集計し、達成率、前月比、トレンド分析を行ってレポート形式で出力するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    },
    {
        "id": 40,
        "category": "ビジネス分析",
        "number": "40/100",
        "title": "予算管理システム",
        "desc": "予算執行状況を自動監視",
        "how_to": "各部門の予算と実績を比較し、執行率や残予算を自動計算して予算オーバーの警告を出します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime, timedelta\\nimport matplotlib.pyplot as plt\\n\\nprint('=== 予算管理システム ===')\\n\\n# 予算データ（サンプル）\\nbudget_data = pd.DataFrame({\\n    '部門': ['営業部', 'マーケティング部', '開発部', '人事部', '総務部', '経理部'],\\n    '年間予算': [50000000, 30000000, 80000000, 20000000, 15000000, 10000000],\\n    '上半期予算': [25000000, 15000000, 40000000, 10000000, 7500000, 5000000],\\n    '上半期実績': [28000000, 12000000, 42000000, 8500000, 6800000, 4200000],\\n    '7月実績': [4200000, 2800000, 7200000, 1400000, 1200000, 800000],\\n    '8月実績': [4500000, 3200000, 6800000, 1600000, 1100000, 750000],\\n    '予算項目': ['営業活動費', '広告宣伝費', 'システム開発費', '人件費', '事務用品費', '会計システム費']\\n})\\n\\n# 現在までの実績計算\\nbudget_data['累計実績'] = budget_data['上半期実績'] + budget_data['7月実績'] + budget_data['8月実績']\\nbudget_data['8月末予定予算'] = budget_data['年間予算'] * (8/12)  # 8ヶ月分\\nbudget_data['執行率'] = (budget_data['累計実績'] / budget_data['8月末予定予算'] * 100).round(1)\\nbudget_data['残予算'] = budget_data['年間予算'] - budget_data['累計実績']\\nbudget_data['予算達成ペース'] = (budget_data['累計実績'] / budget_data['年間予算'] * 100).round(1)\\n\\n# 予算ステータス判定\\ndef get_budget_status(execution_rate, pace):\\n    if execution_rate > 110:\\n        return '予算超過 🚨'\\n    elif execution_rate > 100:\\n        return '予算オーバー ⚠️'\\n    elif execution_rate > 90:\\n        return '適正 ✅'\\n    elif execution_rate > 70:\\n        return '順調 🟢'\\n    else:\\n        return '未執行 🔵'\\n\\nbudget_data['ステータス'] = budget_data.apply(lambda x: get_budget_status(x['執行率'], x['予算達成ペース']), axis=1)\\n\\n# 月次実績計算\\nbudget_data['7月執行率'] = (budget_data['7月実績'] / (budget_data['年間予算']/12) * 100).round(1)\\nbudget_data['8月執行率'] = (budget_data['8月実績'] / (budget_data['年間予算']/12) * 100).round(1)\\n\\nprint('💰 予算執行状況レポート')\\nprint('=' * 80)\\nprint(f'集計期間: 2024年1月〜8月 (レポート作成: {datetime.now().strftime(\"%Y/%m/%d %H:%M\")})')\\nprint()\\n\\n# 全体サマリー\\ntotal_budget = budget_data['年間予算'].sum()\\ntotal_actual = budget_data['累計実績'].sum()\\noverall_execution_rate = (total_actual / (total_budget * 8/12) * 100)\\n\\nprint('📊 全体サマリー:')\\nprint(f'   年間総予算: {total_budget:,}円')\\nprint(f'   8月末累計実績: {total_actual:,}円')\\nprint(f'   全体執行率: {overall_execution_rate:.1f}%')\\nprint(f'   残予算: {total_budget - total_actual:,}円')\\nprint()\\n\\n# 部門別詳細\\nprint('🏢 部門別執行状況:')\\nfor _, dept in budget_data.iterrows():\\n    print(f'\\n【{dept[\"部門\"]}】')\\n    print(f'  年間予算: {dept[\"年間予算\"]:,}円 | 累計実績: {dept[\"累計実績\"]:,}円')\\n    print(f'  執行率: {dept[\"執行率\"]}% | ステータス: {dept[\"ステータス\"]}')\\n    print(f'  残予算: {dept[\"残予算\"]:,}円 | 予算項目: {dept[\"予算項目\"]}')\\n    \\n    # 月別実績\\n    print(f'  月別実績: 7月 {dept[\"7月実績\"]:,}円({dept[\"7月執行率\"]}%) | 8月 {dept[\"8月実績\"]:,}円({dept[\"8月執行率\"]}%)')\\n\\n# アラート・注意事項\\nprint('\\n🚨 予算アラート:')\\nover_budget = budget_data[budget_data['執行率'] > 100]\\nif not over_budget.empty:\\n    for _, dept in over_budget.iterrows():\\n        over_amount = dept['累計実績'] - dept['8月末予定予算']\\n        print(f'⚠️  {dept[\"部門\"]}: 予定予算を{over_amount:,}円超過 (執行率{dept[\"執行率\"]}%)')\\nelse:\\n    print('✅ 現在、予算超過の部門はありません')\\n\\n# 推奨アクション\\nprint('\\n💡 推奨アクション:')\\nlow_execution = budget_data[budget_data['執行率'] < 70]\\nhigh_execution = budget_data[budget_data['執行率'] > 90]\\n\\nif not low_execution.empty:\\n    print('📈 執行促進が必要:')\\n    for _, dept in low_execution.iterrows():\\n        print(f'   - {dept[\"部門\"]}: 執行率{dept[\"執行率\"]}% (計画的な予算執行を検討)')\\n\\nif not high_execution.empty:\\n    print('⚠️  執行監視が必要:')\\n    for _, dept in high_execution.iterrows():\\n        remaining_months = 4  # 9-12月\\n        monthly_remaining = dept['残予算'] / remaining_months\\n        print(f'   - {dept[\"部門\"]}: 残り4ヶ月で月平均{monthly_remaining:,.0f}円の執行計画が必要')\\n\\n# 年末予測\\nprint('\\n🔮 年末予算執行予測:')\\ncurrent_pace = budget_data['累計実績'] / (8/12)  # 年間ペース\\nbudget_data['年末予測執行額'] = current_pace.round(0)\\nbudget_data['年末予測執行率'] = (budget_data['年末予測執行額'] / budget_data['年間予算'] * 100).round(1)\\n\\nfor _, dept in budget_data.iterrows():\\n    status = '予算超過' if dept['年末予測執行率'] > 100 else '適正' if dept['年末予測執行率'] > 90 else '未達'\\n    print(f'{dept[\"部門\"]}: {dept[\"年末予測執行率\"]}% ({status})')\\n\\nprint('\\n=== 予算管理システム完了 ===')",
        "libraries": "pandas、numpy、datetime、matplotlib",
        "explanation": "各部門の予算執行状況を監視し、予算オーバーの警告や未執行の改善提案を自動で行います。",
        "benefits": ["予算管理の自動化", "予算超過の早期発見", "部門別執行状況の可視化", "予算計画の精度向上"],
        "time_required": "2-3時間",
        "difficulty": "中級",
        "ai_prompt": "Pythonで予算管理システムのコードを作成してください。各部門の予算と実績を比較し、執行率や残予算を計算して予算オーバーの警告を出すコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    }
]

# 残りのツールを追加（マーケティング、営業・顧客管理、人事・労務、データ処理・分析、ファイル・文書管理、自動化・効率化、リスク・品質管理）
additional_tools = [
    # マーケティング（9ツール）
    {
        "id": 41,
        "category": "マーケティング",
        "number": "41/100",
        "title": "顧客セグメンテーション",
        "desc": "顧客を属性別に自動分類",
        "how_to": "顧客データをRFM分析やクラスタリング手法で分析し、属性別にセグメント化します。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom sklearn.cluster import KMeans\\nfrom sklearn.preprocessing import StandardScaler\\nimport matplotlib.pyplot as plt\\n\\nprint('=== 顧客セグメンテーションシステム ===')\\n\\n# 顧客データ（サンプル）\\ncustomer_data = pd.DataFrame({\\n    '顧客ID': [f'C{i:03d}' for i in range(1, 101)],\\n    '年齢': np.random.normal(40, 15, 100).astype(int),\\n    '年収': np.random.normal(5000000, 1500000, 100).astype(int),\\n    '購入回数': np.random.poisson(5, 100),\\n    '総購入金額': np.random.gamma(2, 50000, 100).astype(int),\\n    '最終購入日': pd.date_range(end='2024-07-25', periods=100, freq='-1D')[::-1]\\n})\\n\\n# RFM分析\\nbase_date = pd.Timestamp('2024-07-25')\\ncustomer_data['Recency'] = (base_date - customer_data['最終購入日']).dt.days\\ncustomer_data['Frequency'] = customer_data['購入回数']\\ncustomer_data['Monetary'] = customer_data['総購入金額']\\n\\n# データ標準化\\nscaler = StandardScaler()\\nrfm_scaled = scaler.fit_transform(customer_data[['Recency', 'Frequency', 'Monetary']])\\n\\n# K-meansクラスタリング\\nkmeans = KMeans(n_clusters=4, random_state=42)\\ncustomer_data['セグメント'] = kmeans.fit_predict(rfm_scaled)\\n\\n# セグメント名付け\\nsegment_names = {\\n    0: 'ロイヤル顧客',\\n    1: '優良顧客', \\n    2: '新規顧客',\\n    3: '離反リスク顧客'\\n}\\ncustomer_data['セグメント名'] = customer_data['セグメント'].map(segment_names)\\n\\n# セグメント別統計\\nprint('顧客セグメント分析結果:')\\nsegment_stats = customer_data.groupby('セグメント名').agg({\\n    '顧客ID': 'count',\\n    'Recency': 'mean',\\n    'Frequency': 'mean', \\n    'Monetary': 'mean',\\n    '年齢': 'mean',\\n    '年収': 'mean'\\n}).round(1)\\nsegment_stats.columns = ['顧客数', '平均経過日数', '平均購入回数', '平均購入金額', '平均年齢', '平均年収']\\nprint(segment_stats)\\n\\n# 各セグメントの特徴\\nprint('\\n📊 セグメント別特徴:')\\nfor segment, stats in segment_stats.iterrows():\\n    percentage = stats['顧客数'] / len(customer_data) * 100\\n    print(f'\\n【{segment}】({stats[\"顧客数\"]:.0f}人, {percentage:.1f}%)')\\n    print(f'  平均購入: {stats[\"平均購入回数\"]:.1f}回, {stats[\"平均購入金額\"]:,.0f}円')\\n    print(f'  最終購入: {stats[\"平均経過日数\"]:.0f}日前, 平均年齢: {stats[\"平均年齢\"]:.0f}歳')\\n\\n# マーケティング戦略提案\\nprint('\\n💡 セグメント別マーケティング戦略:')\\nstrategies = {\\n    'ロイヤル顧客': '【維持戦略】プレミアムサービス、限定オファー、VIP待遇',\\n    '優良顧客': '【育成戦略】アップセル、クロスセル、ポイント特典',\\n    '新規顧客': '【獲得戦略】ウェルカムキャンペーン、チュートリアル、初回割引',\\n    '離反リスク顧客': '【復活戦略】リテンション施策、特別割引、パーソナライズ'\\n}\\n\\nfor segment, strategy in strategies.items():\\n    count = len(customer_data[customer_data['セグメント名'] == segment])\\n    if count > 0:\\n        print(f'{segment}: {strategy}')\\n\\nprint('\\n=== 顧客セグメンテーション完了 ===')",
        "libraries": "pandas、numpy、scikit-learn、matplotlib",
        "explanation": "顧客データをクラスタリング分析し、効果的なマーケティング戦略を立案するためのセグメント化を行います。",
        "benefits": ["ターゲティング精度向上", "マーケティング効率化", "顧客理解深化", "個別戦略立案"],
        "time_required": "3-4時間",
        "difficulty": "上級",
        "ai_prompt": "Python で顧客セグメンテーションのコードを作成してください。RFM分析とK-meansクラスタリングを使って顧客を分類し、各セグメントの特徴とマーケティング戦略を提案するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    }
]

# additional_toolsをEXTRA_TOOLSに追加
EXTRA_TOOLS.extend(additional_tools)

# 残りの59ツールも同様に詳細に定義...（スペースの関係で一部のみ表示）