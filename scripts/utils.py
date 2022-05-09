import pandas as pd 


path = "data_dump/"
def save_data(dataframe,name = "save.csv",  path = path  ) : 
    dataframe.to_csv(path +name ,index  = False  )