from tkinter import * 
from tkinter import messagebox

with open('exportvalues.dat', 'r') as _file:
    _s = _file.read()

_values = _s.split()
_val3 = float(_values[0])
_val4 = float(_values[1])
_val5 = float(_values[2])
_val6 = float(_values[3])
_val7 = float(_values[4])
_val8 = float(_values[5])
_val9 = float(_values[6])


with open("pneumatic_armature_parser_table.csv", "r") as _file:
    lines = _file.readlines()

messagebox.showinfo("Pneumatic parser", "Подпрограмма выборки готова. Чтобы начать, нажмите 'ок'")

with open("results_parser.csv", "w") as _file:
    for line in lines:
        data = line.strip().split(",")
        try:
            if len(data) >= 9:
                c = float(data[2])
                d = float(data[3])
                e = float(data[4])
                f = float(data[5])
                g = float(data[6])
                h = float(data[7])
                i = float(data[8])
                if c == _val3 and d == _val4 and e == _val5 and f == _val6 and g >= _val7 and h <= _val8 and i >= _val9:
                    _file.write(line)
        except:
            pass

messagebox.showinfo("Pneumatic parser", "Работа программы завершнена. Откройте файл results_parser.csv")