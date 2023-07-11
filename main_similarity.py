from modules.similarity import *
from modules.StrategicDiagram_npi import *
from modules.StrategicDiagram_ngi import *
from modules.AlliancePerformance import *
from modules.GlobalVariables import *
from os.path import join

import pandas as pd
import os
from functools import partial
import swifter


def main():
    data = functions_(
        # read data
        read_data = True, 
        # preprocess: adding control variables / accumulating patent stock / thesaurus of firms' name
        ctrlVar = False, ctrlVar2 = True, patentStock = False,
        # affil_cleaned = False,
        # measuring technological similarity
        tech_sim = False,

        # measuring status similarity        
        # # strategic diagram of firms
        strategicFirm = False,
        # # strategic diagram of IPCs
        strategicIPC = False,

        # status_similarity
        status_similarity = False,

        # measuring alliance performance        
        alliance_performance = False)


def functions_(read_data, ctrlVar, ctrlVar2, patentStock,
                tech_sim, strategicFirm, strategicIPC, status_similarity, 
                alliance_performance):
    raw_data = func_read_data("13.Robustness_v4(ctrlVar)", "Sheet1", read_data)
    output_techSim = func_tech_sim(raw_data, tech_sim)
    data1 = func_ctrlVar(raw_data, "10.compustat_v1.xlsx", "Sheet1", ctrlVar)
    data2 = func_ctrlVar2(raw_data, ctrlVar2)
    patent_data = func_patentStock(patentStock)
    output_techSim = func_tech_sim(raw_data, tech_sim)
    output_strategicFirm = func_strategicFirm(raw_data, strategicFirm)
    output_strategicIPC = func_strategicIPC(raw_data, strategicIPC)
    output_statusSim = func_status_similarity(raw_data, status_similarity)
    output_perf = func_alliance_performance(output_strategicIPC, alliance_performance)

    return data2

def func_read_data(filename, sheet_, read_data):
    if read_data:
        input_path = join(os.getcwd(), "data")
        os.chdir(input_path)
        if filename.endswith("xlsx"):
            data = pd.read_excel(filename, engine="openpyxl", sheet_name = sheet_)
        else:
            data = pd.read_pickle(filename)
        return data
       
    #    # to make alliance formation from 2000 to 2016
    #     data2 = data.copy()
    #     for i in range(2001, 2017):            
    #         new_data = data.copy()
    #         new_data["year"] = np.where(new_data["year"] == 2000, i, "error")
    #         new_data["year"] = new_data["year"].astype(float)
    #         data2 = pd.concat([data2, new_data])
    #     data2 = data2.reset_index(drop=True)
    #     data2.to_pickle("13.Robustness_v3(allForm3)")
    #     return data2     
        

def func_ctrlVar (raw_data, filename, sheet_, ctrlVar):
    if ctrlVar:
        # read firm data
        input_path = os.getcwd() # because already desginated in the previous function
        os.chdir(input_path)
        firmData = pd.read_excel(filename, engine="openpyxl", sheet_name = sheet_)
        # multiproces
        # target_func_ = partial(add_ctrl_var, firmData)
        # output = multi_process(raw_data, target_func_, "df")
        output = add_ctrl_var(firmData, raw_data)
        output.to_excel("13.Robustness_v4(ctrlVar).xlsx", index = False)
        output.to_pickle("13.Robustness_v4(ctrlVar)")
        return output

def func_ctrlVar2 (raw_data, ctrlVar2):
    """additional control variables included for the final analysis"""
    if ctrlVar2:
        patent_stock = pd.read_pickle("10.patent_stock")
        del patent_stock["index"]
        # multiproces
        target_func_ = partial(add_ctrl_var2, patent_stock)
        output = multi_process(raw_data, target_func_, "df")
        # output = add_ctrl_var2(patent_stock, raw_data)
        output.to_excel("13.Robustness_v5(ctrlVar2).xlsx", index = False)
        output.to_pickle("13.Robustness_v5(ctrlVar2)")
        return output

def func_patentStock(patentStock):
    if patentStock:
        input_path = os.getcwd()
        patent_stock = read_xlsx_directory(input_path)
        patent_stock.to_pickle("10.patent_stock")
        return patent_stock

