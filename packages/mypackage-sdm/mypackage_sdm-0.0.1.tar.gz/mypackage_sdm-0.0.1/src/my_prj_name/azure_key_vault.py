import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential

# keyVaultName = os.environ["KEY_VAULT_NAME"]
keyVaultName = "daiyal"
KVUri = f"https://{keyVaultName}.vault.azure.net"

tenant_id = "44d8cd30-12b4-46ab-82b4-56bec7d7a555"
client_id = "703278cb-7c27-4434-8ebe-c340e5d018e6"
# ade3a2c0-29ad-477a-9c94-53f0abbfb0cc
client_secret = "wCd8Q~.Pv6uyyCELXlhP1JiImvo5MNHPUCmO1aHk"

secret_name = "daiyal-secret"

_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
client = SecretClient(vault_url=KVUri, credential=_credential)

# secretName = input("Input a name for your secret > ")
# secretValue = input("Input a value for your secret > ")
#
# print(f"Creating a secret in {keyVaultName} called '{secretName}' with the value '{secretValue}' ...")
#
# client.set_secret(secretName, secretValue)
#
# print(" done.")
#
# print(f"Retrieving your secret from {keyVaultName}.")

retrieved_secret = client.get_secret(secret_name)

print(f"Your secret is '{retrieved_secret.value}'.")
# print(f"Deleting your secret from {keyVaultName} ...")
#
# poller = client.begin_delete_secret(secret_name)
# deleted_secret = poller.result()

print(" done.")
