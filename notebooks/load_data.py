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
from src.dataload.customers_balance import get_data_from_query , create_temporary_table
from src.utils.utils import save_data
import pandas as pd
## get the currient customer balance 
## we need to specify a simple of customers, datapoints(daily , weekly or something else) and in witch
#  product we want to track them

## set variable for query
random_sample_nb  = 176
samples_year  =  2021 
game = 'Casino'





# %%
## create a temporary table for customer samples with the requirement mentioned above  
query = f"""
select customerID
into ##customersample
from dimCustomer join dimProduct WITH (NOLOCK) on dimCustomer.productID = dimProduct.productID
where dimCustomer.customerID % {random_sample_nb}= 0 
and dimProduct.productType = '{game}'
and year(dimCustomer.createdate) = {samples_year} 
"""
create_temporary_table(query)


# %%
## create a temporary table from the customersid and balance table where each customer have only one product
query = """
Select db.customerID 
into ##TempTable
from dimCustomerBalance as db join ##customersample WITH (NOLOCK) as customersample on db.customerID = customersample.customerID  
group by db.customerID having count(distinct db.productID )  = 1 
"""
create_temporary_table(query)

# %%
### get customer data from dimcustmer
query = """
select * 
from dimCustomer join ##TempTable as final_ids
on dimCustomer.customerID = final_ids.customerID
"""
balance_data = get_data_from_query(query)
save_data(balance_data , "customer_data_0")


# %%
## get the balance data 
query = """
select * 
from dimCustomerBalance join ##TempTable as final_ids
on dimCustomerBalance.customerID = final_ids.customerID
"""
balance_data = get_data_from_query(query)
save_data(balance_data , "balance_data_0")


# %%
## get the payement transaction data 
query = """select fpt.paymentTransactionID , fpt.customerID ,amount,  amountUSD , productID , createdateUTC , transactionTypeID ,transactionStatusID
from factPaymentTransaction as fpt  join ##TempTable as samples 
on fpt.customerID = samples.customerID """
payement_data = get_data_from_query(query)
save_data(payement_data , "payement_data_0")

# %%
## get the bonus data 
query = """select * 
from factBonus as b  join ##TempTable as samples 
on b.customerID = samples.customerID """
bonus_data = get_data_from_query(query)
save_data(bonus_data , "bonus_data_0")

# %%
## get the bets data 
query = """select * 
from factCasinoBet as b  join ##TempTable
as samples on b.customerID = samples.customerID """
bets_data = get_data_from_query(query)
save_data(bets_data , "bets_data_0")

# %%
balance_data.head()

# %%
