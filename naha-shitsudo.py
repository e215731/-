'''
「湿度」データを加工し,
"加工後データ/new_naha_shitsudo.csv"に保存
'''

in_file = "データセット/naha_shitsudo.csv"
out_file = "加工後データ/new_naha_shitsudo.csv"

# ファイルを読み込む
with open(in_file, "rt", encoding="Shift_JIS") as fr:
    lines = fr.readlines()

# 先頭から5行分を削除し、新たな行ヘッダをつける
lines = ["年,月,日,湿度,品質,均質\n"] + lines[5:]

lines = map(lambda v: v.replace('/', ','), lines)

result = "".join(lines).strip()

# 加工されたデータを出力する
with open(out_file, "wt", encoding="utf-8") as fw:
    fw.write(result)


