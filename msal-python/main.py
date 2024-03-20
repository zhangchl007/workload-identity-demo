import os
import uuid
import time
import logging

from token_credential import MyClientAssertionCredential
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

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
    token_credential = MyClientAssertionCredential(azure_client_id, azure_tenant_id, azure_authority_host, azure_federated_token_file)
 
    # create a blob service client
    blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net/", credential=token_credential)
    
    # create a container client
    container_client = blob_service_client.get_container_client(storage_container_name)
    
    while True:  # This creates an infinite loop
        with open('/tmp/sample-source.txt', 'a') as f:
            f.write(f"Timestamp: {time.time()}\n")
            f.write(f"POD Name: {pod_name}\n")
            f.write(f"POD IP: {pod_ip}\n")
            f.write('hello ,I am writing ') 

        # generate a unique blob name for each iteration
        storage_blob_name=f"sample-blob-{str(uuid.uuid4())[0:5]}.txt"
        
        # upload the file to the blob
        blob_client = container_client.get_blob_client(storage_blob_name)
        
        with open("/tmp/sample-source.txt", "rb") as data:
            blob_client.upload_blob(data)
            logging.info(f"Uploaded sample-source.txt to {blob_client.url}")
        # sleep for 5 seconds
        time.sleep(5)
            
if __name__ == '__main__':
    main()

