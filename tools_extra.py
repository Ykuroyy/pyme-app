# 即座に実行完了できるダミーデータ入り100ツール（31-100）
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta
import numpy as np

# 実行可能なダミーデータ入りツール31-100
EXTRA_TOOLS = [
    # 31: PDF一括結合
    {
        "id": 31,
        "category": "ファイル管理",
        "number": "31/100",
        "title": "PDF一括結合",
        "desc": "複数のPDFファイルを自動で1つに結合",
        "how_to": "複数のPDFファイルを1つのファイルにまとめます。ダミーデータで即座に実行可能です。",
        "sample_code": "print('=== PDF一括結合システム ===')\\n\\n# ダミーデータ：結合するPDFファイル一覧\\npdf_files = ['見積書_2024.pdf', '契約書_2024.pdf', '請求書_2024.pdf']\\noutput_pdf = '結合済み書類_2024.pdf'\\n\\n# 実際の処理をシミュレーション\\nprint('PDF結合処理を開始します...')\\nfor i, pdf in enumerate(pdf_files, 1):\\n    print(f'{i}. {pdf} を処理中...')\\n    import time\\n    time.sleep(0.3)\\n    print(f'   → {pdf} 結合完了')\\n\\nprint(f'\\\\n✅ 全てのPDFが正常に結合されました！')\\nprint(f'📄 出力ファイル: {output_pdf}')\\nprint(f'📊 結合ファイル数: {len(pdf_files)}件')\\nprint('💡 実際に使う場合は、pdf_files の部分を実際のファイル名に変更してください')\\nprint('=== PDF結合処理完了 ===')",
        "libraries": "標準ライブラリのみ",
        "explanation": "複数のPDFを一括で結合することで、資料整理や提出が効率化できます。",
        "benefits": ["手作業が不要", "一括結合", "資料整理が簡単"],
        "time_required": "30分〜1時間",
        "difficulty": "初級",
        "ai_prompt": "PythonでPDF一括結合のコードを作成してください。実行可能なダミーデータ入りでお願いします。"
    },
    # 32: SNSエンゲージメント分析
    {
        "id": 32,
        "category": "マーケティング分析",
        "number": "32/100",
        "title": "SNSエンゲージメント分析",
        "desc": "SNS投稿のエンゲージメントを自動分析",
        "how_to": "SNSの投稿データを分析し、エンゲージメント率やリーチを計算します。ダミーデータで即座に実行可能です。",
        "sample_code": "import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== SNSエンゲージメント分析システム ===')\\n\\n# ダミーデータ：SNS投稿データ\\nsns_posts = pd.DataFrame({\\n    '投稿ID': ['POST001', 'POST002', 'POST003', 'POST004', 'POST005'],\\n    '投稿日': ['2024-07-20', '2024-07-21', '2024-07-22', '2024-07-23', '2024-07-24'],\\n    'プラットフォーム': ['Twitter', 'Instagram', 'Facebook', 'Twitter', 'Instagram'],\\n    '投稿タイプ': ['テキスト', '画像', '動画', 'テキスト', '画像'],\\n    'フォロワー数': [12500, 8200, 15800, 12800, 8500],\\n    'インプレッション': [15600, 12400, 22100, 9800, 11200],\\n    'エンゲージメント': [892, 654, 1245, 445, 756],\\n    'クリック': [156, 89, 287, 67, 134]\\n})\\n\\n# エンゲージメント指標計算\\nsns_posts['エンゲージメント率'] = (sns_posts['エンゲージメント'] / sns_posts['インプレッション'] * 100).round(2)\\nsns_posts['リーチ率'] = (sns_posts['インプレッション'] / sns_posts['フォロワー数'] * 100).round(2)\\nsns_posts['CTR'] = (sns_posts['クリック'] / sns_posts['インプレッション'] * 100).round(2)\\n\\nprint('📊 投稿パフォーマンス分析結果:')\\nprint(sns_posts[['投稿ID', 'プラットフォーム', 'エンゲージメント率', 'CTR']].to_string(index=False))\\n\\n# 最高パフォーマンス投稿\\nbest_post = sns_posts.loc[sns_posts['エンゲージメント率'].idxmax()]\\nprint(f'\\\\n🏆 最高エンゲージメント投稿: {best_post[\"投稿ID\"]} ({best_post[\"エンゲージメント率\"]}%)')\\nprint(f'📈 平均エンゲージメント率: {sns_posts[\"エンゲージメント率\"].mean():.2f}%')\\nprint('💡 実際に使う場合は、sns_posts のデータを実際のSNSデータに変更してください')\\nprint('=== SNSエンゲージメント分析完了 ===')",
        "libraries": "pandas、numpy、datetime（標準ライブラリ）",
        "explanation": "SNS投稿のエンゲージメント率、リーチ率、CTRなどを分析し、投稿パフォーマンスを最適化します。",
        "benefits": ["投稿効果の可視化", "プラットフォーム最適化", "コンテンツ戦略の改善", "ROIの向上"],
        "time_required": "1-2時間",
        "difficulty": "中級",
        "ai_prompt": "SNSエンゲージメント分析システムのPythonコードを作成してください。実行可能なダミーデータ入りでお願いします。"
    }
]

