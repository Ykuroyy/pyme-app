import os
import pandas as pd
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import numpy as np
from datetime import datetime, timedelta

# ダミーデータを保存するディレクトリ
DUMMY_DIR = "dummy_data"
os.makedirs(DUMMY_DIR, exist_ok=True)

print(f"'{DUMMY_DIR}' ディレクトリを作成しました。")

# --- CSVファイルの生成 ---

# sales.csv (ID 34, 44, 60, 91, 99)
sales_data = {
    '日付': pd.to_datetime(['2024-01-01', '2024-01-15', '2024-02-01', '2024-02-10', '2024-03-01']),
    '商品名': ['商品A', '商品B', '商品A', '商品C', '商品B'],
    '取引先': ['取引先X', '取引先Y', '取引先X', '取引先Z', '取引先Y'],
    '売上': [10000, 15000, 12000, 8000, 18000],
    '月': ['1月', '1月', '2月', '2月', '3月'],
    '数量': [10, 5, 8, 3, 7],
    '単価': [1000, 3000, 1500, 2500, 2500],
    '売上金額': [10000, 15000, 12000, 7500, 17500],
    '担当者': ['山田', '佐藤', '山田', '鈴木', '佐藤'],
    '業種': ['IT', '製造', 'IT', 'サービス', '製造']
}
pd.DataFrame(sales_data).to_csv(os.path.join(DUMMY_DIR, 'sales.csv'), index=False, encoding='utf-8')
print("sales.csv を生成しました。")

# customers.csv (ID 37, 42, 53, 56, 58, 89)
customers_data = {
    '顧客ID': ['C001', 'C002', 'C003', 'C004'],
    '氏名': ['田中太郎', '佐藤花子', '鈴木一郎', '高橋美咲'],
    '購入日': ['2023-01-01', '2023-02-10', '2023-03-05', '2023-04-20'],
    '購入金額': [5000, 12000, 8000, 20000],
    '商品名': ['商品X', '商品Y', '商品Z', '商品X'],
    '最終連絡日': ['2024-06-01', '2024-05-10', '2024-06-15', '2024-04-20'],
    '会社名': ['株式会社A', '株式会社B', '株式会社C', '株式会社D'],
    '担当者': ['田中', '佐藤', '鈴木', '高橋'],
    '電話': ['090-1111-2222', '080-3333-4444', '070-5555-6666', '090-7777-8888'],
    'メール': ['tanaka@example.com', 'sato@example.com', 'suzuki@example.com', 'takahashi@example.com'],
    '敬称': ['様', '様', '様', '様'],
    '郵便番号': ['100-0001', '200-0002', '300-0003', '400-0004'],
    '住所': ['東京都千代田区1-1-1', '大阪府大阪市2-2-2', '愛知県名古屋市3-3-3', '福岡県福岡市4-4-4'],
    '誕生日': ['1990-01-01', '1985-07-15', '1992-11-20', '1988-03-25'],
    '重要度': ['高', '中', '低', '高']
}
pd.DataFrame(customers_data).to_csv(os.path.join(DUMMY_DIR, 'customers.csv'), index=False, encoding='utf-8')
print("customers.csv を生成しました。")

# inventory.csv (ID 39, 52, 83)
inventory_data = {
    '商品名': ['商品A', '商品B', '商品C', '商品D'],
    '在庫数': [5, 12, 3, 20],
    '最小在庫数': [10, 5, 5, 10],
    '商品コード': ['P001', 'P002', 'P003', 'P004'],
    'カテゴリ': ['食品', '飲料', '雑貨', '家電'],
    '単価': [100, 150, 500, 10000],
    '仕入先': ['サプライヤーX', 'サプライヤーY', 'サプライヤーZ', 'サプライヤーW'],
    '最終更新日': ['2024-07-10', '2024-07-11', '2024-07-12', '2024-07-13'],
    '入荷数': [5, 0, 10, 0],
    '出荷数': [2, 8, 0, 5]
}
pd.DataFrame(inventory_data).to_csv(os.path.join(DUMMY_DIR, 'inventory.csv'), index=False, encoding='utf-8')
print("inventory.csv を生成しました。")

