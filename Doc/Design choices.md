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
![[MongoVSPostgres.png]]

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

##### Upload dei file su DB?
L'upload del DB non è parte dei requisiti fondamentali del progetto, è tuttavia logico credere che il sistema finale debba aver la possibilità di caricare e aggiornare i dati nel DB. In questo caso ci limiteremo a delle semplici funzionalità che caricano i dati presi da un json pre formato.

```json
{
	"descrizione": "laptop1",
	"nebula_ip": "192.168.100.11/24",
	"cert": "/path/to/file",
	"config": "/path/to/file"
},
```

i parametri di "cert" e "config" indicano il percorso che identifica i corrispettivi file di certificato e configurazione della macchina. Questo perchè si suppone che la configurazione delle macchine venga fatta in automatico o con l'assistenza di tool, nascondendo la complessità all'utente di gestire grandi quantità di file. Questo ovviamente sarebbe dipendente dai tool usati la soluzione proposta prende in considerazione un possibile scenario senza insinuare che sia il metodo migliore.
##### Come teniamo traccia dei permessi dei vari utenti?
Bisogna salvarsi nel DB una tabella che associa utenti e macchine a cui possono accedere.
molto probabilmente converrà fare una tabella con tutti gli utenti e per ogni utente segnarsi a quale macchina può accedere. Il motivo è che lo spazio in memoria di un DB non è un grosso problema, posso sprecarne quanto ne voglio mentre dato un utente loggato è possibile che questo mi richieda certificati per più macchine e quindi mi tengo i dati salvati in cache o qualcosa di simile per velocizzare la cosa.
##### Come gestiamo la fase di Auth
Speriamo in azure... 🤞
Auth a due fattori?? 👀
- [x] Chiedi al tutor perchè non possiamo accedere alle risorse di Azure sul login (Microsoft Merda):
	- Micorsoft Entra ID

Opzioni per implementare il login senza azure:
- [Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)

> [!tip]- IDEA, zero trust login
> Nebula nasce come una virtual network per Zero-Trust architecture, questo tool nella fase di login ha senso che segua gli stessi principi, come implementare Zero-Trust login settings.
> - Perchè non usiamo lo stesso Nebula per implemetare una architettura Zero-Trust?
> 	- Servirebbe che l'intera applicazione fosse hostata su una macchina dell'architettura di nebula stesso...
> 	- Implementare la cosa su Azure potrebbe non essere così facile.
> 	- A questo si può aggiungere una multi factor auth per gli utenti.
> 	- [Two Factor Auth with Flask](https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask)
> 	- [Flask Login example](https://github.com/theburntcity/flask-login/blob/master/app.py)
> 	- [OneTimePass Lib](https://github.com/tadeck/onetimepass/)
> 	
> 	"Account recovery is harder when two factor authentication is used. If an application allows users to regain access to their accounts without having a valid token, then an attacker can take advantage of this facility as well. Typically users that are locked out of their accounts have to contact an administrator and have their accounts reset manually. You can also opt to add another form of verification, such as security questions, but of course this in part undermines the increased account security."
> 	"As mentioned in the [reddit discussion of this article](http://www.reddit.com/r/Python/comments/2wtfc6/two_factor_authentication_with_flask/), there are a couple of implementation details that can be improved to make the application more secure. Storing the OTP secret and the hashed passwords in the same table can be seen as a security risk, because in the event of a security breach that gives the attacker access to the database, both will be accessible. To mitigate this risk, you could choose to store these two sensitive items in different database tables, or even better, different databases altogether. Encrypting the OTP secret, maybe using Flask's `SECRET_KEY` as encryption key, can also help. In all cases secure HTTP must be used for all communications that include passwords and the OTP secret (which is encoded in the QR code)."


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
##### Gestione dei segreti nell'app
L'app possiede una serie di segreti che devono essere mantenuti tali ad esempio:
- Credenziali google per mandare mail per l'autenticazione a due fattori
- Credenziali del db (username, password, host, pgdb)
- Segreto di Flask-BCrypt
- Forse credenziali del superuser


### Test
#### Testbed
Abbiamo bisogno di:
	- un gestore
	- tante piccole macchinine (3/4 laptop, 2 server, 1 lighthouse qualche web service in una macchina)
		--> Tocca studiare azure
			- Faccio le macchine come vm e faccio il setup del network tutto su azure.
			- Il gestore è una web app.

#### Test di distribuzione 
##### Azure load tester quick start
[Quickstart: Run a load test on a website](https://go.microsoft.com/fwlink/?linkid=2225968)
[Identify performance bottlenecks](https://go.microsoft.com/fwlink/?linkid=2226130)
[Create a load test with a JMeter script](https://go.microsoft.com/fwlink/?linkid=2226327)
[Test applications with authentication](https://go.microsoft.com/fwlink/?linkid=2226328)
##### Automate load testing
[Continuous load testing with GitHub Actions](https://go.microsoft.com/fwlink/?linkid=2226033)
[Continuous load testing with Azure Pipelines](https://go.microsoft.com/fwlink/?linkid=2226033)

##### Test di sicurezza (owasp zap, snyk, git guardian)
[Owasp Zap](https://www.zaproxy.org/)
[snyk](https://app.snyk.io/org/lombax99/)
[git guardian](https://dashboard.gitguardian.com/workspace/553882/get-started)



### Design of the application
##### Django vs Flask?
guarda: [[Framework utilizzato]]


### Piano di progettazione
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



