from modules.similarity import *
from modules.StrategicDiagram_npi import *
from modules.StrategicDiagram_ngi import *
from modules.AlliancePerformance import *
from modules.GlobalVariables import *
from os import path
import pandas as pd
import os
from functools import partial

def main():
    data = functions_(
        # read/clean data
        read_data = True, read_patent = False, affil_cleaned = False,
        # similarity
        tech_sim = False,
        # strategic diagram
        patent_stock = False, npi_firm = False, ngi_firm = False, firm_revised = True,        
        npi_ipc = False, ngi_ipc = False,
        # alliance performance
        alliance_performance = False)


def functions_(
    read_data, read_patent, affil_cleaned, patent_stock,
    tech_sim, npi_firm, ngi_firm, npi_ipc, ngi_ipc,
    firm_revised, 
    alliance_performance):
    # read/clean data
    raw_data = func_read_data("03.Result_v6.3(thesaurus_revised_npi)_pickle", read_data)
    output_patent_stock = func_read_patent(read_patent)
    output_affil_cleaned = func_affil_cleaned(affil_cleaned)    
    # similarity
    data1 = func_tech_sim(raw_data, tech_sim)
    # strategic diagram
    data2 = func_patent_stock(raw_data, patent_stock)
    data3 = func_npi_firm(raw_data, npi_firm)
    data4 = func_ngi_firm(raw_data, ngi_firm)    
    data5 = func_npi_ipc(raw_data, npi_ipc)
    data6 = func_ngi_ipc(raw_data, ngi_ipc)
    # firm_revised
    data7 = func_firm_revised(raw_data, firm_revised)
    # alliance performance
    data8 = func_alliance_performance(raw_data, alliance_performance)
    return data8

def func_read_data(filename, read_data):
    if read_data:
        input_path = join(os.getcwd(), "data")
        os.chdir(input_path)
        if filename.endswith("xlsx"):
            data = pd.read_excel(filename, engine="openpyxl", sheet_name="alliance")
        else:
            data = pd.read_pickle(filename)
        return data  

def func_read_patent(read_patent):
    if read_patent:
        default_directory = os.getcwd()
        input_path = join(default_directory, "data")
        patent_stock = read_xlsx_directory(input_path, read_patent)
        return patent_stock

def func_affil_cleaned(affil_cleaned):
    if affil_cleaned:
        patent_data = pd.read_pickle("patent_stock")
        patent_data2 = affil_firm(patent_data, "perf")
        patent_data2.to_pickle("patent_stock_v2(affil_cleaned)")        
        return patent_data2


# Measure Similarity
def func_tech_sim(df, tech_sim):
    if tech_sim:
        output = measure_similarity(df)
        output.to_excel("03.Result_v1(20220405).xlsx")
        return output


# Measure Strategic Diagram

## Accumulating Patents Applied duirng the Designated Period
def func_patent_stock(df, patent_stock):
    if patent_stock:
        tech_sim = pd.read_excel("03.Result_v1(20220405).xlsx", engine="openpyxl", sheet_name="Sheet1").drop("Unnamed: 0", axis=1)
        df = accumulate_patent_stock(tech_sim)
        df.to_excel("03.Result_v3(patent_stock).xlsx")
        df.to_pickle("03.Result_v4(patent_stock)_pickle")
        return df

## NPI of firms 
def func_npi_firm(df, npi_firm):
    if npi_firm:
        df = pd.read_pickle("03.Result_v4(patent_stock)_pickle")
        df2 = npiFirm_to_alliance(df)
        df2.to_excel("03.Result_v4(npi).xlsx")
        df2.to_pickle("03.Result_v4(npi)_pickle")
        return df2

## NPI of IPCs
def func_npi_ipc(df, npi_ipc):
    if npi_ipc:
        # df = pd.read_pickle("03.Result_v4(npi)_pickle")
        # df_IPC = npi.IPC_firm(df)
        # df_IPC.to_pickle("03.Result_v4.2(IPC_stock)")
        df_IPC2 = df
        df_IPC2 = pd.read_pickle("03.Result_v4.2(IPC_stock)")
        df3 = npiIPC_to_alliance(df_IPC2)
        df3.to_excel("03.Result_v5(npi_ipc).xlsx")
        df3.to_pickle("03.Result_v5(npi_ipc)_pickle")
        return df3

## NGI of firms
def func_ngi_firm(df, ngi_firm):
    if ngi_firm:
        # df = pd.read_pickle("03.Result_v5(npi_ipc)_pickle")        
        # df_stock = ngi.patent_stock_year(df)
        # df_stock.to_pickle("03.Result_v6(year_added)_pickle")
        df_stock2 = df
        df_stock2 = pd.read_pickle("03.Result_v6(year_added)_pickle")
        df4 = ngiFirm_to_alliance(df_stock2)
        df4.to_pickle("03.Result_v6(ngi_firm)_pickle")
        return df4

## modified thesaurus...because of standard deviation
def func_firm_revised(df, firm_revised):
    if firm_revised:
        # df = pd.read_pickle("03.Result_v6(year_added)_pickle")
        # df = df.drop(columns = ["npi_focal", "npi_partner"]) # because previous data has old results on NPIs of firms (but no results on NGIs)
        # df = lookup.change_from_alliance(df)
        # df2 = multi_process(df, npiFirm_to_alliance, "df")
        # df2.to_pickle("03.Result_v6.3(thesaurus_revised_npi)_pickle")
        # df = df.iloc[0:24]
        df3 = multi_process(df, ngiFirm_to_alliance, "df")
        # df3 = df3[["no", "focal", "partner", "year", "concurent", "similarity",
        #     "npi_ipc_focal", "npi_ipc_partner", "ngi_ipc_focal", "ngi_ipc_partner",
        #     "npi_focal", "npi_partner", "ngi_focal", "ngi_partner"]]          
        # df2 = npiFirm_to_alliance(df)
        # df3 = ngiFirm_to_alliance(df)
        df3.to_excel("03.Result_v6.4(thesaurus_revised).xlsx")
        df3.to_pickle("03.Result_v6.4(thesaurus_revised)_pickle")
        return df3

## NGI of IPCs
def func_ngi_ipc(df, ngi_ipc):
    if ngi_ipc:
        df = pd.read_pickle("03.Result_v6.2(thesaurus_applied)_pickle")
        df2 = multi_process(df, ngiIPC_to_alliance, "df")
        df3 = df2[["no", "focal", "partner", "year", "concurent", "similarity",
        "npi_ipc_focal", "npi_ipc_partner", "ngi_ipc_focal", "ngi_ipc_partner",
        "npi_focal", "npi_partner", "ngi_focal", "ngi_partner"]]        
        df3.to_pickle("04.Result_v2(ThesRevised)_pickle")
        df3.to_excel("04.Result_v2(ThesRevised).xlsx")
        return df3

def func_alliance_performance(df, alliance_performance):
    if alliance_performance:
        patent_data = pd.read_pickle("patent_stock_v2(affil_cleaned)")
        target_func_ = partial(performance_stock, patent_data)
        data2 = multi_process(df, target_func_, "df", patent_data)
        # data2 = performance_stock(raw_data, patent_data)
        data2.to_excel("04.Result_v8(performance).xlsx")
        return data2

if __name__ == "__main__":
    result = main()
    