# Find SP by name in all SQL Server instances and databases
import pyodbc
import numpy as np
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import URL       # To support pandas
from sqlalchemy import create_engine    # To support pandas
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=600, relief='raised', bd=30, insertwidth=4, bg="powder blue")
canvas1.pack()

label1 = tk.Label(root, text='Search SP in SQL Servers', bg="powder blue")
label1.config(font=('helvetica', 18))
canvas1.create_window(200, 50, window=label1)

label2 = tk.Label(root, text='Enter Stored Procedure to search', bg="powder blue")
label2.config(font=('helvetica', 14))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)

def find_sp_by_name():
    sp_name = entry1.get()

    line = 210
    query1 = """select name from sys.databases where database_id > 4 and state != 6 order by 1""" 
    print(f"=== Searching for Stored Procedure '{sp_name}' in all SQL Server instances ===")

    # Loop over all SQL Server Instances
    for server in ('USSQL', 'BSQL', 'KSSQL', 'ZSSQL', 'WSSQL', 'SQLCLUST','TESTINGSQL', 'BIDEV16','DWH16-AZURE', 'BMANBAS', 'FSQL2'):
        # server parameters
        database = 'DBA' 
        username = 'naya5' 
        password = '5732@45$DF3!'
        conn_string =  'DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
        
        conn = pyodbc.connect(conn_string)
        conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_string}) # To support pandas

        # Get databases list
        print(f'Connecting to {server}')
        engine = sa.create_engine(conn_url)
        df1 = pd.read_sql_query(query1, engine)
        
        # Loop over all databases
        for i, database in df1.iterrows():
            db_name = database["name"]
            # print (db_name)
            query2 = """SELECT count(1) as count from [""" + db_name + """].sys.procedures where name = '""" + sp_name + """';""".format(input)
            # print(query2)
            df2 = pd.read_sql_query(query2, engine)
            sp_exists = (df2["count"].iloc[0])
            
            if sp_exists > 0:
                # print (f"*** Found '{sp_name}' in Server: {server}, in Database: {db_name} ***")
                msg = "Server: " + server + ", Database: " + db_name
                label3 = tk.Label(root, text=msg, font=('helvetica', 10), bg="powder blue", justify='left')
                canvas1.create_window(210, line, window=label3)
                line = line + 20

    print("=== Done searching ===")   

button1 = tk.Button(text='Search SP', command=find_sp_by_name, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()