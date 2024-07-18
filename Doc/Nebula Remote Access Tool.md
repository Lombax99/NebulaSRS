Build an enterprise remote access tool leveraging Nebula: https://github.com/slackhq/nebula
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
- https://techcommunity.microsoft.com/t5/azure-database-support-blog/using-certificates-in-azure-sql-database-import/ba-p/368949
- https://learn.microsoft.com/it-it/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli
- DEBUG CONSOLE: https://nebularat-webapp.scm.azurewebsites.net/DebugConsole


### Requirements analysis
##### Remote machines
Any machine of the virtual network including both Host and Lighthouse, those includes servers, laptops, mobile phones and anything that can run the nebula software.
##### Nebula Certificate
It's a the host certificate. From the official doc: "A host certificate contains the name, IP address, group membership, and a number of other details about a host. Individual hosts cannot modify their own certificate, because doing so will invalidate it. This allows us to trust that a host cannot impersonate another host within a Nebula network. Each host will have its own private key, which is used to validate the identity of that host when Nebula tunnels are created."
##### Root Certification Autority
The **root certificate** is a self signed Nebula Certificate that identifies the root authority of the entire certificate structure.
##### Hosts
A Nebula host is simply any single node in the network, e.g. a server, laptop, phone, tablet. The Certificate Authority is used to sign keys for each host added to a Nebula network. A host certificate contains the name, IP address, group membership, and a number of other details about a host. Individual hosts cannot modify their own certificate, because doing so will invalidate it. This allows us to trust that a host cannot impersonate another host within a Nebula network. Each host will have its own private key, which is used to validate the identity of that host when Nebula tunnels are created.
##### Lighthouse
In Nebula, a lighthouse is a Nebula host that is responsible for keeping track of all of the other Nebula hosts, and helping them find each other within a Nebula network.
##### Nebula firewall rules
Firewall rules as defined in the nebula [official doc](https://nebula.defined.net/docs/config/firewall/). Any host has its own rules. Management of those rules is outside the scope of the project we will assume that those rules are defined and managed by someone outside of this system.
##### Auth
The process of verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in an information system. In our case is the ability to identify a user and its corresponding authorizations.
##### Portal
Web service remotely available that allows a user to interface with the system.
##### Available machines
Machines that are part of the nebula network and are available to the current user giving his/her authorizations.
##### Admin
The user with the full authorization on the system.
##### User
In our case a user is a system admin of the nebula network or part of it. We will consider only user with a certain degree of knowledge in networking and system administration.
##### Security role
A set of authorizations that are given to one or more user.
##### Short-lived certificate
A dynamically generated certificate that allows a user with the necessary authorization to access temporarily a specific machine. Those certificates will have a valid period of some hours.


-----

### Problem analysis
##### Web interface
Cosa usiamo per implementare una web interface? 
Dove hostiamo la web app? E il database?
Che vantaggi abbiamo usando Azure? Scalabilità? Estendibilità? 
Quante richieste dobbiamo gestire realisticamente? Con che picchi?
Quanti dati dobbiamo gestire? Con che velocità crescono?
See [[Framework utilizzato]].
##### Come popoliamo il database?
- Non sono cazzi nostri, ci limitiamo ad esporre un API per aggiornare il DB.
	1) Aggiungo una singola macchina
	2) Aggiungo tante macchine in una volta sola (rinviato a sprint futuri)
##### Come salviamo i dati nel database?
Mi salvo i due file che mi interessano e associo ad ogni macchina un ID definito da noi. 
Voglio salvare anche la chiave dei certificati della macchina? NO
Anche perchè se perdi la chiave generi un nuovo cert, non la vai a recuperare in un DB.
Vedi [[IMPLEMENTAZIONE DB (Sté)]]
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

Posso mettere una funzione per caricare dati nel sistema, che controlli di sicurezza devono essere fatti?
Yaml è Turing completo? Posso far entrare del codice malevolo? Posso mettere dei certificati falsi? Devo controllare da chi sono stati emessi i certificati. I file di conf sono firmati dalla root cert autority? non penso ma devo controllare.

