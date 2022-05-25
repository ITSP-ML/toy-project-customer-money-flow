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
pd.set_option('display.max_columns', None)
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
def check_date(date , end) : 
    return  date<= end
j = 0 
for index in balance_data.index : 
    #print(balance_data.iloc[index])
    temp_bonus_data = bonus_data[bonus_data.customerID  == balance_data.loc[index , "customerID"]][['bonusID' , 'amount' ,'dateUtc' ]]
    for i in temp_bonus_data.index : 
        #print(transaction_type[payement_data.iloc[i ]])
        if check_date(temp_bonus_data.loc[i , 'dateUtc'] , balance_data.loc[index , "validTo" ]) :
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
final_data = pd.read_csv('data_dump/row_equation_data_1.csv')
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
transactions_count = final_data.groupby('balanceID')["transaction_id"].count().reset_index()
transactions_count

# %%
## create data for the first_hypotheses
## join th result with the nb_transactions 
result.join(transactions_count , on = "balanceID" , lsuffix="_left" ,rsuffix='_right' )
hyp_1 = pd.merge(result, transactions_count, on="balanceID")
hyp_1.rename(columns={'transaction_id' : 'transaction_count'} , inplace= True)
save_data(hyp_1 , 'hyp_1_data')
hyp_1.head()

# %%

nb_transactions = final_data.groupby(['balanceID' , 'type']).type.size()
nb_transactions
def count_types(df) : 
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
final_data[final_data.balanceID == 490203840  ].groupby('type').size()

# %%
test = result


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

# %%
"""
# 2nd try 
"""

# %%
import pandas as pd
final_data = pd.DataFrame(columns=['balanceID' ,'transaction_id', 'type' , 'value' ,'balance' ])
import datetime as dt 
date_format = "%Y-%m-%d %H:%M:%S.%f"

# %%
def add_zero_padding(str_date) : 
    if len(str_date.split('.') ) > 1: 

        reste_of_date , micro_seconds = str_date.split('.')
        nb_of_degits = len(micro_seconds)
        if nb_of_degits < 6  : 
            micro_seconds = '0'*(6-nb_of_degits) + micro_seconds

        return reste_of_date +'.'+ micro_seconds
    else : 
        return str_date
    


add_zero_padding("2021-01-07 14:35:51.573")

# %%

def change_to_datetime(str_date , format ) : 
    if len(str_date.split())> 1 :
        if len(str_date.split('.')) > 1 :  
            return dt.datetime.strptime( str_date, format)
        else : 
            format_without_second = format.split('.')[0]
            return dt.datetime.strptime( str_date, format_without_second)
    else : 
        ## for only date without houres
        format_without_houres = format.split()[0]
        return dt.datetime.strptime( str_date, format_without_houres)

change_to_datetime("2021-01-07 14:35:51.000573" ,date_format )
change_to_datetime("2021-01-01 05:00:00" ,date_format )

# %%
def correct_sign(type , value ) : 
    if type == 1 : 
        return value
    else : 
        return -value  
# pre_payement_data[['type' , 'amountUSD']].apply(correct_sign)
pre_payement_data.apply(lambda x: correct_sign(x['type'], x['amountUSD']), axis=1)


# %%
transaction_type = {1 : 'deposit' , 4 :'widthdraw' , 5 : 'chargeback' , 6 : 'refund' }
pre_payement_data = payement_data[payement_data.transactionTypeID.isin([1,4,5,6]) ][payement_data.transactionStatusID == 1]
pre_payement_data['value'] = pre_payement_data.apply(lambda x: correct_sign(x['transactionTypeID'], x['amountUSD']), axis=1)
pre_payement_data['type'] = pre_payement_data.transactionTypeID.apply(lambda x : transaction_type[x])
data1 = pre_payement_data[['customerID' ,"type" , "amountUSD" ,"createdateUTC" ,"paymentTransactionID" ]]
data1.columns =["customerID" , "type" ,"value" , "date" , 'uid']
## add zero padding to date 
data1.date = data1.date.apply(lambda x : add_zero_padding(x))
## transfrom to date time
data1.date = data1.date.apply(lambda x : change_to_datetime(x , date_format))
data1