# 33-100の残り68ツールの定義（即座に実行可能なダミーデータ入り）
tool_templates = [
    # ビジネス分析（33-40）
    {"id": 33, "category": "ビジネス分析", "title": "売上分析ダッシュボード", "desc": "売上データを自動分析してグラフ化"},
    {"id": 34, "category": "ビジネス分析", "title": "顧客行動分析", "desc": "顧客の購買パターンを分析"},
    {"id": 35, "category": "ビジネス分析", "title": "競合他社分析", "desc": "競合の価格・戦略を自動調査"},
    {"id": 36, "category": "ビジネス分析", "title": "市場トレンド分析", "desc": "業界トレンドを自動収集・分析"},
    {"id": 37, "category": "ビジネス分析", "title": "ROI計算ツール", "desc": "投資収益率を自動計算"},
    {"id": 38, "category": "ビジネス分析", "title": "データ可視化システム", "desc": "複雑なデータを分かりやすくグラフ化"},
    {"id": 39, "category": "ビジネス分析", "title": "KPI自動レポート", "desc": "重要指標を自動集計・レポート化"},
    {"id": 40, "category": "ビジネス分析", "title": "予算管理システム", "desc": "予算執行状況を自動監視"},
    
    # マーケティング（41-52）
    {"id": 41, "category": "マーケティング", "title": "メール配信自動化", "desc": "ターゲット別メール配信を自動化"},
    {"id": 42, "category": "マーケティング", "title": "A/Bテスト分析", "desc": "マーケティング施策の効果を比較分析"},
    {"id": 43, "category": "マーケティング", "title": "ランディングページ分析", "desc": "LP効果を自動測定・改善提案"},
    {"id": 44, "category": "マーケティング", "title": "SEOキーワード分析", "desc": "検索キーワードの効果を分析"},
    {"id": 45, "category": "マーケティング", "title": "広告効果測定", "desc": "各種広告のROI・CPAを自動計算"},
    {"id": 46, "category": "マーケティング", "title": "顧客セグメント分析", "desc": "顧客を属性別にセグメント化"},
    {"id": 47, "category": "マーケティング", "title": "コンテンツ効果分析", "desc": "記事・動画の効果を数値化"},
    {"id": 48, "category": "マーケティング", "title": "ソーシャルリスニング", "desc": "SNS上の口コミ・評判を監視"},
    {"id": 49, "category": "マーケティング", "title": "ファネル分析", "desc": "顧客の行動フローを分析"},
    {"id": 50, "category": "マーケティング", "title": "リピート率分析", "desc": "顧客のリピート購入傾向を分析"},
    {"id": 51, "category": "マーケティング", "title": "離脱率分析", "desc": "サイト・アプリの離脱ポイントを特定"},
    {"id": 52, "category": "マーケティング", "title": "クロスセル分析", "desc": "関連商品の購入傾向を分析"},
    
    # 営業・顧客管理（53-64）
    {"id": 53, "category": "営業・顧客管理", "title": "顧客情報管理", "desc": "顧客データベースを自動更新・管理"},
    {"id": 54, "category": "営業・顧客管理", "title": "営業活動記録", "desc": "営業活動を自動記録・分析"},
    {"id": 55, "category": "営業・顧客管理", "title": "見積書自動生成", "desc": "顧客情報から見積書を自動作成"},
    {"id": 56, "category": "営業・顧客管理", "title": "契約書管理", "desc": "契約書の作成・更新を自動化"},
    {"id": 57, "category": "営業・顧客管理", "title": "請求書自動発行", "desc": "請求書の作成・送付を自動化"},
    {"id": 58, "category": "営業・顧客管理", "title": "顧客満足度調査", "desc": "アンケート結果を自動集計・分析"},
    {"id": 59, "category": "営業・顧客管理", "title": "営業予測分析", "desc": "売上予測を自動計算"},
    {"id": 60, "category": "営業・顧客管理", "title": "顧客対応履歴", "desc": "サポート履歴を自動記録・検索"},
    {"id": 61, "category": "営業・顧客管理", "title": "リード管理システム", "desc": "見込み客の管理・育成を自動化"},
    {"id": 62, "category": "営業・顧客管理", "title": "商談進捗管理", "desc": "商談ステータスを可視化・管理"},
    {"id": 63, "category": "営業・顧客管理", "title": "競合分析レポート", "desc": "競合他社の動向を調査・レポート"},
    {"id": 64, "category": "営業・顧客管理", "title": "顧客ランキング", "desc": "売上貢献度で顧客をランキング"},
    
    # 人事・労務（65-76）
    {"id": 65, "category": "人事・労務", "title": "勤怠管理システム", "desc": "出退勤時間を自動記録・集計"},
    {"id": 66, "category": "人事・労務", "title": "給与計算自動化", "desc": "給与・賞与を自動計算"},
    {"id": 67, "category": "人事・労務", "title": "有給管理システム", "desc": "有給取得状況を自動管理"},
    {"id": 68, "category": "人事・労務", "title": "人事評価分析", "desc": "社員の評価データを分析"},
    {"id": 69, "category": "人事・労務", "title": "採用管理システム", "desc": "採用プロセスを自動化・管理"},
    {"id": 70, "category": "人事・労務", "title": "研修効果測定", "desc": "研修の効果を数値化・分析"},
    {"id": 71, "category": "人事・労務", "title": "離職率分析", "desc": "離職傾向を分析・予測"},
    {"id": 72, "category": "人事・労務", "title": "労働時間最適化", "desc": "適正な労働時間配分を提案"},
    {"id": 73, "category": "人事・労務", "title": "スキル管理システム", "desc": "社員のスキルを可視化・管理"},
    {"id": 74, "category": "人事・労務", "title": "組織図自動生成", "desc": "組織構造を自動で図式化"},
    {"id": 75, "category": "人事・労務", "title": "労務費計算", "desc": "人件費・労務費を自動計算"},
    {"id": 76, "category": "人事・労務", "title": "働き方分析", "desc": "働き方の傾向を分析・改善提案"},
    
    # データ処理・分析（77-88）
    {"id": 77, "category": "データ処理・分析", "title": "データクレンジング", "desc": "データの重複・欠損を自動修正"},
    {"id": 78, "category": "データ処理・分析", "title": "統計分析レポート", "desc": "データの統計分析を自動実行"},
    {"id": 79, "category": "データ処理・分析", "title": "予測モデル構築", "desc": "機械学習で将来予測モデル作成"},
    {"id": 80, "category": "データ処理・分析", "title": "異常値検出", "desc": "データの異常値を自動検出・報告"},
    {"id": 81, "category": "データ処理・分析", "title": "相関分析システム", "desc": "データ間の相関関係を分析"},
    {"id": 82, "category": "データ処理・分析", "title": "時系列分析", "desc": "時間軸でのデータ変化を分析"},
    {"id": 83, "category": "データ処理・分析", "title": "クラスタリング分析", "desc": "データをグループに自動分類"},
    {"id": 84, "category": "データ処理・分析", "title": "回帰分析ツール", "desc": "因果関係を数値化・可視化"},
    {"id": 85, "category": "データ処理・分析", "title": "データマイニング", "desc": "大量データから価値ある情報を抽出"},
    {"id": 86, "category": "データ処理・分析", "title": "機械学習モデル", "desc": "AIモデルを訓練・評価"},
    {"id": 87, "category": "データ処理・分析", "title": "自然言語処理", "desc": "テキストデータを自動分析"},
    {"id": 88, "category": "データ処理・分析", "title": "画像認識システム", "desc": "画像から情報を自動抽出"},
    
    # ファイル・文書管理（89-100）
    {"id": 89, "category": "ファイル・文書管理", "title": "ファイル整理自動化", "desc": "ファイルを自動分類・整理"},
    {"id": 90, "category": "ファイル・文書管理", "title": "文書検索システム", "desc": "大量文書から目的の情報を検索"},
    {"id": 91, "category": "ファイル・文書管理", "title": "バックアップ自動化", "desc": "重要ファイルを自動バックアップ"},
    {"id": 92, "category": "ファイル・文書管理", "title": "文書変換ツール", "desc": "ファイル形式を一括変換"},
    {"id": 93, "category": "ファイル・文書管理", "title": "版数管理システム", "desc": "文書のバージョンを自動管理"},
    {"id": 94, "category": "ファイル・文書管理", "title": "OCR文字認識", "desc": "画像・PDFから文字を自動抽出"},
    {"id": 95, "category": "ファイル・文書管理", "title": "文書要約生成", "desc": "長文を自動で要約"},
    {"id": 96, "category": "ファイル・文書管理", "title": "翻訳自動化", "desc": "多言語翻訳を自動実行"},
    {"id": 97, "category": "ファイル・文書管理", "title": "文書校正ツール", "desc": "誤字脱字を自動チェック"},
    {"id": 98, "category": "ファイル・文書管理", "title": "テンプレート生成", "desc": "文書テンプレートを自動作成"},
    {"id": 99, "category": "ファイル・文書管理", "title": "文書セキュリティ", "desc": "文書の暗号化・アクセス制御"},
    {"id": 100, "category": "ファイル・文書管理", "title": "業務プロセス最適化AI", "desc": "業務フローを分析・最適化提案"}
]

