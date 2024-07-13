
### DB da utilizzare?
Avevamo tre possibilità: postgres, azure sql e mongodb. abbiamo scelto postgres, poiché è SEMPRE conforme  alle proprietà ACID, a differenza di Mongo che non lo è e azure sql, che lo è solo con determinati motori di archiviazione

### Libreria python da usare?
Le possibilità erano due:
- psycop2 --> libreria python SOLO per il collegamento a postgres. 
- SQLAlchemy --> ORM che permette il collegamento a diversi tipi di db. Abbiamo scelto questa, perché, a differenza di psycopg, ci permette di gestire i dati immagazzinati nel db, come oggetti, riducendo il numero di query da progettare per ottenere le info. Inoltre, opera a stretto contatto con Flask, il framework che abbiamo scelto di utilizzare per la nostra webapp

>[!info]- GESTIONE CREDENZIALI
>
> Viene fatto uso della sottolibreria flask_bcrypt per salvare le password nel db in maniera sicura: la funzione generate_password_hash permette di generare un dato di tipo byte, che sarebbe l'hash della password, così da non salvarla in chiaro. Un'altra funzione è check_password_hash, che permette di verificare l'uguaglianza tra l'hash della password di un utente e la password candidata, inserita al momento del login.
> 
> Inoltre, è stato ideato anche un meccanismo per cambiare la password, usufruibile sia da super admin che dagli altri utenti del sistema: esso richiede di inserire prima la password attuale e poi la nuova, con successiva ripetizione di ques'ultima per conferma. Successivamente controlla che:
> - La prima password inserita (old password) sia uguale a quella attuale; altrimenti richiede di inserire una password corretta.  
> - Non si stia riutilizzando la vecchia password come nuova password.
> - La nuova password e la sua ripetizione siano uguali.
> Tutto viene fatto con l'ausilio della sopra citata libreria flask_bcrypt.
> Questo meccanismo è stato inserito perché, essendo il super admin a creare gli utenti, per ognuno di essi definisce anche una password temporanea; quindi, in qualche modo l'utente deve mettere in sicurezza il proprio account quando ne ottiene il controllo.

>[!info]- GENERAZIONE E DOWNLOAD CERTIFICATI TEMPORANEI
>
>L'idea sarebbe quella di utilizzare Tkinter per far scegliere all'utente dove salvare i cert tramite UI. Tuttavia, Azure presenta problemi nella import di tale libreria, sebbene il download viene eseguito con successo. 
>
>Bisognerebbe trovare un modo per far salvare direttamente tutto nella cartella di download, rendendo il suo percorso system independent...
>
>**SOLUZIONE**: non appena genera cert e key, li pone in un file zip e li fa scaricare direttamente nella cartella dei Download, attraverso l'utilizzo del metodo *send_file* di Flask.
>

### Questioni di sicurezza
In questo progetto, sono stati riscontrati dei problemi di sicurezza. Queste falle sono state individuate per mezzo di un web tool chiamato "Snyk", che ha controllato il codice delle varie funzioni presenti nella nostra repository su GitHub, evidenziando:

- Vulnerabilità legate a **versioni, non aggiornate, delle librerie utilizzate**. Esse possono avere degli exploit. Fra i tanti, il più "importante" è quello dovuto alla versione della libreria *werkzeug*, usata nel nostro progetto: infatti, in questa versione è presente una vulnerabilità, dovuta all'uso di funzioni come *eval()*, che potrebbe rendere possibili attacchi di tipo **Code Injection**. Tuttavia, questa funzione non è mai stata utilizzata e questo problema è stato banalmente risolto aggiornando le librerie alle rispettive ultime versioni.
- Vulnerabilità legate alla **presenza dei parametri da passare alle query**, scritte in SQL Raw, **all'interno della funzione *text()***. Questa funzione traduce la stringa rappresentante la query in un formato testuale compatibile con SQLAlchemy (vedi la sezione sottostante per maggiori informazioni). 

>[!info]- SQL INJECTION
>
>Il sistema di esecuzione delle query prevedeva l'utilizzo di query create ad hoc, contenute in un'apposita libreria python. Queste query venivano trasformate, inserendovi i parametri necessari a mostrare le varie informazioni, a seconda dello scenario (es. mostrare le macchine di un utente, piuttosto che quelle di un altro). Tuttavia, questo meccanismo era grossolano e rendeva possibile la SQL Injection, dato che viene utilizzato del codice SQL RAW. 
>
>**SOLUZIONE**
>
>Il problema si potrebbe risolvere sanificando l'input passato alla funzione adibita all'esecuzione delle query e utilizzando il parametro '%s' all'interno del codice SQL. In pratica, si è passati da un'esecuzione del tipo
>
>	macchine = db.session.execute(text(build_query("utente", session["username"])))
>	
>ad una come
>
>	macchine = db.session.execute(text(sel_macchine % session["username"]))
>
>inserendo il parametro di cui sopra al posto di una variabile. Ciò ci permetterebbe di eliminare quella farraginosa e grezza funzione che si occupava di sostituire i valori necessari nelle query.
>
>Tuttavia, una soluzione più ottimale a questo problema è quella di passare il parametro per risolvere la query, come ad esempio l'username, non all'interno della funzione text, bensì all'esterno di essa, utilizzando un dizionario con una sola coppia key-value, come
>
>	macchine = db.session.execute(text(sel_macchine), {'username':session["username"]}).
>
>e trasformando la query in questo modo:
>
>	query = SELECT [...] WHERE username = :username;
>
>Questa è stata la soluzione adottata, perché in tal caso la query si aspetta esattamente il valore passato nella execute; quindi, non sarebbe possibile modificarlo.
>
>**ATTENZIONE**: questa problematica non affligge le query lanciate nelle fasi di login e registrazione, oltre a tutte quelle volte in cui era necessario ottenere info su uno specifico utente, poiché per ottenere tali informazioni non è stato utilizzato del codice SQL, bensì una funzione di SQLAlchemy, che non prevede l'utilizzo di codice RAW.

- Vulnerabilità legate all'utilizzo di **percorsi a risorse**, utilizzati per quanto riguarda generazione e download degli *short-lived certificates* (vedi sezione sottostante per maggiori informazioni).  

>[!info]- PATH TRAVERSAL 
>
>Il path traversal era dovuto al fatto che la funzione *send_file* era eseguita senza un previo controllo sull'autenticità del path che le si dava in input (= se quel path portasse ai file in questione.)
>I file in considerazione sono tre: il certificato e la chiave appena generati, e il file .zip che contiene entrambi e che viene creato successivamente alla loro generazione.
>
>**SOLUZIONE**: è stato creato uno script che, di volta in volta, dato in input il path ricevuto dalla funzione che genera cert e key:
>	1) genera il base path, che va dalla cartella corrente fino alla cartella che continene tutti i file che vengono generati;
>	2) costruisce il percorso completo alla risorsa e verifica che sia effettivamente un file (se non lo è, determina che quel percorso sia stato "contaminato" da un attaccante);
>	3) genera il vero path (assoluto) al file e calcola il percorso in comune tra questo e il percorso completo al file (se il common path è diverso dal base path, allora dichiara che è in atto un tentativo di path traversal);
>	4) effettua un ultimo controllo tra il file specificato nel path reale e quello specificato dall'utente (se sono diversi, determina che c'è un tentativo di attacco)
>	5) Lo script restituisce True, se è in atto l'attacco, False altrimenti.
>
>Se lo script restituisce False in entrambi i controlli (cert, key e file zip), allora procede al download del file, altrimenti indirizza l'utente verso una pagina di errore (403 - Forbidden Access to requested Resource).