# data.csv (ID 40, 36)
data_csv = {
    '列1': [1, 2, np.nan, 4, 5, 1, 2],
    '列2': ['A', 'B', 'C', 'D', 'E', 'A', 'B'],
    '売上': [100, 200, 300, 400, 500, 600, 700]
}
pd.DataFrame(data_csv).to_csv(os.path.join(DUMMY_DIR, 'data.csv'), index=False, encoding='utf-8')
print("data.csv を生成しました。")

# evaluations.csv (ID 43)
evaluations_data = {
    '社員名': ['山田', '佐藤', '山田', '鈴木'],
    '評価点': [4, 5, 3, 4],
    '評価項目': ['リーダーシップ', '協調性', '積極性', '問題解決能力'],
    '評価者': ['部長', '課長', '部長', '主任']
}
pd.DataFrame(evaluations_data).to_csv(os.path.join(DUMMY_DIR, 'evaluations.csv'), index=False, encoding='utf-8')
print("evaluations.csv を生成しました。")

# sales_history.csv (ID 44, 99)
sales_history_data = {
    '日付': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01']),
    '売上': [100, 120, 110, 130, 140],
    '顧客名': ['田中', '佐藤', '田中', '鈴木', '佐藤']
}
pd.DataFrame(sales_history_data).to_csv(os.path.join(DUMMY_DIR, 'sales_history.csv'), index=False, encoding='utf-8')
print("sales_history.csv を生成しました。")

# employees.csv (ID 48, 65)
employees_data = {
    '社員ID': ['E001', 'E002', 'E003'],
    '氏名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '部署': ['営業部', '開発部', '総務部'],
    '入社日': ['2020-04-01', '2019-10-01', '2021-01-01'],
    'メールアドレス': ['yamada@example.com', 'sato@example.com', 'suzuki@example.com'],
    '役職': ['主任', '課長', '一般'],
    '内線番号': ['1001', '2001', '3001'],
    '携帯電話': ['090-1234-5678', '080-9876-5432', '070-1111-2222'],
    '緊急連絡先': ['090-9999-8888', '080-7777-6666', '070-5555-4444']
}
pd.DataFrame(employees_data).to_csv(os.path.join(DUMMY_DIR, 'employees.csv'), index=False, encoding='utf-8')
print("employees.csv を生成しました。")

# kintai.csv (ID 49)
kintai_data = {
    '氏名': ['山田', '佐藤', '山田'],
    '日付': ['2024-07-01', '2024-07-01', '2024-07-02'],
    '勤務時間': [8, 7, 8],
    '出勤時刻': ['09:00', '09:30', '09:00'],
    '退勤時刻': ['17:00', '17:30', '17:00']
}
pd.DataFrame(kintai_data).to_csv(os.path.join(DUMMY_DIR, 'kintai.csv'), index=False, encoding='utf-8')
print("kintai.csv を生成しました。")

# survey.csv (ID 51, 61, 79)
survey_data = {
    '回答者': ['Aさん', 'Bさん', 'Cさん'],
    '満足度': [5, 4, 3],
    '年齢': [30, 40, 25],
    '性別': ['男性', '女性', '男性'],
    '評価': [5, 4, 3],
    '改善点': ['特になし', 'UI改善希望', '機能追加希望'],
    'コメント': ['とても良い', '使いやすい', '普通'],
    '部署': ['営業部', '開発部', '総務部'],
    '研修名': ['Python基礎', 'Excel応用', 'コミュニケーション']
}
pd.DataFrame(survey_data).to_csv(os.path.join(DUMMY_DIR, 'survey.csv'), index=False, encoding='utf-8')
print("survey.csv を生成しました。")

