
# Cone
import io
import json
import requests
import msoffcrypto

import pandas as pd

passwd = 'RPA-process-monitoring'
config_file = r"C:\Users\Dell 3\Desktop\faculdade\3ano\TFC\Projeto\CGI-Process-Monitoring-302-303\process_monitor\config.xlsx"

decrypted_workbook = io.BytesIO()
with open(config_file, 'rb') as file:
    office_file = msoffcrypto.OfficeFile(file)
    office_file.load_key(password=passwd)
    office_file.decrypt(decrypted_workbook)

credentials_df = pd.read_excel(decrypted_workbook, engine='openpyxl')

creds = {
    "usernameOrEmailAddress": credentials_df[credentials_df["Name"] == "usernameOrEmailAddress"]["Value"].iloc[0],
    "password": credentials_df[credentials_df["Name"] == "password"]["Value"].iloc[0],
    "tenancyName": credentials_df[credentials_df["Name"] == "tenancyName"]["Value"].iloc[0],
    "grant_type": "refresh_token",
    "client_id": "8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
    "refresh_token": "2lRK1sYCtT3HA2g13WiBFJIOiETIDKOSfKtp9mgzuQuXo",
}

credentials = {
    'text-column': 'email',
    'id-column': 'id',
    'url': credentials_df[credentials_df["Name"] == "url"]["Value"].iloc[0],
}
header = {'content-type': 'application/json'}

r = requests.Session()

token = json.loads(r.post(
    'https://account.uipath.com/oauth/token',
    data=json.dumps(creds),
    headers=header, verify=False).content.decode('utf-8'))['access_token']

header['authorization'] = 'Bearer ' + token

header['X-UIPATH-TenantName'] = creds['tenancyName']
