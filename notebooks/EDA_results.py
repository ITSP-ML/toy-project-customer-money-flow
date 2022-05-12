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
data[data.equation_test ==  False].sample(50)

# %%