# %%
pre_bonus_data = bonus_data
pre_bonus_data['type'] = 'bonus'
data2 = pre_bonus_data[['customerID' ,"type" , "amount" ,"dateUtc" , 'bonusID']]
data2.columns =["customerID" , "type" ,"value" , "date" , 'uid']
## add zero padding to date 
data2.date = data2.date.apply(lambda x : add_zero_padding(x) )
## transfrom to date time
data2.date = data2.date.apply(lambda x : change_to_datetime(x , date_format) )
data2

# %%
pre_bets_data = bets_data
pre_bets_data['type'] = 'bets'
data3 = pre_bets_data[['customerID' ,"type" , "grossProfit" ,"dateUtc" , "casinoBetID"]]
data3.columns =["customerID" , "type" ,"value" , "date" , 'uid']
## set the value ready for the equation 
data3.value = -data3.value
## add zero padding to date 
data3.date = data3.date.apply(lambda x : add_zero_padding(x) )
## transfrom to date time
data3.date = data3.date.apply(lambda x : change_to_datetime(x , date_format) )
data3

# %%
pre_balance_data = balance_data
pre_balance_data['type'] = 'balance'
data4 = pre_balance_data[['customerID' ,"type" , "balance" ,"validFrom", "balanceID"]]
data4.columns =["customerID" , "type" ,"value" , "date" , "uid"]
## add zero padding to date 
data4.date = data4.date.apply(lambda x : add_zero_padding(x) )
## transfrom to date time
data4.date = data4.date.apply(lambda x : change_to_datetime(x , date_format) )
data4

# %%
data = pd.concat([data1 , data2 , data3 , data4])
data

# %%
x = data[data.customerID == 23626064]
x

# %%

def get_balance_equation(df) :
    final_result = pd.DataFrame(columns = ["balanceID" ,'nb_transaction' ,'acc_nb_transaction' , "left_side" ,"right_side","date"  , "last_day_bets" ,'productID'])
    balances = df[df.type == "balance"]
    prevous_calcul = 0
    previous_nb_transactions = 0 
    prevous_date = pd.to_datetime('1679-09-21 00:12:43.145225')
    for index , row in balances.iterrows():
        right_side = row.value 
        date = row.date
        days = dt.timedelta(1)
        day_before_date = dt.datetime.strftime(dt.datetime.strptime(date , '%Y-%m-%d') - days , '%Y-%m-%d')
        new_df = df[(df.date> prevous_date) & (df.date <=  date) ]
        # print(new_df.shape)
        deposits = new_df[new_df.type == 'deposit'].value.sum()
        withdraws = new_df[new_df.type == 'withdraw'].value.sum()
        chargebacks = new_df[new_df.type == 'chargeback'].value.sum()
        bonuses = new_df[new_df.type == 'bonus'].value.sum()
        bets = new_df[new_df.type == 'bets'].value.sum()
        refunds = new_df[new_df.type == 'refund'].value.sum()
        last_day_bets= df[(df.date> day_before_date) & (df.date <=  date) ]
        last_day_bets  = last_day_bets[last_day_bets.type == 'bets']
        
        # print(deposits , chargebacks , withdraws , refunds , bonuses , bets)
        left_side =prevous_calcul +  deposits - withdraws-chargebacks - refunds - bets + bonuses
        nb_transactions = len(new_df) -1
        acc_nb_transaction = previous_nb_transactions + nb_transactions
        # print(last_day_bets , "hhhhhhhhhhhh" ,len(last_day_bets) )
        prevous_date = date
        prevous_calcul = left_side
        previous_nb_transactions = acc_nb_transaction
        # print(left_side , right_side , left_side == right_side)
        # print(prevous_date , date , )
        row = pd.DataFrame({ 'balanceID' : [row.uid] ,'nb_transaction' : nb_transactions ,'acc_nb_transaction'  : acc_nb_transaction , 'left_side' : [left_side] , 'right_side' : [right_side]  
        ,"date" :  date , "last_day_bets" : len(last_day_bets)})
        final_result = pd.concat([final_result , row])

    return final_result