def func_tech_sim(data, tech_sim): 
    if tech_sim:
        # del data["Unnamed: 0"]
        patent_stock = pd.read_pickle("10.patent_stock")
        del patent_stock["index"]
        target_func_ = partial(measure_similarity, patent_stock)
        data2 = multi_process(data, target_func_, "df")
        data2.to_excel("13.Robustness_v3.2(tech_sim).xlsx", index = False)
        data2.to_pickle("13.Robustness_v3.2(tech_sim)")  
        # data["tech_sim"] = data.swifter.apply(lambda x: measure_similarity(
        #     x["focal"], x["partner"], x["year"], patent_stock), axis = 1)
        # data.to_excel("13.Robustness_v3.2(tech_sim).xlsx", index = False)
        # data.to_pickle("13.Robustness_v3.2(tech_sim)")
        return data2


def func_strategicFirm(data, strategicFirm):
    if strategicFirm:
        patent_stock = pd.read_pickle("10.patent_stock")
        del patent_stock["index"]
        del data["Unnamed: 0"]
        # measuring ngi of firms
        # ngiFirm = ngiFirm_to_alliance(patent_stock, data)
        target_func = partial(ngiFirm_to_alliance, patent_stock)
        ngiFirm = multi_process(data, target_func, "df")
        # measuring npi for firms
        # npiFirm = npiFirm_to_alliance(patent_stock, data)
        target_func = partial(npiFirm_to_alliance, patent_stock)
        npiFirm = multi_process(ngiFirm, target_func, "df")
        npiFirm.to_excel("12.Result_v3(npiFirm).xlsx", index = False)
        return npiFirm

def func_strategicIPC(data, strategicIPC):
    if strategicIPC:
        patent_stock = pd.read_pickle("10.patent_stock")
        del patent_stock["index"]
        # measuring ngi of IPCs     
        # data = data.head(5)
        # ngiIPC = ngiIPC_to_alliance(patent_stock, data)   
        target_func = partial(ngiIPC_to_alliance, patent_stock)
        ngiIPC = multi_process(data, target_func, "df")
        ngiIPC.to_excel("12.Result_v4(ngi_IPC2).xlsx", index = False)
        print("ngi_IPC done!")
        # measruing npi of IPCs
        # npiIPC = npiIPC_to_alliance(patent_stock, ngiIPC)
        target_func = partial(npiIPC_to_alliance, patent_stock)
        npiIPC = multi_process(ngiIPC, target_func, "df")
        npiIPC.to_excel("12.Result_v4(ngi_npi_IPC2).xlsx", index = False)
        return ngiIPC

def func_status_similarity(raw_data, status_similarity):
    if status_similarity:
        # drop empty rows
        data = raw_data.copy()
        # into vector
        data["status_focal"] = data.swifter.apply(lambda x: status_position(x["npi_focal"], x["ngi_focal"]), axis = 1)
        data["status_partner"] = data.swifter.apply(lambda x: status_position(x["npi_partner"], x["ngi_partner"]), axis = 1)
        data["status_IPC_focal"] = data.swifter.apply(lambda x: status_position(x["npi_IPC_focal"], x["ngi_IPC_focal"]), axis = 1)
        data["status_IPC_partner"] = data.swifter.apply(lambda x: status_position(x["npi_IPC_partner"], x["ngi_IPC_partner"]), axis = 1)
        # euclidean distance between two vectors
        data["status_similarity_firm"] = data.swifter.apply(lambda x: np.linalg.norm(x["status_focal"] - x["status_partner"]), axis = 1)
        data["status_similarity_IPC"] = data.swifter.apply(lambda x: np.linalg.norm(x["status_IPC_focal"] - x["status_IPC_partner"]), axis = 1)
        data.to_excel("12.Result_v6(status_similarity).xlsx", index = False)
        return data

def func_alliance_performance(raw_data, alliance_performance):
    if alliance_performance:
        patent_stock = pd.read_pickle("10.patent_stock")
        del patent_stock["index"]      
        # raw_data = raw_data.loc[raw_data["focal"] == "texasinstruments"]
        target_func_ = partial(performance_stock, patent_stock)
        data2 = multi_process(raw_data, target_func_, "df")
        # data2 = performance_stock(patent_data, raw_data)
        data2.to_excel("12.Result_v8(final4_sensitivity).xlsx", index = False)
        return data2


if __name__ == "__main__":
    main()