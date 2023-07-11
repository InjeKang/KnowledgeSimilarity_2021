import arviz as az
import bambi as bmb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import nbinom

import os

az.style.use("arviz-darkgrid")

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

os.chdir("D:/Analysis/2021_Similarity/data")
data = pd.read_excel("12.Result_v8(final2).xlsx", engine="openpyxl", sheet_name = "Sheet1")