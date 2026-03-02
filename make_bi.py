# %%
import pandas as pd
import pyodbc
 # %%
vol_books = ['HNAT','HPHM','HREC','TREC']

server = 'eemnaproddb'
database = 'MidOfficeReporting'
driver = '{ODBC Driver 17 for SQL Server}'   # or 18 depending on your system

# Windows Authentication
conn_str = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"   # remove this if using a trusted SSL cert
)

conn_str_znet = (
    "DRIVER={Oracle in OraClient12Home1};"
    "DBQ=//pdal1orac02.d90.tes.local:1521/zainet;"
    "Uid=Tracread;"
    "Pwd=sungard;"
)

# %%
# get the daily pnl query
with open('./sql/eemna_pnl.sql', 'r') as file:
    pnl_query = file.read() 
# get the daily pos query
with open('./sql/eemna_position.sql', 'r') as file:
    pos_query = file.read() 

# execute pnl_query to pnl_df and pos_query to pos_df
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute(pos_query)
rows = cursor.fetchall() 
pos_df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
cursor.close()

cursor = conn.cursor()
cursor.execute(pnl_query)
rows = cursor.fetchall()
pnl_df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
cursor.close()
conn.close()

# read mapping data
mapping_loc = 'M:\Dept\TESI\Supply\Position Management\REC\POWER BI\Curve Mapping - IRIS vs ALIGNE.xlsx'
mapping_df = pd.read_excel(mapping_loc, sheet_name='ALIGNE')
pos_df = pos_df.merge(mapping_df, on = 'MARKET', how='left')


# %%
# filter position df for BOOK in vol_books, ISO not equal to NYISO, PJM, or NEPOOL and SOURCE not equal to CP
filt = (pos_df['BOOK'].isin(vol_books)) & (~pos_df['ISO'].isin(['NYISO', 'PJM', 'NEPOOL'])) & (pos_df['SOURCE'] != 'CP')
vol_book = pos_df[filt].copy(deep = True)

#make a pivot table where index is TYPE, column is YEAR, values is sum of DELTA_ND. 
vol_pivot = vol_book.pivot_table(index='TYPE', columns='YEAR', values='DELTA', aggfunc='sum')
vol_nd = vol_book.pivot_table(index='TYPE', columns='YEAR', values='DELTA_ND', aggfunc='sum')
# %%
#add a total row for each year, and a colum total for each type
vol_pivot.loc['Total'] = vol_pivot.sum()
vol_pivot['Total'] = vol_pivot.sum(axis=1)
vol_pivot.to_clipboard()

vol_nd.loc['Total'] = vol_nd.sum()
vol_nd['Total'] = vol_nd.sum(axis=1)
vol_nd.to_clipboard()

# %%

# filter pnl_df for ATTRIBUTE = 'REC', YEAR > 2022
filt = (pnl_df['ATTRIBUTE'] == 'REC') & (pnl_df['YEAR'] != '2020')
rec_pnl = pnl_df[filt].copy(deep = True)
#pivot table where index is BOOK, column is YEAR, values is sum of 'PL_DAILY_NPV_NET_C'
rec_pnl_pivot = rec_pnl.pivot_table(index='BOOK', columns='YEAR', values='PL_DAILY_NPV_NET_C', aggfunc='sum')
# add total row and column
rec_pnl_pivot.loc['Total'] = rec_pnl_pivot.sum()
rec_pnl_pivot['Total'] = rec_pnl_pivot.sum(axis=1)
rec_pnl_pivot.to_clipboard()
# %%
pnl_df[filt].merge(mapping_df, on = 'MARKET', how='left').to_clipboard()
# %%

###############################REC Specific PnL. Missing trade details
query = """
SELECT *
FROM [MidOfficeReporting].[Zainet].[Engie_PL_Detailed_EOD]
WHERE AS_OF_DATE = '2026-02-24'
  AND MRKT_ATTR1 = 'REC';
"""

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
pos_level_pnl = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
#for row in rows:
#    print(row)

cursor.close()
conn.close()
# %%
pos_level_pnl.merge(mapping_df, left_on = "MKT1", right_on = 'MARKET', how='left').to_clipboard()


# %%
pos_df.to_clipboard()
# %%

mapping_df.to_clipboard()