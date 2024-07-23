import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
import numpy as np

# 気温データを読み込む
temper_data = pd.read_csv('new_naha_kion.csv', encoding="utf-8")

# 新しい特徴量を読み込む
humidity_data = pd.read_csv('new_naha_shitsudo.csv', encoding="utf-8")
weather_data = pd.read_csv('new_naha_tenki.csv', encoding="utf-8")
weather_summary_data = pd.read_csv('new_naha_weather.csv', encoding="utf-8")

# 天気概要の数値変換マッピングを定義する
weather_summary_mapping = {
    "快晴": 0, "晴": 1, "曇": 2, "薄曇": 3, "大風": 4, "霧": 5, "霧雨": 6, "雨": 7, "大雨": 8,
    "暴風雨": 9, "みぞれ": 10, "雪": 11, "大雪": 12, "暴風雪": 13, "地ふぶき": 14, "ふぶき": 15,
    "ひょう": 16, "あられ": 17, "雷": 18, "×": 19
}

# 天気変化の数値変換マッピングを定義する
weather_change_mapping = {
    "": 0, "一時": 1, "時々": 2, "後": 3, "後一時": 4, "後時々": 5
}

# 天気データを数値に変換する
weather_summary_data['天気概況'] = weather_summary_data['天気概況'].apply(lambda x: sum([weather_summary_mapping.get(term, 0) for term in x.split()]))
weather_summary_data['天気変化'] = weather_summary_data['天気概況'].apply(lambda x: weather_change_mapping.get(x, 0))

# 新しい特徴量を統合する
def integrate_features(temper_data, humidity_data, weather_data, weather_summary_data):
    # 必要な列を抽出
    humidity = humidity_data['湿度']
    max_temp = weather_data['最高気温(℃)']
    precipitation = weather_data['降水量の合計(mm)']
    sunshine_hours = weather_data['日照時間(時間)']
    weather_summary = weather_summary_data['天気概況']
    weather_change = weather_summary_data['天気変化']

    # データを結合する
    integrated_data = pd.concat([temper_data, humidity, max_temp, precipitation, sunshine_hours, weather_summary, weather_change], axis=1)
    return integrated_data

# 新しい特徴量を統合する
integrated_data = integrate_features(temper_data, humidity_data, weather_data, weather_summary_data)

# 欠損値を平均値で補完
integrated_data.fillna(integrated_data.mean(), inplace=True)

# 過去6日分の気温データと新しい特徴量を特徴量、その翌日の気温を目的変数とする訓練データを作成する関数
def make_data(data, interval):
    x = []
    y = []
    for i in range(len(data)):
        if i < interval: continue
        y.append(data.iloc[i]['湿度'])
        xa = []
        for p in range(interval):
            d = i + p - interval
            xa.extend(data.iloc[d][['気温', '湿度', '最高気温(℃)', '降水量の合計(mm)', '日照時間(時間)', '天気概況', '天気変化']])
        x.append(xa)
    return (x, y)

# 訓練データの作成
train_year = (integrated_data["年"] <= 2023)
interval = 34

# 訓練データの作成
train_x, train_y = make_data(integrated_data[train_year], interval)

# 訓練データの標準化
scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)

# Lasso回帰モデルを用いたハイパーパラメータの調整例
lasso = Lasso()
parameters = {'alpha': [0.05, 0.1, 0.5, 1, 5]}   # alphaは正則化項の強さを示すパラメータ

# グリッドサーチによる最適なパラメータの探索
lasso_regressor = GridSearchCV(lasso, parameters, scoring='neg_mean_absolute_error', cv=5)
lasso_regressor.fit(train_x_scaled, train_y)

# 最適なパラメータでモデルを訓練
best_alpha = lasso_regressor.best_params_['alpha']
lasso = Lasso(alpha=best_alpha)
lasso.fit(train_x_scaled, train_y)

# 2023年のデータを使用して2024年の気温を予測
test_year_2023 = (integrated_data["年"] == 2023)

# テストデータの作成
test_x_2023, _ = make_data(integrated_data[test_year_2023], interval)

# テストデータの標準化
test_x_2023_scaled = scaler.transform(test_x_2023)

# 2024年の気温を予測
pre_y_2024_lasso = lasso.predict(test_x_2023_scaled)

# 予測した2024年の気温データを保存
test_data_2023 = integrated_data[test_year_2023].iloc[interval:]  # 最初のinterval日を除く
months_2024 = test_data_2023['月'].values
days_2024 = test_data_2023['日'].values

predicted_2024_df_lasso = pd.DataFrame({
    '年': 2024,
    '月': months_2024,
    '日': days_2024,
    '予測湿度': pre_y_2024_lasso
})

# 予測した2024年の気温データをCSVファイルとして保存
predicted_2024_df_lasso.to_csv('lasso_湿度予測.csv', index=False, encoding='utf-8')
print("Lassoモデルによる予測を保存しました。")


print(f"最適なalphaの値: {best_alpha}")

# 各特徴量の重みを出力
feature_names = ['気温', '湿度', '最高気温(℃)', '降水量の合計(mm)', '日照時間(時間)', '天気概況', '天気変化']
n_features = len(feature_names)
coefs = lasso.coef_

print("各特徴量の重み:")
for i, feature in enumerate(feature_names):
    print(f"{feature}: {np.mean(coefs[i::n_features])}")