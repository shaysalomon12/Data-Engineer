# Migrate Data Between database1 and database2
import pyodbc
import sqlalchemy as sa
import pandas as pd
from sqlalchemy.engine import URL       # To support pandas
from sqlalchemy import create_engine    # To support pandas
import time
from datetime import datetime           # To wtite timestamp to terminal

#######################
table_name = 'test_log'
chunksize = 100
# Size the chunksize parameter so you will not get SQL Server limit for 2100 parameters:
# https://stackoverflow.com/questions/50645445/python-pandas-to-sql-maximum-2100-parameters

# server1 parameters - source 
server1 = 'TestingSQL' 
database1 = 'DBA' 
username1 = 'naya5' 
password1 = '5732@45$DF3!'
conn_string1 =  'DRIVER={SQL Server};SERVER=' + server1 + ';DATABASE=' + database1 + ';UID=' + username1 + ';PWD='+ password1
# conn1 = pyodbc.connect(conn_string1)
conn_url1 = URL.create("mssql+pyodbc", query={"odbc_connect": conn_string1}) # To support pandas
engine1 = sa.create_engine(conn_url1)

# server2 parameters - target
server2 = 'TestingSQL' 
database2 = 'LearningTogetherTesting_OLD' 
username2 = 'naya5' 
password2 = '5732@45$DF3!'
conn_string2 =  'DRIVER={SQL Server};SERVER=' + server2 + ';DATABASE=' + database2 + ';UID=' + username2 + ';PWD='+ password2
conn2 = pyodbc.connect(conn_string2)
conn_url2 = URL.create("mssql+pyodbc", query={"odbc_connect": conn_string2}) # To support pandas
engine2 = sa.create_engine(conn_url2)

# Truncate table in server2
truncate_query = 'truncate table ' + table_name
conn2.execute(truncate_query).commit()
conn2.close()

# Load df in chunks from source database1
query = 'select * from ' + table_name
n = 1

for df in pd.read_sql(query, con=engine1, chunksize=chunksize):
    # time.sleep(0.00001)
    # Write df to target database2
    print(datetime.now().strftime("%H:%M:%S") + ' Writing ... ')
    df.to_sql(table_name, engine2, if_exists='append', index=False, method='multi')
    # print(df)
    print(datetime.now().strftime("%H:%M:%S") + ' Records transfered: ' + str(n*chunksize))
    n = n+1
    if (n*chunksize)>1000:
        break

# Close connections
engine1.dispose()
engine2.dispose()


