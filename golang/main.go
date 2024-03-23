// workload identity with Azure AD MSAL to access Azure Storage Account
// This example demonstrates how to use Azure AD Workload Identity with MSAL to access an Azure Storage Account
// The Azure AD Workload Identity webhook will inject the following environment variables:
package main

import (
	"context"
	"os"
	"time"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
	"k8s.io/klog"
)

func main() {

	// Azure Container

	azure_storage_account_Name := os.Getenv("STORAGE_ACCOUNT_NAME")

	if azure_storage_account_Name == "" {
		klog.Fatal("AZURE_STORAGE_ACCOUNT_NAME environment variable is not set")
	}

	azure_storage_container_Name := os.Getenv("STORAGE_CONTAINER_NAME")

	if azure_storage_container_Name == "" {
		klog.Fatal("AZURE_STORAGE_CONTAINER_NAME environment variable is not set")
	}

	pod_name := os.Getenv("POD_NAME")

	if pod_name == "" {
		klog.Fatal("POD_NAME environment variable is not set")
	}

	pod_ip := os.Getenv("POD_IP")

	if pod_ip == "" {
		klog.Fatal("POD_IP environment variable is not set")

	}

	// Azure AD Workload Identity webhook will inject the following env vars
	// 	AZURE_CLIENT_ID with the clientID set in the service account annotation
	// 	AZURE_TENANT_ID with the tenantID set in the service account annotation. If not defined, then
	// 	the tenantID provided via azure-wi-webhook-config for the webhook will be used.
	// 	AZURE_FEDERATED_TOKEN_FILE is the service account token path
	// 	AZURE_AUTHORITY_HOST is the AAD authority hostname
	clientID := os.Getenv("AZURE_CLIENT_ID")
	tenantID := os.Getenv("AZURE_TENANT_ID")
	tokenFilePath := os.Getenv("AZURE_FEDERATED_TOKEN_FILE")
	//authorityHost := os.Getenv("AZURE_AUTHORITY_HOST")

	// ...

	if clientID == "" {
		klog.Fatal("AZURE_CLIENT_ID environment variable is not set")
	}
	if tenantID == "" {
		klog.Fatal("AZURE_TENANT_ID environment variable is not set")
	}

	// newClientAssertionCredential
	cred, err := azidentity.NewWorkloadIdentityCredential(&azidentity.WorkloadIdentityCredentialOptions{
		ClientID:      clientID,
		TenantID:      tenantID,
		TokenFilePath: tokenFilePath,
	})

	if err != nil {
		klog.Fatal(err)
	}

	storageaccountURL := "https://" + azure_storage_account_Name + ".blob.core.windows.net"
	containerName := azure_storage_container_Name
	blobName := pod_name + ".txt"
	ctx := context.Background()

	// Create a new container client

	client, err := azblob.NewClient(storageaccountURL, cred, nil)

	if err != nil {
		klog.Fatal(err)

	}

	ticker := time.NewTicker(10 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		// data to write to blob
		mydata := time.Now().Format(time.RFC3339) + pod_name + "Hello, World!" + "\n"
		data := []byte(mydata)

		data = append(data, []byte(mydata)...)

		// write a buffer to a blob
		_, err = client.UploadBuffer(ctx, containerName, blobName, data, &azblob.UploadBufferOptions{})
		if err != nil {
			klog.Fatal(err)
		}

		klog.Infof("Blob uploaded: %s", blobName)
	}

}
