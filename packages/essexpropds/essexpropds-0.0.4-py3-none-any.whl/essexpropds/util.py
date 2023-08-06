import pyodbc
import pandas as pd

def sql_conn(database, query, server="essexbi"):
    """Usage: Read data from a sql server as a pandas dataframe by establishing a trusted pyodbc connection

    Args:
        database (str):
            Name of the database for the table specified in the query
        query (str):
            The full SQL query for the data encased in triple double-quotations
        server (str):  (Default value = "essexbi")
            name of the server for the database specified; by default essexbi

    Returns: 
        df_query (pd.DataFrame):
            The queried data
    """
   
    sqlconn = pyodbc.connect(
        driver='SQL Server',
        host=server,
        database=database,
        Trusted_Connection="yes",
    )
    
    with sqlconn:
        df_query = pd.read_sql(query, sqlconn)
    print(df_query.shape)
    print(df_query.columns)
    return df_query