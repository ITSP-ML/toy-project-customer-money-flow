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
data = pd.read_csv("data_dump/equation_results_2.csv")
balance = pd.read_csv("data_dump/balance_data_0.csv")

# %%
balance.head()

# %%
## first check the balcens that veridie the equation per state (current or not )
# data = result.merge(balance[["balanceID" , "isCurrent"]] , on= "balanceID")
data["differance"]  = np.abs(data.left_side - data.right_side)
data.head()

# %%
data_x = data.groupby('customerID')["differance"].apply(list).reset_index().merge(data.groupby('customerID')["date"].apply(list).reset_index() , on='customerID' ).merge(data.groupby('customerID')["nb_transaction"].apply(list).reset_index() , on='customerID' ).merge(data.groupby('customerID')["last_day_bets"].apply(list).reset_index() , on='customerID' ).merge(data.groupby('customerID').size().reset_index() , on='customerID')
data_x

# %%
data_y = data_x[data_x[0]>2]
for index,row in data_y.iterrows() : 
    print(row.customerID)
    plt.scatter(row.date , row.differance , c = row.nb_transaction)
    plt.show()
    # plt.scatter(row.date , row.nb_tras)
    

# %%
data_y = data_x[data_x[0]>2]
for index,row in data_y.iterrows() : 
    print(row.customerID)
    plt.scatter(row.date , row.differance , c = row.last_day_bets)
    plt.show()
    # plt.scatter(row.date , row.nb_tras)
    

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
balance[balance.balanceID == 491768427]

# %%
balance[balance.balanceID == 499907698]

# %%
balance[balance.customerID == 27230192]

# %%
data[data.isCurrent == True  ][data.equation_test == True] [data.right_side != 0.0]

# %%
## all verified balance that are diff from 0 are curr balance and the only balance for this customer 

# %%
## verifie te effect of last day bets 
plt.figure(figsize=(10, 10))
sns.scatterplot(data.last_day_bets , data.differance)
plt.show()

# %%
## extract boolean column from last day bets 
data["risque_factor"] = data.last_day_bets.apply(lambda x : True if x == 0 else False )
data.left_side = data.left_side.apply(lambda x : np.round(x , 2))
data["equation_test"] = data.left_side == data.right_side
data

# %%
## bar plot for differance 
bar_data = data.groupby(["risque_factor"]).equation_test.value_counts().unstack(0)
bar_data


# %%
plt.figure(figsize= (6,7))
bar_data.plot.bar()
plt.show()

# %%
## get the number of balances with 0 transaction 
data[data.nb_transaction ==0].equation_test.value_counts()

# %%
data[data.nb_transaction ==0]

# %%
## rique factor can't explain false balance esuation alone 

# %%
