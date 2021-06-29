import requests
import random
import pandas
import string
from pypika import Table, MySQLQuery, MSSQLQuery, PostgreSQLQuery, OracleQuery, VerticaQuery, Query
import datetime

from credentials import get_credentials

print(datetime.datetime.now())

query = "./sql/Productos_creation.sql"

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


print(r.json())















