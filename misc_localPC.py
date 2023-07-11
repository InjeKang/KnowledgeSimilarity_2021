import pandas as pd
import numpy as np
import os
import swifter

os.chdir("D:/Analysis/2021_Similarity/data")


# number of alliances in previous years (Garcia-Pont&Nohira, 2002)
"""
1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 
   6    6   19   21   17   20   24   30   32   61   82   87   88   57   52   75   70   58   40   55   50   44   66   49    3    2    1

"""

data = pd.read_excel("13.Robustness_v6.7(matched2).xlsx", engine="openpyxl", sheet_name = "Sheet1")


def no_priorAll(year, df, type_):
    if year == 2000:
        no_all = sum([30, 32, 61]) # number of alliances formed until Y
        # no_all = 40
        potential_alliance = len(df[df["year"] == year])
        output = no_all / potential_alliance
    elif year == 2001:
        no_all = sum([32, 61, 82])
        # no_all = len(df[(df["year"] == 2000) & (df["formation"] == 1) & (df["top10"] == 1)]) + 30
        potential_alliance = len(df[df["year"] == year])
        output = no_all / potential_alliance
    elif year == 2002:
        no_all = sum([61, 82, 87])
        # no_all = len(df[(df["year"] <= 2001) & (df["formation"] == 1) & (df["top10"] == 1)]) + 19
        potential_alliance = len(df[df["year"] == year])
        output = no_all / potential_alliance
    # elif year == 2003:
    #     no_all = sum([32, 61, 82, 87, 88])
    #     potential_alliance = len(df[df["year"] == year])
    #     output = no_all / potential_alliance
    # elif year == 2004:
    #     no_all = sum([61, 82, 87, 88, 57])
    #     potential_alliance = len(df[df["year"] == year])
    #     output = no_all / potential_alliance
    else:
        no_all = len(df[(df["year"]<year) & (df["year"]>=year-3) & (df["formation"] == 1)]) #  & (df["top10"] == 1)
        potential_alliance = len(df[df["year"] == year])
        output = no_all / potential_alliance
    if type_ == 1:    
        return output
    else:
        return no_all


df2 = data[["focal", "year", "top10", "formation"]]
# data["all_top10"] = data.swifter.apply(lambda x: no_priorAll(x["year"], x["top10"], df2), axis=1)
# data["all_top20"] - data.swifter.apply(lambda x: no_priorAll(x["focal"], x["year"], x["formation"], x["top20"]), axis=1)
data["all_total_no"] = data.swifter.apply(lambda x: no_priorAll(x["year"], df2, 2), axis=1)
data["all_total_density"] = data.swifter.apply(lambda x: no_priorAll(x["year"], df2, 1), axis=1)
data.to_excel("13.Robustness_v6.8(matched3).xlsx", index = False, sheet_name = "Sheet1")





# retrieving top 10/20 firms by revenue
# data = pd.read_excel("99.test_v2.xlsx", engine="openpyxl", sheet_name = "top10firms").iloc[:, 0:8]

# data2 = data.drop_duplicates(subset = ["focal", "year"], keep="first")

# top20 = data2.groupby("year")["revenue"].nlargest(10).reset_index()

# top20.to_excel("D:/Analysis/2021_Similarity/data/99.test_v3.xlsx", index = False, sheet_name = "Sheet2")


# # to make alliance formation from 2000 to 2016
# data2 = data.copy()
# for i in range(2001, 2017):            
#     new_data = data.copy()
#     new_data["year"] = np.where(new_data["year"] == 2000, i, "error")
#     new_data["year"] = new_data["year"].astype(float)
#     data2 = pd.concat([data2, new_data])
# data2 = data2.reset_index(drop=True)


# data2.to_excel("13.Robustness_v2(allForm3).xlsx", index = False)


# for i in range(len(data)):
#     if data["year"][i] == 2000:
#         no_alliance10.append(19)
#         no_alliance20.append(34)
#     else:
#         x = data.loc[(data["top10"]==1) & (data["year"] == data["year"][i]-1) & (data["formation"]==1)]
#         no_x = len(x)
#         no_alliance10.append(no_x)
        
#         y = data.loc[(data["top20"]==1) & (data["year"] == data["year"][i]-1) & (data["formation"]==1)]
#         no_y = len(y)
#         no_alliance20.append(no_y)
        

# data["all_top10"] = no_alliance10
# data["all_top20"] = no_alliance20

# data.to_excel("99.test_v3.xlsx", index = False, sheet_name = "Sheet3")

