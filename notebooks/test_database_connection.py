# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
from src.dataload.customers_balance import test_query 
query = """select top 100 * 
from dimProduct
where year(validTo)  > 2023"""
test_query(query)

# %%
