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
from src.dataload.customers_balance import get_data_from_query
from scripts.utils import save_data
import pandas as pd
## get the currient customer balance 
## we need to specify a simple of customers, datapoints(daily , weekly or something else) and in witch
#  product we want to track them

## set variable for query
random_sample_nb  = 127
year_of_customers : 2021 






# %%
## get the balance data 
query = """select * 
from dimCustomerBalance join (Select db.customerID  
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1) as final_ids
on dimCustomerBalance.customerID = final_ids.customerID"""
balance_data = get_data_from_query(query)
save_data(balance_data , "balance_data_0")

# %%
## get the payement transaction data 
query = """select fpt.paymentTransactionID , fpt.customerID ,amount,  amountUSD , productID , createdateUTC , transactionTypeID ,transactionStatusID
from factPaymentTransaction as fpt  join (Select db.customerID 
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1)
as samples on fpt.customerID = samples.customerID """
payement_data = get_data_from_query(query)
save_data(payement_data , "payement_data_0")

# %%
## get the bonus data 
query = """select * 
from factBonus as b  join (Select db.customerID 
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1)
as samples on b.customerID = samples.customerID """
bonus_data = get_data_from_query(query)
save_data(bonus_data , "bonus_data_0")

# %%
## get the bets data 
query = """select * 
from factBonus as b  join (Select db.customerID 
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1)
as samples on b.customerID = samples.customerID """
bets_data = get_data_from_query(query)
save_data(bets_data , "bets_data_0")

# %%
## get the bets data 
query = """select * 
from factBonus as b  join (Select db.customerID 
	from dimCustomerBalance as db join (select customerID 
	from dimCustomer 
	where customerID % 176= 0 and year(createdate) = 2021  ) as samplecustomer on db.customerID = samplecustomer.customerID  
	group by db.customerID having count(distinct db.productID) =  1)
as samples on b.customerID = samples.customerID """
bets_data = get_data_from_query(query)
save_data(bets_data , "bets_data_0")