# orders.csv (ID 54, 84)
orders_data = {
    '日付': ['2024-07-01', '2024-07-05', '2024-07-02'],
    '取引先': ['取引先A', '取引先B', '取引先A'],
    '商品名': ['商品X', '商品Y', '商品Z'],
    '数量': [10, 5, 8],
    '金額': [10000, 15000, 8000],
    '受発注番号': ['ORD001', 'ORD002', 'ORD003'],
    '単価': [1000, 3000, 1000],
    '受発注種別': ['受注', '発注', '受注'],
    '納期': ['2024-07-10', '2024-07-15', '2024-07-12'],
    '状況': ['完了', '進行中', '完了']
}
pd.DataFrame(orders_data).to_csv(os.path.join(DUMMY_DIR, 'orders.csv'), index=False, encoding='utf-8')
print("orders.csv を生成しました。")

# training_participants.csv (ID 55)
training_participants_data = {
    '研修ID': ['T001', 'T001', 'T002'],
    '氏名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '部署': ['営業部', '開発部', '総務部'],
    'メールアドレス': ['yamada@example.com', 'sato@example.com', 'suzuki@example.com'],
    '参加日時': ['2024-07-01 09:00', '2024-07-01 09:00', '2024-07-05 13:00'],
    '研修名': ['Python基礎', 'Python基礎', 'Excel応用']
}
pd.DataFrame(training_participants_data).to_csv(os.path.join(DUMMY_DIR, 'training_participants.csv'), index=False, encoding='utf-8')
print("training_participants.csv を生成しました。")

# iccard.csv (ID 62)
iccard_data = {
    '利用日': ['2024-07-01', '2024-07-01', '2024-07-02'],
    '利用時刻': ['08:00', '18:00', '09:00'],
    '利用駅': ['新宿', '東京', '渋谷'],
    '利用額': [160, 160, 180],
    '残高': [1000, 840, 660]
}
pd.DataFrame(iccard_data).to_csv(os.path.join(DUMMY_DIR, 'iccard.csv'), index=False, encoding='utf-8')
print("iccard.csv を生成しました。")

# contracts.csv (ID 72)
contracts_data = {
    '取引先': ['株式会社A', '株式会社B', '株式会社A'],
    '契約日': ['2023-01-01', '2023-03-15', '2023-06-01'],
    '契約内容': ['保守契約', '開発契約', 'ライセンス契約'],
    '契約金額': [100000, 500000, 200000],
    '契約期間': ['1年', '6ヶ月', '2年'],
    '担当者': ['田中', '佐藤', '鈴木'],
    '更新予定日': ['2024-01-01', '2023-09-15', '2025-06-01']
}
pd.DataFrame(contracts_data).to_csv(os.path.join(DUMMY_DIR, 'contracts.csv'), index=False, encoding='utf-8')
print("contracts.csv を生成しました。")

# circulation.csv (ID 73)
circulation_data = {
    '回覧文書名': ['重要なお知らせ', '社内規定改定', 'イベント案内'],
    '確認者': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '確認日': ['2024-07-01', '2024-07-02', '2024-07-03'],
    '確認状況': ['確認済み', '未確認', '確認済み']
}
pd.DataFrame(circulation_data).to_csv(os.path.join(DUMMY_DIR, 'circulation.csv'), index=False, encoding='utf-8')
print("circulation.csv を生成しました。")

# inquiry.csv (ID 74)
inquiry_data = {
    '顧客名': ['田中太郎', '佐藤花子', '鈴木一郎'],
    '問い合わせ日': ['2024-07-01', '2024-07-02', '2024-07-03'],
    '問い合わせ内容': ['製品について', 'サービスについて', '料金について'],
    '担当者': ['山田', '佐藤', '鈴木'],
    '対応状況': ['対応済み', '対応中', '未対応'],
    '対応日': ['2024-07-01', np.nan, np.nan],
    '備考': ['迅速に対応', '要確認', '後日連絡']
}
pd.DataFrame(inquiry_data).to_csv(os.path.join(DUMMY_DIR, 'inquiry.csv'), index=False, encoding='utf-8')
print("inquiry.csv を生成しました。")

