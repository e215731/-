from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 気温データを読み込む
temper_data = pd.read_csv('new_naha_kion.csv', encoding="utf-8")

# 過去6日分を特徴量、その翌日の気温を目的変数とする訓練データを作成する関数
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

train_year = (temper_data["年"] <= 2022)
test_year = (temper_data["年"] >= 2023)
interval = 6

train_x, train_y = make_data(temper_data[train_year], interval)
test_x, test_y = make_data(temper_data[test_year], interval)

scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)
test_x_scaled = scaler.transform(test_x)

lr = LinearRegression()
lr.fit(train_x_scaled, train_y)

pre_y = lr.predict(test_x_scaled)

plt.figure(figsize=(10, 6), dpi=100)
plt.plot(test_y, c='r', label='実際の気温')
plt.plot(pre_y, c='b', label='予測された気温')
plt.legend()
plt.savefig('tenki-kion-lr.png')
plt.show()
