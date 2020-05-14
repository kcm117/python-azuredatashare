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
    "SUBSCRIPTIONID":"<YOUR AZURE SUBSCRIPTION ID>",
    "TARGET_AAD": "<AAD TENANT ID OF SUBSCRIBER>",
    "TARGET_OBJECT_ID": "<SERVICE PRINCIPAL OBJECT ID OF SUBSCRIBER>"
}
```

You can store these secure values in another method, or change the code to reference them directly.  I used a non source controlled .json file for simplicity and demo purposes.

# Run

## create_dataset.py
Alter create_dataset.py to include your own resource group, storage account name. Also enter your own Data Share Account, Data Share and Data Set names.

## accept_invitation.py
This is an example script showing how to create an invitation from the perspective of an Azure Data Share publisher, then create a share mapped to the invitation on the subscriber side.  Please note that for this example, the publisher and subscriber are in the same tenant.

**Note**:
    The Service Principal Object ID is not the Application ID or Object ID which is shown on the App Registration in Azure Active Directory.  Use the App Registration ID shown in AAD to get the true Service Principal Object Id.  This can be done via Azure CLI or PowerShell:

PowerShell
```
# Get via App ID
$(Get-AzureADServicePrincipal -Filter "AppId eq 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'").ObjectId

# Get via Display Name
$(Get-AzureADServicePrincipal -Filter "DisplayName eq 'testapp'").ObjectId
```
 
Azure CLI
```
# get via App ID.
az ad sp show --id XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX | jq -r .objectId
```

# References:
Azure Data Share REST API Docs - https://docs.microsoft.com/en-us/rest/api/datashare/