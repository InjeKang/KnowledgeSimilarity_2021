import pandas as pd
import os

file = os.listdir("D:/Analysis/2021_Similarity/data/patent/KISTI")
file = [x for x in file if str(x) != "old_data"]
firm = pd.read_excel("D:/Analysis/2021_Similarity/data/firm_list.xlsx", engine="openpyxl")
firm = firm[4].tolist()

for i in range(len(firm)):
    if file[i].lower() == firm[i].lower():
        print("good")
    else:
        print("error form # {}".format(i+1))
        file[i]
        firm[i]
        break
