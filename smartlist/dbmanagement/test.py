import requests
import pandas
import matplotlib
import matplotlib.pyplot as plt

db2id= {
  "db": "BLUDB",
  "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=xxh22004;PWD=m@vdgt648kvfqfpp;",
  "host": "dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net",
  "hostname": "dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net",
  "https_url": "https://dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net",
  "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net:50000/BLUDB",
  "parameters": {
    "role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
    "serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/f1acb48d9e984f8091edc2561e085c44::serviceid:ServiceId-5dc679ca-01ac-41fb-87c6-dfe7d7cf7e22"
  },
  "password": "m@vdgt648kvfqfpp",
  "port": 50000,
  "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=xxh22004;PWD=m@vdgt648kvfqfpp;Security=SSL;",
  "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;",
  "uri": "db2://xxh22004:m%40vdgt648kvfqfpp@dashdb-txn-sbox-yp-dal09-14.services.dal.bluemix.net:50000/BLUDB",
  "username": "xxh22004"
}

api = '/dbapi/v3'
host = db2id['https_url'] + api

userinfo = {
    "userid" : db2id['username'],
    "password" : db2id['password']
}



service = "/auth/tokens"

r = requests.post(host+service,json=userinfo)
print(r.status_code)
response = r.json()

#ESTO ES LO QUE NECESITAMOS PARA EJECUTAR SQL
access_token = r.json()['token']

auth_header = {
    "Authorization" : "Bearer " + access_token
}

sql_code = "SELECT * FROM Persons"

sql_code_creation = "CREATE TABLE Persons3 (" \
                    "PersonID int," \
                    "LastName varchar(255)," \
                    "FirstName varchar(255)," \
                    "Address varchar(255)," \
                    "City varchar(255)" \
                    ");"

sql_command = {
    "commands" : sql_code_creation,
    "limit" : 1000,
    "separator" : ";",
    "stop_on_error" : "yes"
}

service2 = "/sql_jobs"
r2 = requests.post(host + service2, headers=auth_header, json= sql_command)

jobid = ""
if r2.status_code == 201:
    jobid =r2.json()['id']

else:
    print("ERROR")

#EXTRAEMOS RESULTADOS

print(jobid)
r3 = requests.get(host + service2 + "/" + jobid, headers= auth_header)
if r3.status_code != 200:
    print("ERROR DE NUEVO")
print(r3.status_code)
results = r3.json()['results']
print(results)
columns = results[0]['columns']
rows = results[0]['rows']


df =pandas.DataFrame(data=rows, columns=columns)
cols = df.columns
df[cols] = df[cols].apply(pandas.to_numeric, errors = "ignore")

print(df)