> [!Tip] Per sprint futuri
> Se voglio assicurarmi che i file non siano cambiati senza che la nostra applicazione lo sappia vado a controllare randomicamente a campione la data di modifica del file di conf di una macchina e la confronto con quella nel mio database... devo quindi aggiungerlo al database.
##### Come teniamo traccia dei permessi dei vari utenti?
Bisogna salvarsi nel DB una tabella che associa utenti e macchine a cui possono accedere.
molto probabilmente converrà fare una tabella con tutti gli utenti e per ogni utente segnarsi a quale macchina può accedere. Il motivo è che lo spazio in memoria di un DB non è un grosso problema, posso sprecarne quanto ne voglio mentre dato un utente loggato è possibile che questo mi richieda certificati per più macchine e quindi mi tengo i dati salvati in cache o qualcosa di simile per velocizzare la cosa.

Ovviamente i dati di una macchina saranno visibili solo agli utenti associati alla macchina in questione.
##### Come gestiamo la fase di Auth
- processo di auth
	- fase di sicurezza (progettazione e testing)
	- 2 tipi di utenti:
		- normal user --> show only
		- admin --> può anche modificare cose
	- Per l'auth se usiamo il sistema di azure di base (che richiede necessariamente che un utente abbia un account microsoft) e far finta che tutti i nostri user abbiano account microsoft?
	- **TT**: questa è una piattaforma pensata per utenti esperti (informatici puri); quindi non dobbiamo contare gli utenti finali. 

NOTE: Spero che azure faccia il suo lavoro e implementi un sistema di Auth decente. 🤞
HAHAHAHAH che stolti che eravamo...

Auth a due fattori?? 👀
- Micorsoft Entra ID
- [[Autenticazione a due fattori]]

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

Si tratta solo di assegnare la visibilità delle macchine ad un utente specifico. Non è vero, ci sono anche ruoli che possono fare cose diverse con le macchine, qualcuno potrebbe avere il permesso di fare ssh mentre altri no...
#Sprint1 Decidiamo che per questo primo sprint ci limitiamo solo ad un discorso di visibilità.

