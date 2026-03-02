

import sys
import pyodbc
import pandas as pd

# read kw arg format yyyy mm from command line
if len(sys.argv) != 3:
    print("Usage: python futures_entries.py <year> <month   >")
    sys.exit(1)
year = sys.argv[1]
month = sys.argv[2] 
# read deliv_excel.sql and store output in a dataframe
with open('./sql/deliv_excel.sql', 'r') as file:
    sql_query = file.read()
    conn_str = (
    "DRIVER={Oracle in OraClient12Home1};"
    "DBQ=//pdal1orac02.d90.tes.local:1521/pdal1orac02;"
    "Uid=Tracread;"
    "Pwd=sungard;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute(sql_query, year, month)
rows = cursor.fetchall()
df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
cursor.close()
conn.close()

# read list of futures contracts
# filter where where DMO is equal to first of the month/year specified and contract is in futures contracts 
futures_contracts = pd.read_csv('./data/futures_contracts.csv')
#futures_contracts['DMO'] = pd.to_datetime(futures_contracts['DMO'])
futures_contracts['CONTRACT'] = futures_contracts['CONTRACT'].str.strip()
df['DMO'] = pd.to_datetime(df['DMO'])


# create futures offset leg
# create physical deliv leg

