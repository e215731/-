'''
実際の気温（2024 1/1~6/30）と予測気温の比較
'''

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# データの読み込み
predicted_df = pd.read_csv('予測データ/predicted_2024_temperatures.csv', encoding="utf-8")
actual_df = pd.read_csv('加工後データ/new_2024_kion_11630.csv', encoding="utf-8")

# 2024年のデータにフィルタリング
predicted_2024_df = predicted_df[predicted_df['年'] == 2024]
predicted_2024_df['date'] = pd.to_datetime(predicted_2024_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))

# 実際の2024年データ
actual_df['date'] = pd.to_datetime(actual_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))

# 1月7日から6月30日までのデータにフィルタリング
actual_2024_half_df = actual_df[(actual_df['date'] >= '2024-01-07') & (actual_df['date'] <= '2024-06-30')]

# 予測データと実際のデータをマージ
merged_df = pd.merge(predicted_2024_df, actual_2024_half_df, on='date', suffixes=('_pred', '_actual'))


predicted_temperatures = merged_df['予測気温']
actual_temperatures = merged_df['気温']

# 精度の計算
mae = mean_absolute_error(actual_temperatures, predicted_temperatures)
mse = mean_squared_error(actual_temperatures, predicted_temperatures)
mape = (mae / actual_temperatures.mean()) * 100

print(f'平均絶対誤差 (MAE): {mae}')
print(f'平均二乗誤差 (MSE): {mse}')
print(f'平均絶対誤差率 (MAPE): {mape:.2f}%')

# グラフの作成
plt.figure(figsize=(15, 8))
plt.plot(merged_df['date'], actual_temperatures, label='実際の気温', color='red')
plt.plot(merged_df['date'], predicted_temperatures, label='予測気温', color='blue')
plt.xlabel('日付')
plt.ylabel('気温 (℃)')
plt.title('2024年の実際の気温と予測気温の比較 (1/7 ~ 6/30)')
plt.legend()
plt.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
