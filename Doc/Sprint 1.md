### Requirements
1) Build a database of ==remote machines== by importing the ==Nebula certificates== and the current ==Nebula firewall rules== for reaching them.
2) Web interface protected by ==auth== to access a ==portal== showing all the ==available machines== to the user.
3) ==Admin== interface to define ==security roles== for ==users== and configure what machines can be available.
4) Generate on the fly a ==short-lived certificate== to allow the user to connect to the desired machine.
==Root certification Autority==

Resources
- [nebula github](https://github.com/slackhq/nebula)
- [medium: introducing nebula, the open source global overlay network](https://medium.com/several-people-are-coding/introducing-nebula-the-open-source-global-overlay-network-from-slack-884110a5579)
- [nebula doc](https://nebula.defined.net/docs/)
- [nebula quick start](https://nebula.defined.net/docs/guides/quick-start/)
- [nebula config reference](https://nebula.defined.net/docs/config/)
- [nebula official slack](https://join.slack.com/t/nebulaoss/shared_invite/enQtOTA5MDI4NDg3MTg4LTkwY2EwNTI4NzQyMzc0M2ZlODBjNWI3NTY1MzhiOThiMmZlZjVkMTI0NGY4YTMyNjUwMWEyNzNkZTJmYzQxOGU) 
Resources Azure
- [Super tutorial indiano](https://www.youtube.com/watch?v=tDuruX7XSac&t=2464s)
- https://techcommunity.microsoft.com/t5/azure-database-support-blog/using-certificates-in-azure-sql-database-import/ba-p/368949
- https://learn.microsoft.com/it-it/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli


### Requirements analysis
[[Nebula Remote Access Tool#Requirements analysis|link here]]

-----

### Problem analysis
##### Come popoliamo il database?
- Non sono cazzi nostri, ci limitiamo ad esporre un API per aggiornare il DB.
	1) Aggiungo una singola macchina
	2) Aggiungo tante macchine in una volta sola (rinviato a sprint futuri)
##### Come salviamo i dati nel database?
Mi salvo i due file che mi interessano e associo ad ogni macchina un ID definito da noi. 
Voglio salvare anche la chiave dei certificati della macchina? NO
Anche perchè se perdi la chiave generi un nuovo cert, non la vai a recuperare in un DB.
##### Chi può accedere al DB?
Separiamo i permessi di lettura e scrittura.
- Scrittura: Solo l'Admin.
- Lettura: Ogni utente può visualizzare solo le macchine a lui assegnato.

##### Ipotesi di deployment (Sté)
Tenendo comunque in conto che una valutazione sulla scalabilità della seguente soluzione sia necessaria, si può usare il BLOB Storage di Azure, che mette anche a disposizione delle API per accedervi: [Azure Storage REST API](https://learn.microsoft.com/en-us/rest/api/storageservices/blob-service-rest-api), [Azure PowerShell](https://learn.microsoft.com/en-us/powershell/module/az.storage), [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/storage), o la libreria client di Azure Storage.

Link utili:
- Azure BLOB Storage overview: https://azure.microsoft.com/en-us/products/storage/blobs
- Introduction to Azure BLOB Storage: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction

##### MongoDB o PostgreSQL?
![[Pasted image 20240507173320.png]]

PostgreSQL sfrutta un DB relazionale --> Meglio, perché così basta sfruttare la sintassi di SQL e stiamo a posto, senza dover rappresentare i documenti come file JSON. Inoltre, è scalabile ed effettua il load balancing. Cosa molto importante: ==POSTGRESQL GARANTISCE ACID SEMPRE E COMUNQUE==, mentre MongoDB solo in scenari limitati e dalla versione 4.0 in poi (nabbo).

Ergo, la migliore soluzione è usare PostgreSQL.

> [!Tip]- Appunti di lezione
> Come scegliere la replicazione del DB:
> - Tradeoff tra availability e scalability
> - sincronizzazione dei DB
> - Strong consistency --> Weak consistency --> No consistency (between DB)
> - Primary server/DB full consistency always (check differency between primary and master)
> - Secondary server/DB consistency eventually (lazy consistency)
> - Regola dei 3 backup (è una cosa diversa dalla distribuzione del DB)
##### Come teniamo traccia dei permessi dei vari utenti?
Bisogna salvarsi nel DB una tabella che associa utenti e macchine a cui possono accedere.
molto probabilmente converrà fare una tabella con tutti gli utenti e per ogni utente segnarsi a quale macchina può accedere. Il motivo è che lo spazio in memoria di un DB non è un grosso problema, posso sprecarne quanto ne voglio mentre dato un utente loggato è possibile che questo mi richieda certificati per più macchine e quindi mi tengo i dati salvati in cache o qualcosa di simile per velocizzare la cosa.
##### Come gestiamo la fase di Auth
Speriamo in azure... 🤞
Auth a due fattori?? 👀
- [ ] Chiedi al tutor perchè non possiamo accedere alle risorse di Azure sul login (Microsoft Merda):
	- Micorsoft Entra ID
##### Che tipi di utenti esistono? Come li generiamo? Come gestiamo i permessi?
Decidiamo che per questo primo sprint ci limitiamo solo ad un discorso di visibilità.
Quindi oltre all'admin ho solo normal users. L'unica differenza tra i vari user è a quali macchine sono assegnati.
##### Cosa possono fare questi utenti con le macchine?
Per questo primo sprint ci limitiamo a lasciare la possibilità di collegarsi tramite ssh poi vedremo.
##### A quali dati può accedere un utente?
Stiamo lavorando solo con i due file quindi uno user può stampare a video i dati nei due file del DB associati alle macchine a lui assegnati.
Chiaramente un utente può vedere solo le macchine a lui assegnate, le altre non le vede nemmeno.
##### Come fa l'admin ad associare ad un utente una macchina?
Per ora ci limitiamo ad un'assegnazione manuale stupida una macchina alla volta. Più avanti avrà senso pensare anche a soluzioni a gruppi di macchine sfruttando il concetto di sottodomini.
##### Come generiamo i certificati short lived?
Per il primo sprint ci limitiamo a dare la chiave della rootCA alla nostra super macchina in modo che possa creare nuovi certificati. Questo comporta GIGANTESCHI problemi di sicurezza che però gestiremo nei prossimi sprint.
##### Quanto può durare uno short-lived certificate?
Mettiamo durante la generazione la possibilità di definire il periodo di tempo di validità all'utente entro certi parametri, per questo primo sprint diciamo tra 1 e 8 ore.
##### La nostra macchina si può collegare a tutte le macchine che gestisce in ogni momento? Serve che lo faccia?
Per come è impostata al momento il nostro servizio non ha nessun bisogno di collegarsi con le macchine nella rete. Se volessi fornire servizi extra tipo monitorare lo stato delle macchine (se solo online o meno) le cose cambierebbero.

### Test
#### Testbed
Abbiamo bisogno di:
	- un gestore
	- tante piccole macchinine (3/4 laptop, 2 server, 1 lighthouse qualche web service in una macchina)
		--> Tocca studiare azure
			- Faccio le macchine come vm e faccio il setup del network tutto su azure.
			- Il gestore è una web app.

### Design of the application
##### Django vs Flask?
il codice prodotto e le scelte di progettazione


### Division of work
- Stefano
	- [ ] Postgres VS Mongo
- Luca
	- [ ] Finire di tirare su Nebula nelle vm su azure
	- [ ] Fare un mini esempio di webapp con flask e DB (postgres al momento)
- Pasquale
	- [ ] HTML e frontend in generale