# skills.csv (ID 75)
skills_data = {
    '社員名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    'スキル名': ['Python', 'Excel', 'プレゼン'],
    'レベル': ['上級', '中級', '初級'],
    '取得日': ['2023-01-01', '2023-03-15', '2023-06-01'],
    '部署': ['開発部', '営業部', '総務部']
}
pd.DataFrame(skills_data).to_csv(os.path.join(DUMMY_DIR, 'skills.csv'), index=False, encoding='utf-8')
print("skills.csv を生成しました。")

# projects.csv (ID 77)
projects_data = {
    'プロジェクト名': ['プロジェクトA', 'プロジェクトB', 'プロジェクトC'],
    '担当者': ['山田', '佐藤', '鈴木'],
    '開始日': ['2024-01-01', '2024-02-01', '2024-03-01'],
    '期限': ['2024-07-31', '2024-08-31', '2024-09-30'],
    '進捗率': [80, 50, 20],
    'ステータス': ['進行中', '遅延', '未開始'],
    '優先度': ['高', '中', '低']
}
pd.DataFrame(projects_data).to_csv(os.path.join(DUMMY_DIR, 'projects.csv'), index=False, encoding='utf-8')
print("projects.csv を生成しました。")

# event_attendance.csv (ID 67, 78)
event_attendance_data = {
    'イベント名': ['忘年会', '新年会', 'BBQ'],
    '開催日': ['2024-12-20', '2025-01-10', '2024-08-01'],
    '氏名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '部署': ['営業部', '開発部', '総務部'],
    '出欠状況': ['出席', '欠席', '出席'],
    '参加費': [5000, 0, 3000],
    '回答日': ['2024-11-01', '2024-12-01', '2024-07-10']
}
pd.DataFrame(event_attendance_data).to_csv(os.path.join(DUMMY_DIR, 'event_attendance.csv'), index=False, encoding='utf-8')
print("event_attendance.csv を生成しました。")

# transport_expense.csv (ID 80)
transport_expense_data = {
    '日付': ['2024-07-01', '2024-07-01', '2024-07-02'],
    '氏名': ['山田太郎', '山田太郎', '佐藤花子'],
    '出発地': ['新宿', '東京', '渋谷'],
    '到着地': ['東京', '新宿', '品川'],
    '路線': ['JR', 'JR', '地下鉄'],
    '金額': [160, 160, 200],
    '目的': ['会議', '出張', '研修']
}
pd.DataFrame(transport_expense_data).to_csv(os.path.join(DUMMY_DIR, 'transport_expense.csv'), index=False, encoding='utf-8')
print("transport_expense.csv を生成しました。")

# partner_data.csv (ID 81)
partner_data = {
    '会社名': ['株式会社A', '株式会社B', '株式会社C'],
    '担当者': ['田中', '佐藤', '鈴木'],
    '役職': ['部長', '課長', '主任'],
    '電話': ['03-1111-2222', '06-3333-4444', '052-5555-6666'],
    'メール': ['a@example.com', 'b@example.com', 'c@example.com'],
    '業種': ['IT', '製造', 'サービス'],
    '取引開始日': ['2020-01-01', '2019-05-01', '2021-03-01'],
    '最終連絡日': ['2024-07-10', '2024-07-05', '2024-07-12']
}
pd.DataFrame(partner_data).to_csv(os.path.join(DUMMY_DIR, 'partner_data.csv'), index=False, encoding='utf-8')
print("partner_data.csv を生成しました。")

# training_history.csv (ID 82)
training_history_data = {
    '社員名': ['山田太郎', '佐藤花子', '山田太郎'],
    '部署': ['営業部', '開発部', '営業部'],
    '研修名': ['営業スキル', 'Python基礎', 'プレゼン'],
    '研修日': ['2023-04-01', '2023-05-10', '2023-06-20'],
    '時間': [8, 16, 4],
    '講師': ['A先生', 'B先生', 'C先生'],
    '評価': [4, 5, 3],
    '費用': [50000, 80000, 30000]
}
pd.DataFrame(training_history_data).to_csv(os.path.join(DUMMY_DIR, 'training_history.csv'), index=False, encoding='utf-8')
print("training_history.csv を生成しました。")

