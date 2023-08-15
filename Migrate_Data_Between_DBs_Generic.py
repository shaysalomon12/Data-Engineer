# Migrate Data Between database1 and database2
import pyodbc
import sqlalchemy as sa
import pandas as pd
from sqlalchemy.engine import URL       # To support pandas
from sqlalchemy import create_engine    # To support pandas
from sqlalchemy import event, DDL, text
import time
from datetime import datetime           # To wtite timestamp to terminal

######################
table_name = 'test_log'
chunksize = 1000
# Size the chunksize parameter so you will not get SQL Server limit for 2100 parameters:
# https://stackoverflow.com/questions/50645445/python-pandas-to-sql-maximum-2100-parameters
#
# Creating engine for Oracle/MySQL/SQL Server/PostgreSQL (Engine Configuration):
# https://docs.sqlalchemy.org/en/20/core/engines.html

# Server1 parameters - source SQL Server 
server1 = 'TestingSQL' 
database1 = 'DBA' 
username1 = 'naya5' 
password1 = '5732@45$DF3!'
port1 = 1433
# conn_string1 =  'DRIVER={SQL Server};SERVER=' + server1 + ';DATABASE=' + database1 + ';UID=' + username1 + ';PWD='+ password1
# conn_url1 = URL.create("mssql+pyodbc", query={"odbc_connect": conn_string1})  # To support pandas
conn_url1 = URL.create("mssql+pyodbc", username=username1, password=password1, host=server1, port=port1, database=database1, query={
                                                                                                            "driver": "SQL Server",
                                                                                                            "TrustServerCertificate": "yes",
                                                                                                            "authentication": "ActiveDirectoryIntegrated",
                                                                                                        },)
engine1 = create_engine(conn_url1)

# Server2 parameters - target MySQL
server2 = '172.40.3.65' 
database2 = 'sherutleumitest' 
username2 = 'sa@moodletestmysql' 
password2 = 'global11!'
port2 = 3306
# engine2 = create_engine(f"mysql+pymysql://{username2}:{password2}@{server2}:{port2}/{database2}")
conn_url2 = URL.create("mysql+pymysql", username=username2, password=password2, host=server2, port=port2, database=database2)
engine2 = create_engine(conn_url2)

# Truncate table in server2
truncate_query = text(f"truncate table {table_name}")
# engine2.connect().execute(truncate_query)
engine2.execute(truncate_query)

# Load df in chunks from source database1
migrate_query = 'select * from ' + table_name
n = 1

for df in pd.read_sql(migrate_query, con=engine1, chunksize=chunksize):
    # Write df to target database2
    print(datetime.now().strftime("%H:%M:%S") + ' Writing ... ')
    df.to_sql(table_name, engine2, if_exists='append', index=False, method='multi')
    # print(df)
    print(datetime.now().strftime("%H:%M:%S") + ' Records transfered: ' + str(n*chunksize))
    n = n+1
    if (n*chunksize)>2000:
        break

# Close connections
engine1.dispose()
engine2.dispose()


