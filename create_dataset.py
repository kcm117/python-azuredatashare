import json
import os
import requests

def get_secrets():
    with open('keys.json') as file:
        secrets = json.load(file)
    return secrets

def authenticate_to_azure(secrets):
    tenant_id = secrets['AZURE_TENANT_ID']
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    data = {
        'grant_type':'client_credentials',
        'client_id':secrets['AZURE_CLIENT_ID'],
        'client_secret':secrets['AZURE_CLIENT_SECRET'],
        'resource': secrets['RESOURCE']
    }

    r = requests.post(url,headers=headers,data=data)
    return r.json()['access_token']

def create_dataset(
    secrets,token,storage_resource_group,storage_account_name,
    datashare_resource_group,datashare_name,share_name,dataset_name
    ):
    api_version = '2019-11-01'
    subscription_id = secrets['SUBSCRIPTIONID']

    body = {
        "kind":"AdlsGen2FileSystem",
        "properties":{
            "storageAccountName": storage_account_name,
            "fileSystem":"data",
            "resourceGroup": storage_resource_group,           
            "subscriptionId": subscription_id
        }
    }

    h = {'Authorization':'Bearer '+ token,'Content-Type':'application/json'}
    p = {'api-version': api_version}
    
    url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{datashare_resource_group}/providers/Microsoft.DataShare/accounts/{datashare_name}/shares/{share_name}/dataSets/{dataset_name}'

    r = requests.put(url=url,headers=h,params=p,json=body)
    return r.json()
    

if __name__ == '__main__':
    secrets = get_secrets()
    token = authenticate_to_azure(secrets)
    dataset = create_dataset(
        secrets=secrets,
        token=token,
        storage_resource_group='rg_crosstenant',
        storage_account_name='kmstorageaccount',
        datashare_resource_group = 'rg_crosstenant',
        datashare_name='kmdatashare',
        share_name='kmdatalakeshare',
        dataset_name='data'
        )
    print(f'{dataset}')
