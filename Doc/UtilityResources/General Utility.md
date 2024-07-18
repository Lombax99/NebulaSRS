

DEBUG CONSOLE: https://nebularat-webapp.scm.azurewebsites.net/DebugConsole

### Azure Cli
##### Installation
How to [install](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt) Azure Cli on Linux
##### Usefull Commands
Comandi di gestione dell'account
```
az account list --output table                 #per stampare le iscrizioni e i loro id
az account set --subscription sub-id           #per impostare quella iscrizione
```

Comando utile per vedere delle variabili della webapp: 
```
az webapp config appsettings list --name NebulaRAT-webapp --resource-group srs2024-stu-g2
```

Per modificare la variabile più importante della storia:
```
az webapp config appsettings set --resource-group <group-name> --name <app-name> --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```


