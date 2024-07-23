'''
「気象要素」データを加工し,
"加工後データ/new_naha_tenki.csv"に保存
'''

import pandas as pd

in_file = "データセット/naha_tenki.csv"
out_file = "加工後データ/new_naha_tenki.csv"

# ファイルを読み込む
df = pd.read_csv(in_file, encoding="Shift_JIS", skiprows=3)


# 不要な行を削除する
df = df.iloc[3:]

# 日付の形式に変換する
df['年月日'] = pd.to_datetime(df['年月日'])

# 年、月、日の列を追加する
df['Year'] = df['年月日'].dt.year
df['Month'] = df['年月日'].dt.month
df['Day'] = df['年月日'].dt.day


df_processed = df[[
    'Year',
    'Month',
    'Day',
    '最高気温(℃)',
    '降水量の合計(mm)',
    '日照時間(時間)'
]]

# 指定の列名変更する
df_processed.columns = ['年', '月', '日', '最高気温(℃)', '降水量の合計(mm)', '日照時間(時間)']

# 加工されたデータを保存する
df_processed.to_csv(out_file, index=False, encoding="utf-8")


