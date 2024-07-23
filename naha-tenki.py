import pandas as pd

# 入力と出力のファイル名
in_file = "naha_tenki.csv"
out_file = "new_naha_tenki.csv"

# CSVファイルを読み込む（Shift_JISでエンコード）
df = pd.read_csv(in_file, encoding="Shift_JIS", skiprows=3)

# 列名を確認する
print(df.columns)

# 不要な最初の数行を削除する
df = df.iloc[3:]

# 年月日列を日付の形式に変換する
df['年月日'] = pd.to_datetime(df['年月日'])

# 年、月、日の列を追加する
df['Year'] = df['年月日'].dt.year
df['Month'] = df['年月日'].dt.month
df['Day'] = df['年月日'].dt.day

# 必要な列を選択する
df_processed = df[[
    'Year',
    'Month',
    'Day',
    '最高気温(℃)',
    '降水量の合計(mm)',
    '日照時間(時間)'
]]

# 列名を指定した通りに変更する
df_processed.columns = ['年', '月', '日', '最高気温(℃)', '降水量の合計(mm)', '日照時間(時間)']

# 加工されたデータを新しいCSVファイルに保存する
df_processed.to_csv(out_file, index=False, encoding="utf-8")

print("加工されたデータを", out_file, "に保存しました。")
