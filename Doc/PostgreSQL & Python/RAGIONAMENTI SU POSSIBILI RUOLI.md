
Idee base:
- decoupling tra utente e macchina --> io ho l'elenco degli utenti e l'elenco delle macchine. In base alle regole date agli utenti, posso associare le macchine;
- creare un sistema che dia la possibilità di poter gestire la propria rete come si vuole (pochi limiti) --> il sw deve essere estremamente libero 
- definire diverse modalità (automatiche) per associare utenti e macchine;
- i dati come IP e configurazione della macchina possono cambiare, ma non viene attraverso l'app --> campo IP nella tabella macchina che è unique ma che non sia una primary key
- associazione utente-macchina (regole)
	- per ora solo con ID utente - ID macchina
	- potremmo associare l'IP della macchina all'ID utente nel momento in cui andiamo ad inserire l'ip della macchina nelle tabelle (as VARCHAR)