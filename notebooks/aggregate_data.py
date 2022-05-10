# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload
# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## read all datasets
import pandas as pd 
balance_data = pd.read_csv("data_dump/balance_data_0.csv")
bets_data = pd.read_csv("data_dump/bets_data_0.csv")
bonus_data = pd.read_csv("data_dump/bonus_data_0.csv")
payement_data = pd.read_csv("data_dump/payement_data_0.csv")


# %%
## payement data transformation 
#payement_data.head()
payement_data.groupby("customerID")["amountUSD"].apply(list)

# %%
payement_data[payement_data.customerID == 23538416 ]

# %%
payement_data.amount.isna()

# %%
