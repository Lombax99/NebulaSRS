1) Definizione dell'ambiente e setup CI/CD
2) Sviluppo dell'applicazione
	- front end
	- back end
	- integrazione col db
	- generazione dei certificati temporanei
	- gestione degli utenti e dei ruoli
	- gestione dei dati delle macchine (config e cert)
3) Implementazione dei tool azure con la nostra applicazione (application insight, application backup, key vault, microsoft defender for cloud, auto heal, transparent data encryption, backup del DB)
4) Test di distribuzione (azure load tester)
5) Test di sicurezza (owasp zap, snyk)
6) Correzione applicazione con i risultati dei test
7) Analisi dei costi (anche in termini di crescita futura)
8) Report e Presentazione



IMPORTANTISSIMO: https://nebularat-webapp.scm.azurewebsites.net/DebugConsole

Comando utile per vedere delle variabili della webapp: 
```
az webapp config appsettings list --name NebulaRAT-webapp --resource-group srs2024-stu-g2
```

Per modificare la variabile più importante della storia:
```
az webapp config appsettings set --resource-group <group-name> --name <app-name> --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```