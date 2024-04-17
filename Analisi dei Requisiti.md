Build an enterprise remote access tool leveraging Nebula: https://github.com/slackhq/nebula
### Requirements
1) Build a database of ==remote machines== by importing the ==Nebula certificates== and the current ==Nebula firewall rules== for reaching them.
2) Web interface protected by ==auth== to access a ==portal== showing all the ==available machines== to the user.
3) ==Admin== interface to define ==security roles== for ==users== and configure what machines can be available.
4) Generate on the fly a ==short-lived certificate== to allow the user to connect to the desired machine.
==Root certification Autority==

Resources Nebula
- [nebula github](https://github.com/slackhq/nebula)
- [medium: introducing nebula, the open source global overlay network](https://medium.com/several-people-are-coding/introducing-nebula-the-open-source-global-overlay-network-from-slack-884110a5579)
- [nebula doc](https://nebula.defined.net/docs/)
- [nebula quick start](https://nebula.defined.net/docs/guides/quick-start/)
- [nebula config reference](https://nebula.defined.net/docs/config/)
- [nebula official slack](https://join.slack.com/t/nebulaoss/shared_invite/enQtOTA5MDI4NDg3MTg4LTkwY2EwNTI4NzQyMzc0M2ZlODBjNWI3NTY1MzhiOThiMmZlZjVkMTI0NGY4YTMyNjUwMWEyNzNkZTJmYzQxOGU) 
Resources Azure
- https://techcommunity.microsoft.com/t5/azure-database-support-blog/using-certificates-in-azure-sql-database-import/ba-p/368949

### Requirements analysis
qua ci vanno le definizioni dei termini dei requisiti che passano da linguaggio formale a definizione rigorosa o addirittura linguaggio macchina.



#### Key points: ci stiamo appoggiando su azure
### Requisito 1 - Il database
- Database remoto --> usiamo azure, che funzionalità ci dà? 
> Importing nebula cert
> Questi sono dei semplici file, vengono aggiornati di tanto in tanto ma solo dalla root cert autority
> 
> Importing nebula firewall rules
> Questi sono più problematici perché possono cambiare nel tempo
##### Come salviamo i dati?

| ID macchina | certificato | file di config |
| ----------- | ----------- | -------------- |
|             |             |                |
Mi salvo i due file che mi interessano e ciccia.
Voglio salvare anche la chiave dei certificati della macchina? Secondo me NO ma.
##### Come aggiorniamo i dati
Nel primo sprint mi accontento di dire che chiunque modifichi i dati si debba prende la briga di modificarli anche nel database.
Dobbiamo fare un'interfaccia carina per permettere tutto questo in modo scalabile. Posso mettere una funzione per caricare dati nel sistema, che controlli di sicurezza devono essere fatti?
Yaml è Turing completo? Posso far entrare del codice malevolo? Posso mettere dei certificati falsi? Devo controllare da chi sono stati emessi i certificati. I file di conf sono firmati dalla root cert autority? non penso ma devo controllare.

> [!Tip] Per sprint futuri
> Se voglio assicurarmi che i file non siano cambiati senza che la nostra applicazione lo sappia vado a controllare randomicamente a campione la data di modifica del file di conf di una macchina e la confronto con quella nel mio database... devo quindi aggiungerlo al database.

##### A cosa servono i dati?
Stampiamo a schermo le regole di firewall e i certificati se richiesto.

### Requisito 2 - Web interface 
Web interface protected by ==auth== to access a ==portal== showing all the ==available machines== to the user.
##### Auth
Spero che azure faccia il suo lavoro
##### Showing available machines
Dipende dai security roles




### Requisito 3 - Security Roles 
NOTA: Ruolo dell'admin supremo necessariamente deve esistere

Si tratta solo di assegnare la visibilità delle macchine ad un utente specifico. Non è vero, ci sono anche ruoli che possono fare cose diverse con le macchine, qualcuno potrebbe avere il permesso di fare ssh mentre altri no...
Decidiamo che per questo primo sprint ci limitiamo solo ad un discorso di visibilità.

Come assegniamo le macchine? Questi metodi non sono mutualmente esclusivi:
- Posso assegnare un singolo ID
- Posso assegnare un sottodominio


### Requisito 4 - Short lived certificates
Primo problema è capire come fare a creare certificati mirati verso una macchina senza toccare le regole di firewall delle macchine stesse.







