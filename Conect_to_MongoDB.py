from pymongo import MongoClient
import pandas as pd     # Not sure Pandas can show in PyCharm
from tabulate import tabulate
import pql              # Python-Query-Language: translates python expressions to MongoDB queries.

# MongoDB connection string
myClient = MongoClient(
    host='172.17.30.23:27017',
    serverSelectionTimeoutMS=3000,
    username="sa",
    password="global11!"
)

# Select Database and Collection
myDB = myClient["test"]
myCollection = myDB["demo"]

# Query1 collection test.demo for balance between 20 and 30
myQuery1 = {"balance" : {"$gte" : 20, "$lte" : 30}}

# Run query1 (using sort and limit) and display results using pandas data frames
myDoc = myCollection.find(myQuery1).sort("balance", -1).limit(5)  # -1 descending

# Print query1 using Pandas and tabulate (pandas is supported only inside notebooks)
entries = list(myDoc)
df = pd.DataFrame(entries, columns = ['_id', 'number', 'currency', 'balance'])
print(tabulate(df, headers='keys', tablefmt='psql'))
# print(df.head)

print('')

# Run Query2 (using limit) and dislay results with for loop
# Copy and paste here between the round parenthesis the MongoDB equivalent from SQL to MongoDB converter that is in the db.<collection_name>.find('<text_to_copy>')
# https://www.javainuse.com/sql2mongo
for x in myCollection.find({"balance" : {"$gte" : 20, "$lte" : 30000}},{ "_id": 1, "number": 1, "currency": 1, "balance": 1 }).limit(10):
  print(x)

# Query first 10 records without any filter
# for x in myCollection.find({}).limit(10):
#   print(x)

# Show all Databases
# database_names = myClient.list_database_names()
# print ("\ndatabases:", database_names)

# PQL translates python expressions to MongoDB queries.
# pql.SchemaFreeParser("a > 1 and b == 'foo'")

