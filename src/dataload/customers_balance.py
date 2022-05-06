from ast import parse
from weakref import finalize
import pandas as pd

from src.dataload.database_connector import MicrosoftSQLDBConnector
from src.dataload.str_query_parser import parse_query

def getAmountAndCurrencyIDCols(col, nativeCurrencyID = None):
    def getAmountCurrencyDict(values):
        keys = ['amount', 'currencyID']
        return dict(zip(keys, values))

    amountCols = {
        'amountOriginal': getAmountCurrencyDict(['pt.amount', 'pt.currencyID']),
        'amountUSD': getAmountCurrencyDict(['pt.amountUSD', 1 ]),
        'amountRequested': getAmountCurrencyDict(['pt.amountRequested', nativeCurrencyID]),
        'amountNative': getAmountCurrencyDict([f'''round(case
                                  when pt.currencyID = {nativeCurrencyID} then pt.amount
                                  else pt.amountUSD/er.toUSD
                              end, 2)''', nativeCurrencyID]),
        }
    return amountCols[col]

def getAffiliateCol(col):
    affiliateCols = {
        'affix': 'a.AffixID', # for Affix
        'IA': 'a.IAMemberID', # for Income Access
        'oldIntertops': 'a.ispref', # for old Intertops affiliate system
    }
    return affiliateCols[col]

def getComputedAmount(type, amountCol, nativeCurrencyID = None):
    amountColName = getAmountAndCurrencyIDCols(amountCol, nativeCurrencyID)['amount']
    computedAmounts = {
        'deposit': f"""{amountColName} * case
                        when pt.transactionStatusID = 1 and pt.transactionTypeID = 1 then 1
                        else 0 end deposit""",
        'netcash': f"""{amountColName} * case
                        when pt.transactionStatusID = 1 and pt.transactionTypeID = 1 then 1
                        when pt.transactionStatusID = 1 and pt.transactionTypeID in (4,5,6) then -1
                        else 0 end netcash"""
    }
    return computedAmounts[type]

def getIncludedCols(colGroups, affiliateCol, amountCol, computedAmounts, nativeCurrencyID = None):
    includedCols = ['pt.paymentTransactionID', 'c.customerID']
    includedCols.append(f'{getAffiliateCol(affiliateCol)} as affiliate')
    includedCols.extend(['fd.ftdDate', 'c.createdate as signupDate'])
    includedCols.extend(['pt.createdateUTC as tranDate', 'pt.transactionTypeID', 'pt.transactionStatusID'])
    includedCols.extend([f"{getAmountAndCurrencyIDCols(amountCol, nativeCurrencyID)['amount']} as tranAmount",
                         f"{getAmountAndCurrencyIDCols(amountCol, nativeCurrencyID)['currencyID']} as tranCurrencyID"])
    includedCols.extend([getComputedAmount(type, amountCol, nativeCurrencyID) for type in computedAmounts])
    if 'tranAmountsOtherCurrencies' in colGroups:
        pairs = [[
            f"{getAmountAndCurrencyIDCols(amount, nativeCurrencyID)['amount']} as tranAmount{amount[6:]}",
            f"{getAmountAndCurrencyIDCols(amount, nativeCurrencyID)['currencyID']} as tranCurrencyID{amount[6:]}"
        ] for amount in ['amountOriginal', 'amountUSD', 'amountRequested', 'amountNative'] if amount != amountCol]
        includedCols.extend([item for pair in pairs for item in pair])
    if 'affiliateCommission' in colGroups:
        includedCols.extend(['a.commissionType'])
    if 'affiliateDetails' in colGroups:
        includedCols.extend(['a.affiliateID', 'a.IAMemberID', 'a.AffixID', 'a.ispref', 'a.jcAffiliateID', 'a.productID as affiliateProductID',])
    if 'customerDetails' in colGroups:
        includedCols.extend(['c.productID as customerProductID', 'c.countryID'])
    if 'customerSoftware' in colGroups:
        includedCols.extend(['sc.name as softwareClient'])
    if 'customerDemographics' in colGroups:
        includedCols.extend(['c.firstName', 'c.lastName', 'c.gender', 'c.birthdate'])
    if 'customerCurrentStatus' in colGroups:
        includedCols.extend(['s.isEnabled', 's.isCheat', 's.isDuplicate', 's.isInternal', 's.category', 's.categoryName', 's.validFrom as lastStatusChangeDate'])
    return includedCols

def getWhereClauses(selectCriteria):
    whereClauseGenerators = {
        'productIDin': lambda IDs: f"c.productID in ({','.join([str(id) for id in IDs])})",
        'FTDbetween': lambda dateFrom = None, dateTo = None: f"fd.ftdDate between '{dateFrom or '1900-01-01'}' and '{dateTo or '2099-12-31'}'",
        'transactionsBetween': lambda dateFrom = None, dateTo = None: f"pt.createdateUTC between '{dateFrom or '1900-01-01'}' and '{dateTo or '2099-12-31'}'",
        'signupBetween': lambda dateFrom = None, dateTo = None: f"c.createdate between '{dateFrom or '1900-01-01'}' and '{dateTo or '2099-12-31'}'",
        'statusAt': lambda date: f"s.validFrom <= '{date}' and '{date}' < s.validTo",
    }
    whereClauses = [whereClauseGenerators[generator](**kwargs) for generator, kwargs in selectCriteria.items()]
    return whereClauses

def constructQuery(selectCriteria, colGroups, affiliateCol, amountCol, computedAmounts, orderby, nativeCurrencyID = None, printQuery = False):
    query = f"""select
                    {','.join(getIncludedCols(colGroups, affiliateCol, amountCol, computedAmounts, nativeCurrencyID))}
                from dimAffiliate a
                    right join dimCustomerStatus s on a.affiliateID = s.affiliateID
                    inner join dimCustomer c on s.customerID = c.customerID
                    {'left join dimSoftwareClient sc on c.softwareClientID = sc.softwareClientID' if 'customerSoftware' in colGroups else '' }
                    left join factPaymentTransaction pt on c.customerID = pt.customerID
                    left join
                        (
                        select ipt.customerID, min(ipt.createdateUTC) ftdDate
                        from factPaymentTransaction ipt
                        where ipt.transactionTypeID = 1
                            and ipt.transactionStatusID = 1
                        group by ipt.customerID
                        ) fd on fd.customerID = pt.customerID		
                    {'''left join workCurrencyER er on er.currencyID = 20
                        and pt.createdateUTC between er.datefrom and er.dateto''' if (amountCol == 'amountNative' or 'tranAmountsOtherCurrencies' in colGroups) else ''}		
                where
                    {' and '.join(getWhereClauses(selectCriteria))}
                order by {orderby}"""
    if printQuery:
        print(query)
    return parse_query(query)

def getCustomersByAffiliateData(selectCriteria, colGroups, affiliateCol, amountCol, computedAmounts, orderby, nativeCurrencyID = None, debugQuery = False):
    ITDWHconn = MicrosoftSQLDBConnector('ITDWH').connect()
    query = constructQuery(selectCriteria, colGroups, affiliateCol, amountCol, computedAmounts, orderby, nativeCurrencyID, printQuery = debugQuery)
    df = pd.read_sql(query, ITDWHconn)
    return df



def test_query(query) :
  
    ITDWHconn = MicrosoftSQLDBConnector('ITDWH').connect()
    final_query = parse_query(query)
    df = pd.read_sql(final_query, ITDWHconn)
    return df 
