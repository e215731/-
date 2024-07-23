'''
「天気概況」データを加工し,
"加工後データ/new_naha_weather.csv"に保存
'''


in_file = "データセット/naha_weather.csv"
out_file = "加工後データ/new_naha_weather.csv"

# ファイルを読み込む
with open(in_file, "rt", encoding="Shift_JIS") as fr:
    lines = fr.readlines()

# 先頭から5行分を削除し、新たな行ヘッダをつける
lines = ["年,月,日,天気概況,品質,均質\n"] + lines[5:]


lines = map(lambda v: v.replace('/', ','), lines)

result = "".join(lines).strip()

with open(out_file, "wt", encoding="utf-8") as fw:
    fw.write(result)


