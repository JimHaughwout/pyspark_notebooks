import pandas as pd

def list_to_sqldf(list_data, col_name):
    """Takes in a list and name and returns a pyspark.sql.dataframe.DataFrame"""
    pd_df = pd.DataFrame(list_data, columns=[col_name])
    return sqlContext.createDataFrame(pd_df)
