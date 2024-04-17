Build an enterprise remote access tool leveraging Nebula: https://github.com/slackhq/nebula
### Requirements
1) Build a database of remote machines by importing the Nebula certificates and the current Nebula firewall rules for reaching them.
2) Web interface protected by auth to access a portal showing all the available machines to the user.
3) Admin interface to define security roles for users and configure what machines can be available.
4) Generate on the fly a short-lived certificate to allow the user to connect to the desired machine.

Resources
- [nebula github](https://github.com/slackhq/nebula)
- [medium: introducing nebula, the open source global overlay network](https://medium.com/several-people-are-coding/introducing-nebula-the-open-source-global-overlay-network-from-slack-884110a5579)
- [nebula doc](https://nebula.defined.net/docs/)
- [nebula quick start](https://nebula.defined.net/docs/guides/quick-start/)
- [nebula config reference](https://nebula.defined.net/docs/config/)
- [nebula official slack](https://join.slack.com/t/nebulaoss/shared_invite/enQtOTA5MDI4NDg3MTg4LTkwY2EwNTI4NzQyMzc0M2ZlODBjNWI3NTY1MzhiOThiMmZlZjVkMTI0NGY4YTMyNjUwMWEyNzNkZTJmYzQxOGU) 

### Requirements analysis
qua ci vanno le definizioni dei termini dei requisiti che passano da linguaggio formale a definizione rigorosa o addirittura linguaggio macchina.

### Key-points
##### Testbed
Abbiamo bisogno di:
	- un gestore
	- tante piccole macchinine (3/4 laptop, 2 server, 1 lighthouse o magari due se vogliamo essere molto fighi, qualche web service in una macchina)
		--> Tocca studiare azure

##### Req 1 - Database: 
- database remoto su azure
- i certificati sono file quindi possiamo caricarli e basta
- per le regole di firewall?
	- dobbiamo trovare un modo per rappresentarle e salvarle nel db
	--> Possiamo salvare una regola per riga con tutti i parametri opzionali di firewall
	- Un conto è se devo solo salvarmi quali regole ha un nodo e un conto è se devo anche generare le regole e i file yaml a partire dai dati nel db. (non è nei requisiti ma è una bella idea)
	- Chiaramente salviamo solo i cert non le chiavi (anche se... forse forse... tanto i cert passano in chiaro nella rete... serve salvarli? se devo creare dei nodi nuovi...)

##### Req 2 - Web interface:
- processo di auth
	- fase di sicurezza (progettazione e testing)
	- 2 tipi di utenti:
		- normal user --> show only
		- admin --> può anche modificare cose
	- Per l'auth se usiamo il sistema di azure di base (che richiede necessariamente che un utente abbia un account microsoft) e far finta che tutti i nostri user abbiano account microsoft?
	- **TT**: questa è una piattaforma pensata per utenti esperti (informatici puri); quindi non dobbiamo contare gli utenti finali. 

##### Req 3 - Admin role:
- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user?
	- **TT**: gli utilizzatori della piattaforma non hanno tutti lo stesso ruolo --> Ci sono diversi tipi di admin. Dobbiamo trovare quanti più ruoli possibile
	- Legato alle SecDom? 
		- **TT**: Se riusciamo, possiamo tener conto dei SecDom. Tanto meglio se ci riusciamo.
	- Generare ruoli dinamicamente? 
		- **TT**:  ????
- Quali casi gestire? Cosa si intende per "available machine" nel sistema?

##### Req 4 - short-lived cert: 
- Quale "user"?
- Cosa vuol dire "short-lived"? E' diverso dal concetto di ruolo? Dobbiamo dare sempre un nuovo cert?
	- **TT**: Questo è un dettaglio implementativo. Idealmente, nessuno deve avere un cert permanente. Si generano i cert e la piattaforma li gestisce.

- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user? SI vedi dopo
	- Legato alle SecDom? possibilmente si
	- Generare ruoli dinamicamente? non proprio...
- Quali casi gestire? Cosa si intende per "available machine" nel sistema? Solo una questione dei permessi del tuo utente.

Ruoli:
- Un utente che può entrare in ssh in tutte le macchine (rdp invece che ssh cos'è?)
- Un utente che ha i permessi per modificare i ruoli
- In generale è pensato solo per gli amministratori di sistema e non tutti gli utenti di un'azienda

##### Req 4 - short-lived cert: 
- Quale "user"? si tratta solo di admin non di utenti comuni
- Cosa vuol dire "short-lived"? 1 oretta ma modificabile forse...

Stashed changes
- Come gestiamo le regole di firewall? Dobbiamo aggiungerne una temporanea e poi eliminarla...

##### Hidden Req:
- La nostra applicazione deve poter modificare le regole di firewall di tutte le macchine remote? NO
- Deve poter modificare il layout della network? NO
- Deve poter generare nuove macchine dinamicamente? NO

##### IMPORTANTE
- definire i test di sicurezza e i test di scalabilità

##### La nostra macchina si può collegare a tutte le macchine che gestisce in ogni momento? Serve che lo faccia?


### Discussions with the commissioner
- punti discussi con il committente

### Test Plan
- cosa usiamo per testare la nostra applicazione? su quali tecnologie ci appoggiamo?
	- **TT**: test di scalabilità e sicurezza. possiamo mettere dei cert nei nostri pc.
- In cosa consistono i nostri test?
	- **TT**: 
		- scalabilità --> Quello che possiamo verificare è: quanti admin può gestire/quanti certificati può firmare simmultaneamente
		- sicurezza --> Accessi non autorizzati a macchine. Problemi di intrusion.

### Division of work
- Divisione per sprint - data di consegna
	- Divisione dei membri nei vari sprint