Come assegniamo le macchine? Questi metodi non sono mutualmente esclusivi:
- Posso assegnare un singolo ID
- Posso assegnare un sottodominio
##### Come generiamo i certificati short lived?
Per il primo sprint ci limitiamo a dare la chiave della rootCA alla nostra super macchina in modo che possa creare nuovi certificati. Questo comporta GIGANTESCHI problemi di sicurezza che però gestiremo nei prossimi sprint.
##### Quanto può durare uno short-lived certificate?
Mettiamo durante la generazione la possibilità di definire il periodo di tempo di validità all'utente entro certi parametri, per questo primo sprint diciamo tra 1 e 8 ore.
##### Aggiornamento del certificato che genera gli altri certificati
Dobbiamo tenere presente che il certificato deve essere aggiornato di tanto in tanto...
Non abbiamo accesso a EntraID per limiti del nostro account, non ha senso perdere la testa a reinventare la ruota per questo motivo...
##### La nostra macchina si può collegare a tutte le macchine che gestisce in ogni momento? Serve che lo faccia?
Per come è impostata al momento il nostro servizio non ha nessun bisogno di collegarsi con le macchine nella rete. Se volessi fornire servizi extra tipo monitorare lo stato delle macchine (se solo online o meno) le cose cambierebbero.
##### Gestione dei segreti nell'app
L'app possiede una serie di segreti che devono essere mantenuti tali ad esempio:
- Credenziali google per mandare mail per l'autenticazione a due fattori
- Credenziali del db (username, password, host, pgdb)
- Segreto di Flask-BCrypt
- Credenziali del superuser
- Certificato e chiave della Authority
##### Hidden Req:
- La nostra applicazione deve poter modificare le regole di firewall di tutte le macchine remote?
- Deve poter modificare il layout della network?
- Deve poter generare nuove macchine dinamicamente?
- La nostra macchina si può collegare a tutte le macchine che gestisce in ogni momento? Serve che lo faccia?
Vedi le [[Nebula Remote Access Tool#Discussioni con il committente|discussioni con il committente]] 
##### Req 4 - short-lived cert: 
>[!Note] Requirement
>Generate on the fly a ==short-lived certificate== to allow the user to connect to the desired machine.


- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user? SI vedi dopo
	- Legato alle SecDom? possibilmente si
	- Generare ruoli dinamicamente? non proprio...

Ruoli:
- Un utente che può entrare in ssh in tutte le macchine
- Anche rdp (ha senso dare sia rdp che ssh o è meglio tenerli separati?)
- Un utente che ha i permessi per modificare i ruoli
- In generale è pensato solo per gli amministratori di sistema e non tutti gli utenti di un'azienda

Stashed changes
- Come gestiamo le regole di firewall? Non gestiamo noi le regole, non è compito nostro


Primo problema è capire come fare a creare certificati mirati verso una macchina senza toccare le regole di firewall delle macchine stesse.

==Problema fondamentale==: come fare in modo che un certificato emesso per accedere alla macchina Laptop1 non mi permetta di accedere anche ad altre macchine...
- A livello di firewall ho le seguenti opzioni per filtrare il traffico:
	- `port`: Takes `0` or `any` as any, a single number (e.g. `80`), a range (e.g. `200-901`), or `fragment` to match second and further fragments of fragmented packets (since there is no port available).
	- `proto`: One of `any`, `tcp`, `udp`, or `icmp`
	- `ca_name`: An issuing CA name
	- `ca_sha`: An issuing CA shasum
	- `host`: Can be `any` or a literal hostname, ie `test-host`
	- `group`: Can be `any` or a literal group name, ie `default-group`
	- `groups`: Same as `group` but accepts a list of values. Multiple values are AND'd together and a certificate must contain all groups to pass.
	- `cidr`: a CIDR, `0.0.0.0/0` is any. This restricts which Nebula IP addresses the rule allows.
	- `local_cidr`: a local CIDR, `0.0.0.0/0` is any. This restricts which destination IP addresses, when using unsafe_routes, the rule allows. If unset, the rule will allow access to the specified ports on both the node itself as well as any IP addresses it routes to.
	Per requisiti la nostra app non può modificare dinamicamente le regole delle varie macchine.
- Ho accesso alla loro configurazione in read-only tramite il database.
- Informazioni che ho a priori:
	- ca_name/ca_sha
	- group (maybe...)
	- cidr (circa... ma non è molto scalabile come metodo...)
- Un certificato è solitamente definito in questo modo:
```
NebulaCertificate {  
	Details {  
		Name: host1  
		Ips: [  
			192.168.100.5/24  
		]  
		Subnets: [  
			10.0.0.0/8  
		]  
		Groups: [  
			"prod"  
			"api"  
		]  
		Not before: 2023-02-30 16:22:00 -0400 EDT  
		Not After: 2023-07-30 16:08:16 -0400 EDT  
		Is CA: false  
		Issuer: d5978d6d54a58e4685551708c5f57fbdd3774be67d470ecb0033cf70bbf5fbb5  
		Public key: 4a915591ff1a6869acb085d0292cbd25ba88624b9729420acb20d03644e0b016  
		Curve: CURVE25519  
	}  
	Fingerprint: 92efefd0575f71c10973dc96d9e2111d62703139383855f5a6a74feea68af05e  
	Signature: dc680011a11078fc00cce84d176662f54c96fa071d1bd49d5410a987f5743c3a641e27142ec19d5ed1929d5464bcdffe927a787b3a4f200b008d84821e3c4a0d  
}
```

- La piattaforma è studiata per admin di sistema, non sarebbe troppo sbagliato basarsi sui gruppi per una prima forma di limitazione, supponendo che tutto sia diviso in subdomain e ogni admin abbia accesso a tutte le macchine del subdomain (o dei subdomains) a lui assegnati.
- Seconda opzione è avere un sistema di CA dinamico in cui per ogni macchina creo e gestisco una CA con l'unico scopo di permettere l'accesso ad essa dinamicamente. Aggiornare ogni CA quando scade diventerebbe un trauma se non fosse automatizzato.
- Mi appoggio ad un sistema esterno per richiedere la generazione di regole dinamicamente sulle macchine per cui richiedo un certificato.

==Soluzione==: tramite cidr possiamo definire degli ip specifici in ogni macchina che ci aspettiamo un admin abbia quando prova a connettersi con un certificato temporaneo.
Questo richiede che in fase di deployment della configurazione alcuni ip siano riservati (che non dovrebbe essere un problema) e che ad ogni macchina vengano assegnati questi ip extra, non è difficile da fare in modo automatico, se ho già dei tool per generare i file di conf delle macchine posso facilmente aggiungere una regola di firewall extra.
- Come genero gli IP? Dovrebbero essere randomici / non predicibili? In realtà non mi interessa particolarmente, la sicurezza del processo ricade nella sicurezza dei certificati e dei processi che li generano non nei dati contenuti. Anche se un attaccante conoscesse l'ip necessario non potrebbe generarsi un certificato valido.

``` yaml
#esempio di regola di firewall
    inbound:
      - port: any
        proto: any
        cidr: 192.168.100.100/32
        ca_name: Myorg, Inc
```

> [!Tip]- Possiamo estendere i controlli impostando anche come un utente si collega?
> Esiste un modo senza andare a modificare dinamicamente i file di conf delle varie macchine per definire anche come un admin si collega (ssh invece che rdp)?
### Discussioni con il committente
- La nostra applicazione deve poter modificare le regole di firewall di tutte le macchine remote? NO
- Deve poter modificare il layout della network? NO
- Deve poter generare nuove macchine dinamicamente? NO
- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user?
	- **TT**: gli utilizzatori della piattaforma non hanno tutti lo stesso ruolo --> Ci sono diversi tipi di admin. Dobbiamo trovare quanti più ruoli possibile
	- Legato alle SecDom?
		- **TT**: Se riusciamo, possiamo tener conto dei SecDom. Tanto meglio se ci riusciamo.
	- Generare ruoli dinamicamente?
		- **TT**:  ????
### Test Plan
- cosa usiamo per testare la nostra applicazione? su quali tecnologie ci appoggiamo?
	- **TT**: test di scalabilità e sicurezza. possiamo mettere dei cert nei nostri pc.
- In cosa consistono i nostri test?
	- **TT**: 
		- scalabilità --> Quello che possiamo verificare è: quanti admin può gestire/quanti certificati può firmare simmultaneamente.
			     --> Quanto è facile gestire un numero crescente di macchine ed utenti
		- sicurezza --> Accessi non autorizzati a macchine. Problemi di intrusion.
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
[Owasp Zap](https://www.zaproxy.org/) (ritenuto ridondante, non è stato utilizzato)
[snyk](https://app.snyk.io/org/lombax99/)
[git guardian](https://dashboard.gitguardian.com/workspace/553882/get-started)
#### Analisi dei Costi
1) **Primo test basilare**:
	- WebApp Pricing plan: B1 (Super basilare, costo al mese 12.30 Euro)
	- Database Plan: Standard_B1ms (1 vCore) (Super Basilare, costo al mese 13.60 Euro)

![[StatsTest50usersBasicPlan.png]]
*test con 50 utenti*
![[StatsTest100usersBasicPlan.png]]
*test con 100 utenti*

**NOTA**: anche con i servizi più basilari che Azure mette a disposizione la webapp riesce a gestire un carico di 50 utenti contemporaneamente mantenendo un response time inferiore al secondo. Già con 100 utenti il tempo di risposta medio aumenta sopra il secondo. Nella maggior parte dei casi comunque riuscire a gestire 50 utenti contemporaneamente può essere ritenuto sufficiente (ricordo che questa applicazione ha come utente ultimo solo un ristretto gruppo di persone in una azienda).

2) **Test con servizi Premium**
	- WebApp Pricing plan: B1 (Minimum premium plan, costo al mese 79.266 Euro)
	- Database Plan: Premium v3 P0V3 (1 vCore) (Minimum premium plan, costo al mese 108. Euro)

![[StatsTest500usersPremiumPlan.png]]
*test con 500 utenti*
![[StatsTest1000usersPremiumPlan.png]]
*test con 1000 utenti*

**NOTA**: Migliorando l'hardware vediamo un netto miglioramento delle prestazioni arrivando a gestire 500 utenti contemporaneamente in modo agevolo. Questo risultato è importante per escludere un immediato collo di bottiglia nel codice. Azure inoltre permette di scalare a servizi con performance ancora migliori, con ovviamente un aumento del costo proporzionale, ma non reputiamo la cosa necessaria.

### Design of the application
##### Infrastructure as a code
L'infrastruttura dell'applicazione è stata definita tramite Terraform, tutti i dettagli in [[Terraform + Azure setup]].
##### Django vs Flask?
Python dispone di vari Framework web, i quali consentono lo sviluppo rapido di funzionalità come l'autenticazione, l'interfacciamento con il database, la gestione degli utenti ed altro. Tra i vari framework disponibili, abbiamo scelto di utilizzare Flask, per vari motivi:

- **Semplicità e leggerezza**: semplice da utilizzare e facile da imparare
- **Flessibilità:** flask è altamente flessibile, siccome si possono aggiungere varie estensioni per gestire diverse funzionalità, infatti noi abbiamo usato Flask-Login, Flask-SqlAlchemy.
- **Azure e Flask**: Azure offre supporto per applicazioni Flask, attraverso Azure App Service che semplifica il deployment e la gestione dell'applicazione web Flask su Azure
- *Django* ha una curva di apprendimento più ripida rispetto a Flask

Una cosa molto importante in Flask sono le route, che sono i punti di accesso alle diverse funzioni e risorse dell'applicazione web. Per definire una route utilizzeremo il decoratore '@app.route()' seguito dall'URL desiderato come argomento. All'interno del decoratore, oltre all'URL, è possibile specificare i metodi HTTP (GET e POST). All'interno della nostra app, abbiamo deciso di realizzare due route per quanto riguarda l'assegnamento e la revoca della macchina, perché una route si occuperà di mostrare le varie opzione, scelte all'utente autorizzato, mentre l'altra route gestirà l'azione effettiva e l'elaborazione dei dati. Un'altra scelta progettuale è state quella di definire una route per la dashboard dell'utente standard, ed un'altra route per la dashboard dell'admin. Questa separazione è importante per separare chiaramente le responsabilità, dal momento che avremo l'utente standard potrà visualizzare semplicemente la dashboard, con solo la tabella delle macchine disponibili, mentre l'admin oltre a visualizzare la dashboard, potà effettuare delle funzionalità aggiuntive, ovvero l'aggiunte di un nuovo utente, e operazioni di gestione, ovvero l'assegnazione e la revoca di una macchina, e la rimozione di un utente. Quindi, differenziare queste due route permette di gestire in maniera efficiente e sicuro l'accesso delle diverse tipologie di utenti. Uno sviluppo futuro, sarebbe quello di utilizzare una singola route per entrambe le dashboard, gestendo in maniera dinamica i contenuti basati sul ruolo dell'utente.

Maggiori dettagli in [[Framework utilizzato]].
##### Populate DB 
Abbiamo deciso di creare uno script, che legge dei file di configurazioni iniziali, simulando in questo modo la config dell'azienda utilizzatrice della nostra web app. Questi file dovranno essere in formato JSON, e tramite i dati che recupera da questi file, va a popolare le tabelle presenti all'interno del database. La scelta di utilizzare questo script che popola automaticamente le tabelle permette di avere:

- **Automazione ed efficienza**: utilizzare uno script consente di popolare in maniera automatica il database. Questo è molto vantaggioso quando si hanno molti dati o quando i dati vengono aggiornati spesso. Inoltre lo script riduce il rischio di errori umani, e consente di risparmiare tempo e sforzi.
- **Scalabilità**: con uno script, è più facile gestire grandi quantità di dati. Si può semplicemente modificare lo script, per gestire più dati o per aggiungere nuovi campi senza dover ripetere manualmente il processo di inserimento dei dati.
- **Consistenza dei dati**: l'utilizzo dello script garantisce la coerenza e la validità dei dati inseriti nelle tabelle e questo è molto importante quando si tratta di dati strutturati in modo complesso.

Quindi abbiamo detto che i file di configurazione devono essere in formato JSON, questo perché:

- **Struttura dei dati**: JSON è adatto per dati strutturati come i nostri, e quindi permette una facile comprensione e manipolazione dei dati sia per gli sviluppatori che per le macchine.
- **Interoperabilità**: diversi linguaggi di programmazione e framework supportano JSON e quindi questo rende tutto più facile l'integrazione dei dati estratti

Abbiamo ipotizzato che ci siano due file di configurazione iniziali, uno che contiene le informazioni relative alla configurazione delle rete, ed uno che contiene i dati relativi all'utente. Inizialmente, avevamo previsto che nei file di configurazione relativo all'utente, avevamo previsto che la password fosse quella di default e che venisse mostrata in chiara, presupponendo che l'utente la cambiasse al primo accesso. Tuttavia, per motivi di sicurezza abbiamo deciso di inserire nel file JSON, l'hash della password, evitando di mostrarla in chiaro.

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



