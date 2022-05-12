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
payement_data[payement_data.customerID == 23538416 ]

# %%
payement_data.amount.isna()

# %%
## first method 
## work with indepndendenet tables 

## for each customerbalance we need to find 

balance_data.head()
ex = balance_data.iloc[0]

# %%
def  get_payements( id , vfrom , vto ) : 
    ## first check if the client with id has make any payement or the payement amount is NUll 
    if (payement_data[payement_data.customerID  == id].empty or payement_data[payement_data.customerID  == id].amountUSD == np)




# %%
balance_data.head(4)

# %%
payement_data[payement_data.customerID  == 23754192].amountUSD.isna()

# %%
## 2nd method 

balance_data.head(3)

# %%
# ['customerID' , 'type' , 'value' , 'date']
# key = (customerid , balance_data_range) == balanceid


# balanceid|type|value
# 496085452|depot|500 
# 501243830|balanceamount| 600
# 501243830|betamount| 200
# 501243830|bonusus| 200


# %%
### 2nd method
balance_data[['customerID' , 'validFrom' ,  'validTo']].apply(get_type)

def get_type(id , vfrom , cto) : 
    
    bonus_data[bonus_data['customerID'] == id]
   

# %%
bonus_data[bonus_data['customerID'] == 27796384]

# %%
final_data = pd.DataFrame(columns=['balanceID' ,'transaction_id', 'type' , 'value' ,'balance' ])

final_data

# %%
transaction_type = {1 : 'deposit' , 4 :'widthdraw' , 5 : 'chargeback' , 6 : 'refund' }
import numpy as np 
def check_date(date , start , end) : 
    return start<= date<= end
j = 0 
for index in balance_data.index : 
    #print(balance_data.iloc[index])
    temp_pay_data = payement_data[payement_data.customerID  == balance_data.loc[index , "customerID"]]
    for i in temp_pay_data.index : 
        #print(transaction_type[payement_data.iloc[i ]])
        if check_date(temp_pay_data.loc[i , 'createdateUTC'] , balance_data.loc[index , "validFrom" ] , balance_data.loc[index , "validTo" ]) :
            if temp_pay_data.loc[i , "transactionTypeID" ]in [1,4,5,6] and temp_pay_data.loc[i , "transactionStatusID"  ] == 1:
                bid = balance_data.loc[index , "balanceID"]
                bamount = balance_data.loc[index , "balance"]
                tid = temp_pay_data.loc[i , "paymentTransactionID"]	
                type_t = transaction_type[temp_pay_data.loc[i , "transactionTypeID" ]] 
                value = temp_pay_data.loc[i , "amountUSD" ]
                #print(id , type_t , value)
                # row = [ id,type_t,value ]
                row = pd.DataFrame({'balanceID': [bid], 'transaction_id' : [tid] , 
                    'type' : [type_t],
                    'value' : [value] , 'balance' : [bamount] })
                # np.array([ id,type_t,value ])
                # row = pd.Series(row).T
                final_data = pd.concat([final_data, row], ignore_index = True, axis = 0)
              
                # final_data_2 = pd.concat([final_data_2 , row])
                #print(final_data_2)
    

 

# %%
final_data_2

# %%
## 2nd method : try to work with vectors
transaction_type = {1 : 'deposit' , 4 :'widthdraw' , 5 : 'chargeback' , 6 : 'refund' }
def check_date(date , start , end) : 
    return start<= date<= end
for index in balance_data.index : 
    bid = balance_data.loc[index , "balanceID"]
    cid = balance_data.loc[index , "customerID"]
    vfrom = balance_data.loc[index , "validFrom"]
    vto = balance_data.loc[index , "validTo"]
    temp_payement_data = payement_data[payement_data.customerID == cid][['customerID' , 'createdateUTC' , 'transactionTypeID' , 'amountUSD']]
    if not (temp_payement_data.empty ):
        temp_payement_data['pick'] = temp_payement_data['createdateUTC'].apply(lambda x : vfrom<= x<= vto) 
        temp_payement_data['type'] = temp_payement_data['transactionTypeID'].apply(lambda x :transaction_type[x] if x in [1,4,5,6] else x) 
        final_temp_data = temp_payement_data[temp_payement_data.pick == True]
        final_temp_data['balanceID'] = bid 
        final_temp_data['value'] = final_temp_data['amountUSD'] 
        output = final_temp_data[['balanceID' ,'type', 'value']]
        final_data = pd.concat([final_data , output])
    

        




# %%
final_data.type.value_counts()

# %%
## bonus add 
final_data_3 = pd.DataFrame(columns=['balanceID' , 'type' , 'value'])
transaction_type = {1 : 'deposit' , 4 :'widthdraw' , 5 : 'chargeback' , 6 : 'refund' }
import numpy as np 
def check_date(date , start , end) : 
    return start<= date<= end
