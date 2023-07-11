import pandas as pd
import os
import openpyxl

# Pilot test

def read_xlsx_glob(firm_name):
    os.chdir("D:/Analysis/2021_Similarity/data/patent/KISTI")
    patent = openpyxl.load_workbook(firm_name + ".xlsx") # can no longer open xlsx file from pandas' read_excel >> used openpyxl
    sheet = patent["Sheet0"]
    sheet.delete_rows(0, 2)
    firm_patent = pd.DataFrame(sheet.values)
    # firm_patent = firm_patent[[9, 10, 18, 32]] #select columns - application number, application year, assignee, ipc
    # os.chdir("D:/Analysis/2021_Similarity/data")
    return firm_patent  


# alliance
year = 1996

total_list = ["AdvancedMicroDevices", "HewlettPackard", "DupontPhotomasks", "AnalogDevices"]
total = pd.concat((read_xlsx_glob(files) for files in total_list))
total2 = total[(pd.to_numeric(total[10]) >= year-5) & 
        (pd.to_numeric(total[10]) <= year-1)].reset_index(drop=True, inplace=False)

total2.to_excel("test3_1996.xlsx")

amd = read_xlsx_glob("AdvancedMicroDevices")
amd2 = amd[(pd.to_numeric(amd[10]) >= year-5) & 
        (pd.to_numeric(amd[10]) <= year-1)].reset_index(drop=True, inplace=False) 


hp = read_xlsx_glob("HewlettPackard")
hp2 = hp[(pd.to_numeric(hp[10]) >= year-5) & 
        (pd.to_numeric(hp[10]) <= year-1)].reset_index(drop=True, inplace=False) 

dp = read_xlsx_glob("DupontPhotomasks")
dp2 = dp[(pd.to_numeric(dp[10]) >= year-5) & 
        (pd.to_numeric(dp[10]) <= year-1)].reset_index(drop=True, inplace=False) 

ad = read_xlsx_glob("AnalogDevices")
ad2 = ad[(pd.to_numeric(ad[10]) >= year-5) & 
        (pd.to_numeric(ad[10]) <= year-1)].reset_index(drop=True, inplace=False) 

sum(amd2[10].value_counts())
sum(hp2[10].value_counts())
sum(dp2[10].value_counts())
sum(ad2[10].value_counts())