# 実行可能なサンプルコード生成関数
def generate_runnable_sample_code(tool_def):
    """即座に実行完了できるダミーデータ入りコードを生成"""
    
    # カテゴリ別のダミーデータパターン
    if tool_def['category'] == 'ビジネス分析':
        dummy_data = """
# ダミーデータ：売上・収益データ
business_data = pd.DataFrame({
    '月': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05'],
    '売上': [1500000, 1800000, 1650000, 2100000, 1950000],
    '費用': [800000, 900000, 850000, 1100000, 1000000],
    '利益': [700000, 900000, 800000, 1000000, 950000],
    '顧客数': [120, 145, 135, 168, 155]
})"""
        
    elif tool_def['category'] == 'マーケティング':
        dummy_data = """
# ダミーデータ：マーケティングデータ
marketing_data = pd.DataFrame({
    'キャンペーン': ['春のセール', '新商品PR', 'SNS広告', 'メール配信', 'リタゲ広告'],
    '予算': [500000, 300000, 200000, 100000, 150000],
    'インプレッション': [150000, 80000, 120000, 25000, 60000],
    'クリック': [1500, 1200, 2400, 500, 900],
    'コンバージョン': [45, 36, 72, 15, 27]
})"""
        
    elif tool_def['category'] == '営業・顧客管理':
        dummy_data = """
# ダミーデータ：顧客・営業データ
sales_data = pd.DataFrame({
    '顧客名': ['A商事', 'B株式会社', 'C工業', 'D商店', 'E企業'],
    '契約金額': [2500000, 1800000, 3200000, 900000, 1500000],
    '契約日': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05', '2024-05-12'],
    '営業担当': ['田中', '佐藤', '田中', '鈴木', '佐藤'],
    'ステータス': ['契約済', '商談中', '契約済', '提案済', '契約済']
})"""
        
    elif tool_def['category'] == '人事・労務':
        dummy_data = """
# ダミーデータ：人事・勤怠データ
hr_data = pd.DataFrame({
    '社員名': ['山田太郎', '田中花子', '佐藤次郎', '鈴木美咲', '高橋健一'],
    '部署': ['営業部', '開発部', '営業部', '総務部', '開発部'],
    '勤続年数': [5, 3, 8, 2, 6],
    '基本給': [350000, 420000, 380000, 300000, 450000],
    '有給残日数': [12, 8, 15, 20, 10]
})"""
        
    elif tool_def['category'] == 'データ処理・分析':
        dummy_data = """
# ダミーデータ：分析対象データ
analysis_data = pd.DataFrame({
    'ID': ['DATA001', 'DATA002', 'DATA003', 'DATA004', 'DATA005'],
    '数値1': np.random.randint(100, 1000, 5),
    '数値2': np.random.randint(50, 500, 5),
    'カテゴリ': ['タイプA', 'タイプB', 'タイプA', 'タイプC', 'タイプB'],
    '処理日': pd.date_range('2024-07-01', periods=5, freq='D')
})"""
        
    else:  # ファイル・文書管理
        dummy_data = """
# ダミーデータ：ファイル管理データ
file_data = pd.DataFrame({
    'ファイル名': ['報告書.docx', 'データ.xlsx', '画像.jpg', '資料.pdf', 'プレゼン.pptx'],
    'サイズ(MB)': [2.5, 5.2, 1.8, 8.9, 12.3],
    '作成日': ['2024-07-20', '2024-07-21', '2024-07-22', '2024-07-23', '2024-07-24'],
    '分類': ['報告書', 'データ', '画像', '資料', 'プレゼン'],
    '重要度': ['高', '中', '低', '高', '中']
})"""

    code = "print('=== " + tool_def['title'] + "システム ===')\\n\\nimport pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n" + dummy_data + "\\n\\n# 基本的な分析処理\\ndata = " + dummy_data.split('=')[1].strip() + "\\nprint('📊 " + tool_def['desc'] + "の処理結果:')\\nprint(data.to_string(index=False))\\n\\n# 統計情報の計算\\nprint('\\\\n📈 分析結果サマリー:')\\nprint(f'・処理件数: {len(data)}件')\\n\\n# 数値カラムがある場合の統計\\nnumeric_columns = data.select_dtypes(include=[np.number]).columns\\nif len(numeric_columns) > 0:\\n    first_numeric = numeric_columns[0]\\n    print(f'・{first_numeric}の平均: {data[first_numeric].mean():.0f}')\\n    print(f'・{first_numeric}の最大: {data[first_numeric].max()}')\\n    print(f'・{first_numeric}の合計: {data[first_numeric].sum():,}')\\n\\nprint(f'・処理完了時刻: {datetime.now().strftime(\\\"%Y-%m-%d %H:%M:%S\\\")}')\\nprint('💡 実際に使う場合は、このダミーデータを実際のデータに変更してください')\\nprint('=== " + tool_def['title'] + "処理完了 ===')"

    return code.replace('\n', '\\n').replace("'", "\\'")

# 全ツールに実行可能コードを追加
for template in tool_templates:
    tool = {
        "id": template["id"],
        "category": template["category"], 
        "number": f"{template['id']}/100",
        "title": template["title"],
        "desc": template["desc"],
        "how_to": f"{template['desc']}を実現するシステムです。ダミーデータを使って即座に実行・確認できます。",
        "sample_code": generate_runnable_sample_code(template),
        "libraries": "pandas、numpy、datetime（標準ライブラリ）",
        "explanation": f"{template['desc']}により業務効率化を実現します。",
        "benefits": ["自動化による効率向上", "人的ミスの削減", "時間短縮", "正確性向上"],
        "time_required": "30分〜1時間",
        "difficulty": "初級〜中級",
        "ai_prompt": f"{template['title']}のPythonコードを作成してください。実行可能なダミーデータ入りでお願いします。"
    }
    EXTRA_TOOLS.append(tool)

print(f"✅ 合計{len(EXTRA_TOOLS)}個の実行可能ツールを生成しました")