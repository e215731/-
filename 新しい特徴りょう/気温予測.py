#重みつけたお


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np

# 気温データを読み込む
temper_data = pd.read_csv('new_naha_kion.csv', encoding="utf-8")

# 新しい特徴量を読み込む
humidity_data = pd.read_csv('new_naha_shitsudo.csv', encoding="utf-8")
weather_data = pd.read_csv('new_naha_tenki.csv', encoding="utf-8")

# 新しい特徴量を統合する
def integrate_features(temper_data, humidity_data, weather_data):
    # 必要な列を抽出
    humidity = humidity_data['湿度']
    max_temp = weather_data['最高気温(℃)']
    precipitation = weather_data['降水量の合計(mm)']
    sunshine_hours = weather_data['日照時間(時間)']

    # データを結合する
    integrated_data = pd.concat([temper_data, humidity, max_temp, precipitation, sunshine_hours], axis=1)
    return integrated_data

# 新しい特徴量を統合する
integrated_data = integrate_features(temper_data, humidity_data, weather_data)

# 欠損値を平均値で補完
integrated_data.fillna(integrated_data.mean(), inplace=True)

# 過去6日分の気温データと新しい特徴量を特徴量、その翌日の気温を目的変数とする訓練データを作成する関数
def make_data(data, interval):
    x = []
    y = []
    for i in range(len(data)):
        if i < interval: continue
        y.append(data.iloc[i]['気温'])
        xa = []
        for p in range(interval):
            d = i + p - interval
            xa.extend(data.iloc[d][['気温', '湿度', '最高気温(℃)', '降水量の合計(mm)', '日照時間(時間)']])
        x.append(xa)
    return (x, y)

# 訓練データの作成
train_year = (integrated_data["年"] <= 2023)
interval = 6

# 訓練データの作成
train_x, train_y = make_data(integrated_data[train_year], interval)

# 訓練データの標準化
scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)

# 線形回帰モデルの訓練
lr = LinearRegression()
lr.fit(train_x_scaled, train_y)

# 各特徴量の重みを表示
feature_names = []
for i in range(interval):
    feature_names.extend([f'気温_{i+1}', f'湿度_{i+1}', f'最高気温_{i+1}', f'降水量_{i+1}', f'日照時間_{i+1}'])
    
feature_weights = pd.DataFrame({'特徴量': feature_names, '重み': lr.coef_})
print(feature_weights)

# 2023年のデータを使用して2024年の気温を予測
test_year_2023 = (integrated_data["年"] == 2023)

# テストデータの作成
test_x_2023, _ = make_data(integrated_data[test_year_2023], interval)

# テストデータの標準化
test_x_2023_scaled = scaler.transform(test_x_2023)

# 2024年の気温を予測
pre_y_2024 = lr.predict(test_x_2023_scaled)

# 予測した2024年の気温データを保存
test_data_2023 = integrated_data[test_year_2023].iloc[interval:]  # 最初のinterval日を除く
months_2024 = test_data_2023['月'].values
days_2024 = test_data_2023['日'].values

predicted_2024_df = pd.DataFrame({
    '年': 2024,
    '月': months_2024,
    '日': days_2024,
    '予測気温': pre_y_2024
})

# 予測した2024年の気温データをCSVファイルとして保存
predicted_2024_df.to_csv('vvs_気温予測_v2.csv', index=False, encoding='utf-8')


# 各特徴量に手動で重みを設定する関数
def apply_weights(data, weights):
    weighted_data = data.copy()
    for i, weight in enumerate(weights):
        weighted_data.iloc[:, i] *= weight
    return weighted_data

# 各特徴量の重みを設定
weights = [1.0, 0.1, 10.0, 0.1, 0.1] * interval  # 重みの例（ここでは各特徴量に異なる重みを設定）

# 訓練データの作成（重みを適用）
train_x_weighted = apply_weights(pd.DataFrame(train_x), weights)

# 訓練データの標準化
train_x_scaled_weighted = scaler.fit_transform(train_x_weighted)

# 線形回帰モデルの訓練
lr.fit(train_x_scaled_weighted, train_y)

# テストデータの作成（重みを適用）
test_x_2023_weighted = apply_weights(pd.DataFrame(test_x_2023), weights)

# テストデータの標準化
test_x_2023_scaled_weighted = scaler.transform(test_x_2023_weighted)

# 2024年の気温を予測
pre_y_2024_weighted = lr.predict(test_x_2023_scaled_weighted)

# 予測した2024年の気温データを保存（重みを適用した場合）
predicted_2024_df_weighted = pd.DataFrame({
    '年': 2024,
    '月': months_2024,
    '日': days_2024,
    '予測気温': pre_y_2024_weighted
})

# 予測した2024年の気温データをCSVファイルとして保存
predicted_2024_df_weighted.to_csv('vvs_気温予測_weighted.csv', index=False, encoding='utf-8')
