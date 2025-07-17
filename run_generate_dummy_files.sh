#!/bin/bash

# 仮想環境をアクティベート
source venv/bin/activate

# 必要なライブラリをインストール
pip install pandas Pillow reportlab numpy

# ダミーファイルを生成
python generate_dummy_files.py
