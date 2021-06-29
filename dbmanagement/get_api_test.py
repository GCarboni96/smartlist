import requests
import random
import pandas
import string
from pypika import Table, MySQLQuery, MSSQLQuery, PostgreSQLQuery, OracleQuery, VerticaQuery, Query
import datetime

from credentials import get_credentials

print(datetime.datetime.now())

query = "./sql/Grupos_get_last.sql"

with open(query, 'r') as file:
    sql_code = file.read().replace('\n', '')

host, auth_header = get_credentials()
sql_command = {
    "commands": sql_code,
    "limit": 1000,
    "separator": ";",
    "stop_on_error": "yes"
}
service = "/sql_jobs"
r = requests.post(host + service, headers=auth_header, json=sql_command)

jobid = ""
if r.status_code == 201:
    jobid = r.json()['id']
else:
    print("ERROR")
r2 = requests.get(host + service + "/" + jobid, headers=auth_header)
if r2.status_code != 200:
    print("ERROR DE NUEVO")
results = r2.json()['results']
columns = results[0]['columns']
rows = results[0]['rows']
df = pandas.DataFrame(data=rows, columns=columns)

cols = df.columns
df[cols] = df[cols].apply(pandas.to_numeric, errors="ignore")
print(df[cols])
















