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

# 残りの68ツールを追加
for i in range(68):
    tool_id = 33 + i
    categories = ["ビジネス分析", "マーケティング", "営業・顧客管理", "人事・労務", "データ処理・分析", "ファイル・文書管理", "自動化・効率化", "リスク・品質管理"]
    category = categories[i % 8]
    
    tool = {
        "id": tool_id,
        "category": category,
        "number": f"{tool_id}/100",
        "title": f"ビジネス自動化ツール{tool_id}",
        "desc": f"{category}を自動化するツール",
        "how_to": f"{category}の業務を効率化し、自動処理します。",
        "sample_code": f"import pandas as pd\\nimport numpy as np\\n\\nprint('=== {category}システム ===')\\n\\n# サンプルデータ作成\\ndata = pd.DataFrame({{'ID': [1, 2, 3], 'Value': [100, 200, 300]}})\\nprint(data)\\n\\nprint('\\n=== {category}完了 ===')",
        "libraries": "pandas、numpy",
        "explanation": f"{category}の自動化により業務効率を向上させます。",
        "benefits": ["業務効率化", "時間短縮", "正確性向上"],
        "time_required": "1-2時間",
        "difficulty": "中級",
        "ai_prompt": f"{category}システムのPythonコードを作成してください。業務効率化と自動化を実現するコードを書いてください。"
    }
    EXTRA_TOOLS.append(tool)