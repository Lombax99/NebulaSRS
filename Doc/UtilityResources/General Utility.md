

IMPORTANTISSIMO: https://nebularat-webapp.scm.azurewebsites.net/DebugConsole

Comando utile per vedere delle variabili della webapp: 
```
az webapp config appsettings list --name NebulaRAT-webapp --resource-group srs2024-stu-g2
```

Per modificare la variabile più importante della storia:
```
az webapp config appsettings set --resource-group <group-name> --name <app-name> --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```


