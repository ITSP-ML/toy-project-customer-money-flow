# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload
# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## get customurs balance 

from src.dataload.str_query_parser import parse_query
from src.dataload.customers_balance import test_query
from scripts.utils import save_data
import pandas as pd
## get the currient customer balance 
## we need to specify a simple of customers, datapoints(daily , weekly or something else) and in witch
#  product we want to track them

## set variable for query
nb_customers  = 1000
dates : 2021 
productid : 3






# %%
query = """Select * 
from dimCustomerBalance
where isCurrent = 1"""
data = test_query(query)
save_data(data)

# %%
df = pd.read_csv('data_dump\save.csv')
df.head()

# %%
## rethinking about the sampling methode
## first we should get a random sample from our database and those simple should represent the hole population 
## first we need to check the distribution of the hole data 

# %%


query = """Select balance
from dimCustomerBalance
where isCurrent = 1 """
data = test_query(query)
#save_data(data)

# %%
import matplotlib.pyplot as plt 
import numpy as np 
plt.hist(data[data["balance"] <1000000 ])

# %%
### normaliza the balance 
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
new_data = scaler.fit_transform(data)


# %%
## the distribution of the data is right skewed 
## get some statistical muserement 
## median : 0.0
data.balance.median()
# mean  : 0.7221854274093932
data.balance.mean()
# mode : 0.0
data.balance.mode()
## max and min 
data.describe()

# %%
data.skew()

# %%
### apply log transformation to the data to remove skiewness
log_data = np.log(data[data['balance']>0])
plt.hist(log_data)

# %%
import seaborn as sns 
sns.displot(log_data )

# %%
## select 1000 currient balance 
## first we need all data from dimcustomerballance


# %%
query = """select * 
from dimCustomerBalance join (Select db.customerID  
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1) as final_ids
on dimCustomerBalance.customerID = final_ids.customerID"""
balance_data = test_query(query)
save_data(balance_data , "balance_data_0")

# %%



query = """select * 
from dimCustomerBalance join (Select db.customerID  
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1) as final_ids
on dimCustomerBalance.customerID = final_ids.customerID"""
balance_data = test_query(query)
save_data(balance_data , "balance_data_0")

# %%
