# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## hypothesis 1:: the number of transactions can infulence the equation result 


import pandas as pd 
import seaborn as sns 
import numpy as np 
import matplotlib.pyplot as plt 
from src.utils.utils import save_data

# %%
## first we need to result data with count of transaction 
data = pd.read_csv("data_dump/equation_results_3.csv")
data.left_side = data.left_side.apply(lambda x : np.round(x , 4))
data['differance'] = np.abs(data.left_side- data.right_side)
data.head()

# %%
## some statistics about the count of transactions 
plt.hist(data.nb_transaction)
plt.show() 

# %%
## some statistics about the acuumulative count of transactions  
plt.hist(data.acc_nb_transaction)
plt.show() 

# %%
## check for the impact of number of transaction on the differance 
plt.figure(figsize=(10,10))
sns.scatterplot(x= data['nb_transaction' ] , y = data['differance'])
plt.show()

# %%
## check for the impact of number of transaction on the differance 
plt.figure(figsize=(10,10))
sns.scatterplot(x= data['acc_nb_transaction' ] , y = data['differance'])
plt.show()

# %%
## lets have the same data but with barlot
## have the average of differance per nb_of_trasanction 
bar_data = data.groupby('nb_transaction')['differance'].median().reset_index()
fig = plt.figure(figsize=(10,10))
sns.barplot(bar_data.nb_transaction , bar_data.differance)
plt.show()


# %%
## lets have the same data but with barlot
## have the average of differance per nb_of_trasanction 
bar_data = data.groupby('acc_nb_transaction')['differance'].median().reset_index()
fig = plt.figure(figsize=(10,10))
sns.barplot(bar_data.acc_nb_transaction , bar_data.differance)
plt.show()


# %%
"""
 there is some sort of trend but we need to invistigate more 
"""

# %%
## not very clear chart soo we may need to devide them by bins 
def get_bins(arg , x ) : 
    bins 
    if ar
data['transaction_count_bin'] = data.transaction_count.apply(lambda x : 10 if x<10 )

# %%
## barplot for the transactions per differance bins
## first we should shouse the number of bins
## first we need to see the distribution of the the differance columns
## study every type infuendece alone on the balance 
row_data = pd.read_csv("data_dump/row_equation_data_2.csv")
row_data

# %%
x= row_data[row_data.type =='deposit' ].groupby('balanceID').size().reset_index()
plt.figure(figsize=(10,10))
## merge with result data 
df = data.merge(x , on= 'balanceID'  )
## agregate with median all the differance per type_transaction count 
type_data = df.groupby(0).differance.median().reset_index()
sns.barplot(type_data[0] , type_data.differance)
plt.show()


# %%
sns.scatterplot( data[data.customerID == sample[0]].date , data[data.customerID == sample[0]].differance ,)
plt.show()

# %%
## automate this for all the tpes we have 
all_types = row_data.type.value_counts().to_dict()
print("all types : " ,all_types)
fig , axs = plt.subplots(2,3 , figsize=(15,15)) 
plt.figure(figsize=(15,15))
for i , type_x in enumerate(all_types.keys()) :
    x= row_data[row_data.type ==type_x ].groupby('balanceID').size().reset_index()
    ## merge with result data 
    df = data.merge(x , on= 'balanceID' , )
    ## agregate with median all the differance per type_transaction count 
    type_data = df.groupby(0).differance.median().reset_index()
    axs[ i//3 , i%3 ].set(title = type_x)
    sns.barplot(ax =axs[ i//3 , i%3 ] , x= type_data[0] ,  y= type_data.differance) 
    # axs[i , i//3].bar(x= type_data[0] ,  y= type_data.differance)
plt.show()
    


# %%


# %%
## from the chart we can't really detect any correlation 
## it may be unterresting te sea the other transaction types counts


# %%
## add risque_factor 
data["risque_factor"] = data.last_day_bets.apply(lambda x : False if x == 0 else True )
nn_valid = data[data.differance != 0]
## see nn_valid dist 
sns.distplot(nn_valid.differance)

# %%
nn_valid

# %%
## now from those nn_valid values take only the ones 
a = nn_valid[nn_valid.nb_transaction == 0 ]
a.risque_factor.value_counts()
## all the balance that have nb_oftransactions equal to 0 have a risque factor 

# %%
a

# %%
