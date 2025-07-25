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

for tool_def in tool_definitions:
    tool = {
        "id": tool_def["id"],
        "category": tool_def["category"],
        "number": f"{tool_def['id']}/100",
        "title": tool_def["title"],
        "desc": tool_def["desc"],
        "how_to": f"{tool_def['desc']}により業務効率を向上させます。",
        "sample_code": f"import pandas as pd\\nimport numpy as np\\nfrom datetime import datetime\\n\\nprint('=== {tool_def['title']} ===')\\n\\n# サンプルデータ作成\\ndata = pd.DataFrame({{'ID': [1, 2, 3], 'Value': [100, 200, 300]}})\\nprint('処理開始...')\\nprint(data)\\nprint('\\n処理完了！')\\nprint(f'=== {tool_def['title']}完了 ===')",
        "libraries": "pandas、numpy、datetime（標準ライブラリ）",
        "explanation": f"{tool_def['desc']}により業務効率を向上させます。",
        "benefits": ["業務効率化", "時間短縮", "正確性向上", "コスト削減"],
        "time_required": "1-2時間",
        "difficulty": "中級",
        "ai_prompt": f"{tool_def['title']}のPythonコードを作成してください。{tool_def['desc']}を実現するコードを初心者でも理解できるように詳しいコメント付きで書いてください。"
    }
    EXTRA_TOOLS.append(tool)