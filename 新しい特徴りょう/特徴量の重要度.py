import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np

# 気温データを読み込む
temper_data = pd.read_csv('new_naha_kion.csv', encoding="utf-8")

# 新しい特徴量を読み込む
humidity_data = pd.read_csv('new_naha_shitsudo.csv', encoding="utf-8")
weather_data = pd.read_csv('new_naha_tenki.csv', encoding="utf-8")

# 過去6日分の気温データを特徴量、その翌日の気温を目的変数とする訓練データを作成する関数
def make_data(data, interval):
    x = []
    y = []
    temps = list(data["気温"])
    for i in range(len(temps)):
        if i < interval: continue
        y.append(temps[i])
        xa = []
        for p in range(interval):
            d = i + p - interval
            xa.append(temps[d])
        x.append(xa)
    return (x, y)

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

# 新しい特徴量を統合した訓練データを作成
train_year = (temper_data["年"] <= 2023)
interval = 6

# 過去6日分の気温データを特徴量とする
train_x, train_y = make_data(temper_data[train_year], interval)

# 新しい特徴量を統合する
integrated_data = integrate_features(temper_data[train_year], humidity_data, weather_data)

# 訓練データの標準化
scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)

# 欠損値を平均値で補完
integrated_data.fillna(integrated_data.mean(), inplace=True)

# 線形回帰モデルの訓練
lr = LinearRegression()
lr.fit(train_x_scaled, train_y)

# 特徴量の重要度を確認
coefficients = lr.coef_
feature_importance = pd.Series(abs(coefficients), index=integrated_data.columns, name='重要度').sort_values(ascending=False)

# 結果の表示
print("特徴量の重要度:")
print(feature_importance)

print(integrated_data)