# payments.csv (ID 70, 95)
payments_data = {
    '取引先': ['株式会社A', '株式会社B', '株式会社C'],
    '支払日': ['2024-07-10', '2024-07-15', '2024-07-20'],
    '金額': [100000, 50000, 200000],
    '支払条件': ['月末締め翌月末払い', '月末締め翌月15日払い', '即金'],
    '商品名': ['サービス利用料', '備品購入費', 'コンサルティング料'],
    '担当者': ['田中', '佐藤', '鈴木']
}
pd.DataFrame(payments_data).to_csv(os.path.join(DUMMY_DIR, 'payments.csv'), index=False, encoding='utf-8')
print("payments.csv を生成しました。")

# health_checkup.csv (ID 71)
health_checkup_data = {
    '氏名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '部署': ['営業部', '開発部', '総務部'],
    '年齢': [35, 28, 42],
    '性別': ['男性', '女性', '男性'],
    '健康診断日': ['2024-06-01', '2024-06-05', '2024-06-10'],
    '身長': [170, 160, 175],
    '体重': [65, 50, 70],
    'BMI': [22.5, 19.5, 22.9],
    '血圧': ['120/80', '110/70', '130/85'],
    '血糖値': [90, 85, 100],
    '総コレステロール': [180, 160, 200],
    '要再検査': ['なし', 'なし', 'あり'],
    '備考': ['良好', '良好', '要精密検査']
}
pd.DataFrame(health_checkup_data).to_csv(os.path.join(DUMMY_DIR, 'health_checkup.csv'), index=False, encoding='utf-8')
print("health_checkup.csv を生成しました。")

# equipment.csv (ID 69)
equipment_data = {
    '備品名': ['ノートPC', 'プロジェクター', 'モニター'],
    'カテゴリ': ['IT機器', 'AV機器', 'IT機器'],
    '台数': [10, 2, 5],
    '購入日': ['2023-01-01', '2023-03-15', '2023-06-01'],
    '購入金額': [100000, 150000, 30000],
    '管理者': ['山田', '佐藤', '鈴木'],
    '保管場所': ['オフィスA', '会議室B', 'オフィスA'],
    '状態': ['良好', '良好', '一部故障'],
    '備考': ['最新モデル', '高解像度', '修理予定']
}
pd.DataFrame(equipment_data).to_csv(os.path.join(DUMMY_DIR, 'equipment.csv'), index=False, encoding='utf-8')
print("equipment.csv を生成しました。")

# purchase_history.csv (ID 97)
purchase_history_data = {
    '顧客名': ['田中太郎', '佐藤花子', '田中太郎', '鈴木一郎'],
    '購入日': ['2024-01-01', '2024-01-10', '2024-02-01', '2024-02-15'],
    '商品名': ['商品A', '商品B', '商品C', '商品A'],
    '購入金額': [1000, 2000, 1500, 1000]
}
pd.DataFrame(purchase_history_data).to_csv(os.path.join(DUMMY_DIR, 'purchase_history.csv'), index=False, encoding='utf-8')
print("purchase_history.csv を生成しました。")

# business_card.csv (ID 94)
business_card_data = {
    '氏名': ['山田太郎', '佐藤花子', '鈴木一郎'],
    '部署': ['営業部', '開発部', '総務部'],
    '役職': ['課長', '主任', '一般'],
    '現在の名刺枚数': [50, 100, 20],
    '発注予定枚数': [200, 100, 50],
    '最終発注日': ['2024-06-01', '2024-05-15', '2024-07-01'],
    '名刺デザイン': ['A', 'B', 'A'],
    '緊急度': ['高', '中', '低']
}
pd.DataFrame(business_card_data).to_csv(os.path.join(DUMMY_DIR, 'business_card.csv'), index=False, encoding='utf-8')
print("business_card.csv を生成しました。")

