import os
import uuid
import time
import logging

from token_credential import MyClientAssertionCredential
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
from datetime import datetime



def main():
    # get environment variables to authenticate to the key vault
    azure_client_id = os.getenv('AZURE_CLIENT_ID', '')
    azure_tenant_id = os.getenv('AZURE_TENANT_ID', '')
    azure_authority_host = os.getenv('AZURE_AUTHORITY_HOST', '')
    azure_federated_token_file = os.getenv('AZURE_FEDERATED_TOKEN_FILE', '')
    
    storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME', '')
    storage_container_name = os.getenv('STORAGE_CONTAINER_NAME', '')
    pod_name = os.getenv('POD_NAME', '')
    pod_ip = os.getenv('POD_IP', '')
    
    # create a token credential object, which has a get_token method that returns a token
    credential = ManagedIdentityCredential()
    #token_credential = MyClientAssertionCredential(azure_client_id, azure_tenant_id, azure_authority_host, azure_federated_token_file)
 
    # create a blob service client
    #blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net/", credential=token_credential)
    #blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net/", credential=credential)
    
    # create a container client
    storage_url = f"https://{storage_account_name}.blob.core.windows.net/"
    # Create the client object using the storage URL and the credential
    blob_client = BlobClient(
        storage_url,
        container_name=storage_container_name,
        blob_name=pod_name + '.txt',
        credential=credential,
    )
    
    while True:  # This creates an infinite loop
        with open('/tmp/sample-source.txt', 'a') as f:
            f.write(f"Timestamp: {datetime.now()}\n") 
            f.write(f"POD Name: {pod_name}\n")
            f.write(f"POD IP: {pod_ip}\n")
            f.write('hello ,I am writing \n')
          

        
        # upload the file to the blob and overwrite the existing file
        with open("/tmp/sample-source.txt", "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"Uploaded sample-source.txt to {blob_client.url}")
        # sleep for 5 seconds
        time.sleep(10)
        
            
if __name__ == '__main__':
    main()
