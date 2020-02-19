# python-azuredatashare
Create an ADLS Gen2 File System dataset on an Azure Data Share share resource via the REST API.  This uses an application registration + client secret (Service Principal) for authentication and authorization.

# Create Environment (Windows):

```
python.exe -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

# Secrets

Create a keys.json file in the same directory which contains your confidential information.

```
{
    "AZURE_CLIENT_ID":"<YOUR AZURE CLIENT ID>",
    "AZURE_CLIENT_SECRET":"<YOUR AZURE CLIENT SECRET>",
    "AZURE_TENANT_ID":"<YOUR AZURE TENANT ID>",
    "RESOURCE":"https://management.azure.com/",
    "SUBSCRIPTIONID":"<YOUR AZURE SUBSCRIPTION ID>"
}
```

# Run

Alter create_dataset.py to include your own resource group, storage account name. Also enter your own Data Share Account, Data Share and Data Set names.
