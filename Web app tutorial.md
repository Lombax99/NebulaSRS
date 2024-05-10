Based on:
- Azure web app
- Postgres DB
- Python + Flask

[Link](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-python-managed-identity-cli)
[link2](https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app?tabs=flask%2Cwindows&pivots=azure-portal)
### Manage ID
The web app uses its system-assigned **[managed identity](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)** (passwordless connections) with Azure role-based access control to access [Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction) and [Azure Database for PostgreSQL - Flexible Server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server) resources. The code uses the [DefaultAzureCredential](https://learn.microsoft.com/en-us/azure/developer/intro/passwordless-overview#introducing-defaultazurecredential) class of the [Azure Identity client library](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme) for Python. The `DefaultAzureCredential` class automatically detects that a managed identity exists for the App Service and uses it to access other Azure resources.

You can configure passwordless connections to Azure services using Service Connector or you can configure them manually. This tutorial shows how to use Service Connector. For more information about passwordless connections, see [Passwordless connections for Azure services](https://learn.microsoft.com/en-us/azure/developer/intro/passwordless-overview). For information about Service Connector, see the [Service Connector documentation](https://learn.microsoft.com/en-us/azure/service-connector/overview).