get_balance_equation(x)
        


# %%
data

# %%
final_data = data.groupby("customerID").apply(get_balance_equation)
final_data

# %%
final_data = final_data.reset_index()
final_data

# %%
save_data(final_data , 'equation_results_3')

# %%
from src.utils.utils import save_data
save_data(data , "row_equation_data_3")

# %%

def get_balance_equation(df) :
    final_result = pd.DataFrame(columns = ['date','type',"value" ,'balance','balance_nb' ])
    balances = df[df.type == "balance"].sort_values(by= "date")
    prevous_calcul = 0
    previous_nb_transactions = 0 
    valid_from = pd.to_datetime('1679-09-21 00:12:43.145225')
    i = 0
    for index , row in balances.iterrows():
        
        ## get for each bets, bonus, payement 
        date = row.date
        new_df = df[(df.date> valid_from) & (df.date <=  date) ]
        others = new_df [new_df.type != "balance"]
        others["balance_nb"] = i
        others["balance"] = row.value 
        final_result =pd.concat([final_result,others[['date','type',"value" ,'balance','balance_nb'  ]]])
        
        valid_from = date
        i = i +1
        
    return final_result

ss = get_balance_equation(x)
        


# %%
aa = data.groupby('customerID').apply(get_balance_equation).reset_index()
aa

# %%
save_data(aa , 'plot_data')

# %%
l = data.sort_values(by =['customerID' , 'date'])
l.iloc[123: ]

# l[l.customerID == 12203664].head(20) ## verified
# l[l.customerID == 23536480].head(70) ## not for all balances  
# l[l.customerID == 23536656].head(20) ## verified (cutomer with only one bonus)
# l[l.customerID == 23536832].head(20) ## not verified (verified if risque factor = True), he play with bonus wons and lose it all , 59 
# l[l.customerID == 23537008].head(20) ## verified (one balance) , 42 
# l[l.customerID == 23537184].head(20) ## veried  (probably bonus balance but the real balance sosent change because he didnt win), 42
# l[l.customerID == 23537360].head(20) ##  verified (one balance) , 41 
# l[l.customerID == 23537536].head(20) ## not verified (verified if risque factor = True) , 43
# l[l.customerID == 23537712].head(20) ## not verified but dont know why , 54 
# l[l.customerID == 23537888].head(20) ## verified (one balance) , 41 
# l[l.customerID == 23538240].head(20) ## verified  , 41
# l[l.customerID == 23538416].head(20) ## verified (one balance) , 21 
# l[l.customerID == 23538768].head(20) ## verified ,41
# l[l.customerID == 23538944].head(20) ##  verified still have initial bonus(must take into considiration initial bonus dosent count) ,60
# l[l.customerID == 23539120].head(20) ## verified (one balance) ,41
# l[l.customerID == 23539472].head(20) ## verified ,41
# l[l.customerID == 23539648].head(20) ## verified ,41
# l[l.customerID == 23539824].head(20) ## verified ,41
# l[l.customerID == 23540000].head(20) ## verified ,41
# l[l.customerID == 23540176].head(20) ## verified ,41
l[l.customerID == 28774064].head(20) ## verified ,41



# %%
bonus_data[bonus_data.customerID  == 12203664]
bets_data[bets_data.customerID  == 12203664]

# %%
l[l.customerID == 23538768].value.sum()

# %%
def get_product_id(cid) : 
    return balance_data[balance_data.customerID == cid].iloc[0].productID

get_product_id(23538944)

# %%
balance_data[balance_data.customerID  == 23537712]

# %%
balance_data[balance_data.customerID ==23536480 ] [['productID' , 'validFrom' , 'validTo' , 'balance']]

# %%
## define a function to get the exact dates 
import datetime as dt 
def transforme_to_datetime(str_date , format ) : 
    """
    return thestring date to an datetime object """
    
def check_range(date , validf , valid2) : 

# %%
