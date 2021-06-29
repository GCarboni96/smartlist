import requests
import pandas
import matplotlib
import matplotlib.pyplot as plt


def get_credentials():
    db2id= {
  "db": "BLUDB",
  "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=vhr29299;PWD=bjps84p1^k55r2j8;",
  "host": "dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net",
  "hostname": "dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net",
  "https_url": "https://dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net:8443",
  "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net:50000/BLUDB",
  "parameters": {
    "role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager"
  },
  "password": "bjps84p1^k55r2j8",
  "port": 50000,
  "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=vhr29299;PWD=bjps84p1^k55r2j8;Security=SSL;",
  "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net:50001/BLUDB:sslConnection=true;",
  "uri": "db2://vhr29299:bjps84p1%5Ek55r2j8@dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net:50000/BLUDB",
  "username": "vhr29299"
}
    api = '/dbapi/v3'
    host = db2id['https_url'] + api
    userinfo = {
        "userid" : db2id['username'],
        "password" : db2id['password']
    }
    service = "/auth/tokens"
    r = requests.post(host+service,json=userinfo)
    if r.status_code ==200:
        access_token = r.json()['token']
        auth_header = {
            "Authorization": "Bearer " + access_token
        }

        return host, auth_header
    else:
        return "ERROR, HOST INACCESIBLE"