j = 0 
for index in balance_data.index : 
    #print(balance_data.iloc[index])
    temp_bonus_data = bonus_data[bonus_data.customerID  == balance_data.loc[index , "customerID"]][['bonusID' , 'amount' ,'dateUtc' ]]
    for i in temp_bonus_data.index : 
        #print(transaction_type[payement_data.iloc[i ]])
        if check_date(temp_bonus_data.loc[i , 'dateUtc'] , balance_data.loc[index , "validFrom" ] , balance_data.loc[index , "validTo" ]) :
                bid = balance_data.loc[index , "balanceID"]
                bamount = balance_data.loc[index , "balance"]
                tid = temp_bonus_data.loc[i , "bonusID"]	
                type_t = 'bonus'
                value = temp_bonus_data.loc[i , "amount" ]
                row = pd.DataFrame({'balanceID': [bid], 'transaction_id' : [tid] , 
                    'type' : [type_t],
                    'value' : [value] , 'balance' : [bamount] })
                final_data = pd.concat([final_data, row], ignore_index = True, axis = 0)
              
                # final_data_2 = pd.concat([final_data_2 , row])
                #print(final_data_2)
    

 

# %%
final_data_3

# %%
## add bets (wins and loses)
final_data_4 = pd.DataFrame(columns=['balanceID' , 'type' , 'value'])
transaction_type = {1 : 'deposit' , 4 :'widthdraw' , 5 : 'chargeback' , 6 : 'refund' }
import numpy as np 
def check_date(date , start , end) : 
    return start<= date<= end
j = 0 
for index in balance_data.index : 
    #print(balance_data.iloc[index])
    temp_bet_data = bets_data[bets_data.customerID  == balance_data.loc[index , "customerID"]]
    for i in temp_bet_data.index : 
        #print(transaction_type[payement_data.iloc[i ]])
        if check_date(temp_bet_data.loc[i , 'dateUtc'] , balance_data.loc[index , "validFrom" ] , balance_data.loc[index , "validTo" ]) :
                bid = balance_data.loc[index , "balanceID"]
                bamount = balance_data.loc[index , "balance"]
                tid = temp_bet_data.loc[i , "casinoBetID"]
                type_t = 'bets'
                value = temp_bet_data.loc[i , "grossProfit" ]
                row = pd.DataFrame({'balanceID': [bid], 'transaction_id' : [tid] , 
                    'type' : [type_t],
                    'value' : [value] , 'balance' : [bamount] })
                final_data = pd.concat([final_data, row], ignore_index = True, axis = 0)
              
                # final_data_2 = pd.concat([final_data_2 , row])
                #print(final_data_2)
    

 

# %%
final_data_4

# %%
from scripts.utils import save_data
save_data(final_data , 'row_equation_data_1')

# %%
## read_saved_data 
import pandas as pd 
final_data = pd.read_csv('data_dump/row_equation_data.csv')
final_data.head()

# %%
## check for the null values 
print('value calumn null values : ' , final_data.value.isna().sum())
print('balance calumn null values : ' , final_data.balance.isna().sum())

# %%
## verify the equation : deposit-widthrow - refunds - chargeback - (bets - wins) + bonus = balance
## verify the equation : deposit-widthrow - refunds - chargeback - (grossprofit)  + bonus = balance
def verify(df) : 
    left_side = 0 
    first_index = df.index[0]
    balance = df.loc[first_index, 'balance'	] 
    for i in df.index : 
        t = df.loc[i , 'type'	] 
        v = df.loc[i , 'value'	] 
        if t == 'deposit' : 
            left_side += v 
        elif t in ['widthdraw' , 'refund' ,'chargeback'] : 
            left_side -= v
        elif t == 'bets' : 
            left_side -= v
        elif t == 'bonus' : 
            left_side += v
    
    test = balance == left_side
    row = pd.DataFrame({ 'left_side' : [left_side] , 'right_side' : [balance]  , 'equation_test': [test]})
    return row

x = final_data[final_data.balanceID == 491804323]

# %%
x

# %%
## test the verify function 
verify(x) 

# %%
## aplly the verify function to each balance id 

result = final_data.groupby('balanceID').apply(verify ).reset_index()[['balanceID'  , "left_side" ,"right_side" , "equation_test"]]
result


# %%
## save the results into equationresult table 
save_data(result , 'equation_results')


# %%
## final result 

# balanceid || verified || 

# %%
### next step 
## update customer samples to only match the casino games (with productid) //1
## udate the payement transaction with the status transaction 


# %%
## insights 
## when dropping the trasaction with status diff to 1 we loose almost half of the payements data points 
##  most of the shoosen balances dosen't have any transactions 
##