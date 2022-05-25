# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## read equatio results

import pandas as pd
data = pd.read_csv('data_dump/equation_results.csv')
data.head()

# %%
data["equation_test"] = data.left_side == data.right_side
data['differance'] = data.left_side  - data.right_side

# %%
## read equatio results

import pandas as pd
data = pd.read_csv('data_dump/equation_results.csv')
data.head()

# %%
## plot the distribution of the the equation result in a pie chart 

import matplotlib.pyplot as plt 
import seaborn as sns 
fig = plt.figure(figsize=(10,10))
pie_data = data.groupby('equation_test').size()
plt.pie(pie_data , labels=['not verified' , 'verified'  ] , autopct='%.0f%%')
plt.show()

# %%
## most of values are false 
## lets try to make a tolerance range 
##1$ tolerance vs 1% tolerance 

# %%

## first we need to add the differance between balance and calculated balance 
import numpy as np 
data['differance'] = np.abs(data.left_side - data.right_side )
## keep only the data with less then 1$ diff
fig = plt.figure(figsize=(10,10))
less_then_1 = data['differance'].apply(lambda x : True if x > 1 else  False  )
plt.pie(less_then_1.value_counts(), labels=['not verified' , 'verified'  ] , autopct='%.0f%%')
plt.show()

# %%
data['differance'].hist()

# %%
import numpy as np 
x = data[data['differance'] < 1]["differance"]
x.hist()

# %%
## pick random samples from the unvirified equation 
sample = data[data.equation_test ==  False].sample(50)
sample.head()

# %%
## find more information about those results from the row equation data 
balance_data = pd.read_csv("data_dump/balance_data_0.csv")
bets_data = pd.read_csv("data_dump/bets_data_0.csv")
bonus_data = pd.read_csv("data_dump/bonus_data_0.csv")
payement_data = pd.read_csv("data_dump/payement_data_0.csv")
row_data = pd.read_csv('data_dump/row_equation_data_1.csv')

# %%
bid  = sample.iloc[0].balanceID
left = sample.iloc[0].left_side
right = sample.iloc[0].right_side
print(f'balance: {bid } has calculated balance {left} and balance {right}')
## get the balance info 
balance_data[balance_data.balanceID == bid]



# %%
## get the customer id 
cid  = balance_data[balance_data.balanceID == bid].customerID.values[0]
## get all transaction don by the customer
## start with payement transactions 
payement_data[payement_data.customerID == cid]
bonus_data()

# %%


# %%
## it may be smart to ceheck the curreient balances and verifie all the transaction and bonusand bets that he had in all times
## to ckeck if this equation is false cause of aqusation delai  related problemes

# %%
## take alook at balances that verified the equation 

verified_balance = data[data.equation_test == True].right_side
sns.histplot(verified_balance)


# %%
## get the value count 
verified_balance.value_counts()

# %%
## add the number of transaction as a features

# %%
data[(data.equation_test == True) ][data.right_side != 0.0  ]

# %%


# %%
"""
# 2nd try 
"""

# %%
## read equatio results

import pandas as pd
data = pd.read_csv('data_dump/equation_results_2.csv')
data.left_side = data.left_side.apply(lambda x : np.round(x , 4))
data["equation_test"] = data.left_side == data.right_side
data["differance"] = np.abs(data.left_side - data.right_side)
data.head()

# %%
## plot the distribution of the the equation result in a pie chart 

import matplotlib.pyplot as plt 
import seaborn as sns 
fig = plt.figure(figsize=(10,10))
pie_data = data.groupby('equation_test').size()
plt.pie(pie_data , labels=['not verified' , 'verified'  ] , autopct='%.0f%%'  , colors=['b' , 'y'])
plt.show()

# %%

## keep only the data with less then 1$ diff
fig = plt.figure(figsize=(10,10))
less_then_1 = data['differance'].apply(lambda x : True if x >1 else  False  )
plt.pie(less_then_1.value_counts(), labels=['verified' ,'not verified'   ] , autopct='%.0f%%' , colors=['y' , 'b'])
plt.show()

# %%
less_then_1 = data['differance'].apply(lambda x : True if x <=1 else  False  )
less_then_1.value_counts()

# %%
data.differance.hist()

# %%
