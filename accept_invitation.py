import json
import os
import requests


API_VERSION = "2019-11-01"


def get_secrets():
    with open("keys.json") as file:
        secrets = json.load(file)
    return secrets


def authenticate_to_azure(secrets) -> str:
    """
    Function to authenticate to Azure as a service principal via OAUTH2
    """
    tenant_id = secrets["AZURE_TENANT_ID"]
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "client_credentials",
        "client_id": secrets["AZURE_CLIENT_ID"],
        "client_secret": secrets["AZURE_CLIENT_SECRET"],
        "resource": secrets["RESOURCE"],
    }

    r = requests.post(url, headers=headers, data=data)
    return r.json()["access_token"]


def create_invitation(secrets) -> dict:
    """
    Create an invitation for an existing share.
    """
    subscription_id = secrets["SUBSCRIPTIONID"]
    resource_group_name = "rg_crosstenant"
    account_name = "kmdatashare"
    share_name = "publishershare1"
    invitation_name = "invitesp"

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DataShare/accounts/{account_name}/shares/{share_name}/invitations/{invitation_name}"
    h = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    p = {"api-version": API_VERSION}
    body = {
        "properties": {
            "targetActiveDirectoryId": secrets["TARGET_AAD"],
            "targetObjectId": secrets["TARGET_OBJECT_ID"],
        }
    }

    r = requests.put(url=url, headers=h, params=p, json=body)
    return r.json()


def list_invitations(token) -> dict:
    """
    List Azure Data Share invitations.
    """
    url = f"https://management.azure.com/providers/Microsoft.DataShare/ListInvitations"
    h = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    p = {"api-version": API_VERSION}

    r = requests.get(url=url, headers=h, params=p)
    return r.json()


def accept_invitation(secrets, invitation_id, share_subscription_name):
    """
    Accept a share invitation sent to an AAD Service Principal
    """
    account_name = "kmdatashare2"
    resource_group_name = "rg_crosstenant"
    subscription_id = secrets["SUBSCRIPTIONID"]

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DataShare/accounts/{account_name}/shareSubscriptions/{share_subscription_name}"
    h = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    p = {"api-version": API_VERSION}

    body = {
        "properties": {"invitationId": invitation_id, "sourceShareLocation": "eastus2",}
    }

    r = requests.put(url=url, headers=h, params=p, json=body)
    return r.json()


if __name__ == "__main__":
    secrets = get_secrets()
    token = authenticate_to_azure(secrets)

    # 1) Create Invitation (Publisher)
    invite = create_invitation(secrets)
    print("\nInvitation Created\n")
    print(json.dumps(invite, indent=4, sort_keys=True))

    # 2) List Invitations (Subscriber)
    invitations = list_invitations(token)
    print("\nInvitation List\n")
    print(json.dumps(invitations, indent=4, sort_keys=True))
    # Example just grabs the invitation id of the first invitation in the list.
    invitation_id = invitations["value"][0]["properties"]["invitationId"]
    print(f"\nInvite id is {invitation_id}\n")

    # 3) Accept Invitation + Create Share (Subscriber)
    accepted_invite = accept_invitation(secrets, invitation_id, "subscribershare1")
    print(f"\nInvitation ID '{invitation_id}' has been accepted.\n")
    print(json.dumps(accepted_invite, indent=4, sort_keys=True))