# work_hours.csv (ID 90)
work_hours_data = {
    '社員名': ['山田太郎', '佐藤花子', '山田太郎'],
    '日付': ['2024-07-01', '2024-07-01', '2024-07-02'],
    '出勤時間': ['09:00', '09:30', '09:00'],
    '退勤時間': ['18:00', '17:30', '17:00'],
    '勤務時間': [9, 8, 8] # 実際は計算されるがダミーとして
}
pd.DataFrame(work_hours_data).to_csv(os.path.join(DUMMY_DIR, 'work_hours.csv'), index=False, encoding='utf-8')
print("work_hours.csv を生成しました。")

# event_budget.csv (ID 96)
event_budget_data = {
    '項目': ['会場費', '飲食費', '備品費'],
    '予算': [100000, 50000, 20000],
    '実績': [95000, 48000, 18000]
}
pd.DataFrame(event_budget_data).to_csv(os.path.join(DUMMY_DIR, 'event_budget.csv'), index=False, encoding='utf-8')
print("event_budget.csv を生成しました。")

# efficiency_report.csv (ID 100)
efficiency_report_data = {
    '業務名': ['データ入力', 'レポート作成', '会議準備'],
    '改善前': ['2時間', '3時間', '1時間'],
    '改善後': ['30分', '1時間', '15分']
}
pd.DataFrame(efficiency_report_data).to_csv(os.path.join(DUMMY_DIR, 'efficiency_report.csv'), index=False, encoding='utf-8')
print("efficiency_report.csv を生成しました。")

# --- 画像ファイルの生成 ---
# imagesフォルダを作成 (ID 33)
os.makedirs(os.path.join(DUMMY_DIR, 'images'), exist_ok=True)

# ダミー画像ファイル (JPG, PNG)
img_jpg = Image.new('RGB', (60, 30), color = 'red')
img_jpg.save(os.path.join(DUMMY_DIR, 'images', 'dummy_image1.jpg'))
img_png = Image.new('RGB', (60, 30), color = 'blue')
img_png.save(os.path.join(DUMMY_DIR, 'images', 'dummy_image2.png'))
print("dummy_image1.jpg, dummy_image2.png を生成しました。")

# --- PDFファイルの生成 ---
# ダミーPDFファイル (ID 31, 41, 45, 59, 64, 66, 76, 93)
def create_dummy_pdf(filename, content="This is a dummy PDF file."):
    c = canvas.Canvas(os.path.join(DUMMY_DIR, filename), pagesize=letter)
    c.drawString(100, 750, content)
    c.save()

create_dummy_pdf('dummy.pdf', "This is a dummy PDF file.")
create_dummy_pdf('file1.pdf', "This is file1.pdf")
create_dummy_pdf('file2.pdf', "This is file2.pdf")
create_dummy_pdf('file3.pdf', "This is file3.pdf")
print("dummy.pdf, file1.pdf, file2.pdf, file3.pdf を生成しました。")

# --- その他のダミーファイル/フォルダ ---
# target_folder (ID 32)
os.makedirs(os.path.join(DUMMY_DIR, 'target_folder'), exist_ok=True)
with open(os.path.join(DUMMY_DIR, 'target_folder', 'test.txt'), 'w') as f:
    f.write('This is a test file in target_folder.')
print("target_folder を生成しました。")

# pdfs, images フォルダ (ID 35)
os.makedirs(os.path.join(DUMMY_DIR, 'pdfs'), exist_ok=True)
os.makedirs(os.path.join(DUMMY_DIR, 'images_classified'), exist_ok=True) # 衝突を避けるため別名に
print("pdfs, images_classified フォルダを生成しました。")

print("\n全てのダミーファイルの生成が完了しました。")
