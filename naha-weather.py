# 元の天気データファイル
in_file = "naha_weather.csv"
# 加工後の天気データファイル
out_file = "new_naha_weather.csv"

# CSVファイルを読み込む
with open(in_file, "rt", encoding="Shift_JIS") as fr:
    lines = fr.readlines()

# 先頭から5レコード分を削除し、新たな行ヘッダをつける
lines = ["年,月,日,天気概況,品質,均質\n"] + lines[5:]

# / を , に置換している（年、月、日をカンマで分離するため）
lines = map(lambda v: v.replace('/', ','), lines)

# joinで改行付きの全レコードを結合したあと、stripメソッドで最終レコードの改行だけを取り除く
result = "".join(lines).strip()

# 加工された結果を out_file で指定したファイル名で出力する
with open(out_file, "wt", encoding="utf-8") as fw:
    fw.write(result)

print("saved.")
