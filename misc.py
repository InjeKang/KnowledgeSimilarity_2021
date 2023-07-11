from ntpath import join
from pickletools import read_bytes1
import pandas as pd
import re
import os
import glob
from os.path import join

os.chdir(join(os.getcwd(), "data"))

data = pd.read_excel("11.alliance_v1.xlsx", engine="openpyxl", sheet_name="FirmList")

def fileName(x):
    stopwords = "patent\\KISTI\\", ".xlsx"
    stopwords_ = "|".join(map(re.escape, stopwords))
    x2 = re.sub(stopwords_, "", x)
    return x2


excel_files = glob.glob(("patent\KISTI\*.xlsx"))


for i in range(len(data)):
    excel_files2 = [fileName(x) for x in excel_files]
    if data["f"][i].lower() == excel_files2[i].lower():
        pass
    else:
        print(data["f"][i].lower())
        print(excel_files2[i].lower())
        break
