import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 予測した気温データと湿度データを読み込む
temperature_df = pd.read_csv('new_2024_kion_11630.csv', encoding="utf-8")
humidity_df = pd.read_csv('new_2024_shitsudo_11630.csv', encoding="utf-8")

# 不快指数を計算する関数
def calculate_discomfort_index(temp, hum):
    return 0.81 * temp + 0.01 * hum * (0.99 * temp - 14.3) + 46.3

# データをマージして不快指数を計算する
merged_df = pd.merge(temperature_df, humidity_df, on=['年', '月', '日'])
merged_df['不快指数'] = merged_df.apply(lambda row: calculate_discomfort_index(row['気温'], row['湿度']), axis=1)

# 列名を英語に変更
merged_df.rename(columns={'年': 'year', '月': 'month', '日': 'day'}, inplace=True)

# 日付カラムを追加
merged_df['date'] = pd.to_datetime(merged_df[['year', 'month', 'day']])

# 不快指数が80を初めて超えた日を特定
first_over_80 = merged_df[merged_df['不快指数'] > 80].iloc[0]['date']
print(f"不快指数が80を初めて超えた日: {first_over_80}")

# 結果を表示
print(merged_df.head())

# グラフの作成
plt.figure(figsize=(15, 8))
plt.plot(merged_df['date'], merged_df['不快指数'], label='2024年の不快指数', color='purple')
plt.axvline(first_over_80, color='red', linestyle='--', label='不快指数80を超えた日')  # 不快指数が80を初めて超えた日を垂直線で表示
plt.xlabel('日付')
plt.ylabel('不快指数')
plt.title('2024年の不快指数の推移')
plt.legend()
plt.grid(True)

# 日付フォーマットと目盛りの設定
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # 1週間間隔で目盛りを設定
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 日付フォーマットを設定

plt.xticks(rotation=45)  # 日付ラベルを45度回転して表示
plt.tight_layout()  # レイアウトを調整
plt.savefig('discomfort_index_2024.png')
plt.show()
