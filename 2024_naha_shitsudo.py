from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 気温データを読み込む
temper_data = pd.read_csv('new_naha_shitsudo.csv', encoding="utf-8")

# 過去6日分を特徴量、その翌日の気温を目的変数とする訓練データを作成する関数
def make_data(data, interval):
    x = []
    y = []
    temps = list(data["湿度"])
    for i in range(len(temps)):
        if i < interval: continue
        y.append(temps[i])
        xa = []
        for p in range(interval):
            d = i + p - interval
            xa.append(temps[d])
        x.append(xa)
    return (x, y)

# 1994年から2023年までのデータを訓練データとして使用
train_year = (temper_data["年"] <= 2023)
interval = 6

train_x, train_y = make_data(temper_data[train_year], interval)

# 訓練データの標準化
scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)

# 線形回帰モデルの訓練
lr = LinearRegression()
lr.fit(train_x_scaled, train_y)

# 2023年のデータを使用して2024年の気温を予測
test_year_2023 = (temper_data["年"] == 2023)
test_x_2023, _ = make_data(temper_data[test_year_2023], interval)
test_x_2023_scaled = scaler.transform(test_x_2023)
pre_y_2024 = lr.predict(test_x_2023_scaled)

# 予測した2024年の気温データを保存
# ここで月と日を生成
test_data_2023 = temper_data[test_year_2023].iloc[interval:]  # 最初のinterval日を除く
months_2024 = test_data_2023['月'].values
days_2024 = test_data_2023['日'].values

predicted_2024_df = pd.DataFrame({
    '年': 2024,
    '月': months_2024,
    '日': days_2024,
    '予測湿度': pre_y_2024
})

# 2023年の気温データを取得
actual_2023_df = temper_data[test_year_2023][['月', '日', '湿度']].iloc[interval:]

# 2023年と2024年の気温データを比較するためにプロット
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(actual_2023_df['湿度'].values, c='r', label='2023年の実際の湿度')
plt.plot(pre_y_2024, c='b', label='2024年の予測湿度')
plt.legend()
plt.xlabel('日数')
plt.ylabel('湿度 (%)')
plt.title('2023年の実際の湿度と2024年の予測湿度の比較')
plt.savefig('tenki-shitsudo-2023_vs_2024.png')
plt.show()

# 予測した2024年の気温データをCSVファイルとして保存
predicted_2024_df.to_csv('predicted_2024_humidity.csv', index=False, encoding='utf-8')
