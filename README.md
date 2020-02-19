# python-azuredatashare
Create an ADLS Gen2 File System dataset on an Azure Data Share share resource via the REST API.  This uses an AAD application registration + client secret (Service Principal) for authentication and authorization.

# Create Environment (Windows):

You will need a Python 3.7+ environment to run the script.  If you are on Windows and have Python 3.7+ installed, you can run the following command via the command prompt in the same directory where this repo is located:

```
create_env.bat
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
