# %%

# Change the working directory to the project root
%cd C:\Users\feress\Documents\myprojects\toy-project-customer-money-flow

# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
## test the module whithout change 
from src.dataload.str_query_parser import parse_query 

query = """select top 100 * 
from table
where x > 100"""
print(parse_query(query))


# %%
# test the module with changes 
## test the module whithout change 
from src.dataload.str_query_parser import parse_query 

query = """select top 100 * 
from table
where x > 100"""
print(parse_query(query))


# %%
