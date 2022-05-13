# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## hypothesis 2:: there is some date related issue in the database 
import pandas as pd 
import seaborn as sns 
import numpy as np 
import matplotlib.pyplot as plt 
from src.utils.utils import save_data

# %%
## import row data and result data  and balance data
row_data = pd.read_csv("data_dump/row_equation_data_1.csv")
result = pd.read_csv("data_dump/equation_results.csv")
balance = pd.read_csv("data_dump/balance_data_0.csv")

# %%
balance.head()

# %%
## first check the balcens that veridie the equation per state (current or not )
data = result.merge(balance[["balanceID" , "isCurrent"]] , on= "balanceID")
data["differance"]  = data.left_side - data.right_side
data.head()

# %%
## set a barplot with hue set to iscurrent 
df = data.groupby('equation_test').isCurrent.value_counts().unstack(0)
df

# %%
plt.figure(figsize=(10,10))
df.plot.bar()
plt.show()

# %%
## so for is cuurent values we will try to eliminate all create dates
balance[balance.customerID == 23536480]

# %%
result

# %%
balance[balance.balanceID == 490219209]

# %%
result[result.balanceID ==490253835]

# %%
