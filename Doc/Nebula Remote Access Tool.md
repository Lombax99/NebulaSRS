Build an enterprise remote access tool leveraging Nebula: https://github.com/slackhq/nebula
### Requirements
1) Build a database of remote machines by importing the Nebula certificates and the current Nebula firewall rules for reaching them
2) Web interface protected by auth to access a portal showing all the available machines to the user
3) Admin interface to define security roles for users and configure what machines can be available
4) Generate on the fly a short-lived certificate to allow the user to connect to the desired machine

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
	- tante piccole macchinine (3/4 laptop, 2 server, 1 lighthouse, qualche web service in una macchina)
		--> Tocca studiare azure

##### Req 1 - Database: 
- database remoto su azure
- i certificati sono file quindi possiamo caricarli e basta
- per le regole di firewall?
	- dobbiamo trovare un modo per rappresentarle e salvarle nel db
	--> Possiamo salvare una regola per riga con tutti i parametri opzionali di firewall

##### Req 2 - Web interface:
- processo di auth
	- fase di sicurezza (progettazione e testing)
	- 2 tipi di utenti:
		- normal user --> show only
		- admin --> può anche modificare cose

##### Req 3 - Admin role:
- Cazzo è un security role? Ci sono altri gradi di permesso tra admin e normal user?
- Quali casi gestire? Cosa si intende per "available machine" nel sistema?

##### Req 4 - short-lived cert: 
- Quale "user"?
- Cosa vuol dire "short-lived"?
- Come gestiamo le regole di firewall? Dobbiamo aggiungerne una temporanea e poi eliminarla...

##### Hidden Req:
- La nostra applicazione deve poter modificare le regole di firewall di tutte le macchine remote

##### IMPORTANTE
- definire i test di sicurezza e i test di scalabilità

### Discussions with the commissioner
- punti discussi con il committente

### Test Plan
- cosa usiamo per testare la nostra applicazione? su quali tecnologie ci appoggiamo?

### Division of work
- Divisione per sprint - data di consegna
	- Divisione dei membri nei vari sprint
