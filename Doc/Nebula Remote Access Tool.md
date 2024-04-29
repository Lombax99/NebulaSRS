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
The user with the ability to modify authorizations of other users.
##### User
In our case a user is a system admin of the nebula network or part of it. We will consider only user with a certain degree of knowledge in networking and system administration.
##### Security role
A set of authorizations that are given to one or more user.
##### Short-lived certificate
A dynamically generated certificate that allows a user with the necessary authorization to access temporarily a specific machine. Those certificates will have a valid period of some hours.


### Key-points
#### Testbed
Abbiamo bisogno di:
	- un gestore
	- tante piccole macchinine (3/4 laptop, 2 server, 1 lighthouse qualche web service in una macchina)
		--> Tocca studiare azure
			- Faccio le macchine come vm e faccio il setup del network tutto su azure.
			- Il gestore è una web app.

#### Req 1 - Database: 
>[!Note] Requirement
>Build a database of ==remote machines== by importing the ==Nebula certificates== and the current ==Nebula firewall rules== for reaching them.

- database remoto su azure
- i certificati sono file quindi possiamo caricarli e basta
- per le regole di firewall?
	- dobbiamo trovare un modo per rappresentarle e salvarle nel db
	--> Possiamo salvare una regola per riga con tutti i parametri opzionali di firewall
	- Un conto è se devo solo salvarmi quali regole ha un nodo e un conto è se devo anche generare le regole e i file yaml a partire dai dati nel db. (non è nei requisiti ma è una bella idea)
	- Chiaramente salviamo solo i cert non le chiavi (anche se... forse forse... tanto i cert passano in chiaro nella rete... serve salvarli? se devo creare dei nodi nuovi...)

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
#Sprint1 Mi salvo i due file che mi interessano e ciccia.
#Sprint1 Voglio salvare anche la chiave dei certificati della macchina? Secondo me NO ma.
##### Come aggiorniamo i dati
#Sprint1 Nel primo sprint mi accontento di dire che chiunque modifichi i dati si debba prende la briga di modificarli anche nel database.
Dobbiamo fare un'interfaccia carina per permettere tutto questo in modo scalabile. Posso mettere una funzione per caricare dati nel sistema, che controlli di sicurezza devono essere fatti?
Yaml è Turing completo? Posso far entrare del codice malevolo? Posso mettere dei certificati falsi? Devo controllare da chi sono stati emessi i certificati. I file di conf sono firmati dalla root cert autority? non penso ma devo controllare.

> [!Tip] Per sprint futuri
> Se voglio assicurarmi che i file non siano cambiati senza che la nostra applicazione lo sappia vado a controllare randomicamente a campione la data di modifica del file di conf di una macchina e la confronto con quella nel mio database... devo quindi aggiungerlo al database.

##### A cosa servono i dati?
Stampiamo a schermo le regole di firewall e i certificati se richiesto.

#### Req 2 - Web interface:
>[!Note] Requirement
>Web interface protected by ==auth== to access a ==portal== showing all the ==available machines== to the user.


##### Auth
- processo di auth
	- fase di sicurezza (progettazione e testing)
	- 2 tipi di utenti:
		- normal user --> show only
		- admin --> può anche modificare cose
	- Per l'auth se usiamo il sistema di azure di base (che richiede necessariamente che un utente abbia un account microsoft) e far finta che tutti i nostri user abbiano account microsoft?
	- **TT**: questa è una piattaforma pensata per utenti esperti (informatici puri); quindi non dobbiamo contare gli utenti finali. 

NOTE: Spero che azure faccia il suo lavoro e implementi un sistema di Auth decente.
##### Showing available machines
Dipende dai security roles

#### Req 3 - Admin role:
>[!Note] Requirement
>==Admin== interface to define ==security roles== for ==users== and configure what machines can be available.

- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user?
	- **TT**: gli utilizzatori della piattaforma non hanno tutti lo stesso ruolo --> Ci sono diversi tipi di admin. Dobbiamo trovare quanti più ruoli possibile
	- Legato alle SecDom? 
		- **TT**: Se riusciamo, possiamo tener conto dei SecDom. Tanto meglio se ci riusciamo.
	- Generare ruoli dinamicamente? 
		- **TT**:  ????

NOTA: Ruolo dell'admin supremo necessariamente deve esistere

Si tratta solo di assegnare la visibilità delle macchine ad un utente specifico. Non è vero, ci sono anche ruoli che possono fare cose diverse con le macchine, qualcuno potrebbe avere il permesso di fare ssh mentre altri no...
#Sprint1 Decidiamo che per questo primo sprint ci limitiamo solo ad un discorso di visibilità.

Come assegniamo le macchine? Questi metodi non sono mutualmente esclusivi:
- Posso assegnare un singolo ID
- Posso assegnare un sottodominio


#### Req 4 - short-lived cert: 
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

#### Hidden Req:
- La nostra applicazione deve poter modificare le regole di firewall di tutte le macchine remote? NO
- Deve poter modificare il layout della network? NO
- Deve poter generare nuove macchine dinamicamente? NO

#### IMPORTANTE
- definire i test di sicurezza e i test di scalabilità

#### La nostra macchina si può collegare a tutte le macchine che gestisce in ogni momento? Serve che lo faccia?


### Discussions with the commissioner
- punti discussi con il committente

### Test Plan
- cosa usiamo per testare la nostra applicazione? su quali tecnologie ci appoggiamo?
	- **TT**: test di scalabilità e sicurezza. possiamo mettere dei cert nei nostri pc.
- In cosa consistono i nostri test?
	- **TT**: 
		- scalabilità --> Quello che possiamo verificare è: quanti admin può gestire/quanti certificati può firmare simmultaneamente.
			     --> Quanto è facile gestire un numero crescente di macchine ed utenti
		- sicurezza --> Accessi non autorizzati a macchine. Problemi di intrusion.

### Division of work
- Divisione per sprint - data di consegna
	- Divisione dei membri nei vari sprint


