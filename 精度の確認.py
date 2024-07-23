import os
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import japanize_matplotlib

# 不快指数を計算する関数
def calculate_discomfort_index(temp, hum):
    return 0.81 * temp + 0.01 * hum * (0.99 * temp - 14.3) + 46.3

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# カレントディレクトリをスクリプトのディレクトリに変更
os.chdir(script_dir)
print("Current Working Directory after change: ", os.getcwd())

# ファイル名
predicted_temperature_file = '予測データ/lasso_気温予測.csv'
actual_temperature_file = '加工後データ/new_2024_kion_11630.csv'
predicted_humidity_file = '予測データ/lasso_湿度予測.csv'
actual_humidity_file = '加工後データ/new_2024_shitsudo_11630.csv'

# ファイルの存在確認
for file in [predicted_temperature_file, actual_temperature_file, predicted_humidity_file, actual_humidity_file]:
    if not os.path.exists(file):
        print(f"File not found: {file}")
        exit()

# ファイルの読み込み
predicted_temp_df = pd.read_csv(predicted_temperature_file, encoding="utf-8")
actual_temp_df = pd.read_csv(actual_temperature_file, encoding="utf-8")
predicted_hum_df = pd.read_csv(predicted_humidity_file, encoding="utf-8")
actual_hum_df = pd.read_csv(actual_humidity_file, encoding="utf-8")
print("Files read successfully.")

# 列名を表示して確認
print("列名 (actual_hum_df):", actual_hum_df.columns)

# 2024年のデータにフィルタリング
predicted_temp_df = predicted_temp_df[predicted_temp_df['年'] == 2024]
predicted_hum_df = predicted_hum_df[predicted_hum_df['年'] == 2024]
predicted_temp_df['date'] = pd.to_datetime(predicted_temp_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))
predicted_hum_df['date'] = pd.to_datetime(predicted_hum_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))

# 実際の2024年データ
actual_temp_df['date'] = pd.to_datetime(actual_temp_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))

# 列名が確認できた後に適切な列名を使用
actual_hum_df.columns = ['年', '月', '日', '湿度', '品質', '均質']
actual_hum_df['date'] = pd.to_datetime(actual_hum_df[['年', '月', '日']].astype(str).agg('-'.join, axis=1))

# 1月7日から6月30日までのデータにフィルタリング
actual_temp_df = actual_temp_df[(actual_temp_df['date'] >= '2024-01-07') & (actual_temp_df['date'] <= '2024-06-30')]
actual_hum_df = actual_hum_df[(actual_hum_df['date'] >= '2024-01-07') & (actual_hum_df['date'] <= '2024-06-30')]

# 予測データと実際のデータをマージ
merged_temp_df = pd.merge(predicted_temp_df, actual_temp_df, on='date', suffixes=('_pred', '_actual'))
merged_hum_df = pd.merge(predicted_hum_df, actual_hum_df, on='date', suffixes=('_pred', '_actual'))

# 気温カラムを選択
predicted_temperatures = merged_temp_df['予測気温']
actual_temperatures = merged_temp_df['気温']

# 湿度カラムを選択
predicted_humidity = merged_hum_df['予測湿度']
actual_humidity = merged_hum_df['湿度']



# 不快指数の計算
predicted_discomfort_index = calculate_discomfort_index(predicted_temperatures, predicted_humidity)
actual_discomfort_index = calculate_discomfort_index(actual_temperatures, actual_humidity)

# 精度の計算 (気温)
mae_temp = mean_absolute_error(actual_temperatures, predicted_temperatures)
r2_temp = r2_score(actual_temperatures, predicted_temperatures)

# 精度の計算 (湿度)
mae_hum = mean_absolute_error(actual_humidity, predicted_humidity)
r2_hum = r2_score(actual_humidity, predicted_humidity)

# 精度の計算 (不快指数)
mae_di = mean_absolute_error(actual_discomfort_index, predicted_discomfort_index)
r2_di = r2_score(actual_discomfort_index, predicted_discomfort_index)

print(f'気温 - 平均絶対誤差 (MAE): {mae_temp}')
print(f'気温 - 決定係数 (R²): {r2_temp:.2f}')

print(f'湿度 - 平均絶対誤差 (MAE): {mae_hum}')
print(f'湿度 - 決定係数 (R²): {r2_hum:.2f}')

print(f'不快指数 - 平均絶対誤差 (MAE): {mae_di}')
print(f'不快指数 - 決定係数 (R²): {r2_di:.2f}')

# グラフの作成
plt.figure(figsize=(15, 8))
plt.plot(merged_temp_df['date'], actual_discomfort_index, label='実際の不快指数', color='red')
plt.plot(merged_temp_df['date'], predicted_discomfort_index, label='予測不快指数', color='blue')
plt.xlabel('日付')
plt.ylabel('不快指数')
plt.title('2024年の実際の不快指数と予測不快指数の比較 (1/7 ~ 6/30)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/実際の不快指数との比較_lasso.png')
plt.show()