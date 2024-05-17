
L'implementazione comprende 3 tabelle:
1) MACCHINA, con id, descrizione (es. 'laptop_1', 'server', ecc.);
2) UTENTE, con id e username (cioè email);
3) USA, tabella associativa che associa ad un utente le macchine a cui può accedere.

Regole di lettura: 
- Un **utente** può **usare** più **macchine**
- Più **macchine** possono essere **usate** da più **utenti**.

### IDEA PER SPRINT 2 --> Creare una tabella "ACCESSI", in cui si inserisce l'id della coppia utente-macchina che interessa l'accesso, più un timestamp con data e ora.



![[ER_MODEL.png]]


### VANTAGGI:
- ##### Scalabilità:
	  Posso avere più macchine e più utenti, ma alla fine l'associazione è una sola, e giocando su di essa posso realizzare cose più complesse, senza stravolgere l'architettura.
- ##### Semplicità:
	  Posso gestire il database in maniera semplice ed efficiente, perché la struttura viene semplificata dall'utilizzo di un'entità centrale (es. USA)

### SVANTAGGI:
- ##### Ridondanza
	  Le informazioni di utenti e macchine potrebbero essere salvate più volte in diverse tabelle; quindi, la modifica di un'info in una tabella potrebbe richiedere l'aggiornamento nelle altre tabelle.
- ##### Maggiore complessità delle query più articolate
	  Tuttavia, una volta trovata la query adatta alle nostre esigenze, potremmo inserirla in uno script e lanciarla in automatico quando l'admin ne fa richiesta.