'''
「気温」データを加工し,
"加工後データ/new_naha_kion.csv"に保存
'''

in_file = "データセット/naha_kion.csv"
out_file = "加工後データ/new_naha_kion.csv"

# CSVファイルを読み込む
with open(in_file, "rt", encoding="Shift_JIS") as fr:
    lines = fr.readlines()

# 先頭から5レコード分を削除し、新たな行ヘッダをつける
lines = ["年,月,日,気温,品質,均質\n"] + lines[5:]

# / を , に置換している（年、月、日をカンマで分離するため）
lines = map(lambda v: v.replace('/', ','), lines)

# joinで改行付きの全レコードを結合したあと、stripメソッドで最終レコードの改行だけを取り除く
result = "".join(lines).strip()

# 加工された結果を out_file で指定したファイル名で出力する
with open(out_file, "wt", encoding="utf-8") as fw:
    fw.write(result)

print("saved.")
